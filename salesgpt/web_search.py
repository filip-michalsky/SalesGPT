"""Anonymous Parallel Search MCP tools for one SalesGPT conversation.

The small Streamable HTTP client supports Python 3.8, like SalesGPT itself.
HTTP/MCP connections are short lived; the tool session ID belongs to the chat.
"""

import json
from uuid import uuid4
from urllib.parse import urlsplit

import httpx
from langchain_core.tools import ToolException

ENDPOINT = "https://search.parallel.ai/mcp"
USER_AGENT = "SalesGPT (https://github.com/filip-michalsky/SalesGPT)"


def _sse_messages(lines):
    data = []
    for line in lines:
        if not line:
            if data:
                yield json.loads("\n".join(data))
                data = []
        elif line.startswith("data:"):
            data.append(line[5:].lstrip(" "))
    if data:
        yield json.loads("\n".join(data))


def _result(message, request_id):
    if not isinstance(message, dict) or message.get("id") != request_id:
        raise ValueError("Unexpected MCP response ID")
    if "error" in message:
        raise ToolException("Parallel MCP returned a protocol error.")
    result = message.get("result")
    if not isinstance(result, dict):
        raise ValueError("Missing MCP result")
    return result


def _read(response, request_id):
    response.raise_for_status()
    if "text/event-stream" in response.headers.get("content-type", ""):
        for message in _sse_messages(response.iter_lines()):
            if isinstance(message, dict) and message.get("id") == request_id:
                return _result(message, request_id)
        raise ValueError("Missing MCP response")
    response.read()
    return _result(response.json(), request_id)


async def _aread(response, request_id):
    response.raise_for_status()
    if "text/event-stream" in response.headers.get("content-type", ""):
        data = []
        async for line in response.aiter_lines():
            if not line and data:
                message = json.loads("\n".join(data))
                data = []
                if isinstance(message, dict) and message.get("id") == request_id:
                    return _result(message, request_id)
            elif line.startswith("data:"):
                data.append(line[5:].lstrip(" "))
        if data:
            return _result(json.loads("\n".join(data)), request_id)
        raise ValueError("Missing MCP response")
    await response.aread()
    return _result(response.json(), request_id)


class ParallelSearch:
    """Search context owned by a single conversation, never shared globally."""

    def __init__(self, timeout=30.0):
        if not 0 < timeout < float("inf"):
            raise ValueError("search_timeout must be positive and finite")
        self.timeout = timeout
        self.reset()

    def reset(self):
        self.session_id = str(uuid4())

    @staticmethod
    def _headers():
        return {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _request(method, params):
        return {
            "jsonrpc": "2.0",
            "id": str(uuid4()),
            "method": method,
            "params": params,
        }

    @staticmethod
    def _initialize():
        return ParallelSearch._request(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "SalesGPT", "version": "0.1.2"},
            },
        )

    @staticmethod
    def _connected(headers, response, result):
        headers["MCP-Protocol-Version"] = result["protocolVersion"]
        session = response.headers.get("mcp-session-id")
        if session:
            headers["Mcp-Session-Id"] = session

    def _exchange(self, method, params):
        headers = self._headers()
        with httpx.Client(timeout=self.timeout) as client:
            request = self._initialize()
            with client.stream(
                "POST", ENDPOINT, headers=headers, json=request
            ) as response:
                self._connected(headers, response, _read(response, request["id"]))
            try:
                response = client.post(
                    ENDPOINT,
                    headers=headers,
                    json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                )
                response.raise_for_status()
                request = self._request(method, params)
                with client.stream(
                    "POST", ENDPOINT, headers=headers, json=request
                ) as response:
                    return _read(response, request["id"])
            finally:
                if "Mcp-Session-Id" in headers:
                    try:
                        client.delete(ENDPOINT, headers=headers, timeout=5.0)
                    except httpx.HTTPError:
                        pass  # Cleanup failure must not hide the tool result/error.

    async def _aexchange(self, method, params):
        headers = self._headers()
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            request = self._initialize()
            async with client.stream(
                "POST", ENDPOINT, headers=headers, json=request
            ) as response:
                self._connected(
                    headers, response, await _aread(response, request["id"])
                )
            try:
                response = await client.post(
                    ENDPOINT,
                    headers=headers,
                    json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                )
                response.raise_for_status()
                request = self._request(method, params)
                async with client.stream(
                    "POST", ENDPOINT, headers=headers, json=request
                ) as response:
                    return await _aread(response, request["id"])
            finally:
                if "Mcp-Session-Id" in headers:
                    try:
                        await client.delete(ENDPOINT, headers=headers, timeout=5.0)
                    except httpx.HTTPError:
                        pass

    def _params(self, name, query):
        if not isinstance(query, str) or not query.strip():
            raise ToolException("Provide a nonempty search query or HTTP(S) URL.")
        if name == "web_search":
            arguments = {"objective": query, "search_queries": [query]}
        else:
            try:
                url = urlsplit(query.strip())
            except ValueError as exc:
                raise ToolException("WebFetch requires a valid HTTP(S) URL.") from exc
            if (
                url.scheme not in ("http", "https")
                or not url.hostname
                or url.username
                or url.password
            ):
                raise ToolException(
                    "WebFetch requires one HTTP(S) URL without credentials."
                )
            arguments = {"urls": [query.strip()]}
        arguments["session_id"] = self.session_id
        return {"name": name, "arguments": arguments}

    @staticmethod
    def _text(result):
        content = result.get("content")
        if not isinstance(content, list) or any(
            not isinstance(block, dict) for block in content
        ):
            raise ValueError("Invalid MCP tool content")
        text = "\n".join(
            block["text"]
            for block in content
            if block.get("type") == "text" and isinstance(block.get("text"), str)
        )
        if result.get("isError"):
            raise ToolException("Parallel could not complete the request: " + text)
        if not text:
            raise ToolException("Parallel returned no text content.")
        return text

    def call(self, name, query):
        params = self._params(name, query)
        try:
            return self._text(self._exchange("tools/call", params))
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            raise ToolException(
                "Parallel search request failed or timed out. Try again later."
            ) from exc

    async def acall(self, name, query):
        params = self._params(name, query)
        try:
            return self._text(await self._aexchange("tools/call", params))
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            raise ToolException(
                "Parallel search request failed or timed out. Try again later."
            ) from exc

    def search(self, query):
        return self.call("web_search", query)

    async def asearch(self, query):
        return await self.acall("web_search", query)

    def fetch(self, url):
        return self.call("web_fetch", url)

    async def afetch(self, url):
        return await self.acall("web_fetch", url)
