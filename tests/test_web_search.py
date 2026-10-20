"""Scripted-model tests through SalesGPT's normal tool dispatcher; no paid APIs."""

import asyncio
import json
from uuid import UUID
from unittest.mock import MagicMock

import httpx
import pytest
from langchain_community.llms.fake import FakeListLLM

from salesgpt.agents import SalesGPT
from salesgpt.web_search import ENDPOINT, USER_AGENT


class ScriptedLLM(FakeListLLM):
    model: str = "scripted-test-model"
    prompts: list = []

    def _call(self, prompt, stop=None, run_manager=None, **kwargs):
        self.prompts.append(prompt)
        return super()._call(prompt, stop=stop, run_manager=run_manager, **kwargs)


def action(name, value):
    return "Thought: Do I need to use a tool? Yes\nAction: {}\nAction Input: {}".format(
        name, value
    )


@pytest.fixture
def wire(monkeypatch):
    requests = []
    state = {"error": None, "sse": False}

    def handle(request):
        assert str(request.url) == ENDPOINT
        assert request.headers["user-agent"] == USER_AGENT
        assert "authorization" not in request.headers
        if request.method == "DELETE":
            assert request.headers["mcp-session-id"] == "transport-session"
            return httpx.Response(200)
        body = json.loads(request.content)
        requests.append(body)
        method = body["method"]
        if method == "initialize":
            result = {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "serverInfo": {"name": "fixture", "version": "1"},
            }
        elif method == "notifications/initialized":
            assert request.headers["mcp-session-id"] == "transport-session"
            return httpx.Response(202)
        else:
            assert request.headers["mcp-protocol-version"] == "2025-03-26"
            assert request.headers["mcp-session-id"] == "transport-session"
            error = state["error"]
            if isinstance(error, Exception):
                raise error
            if isinstance(error, int):
                return httpx.Response(error)
            if error == "malformed":
                return httpx.Response(200, text="bad JSON")
            if error == "rpc":
                return httpx.Response(
                    200,
                    json={
                        "jsonrpc": "2.0",
                        "id": body["id"],
                        "error": {"code": -32603, "message": "unavailable"},
                    },
                )
            if error == "quota":
                result = {
                    "isError": True,
                    "content": [{"type": "text", "text": "Anonymous quota exceeded"}],
                }
            elif error == "shape":
                result = {"content": [None]}
            elif error == "empty":
                result = {"content": []}
            else:
                args = body["params"]["arguments"]
                UUID(args["session_id"])
                if body["params"]["name"] == "web_search":
                    assert args["search_queries"] == [args["objective"]]
                else:
                    assert args["urls"] == ["https://example.com/source"]
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": "Source: https://example.com/source\nEvidence: public research",
                        }
                    ]
                }
        reply = {"jsonrpc": "2.0", "id": body["id"], "result": result}
        headers = {"Mcp-Session-Id": "transport-session"}
        if state["sse"]:
            # Ignore notifications/comments before the response and join multiline data.
            content = (
                ': keepalive\n\nevent: message\ndata: {"jsonrpc":"2.0","method":"ping"}\n\ndata: '
                + json.dumps(reply)
                + "\n\n"
            )
            return httpx.Response(
                200,
                text=content,
                headers={**headers, "Content-Type": "text/event-stream"},
            )
        return httpx.Response(200, json=reply, headers=headers)

    sync_client, async_client = httpx.Client, httpx.AsyncClient
    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(
        "salesgpt.web_search.httpx.Client",
        lambda **kw: sync_client(transport=transport, **kw),
    )
    monkeypatch.setattr(
        "salesgpt.web_search.httpx.AsyncClient",
        lambda **kw: async_client(transport=transport, **kw),
    )
    monkeypatch.setattr("salesgpt.tools.setup_knowledge_base", lambda _: MagicMock())
    # Prove the anonymous path even in an installation with unrelated credentials.
    for key in ("PARALLEL_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    return requests, state


def agent(responses=None, **kwargs):
    return SalesGPT.from_llm(
        ScriptedLLM(responses=responses or ["Ted: done <END_OF_TURN>"]),
        use_tools=kwargs.pop("use_tools", True),
        product_catalog="not-read-in-fixture",
        **kwargs
    )


def calls(requests):
    return [r["params"] for r in requests if r["method"] == "tools/call"]


@pytest.mark.parametrize("sse", [False, True])
def test_default_dispatch_and_followup_reset(wire, sse):
    requests, state = wire
    state["sse"] = sse
    a = agent(
        [
            action("WebSearch", "current public mattress research"),
            action("WebFetch", "https://example.com/source"),
            "Ted: See https://example.com/source <END_OF_TURN>",
            action("WebSearch", "follow up public research"),
            "Ted: Follow-up done <END_OF_TURN>",
        ]
    )
    a.seed_agent()
    result = a.step()
    assert "https://example.com/source" in result["output"]
    # The normal executor fed source text into the next model prompt.
    observations = result["intermediate_steps"][1]["outputs"]["intermediate_steps"]
    assert len(observations) == 2
    assert all("Evidence: public research" in obs for _, obs in observations)
    llm = a.sales_agent_executor.agent.llm_chain.llm
    assert "Evidence: public research" in llm.prompts[1]
    assert "https://example.com/source" in llm.prompts[2]
    a.human_step("Tell me more")
    a.step()
    first_id = calls(requests)[0]["arguments"]["session_id"]
    assert {x["arguments"]["session_id"] for x in calls(requests)} == {first_id}
    b = agent()
    b.sales_agent_executor.tools[-2].run("independent conversation search")
    assert calls(requests)[-1]["arguments"]["session_id"] != first_id
    a.seed_agent()
    a.sales_agent_executor.tools[-2].run("new conversation search")
    assert calls(requests)[-1]["arguments"]["session_id"] not in (
        first_id,
        b.web_search.session_id,
    )


def test_preserved_sales_tools_and_disable_controls(wire):
    requests, _ = wire
    a = agent(
        [action("WebSearch", "disallowed search"), "Ted: disabled <END_OF_TURN>"],
        search_provider="none",
    )
    assert [t.name for t in a.sales_agent_executor.tools] == [
        "ProductSearch",
        "GeneratePaymentLink",
        "SendEmail",
        "SendCalendlyInvitation",
    ]
    assert a.web_search is None
    assert agent(use_tools=False).sales_agent_executor is None
    assert agent(use_tools="False").web_search is None
    assert not requests
    # The existing tool dispatcher enforces disabled web access even when asked.
    a.step()
    assert not requests
    with pytest.raises(ValueError, match="search_provider"):
        agent(search_provider="misspelled")
    for timeout in (0, -1, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="search_timeout"):
            agent(search_timeout=timeout)


@pytest.mark.parametrize(
    "error",
    [
        429,
        500,
        "quota",
        "rpc",
        "malformed",
        "empty",
        "shape",
        httpx.ReadTimeout("slow"),
        httpx.ConnectError("offline"),
    ],
)
def test_errors_are_observations_and_retry_keeps_identity(wire, error):
    requests, state = wire
    state["error"] = error
    a = agent(
        [
            action("WebSearch", "public mattress research"),
            "Ted: Research unavailable <END_OF_TURN>",
        ]
    )
    a.step()
    observation = a.sales_agent_executor.tools[-2].run("retry same search")
    assert "Parallel" in observation
    assert len(calls(requests)) == 2
    assert (
        calls(requests)[0]["arguments"]["session_id"]
        == calls(requests)[1]["arguments"]["session_id"]
    )


@pytest.mark.parametrize(
    "url",
    [
        "file:///etc/passwd",
        "ftp://example.com",
        "https://user:secret@example.com",
        "https://[broken",
        "not a URL",
        "",
    ],
)
def test_invalid_urls_never_leave_caller(wire, url):
    requests, _ = wire
    a = agent()
    assert "URL" in a.sales_agent_executor.tools[-1].run(url)
    assert not requests


@pytest.mark.asyncio
async def test_async_dispatch_and_interleaved_chats(wire):
    requests, state = wire
    state["sse"] = True
    a = agent(
        [
            action("WebSearch", "async public research"),
            action("WebFetch", "https://example.com/source"),
            "Ted: https://example.com/source <END_OF_TURN>",
        ]
    )
    b = agent(
        [action("WebSearch", "independent async research"), "Ted: done <END_OF_TURN>"]
    )
    a.seed_agent()
    b.seed_agent()
    await asyncio.gather(a.astep(), b.astep())
    assert "https://example.com/source" in a.conversation_history[-1]
    assert a.web_search.session_id != b.web_search.session_id
    assert {x["arguments"]["session_id"] for x in calls(requests)} == {
        a.web_search.session_id,
        b.web_search.session_id,
    }
    for x in calls(requests):
        if x["arguments"].get("objective") == "independent async research":
            assert x["arguments"]["session_id"] == b.web_search.session_id
        else:
            assert x["arguments"]["session_id"] == a.web_search.session_id


@pytest.mark.asyncio
async def test_async_timeout_and_cancellation(wire, monkeypatch):
    requests, state = wire
    a = agent()
    state["error"] = httpx.ReadTimeout("slow")
    assert "timed out" in await a.sales_agent_executor.tools[-2].arun("slow search")
    before = a.web_search.session_id
    started = asyncio.Event()
    original_client = httpx.AsyncClient

    class WaitingTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            started.set()
            await asyncio.Event().wait()

    # Cancel during actual HTTP I/O, rather than mocking the tool coroutine.
    async with original_client(timeout=30) as client:
        real_client = type(client)
    monkeypatch.setattr(
        "salesgpt.web_search.httpx.AsyncClient",
        lambda **kw: real_client(transport=WaitingTransport(), **kw),
    )
    task = asyncio.create_task(a.sales_agent_executor.tools[-2].arun("cancel search"))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert a.web_search.session_id == before
