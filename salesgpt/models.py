from typing import Any, AsyncIterator, Dict, Iterator, List, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel, SimpleChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.runnables import run_in_executor
from langchain_openai import ChatOpenAI

from salesgpt.tools import completion_bedrock


class BedrockCustomModel(ChatOpenAI):
    """A custom chat model that echoes the first `n` characters of the input.

    When contributing an implementation to LangChain, carefully document
    the model including the initialization parameters, include
    an example of how to initialize the model and include any relevant
    links to the underlying models documentation or API.

    Example:

        .. code-block:: python

            model = CustomChatModel(n=2)
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    model: str
    system_prompt: str
    """The number of characters from the last message of the prompt to be echoed."""

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Override the _generate method to implement the chat model logic.

        This can be a call to an API, a call to a local model, or any other
        implementation that generates a response to the input prompt.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        last_message = messages[-1]

        print(messages)
        response = completion_bedrock(
            model_id=self.model,
            system_prompt=self.system_prompt,
            messages=[{"content": last_message.content, "role": "user"}],
            max_tokens=1000,
        )
        print("output", response)
        content = response["content"][0]["text"]
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        stream: Optional[bool] = None,
        **kwargs: Any,
    ) -> ChatResult:
        should_stream = stream if stream is not None else self.streaming
        if should_stream:
            raise NotImplementedError("Streaming not implemented")
        
        last_message = messages[-1]

        print(messages)
        response = await acompletion_bedrock(
            model_id=self.model,
            system_prompt=self.system_prompt,
            messages=[{"content": last_message.content, "role": "user"}],
            max_tokens=1000,
        )
        print("output", response)
        content = response["content"][0]["text"]
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

        # message_dicts, params = self._create_message_dicts(messages, stop)
        # params = {
        #     **params,
        #     **({"stream": stream} if stream is not None else {}),
        #     **kwargs,
        # }
        # response = await self.async_client.create(messages=message_dicts, **params)
        # return self._create_chat_result(response)

import aioboto3
import os
import json

async def acompletion_bedrock(model_id, system_prompt, messages, max_tokens=1000):
    """
    High-level API call to generate a message with Anthropic Claude, refactored for async.
    """
    session = aioboto3.Session()
    async with session.client(service_name="bedrock-runtime", region_name=os.environ.get("AWS_REGION_NAME")) as bedrock_runtime:

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages,
            }
        )

        response = await bedrock_runtime.invoke_model(body=body, modelId=model_id)

        # print('RESPONSE', response)

        # Correctly handle the streaming body
        response_body_bytes = await response['body'].read()
        # print('RESPONSE BODY', response_body_bytes)
        response_body = json.loads(response_body_bytes.decode("utf-8"))
        # print('RESPONSE BODY', response_body)

        return response_body

