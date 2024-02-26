from copy import deepcopy
from typing import Any, Callable, Dict, List, Union

from langchain.agents import AgentExecutor, LLMSingleActionAgent, create_openai_tools_agent
from langchain.chains import LLMChain, RetrievalQA
from langchain.chains.base import Chain
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.language_models.llms import create_base_retry_decorator
from litellm import acompletion
from pydantic import Field

from salesgpt.chains import SalesConversationChain, StageAnalyzerChain
from salesgpt.logger import time_logger
from salesgpt.parsers import SalesConvoOutputParser
from salesgpt.prompts import SALES_AGENT_TOOLS_PROMPT
from salesgpt.stages import CONVERSATION_STAGES
from salesgpt.templates import CustomPromptTemplateForTools
from salesgpt.tools import get_tools, setup_knowledge_base


def _create_retry_decorator(llm: Any) -> Callable[[Any], Any]:
    import openai
    errors = [
        openai.Timeout,
        openai.APIError,
        openai.APIConnectionError,
        openai.RateLimitError,
        openai.APIStatusError,
    ]
    return create_base_retry_decorator(error_types=errors, max_retries=llm.max_retries)


class SalesGPT(Chain):
    """Controller model for the Sales Agent."""

    conversation_history: List[str] = []
    conversation_stage_id: str = "1"
    current_conversation_stage: str = CONVERSATION_STAGES.get("1")
    stage_analyzer_chain: StageAnalyzerChain = Field(...)
    sales_agent_executor: Union[AgentExecutor, None] = Field(
        default=None)  # Adjusted to have a default value of None
    knowledge_base: Union[RetrievalQA, None] = Field(
        default=None)  # Adjusted to have a default value of None
    sales_conversation_utterance_chain: SalesConversationChain = Field(...)
    conversation_stage_dict: Dict = CONVERSATION_STAGES

    model_name: str = "gpt-3.5-turbo-0613"
    # Adjusted default value to match the need for an explicit enabling
    use_tools: bool = False
    salesperson_name: str = "Ted Lasso"
    salesperson_role: str = "Business Development Representative"
    company_name: str = "Sleep Haven"
    company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers."
    company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service."
    conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress."
    conversation_type: str = "call"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Ensure proper initialization of the base class
        if self.use_tools:
            # Assuming `product_catalog` is provided through `kwargs` if needed
            self.product_catalog = kwargs.get(
                'product_catalog', 'default_catalog_path.txt')
            self.knowledge_base = setup_knowledge_base(self.product_catalog)
            self.tools = get_tools(self.knowledge_base)
            self.initialize_tool_executor()

    def initialize_tool_executor(self):
        if self.use_tools:
            self.sales_agent_executor = self.setup_with_tools()
        else:
            # Ensuring this is explicitly set to None if not using tools
            self.sales_agent_executor = None

    @time_logger
    def seed_agent(self):
        # Step 1: seed the conversation
        self.current_conversation_stage = self.retrieve_conversation_stage("1")
        self.conversation_history = []

    @time_logger
    def determine_conversation_stage(self):
        self.conversation_stage_id = self.stage_analyzer_chain.run(
            conversation_history="\n".join(
                self.conversation_history).rstrip("\n"),
            conversation_stage_id=self.conversation_stage_id,
            conversation_stages="\n".join(
                [str(key) + ": " + str(value)
                 for key, value in CONVERSATION_STAGES.items()]
            ),
        )

        print(f"Conversation Stage ID: {self.conversation_stage_id}")
        self.current_conversation_stage = self.retrieve_conversation_stage(
            self.conversation_stage_id
        )

        print(f"Conversation Stage: {self.current_conversation_stage}")

    def human_step(self, human_input):
        human_input = "User: " + human_input + " <END_OF_TURN>"
        self.conversation_history.append(human_input)

    @time_logger
    def step(self, stream: bool = False):
        if not stream:
            self._call(inputs={})
        else:
            return self._streaming_generator()

    @time_logger
    def astep(self, stream: bool = False):
        if not stream:
            self._acall(inputs={})
        else:
            return self._astreaming_generator()

    @time_logger
    def acall(self, *args, **kwargs):
        raise NotImplementedError("This method has not been implemented yet.")

    @time_logger
    def _prep_messages(self):
        prompt = self.sales_conversation_utterance_chain.prep_prompts(
            [
                dict(
                    conversation_stage=self.current_conversation_stage,
                    conversation_history="\n".join(self.conversation_history),
                    salesperson_name=self.salesperson_name,
                    salesperson_role=self.salesperson_role,
                    company_name=self.company_name,
                    company_business=self.company_business,
                    company_values=self.company_values,
                    conversation_purpose=self.conversation_purpose,
                    conversation_type=self.conversation_type,
                )
            ]
        )

        inception_messages = prompt[0][0].to_messages()

        message_dict = {"role": "system",
                        "content": inception_messages[0].content}

        if self.sales_conversation_utterance_chain.verbose:
            print("\033[92m" + inception_messages[0].content + "\033[0m")
        return [message_dict]

    @time_logger
    def _streaming_generator(self):
        """
        Sometimes, the sales agent wants to take an action before the full LLM output is available.
        For instance, if we want to do text to speech on the partial LLM output.

        This function returns a streaming generator which can manipulate partial output from an LLM
        in-flight of the generation.

        Example:

        >> streaming_generator = self._streaming_generator()
        # Now I can loop through the output in chunks:
        >> for chunk in streaming_generator:
        Out: Chunk 1, Chunk 2, ... etc.
        """
        messages = self._prep_messages()

        return self.sales_conversation_utterance_chain.llm.completion_with_retry(
            messages=messages,
            stop="<END_OF_TURN>",
            stream=True,
            model=self.model_name,
        )

    async def acompletion_with_retry(self, llm: Any, **kwargs: Any) -> Any:
        """Use tenacity to retry the async completion call."""
        retry_decorator = _create_retry_decorator(llm)

        @retry_decorator
        async def _completion_with_retry(**kwargs: Any) -> Any:
            return await acompletion(**kwargs)

        return await _completion_with_retry(**kwargs)

    async def _astreaming_generator(self):
        """
        Asynchronous generator to reduce I/O blocking when dealing with multiple
        clients simultaneously.

        Sometimes, the sales agent wants to take an action before the full LLM output is available.
        For instance, if we want to do text to speech on the partial LLM output.

        This function returns a streaming generator which can manipulate partial output from an LLM
        in-flight of the generation.

        Example:

        >> streaming_generator = self._astreaming_generator()
        # Now I can loop through the output in chunks:
        >> async for chunk in streaming_generator:
            await chunk ...
        Out: Chunk 1, Chunk 2, ... etc.
        """
        messages = self._prep_messages()

        return await self.acompletion_with_retry(
            llm=self.sales_conversation_utterance_chain.llm,
            messages=messages,
            stop="<END_OF_TURN>",
            stream=True,
            model=self.model_name,
        )

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run one step of the sales agent."""
        if self.sales_agent_executor is None:
            print("sales_agent_executor is not initialized.")
            return {}
        # Prepare inputs based on the current conversation context and other parameters.
        ai_message = self.sales_agent_executor.invoke(inputs)
        # Further implementation to process the AI message and integrate it into the conversation history...

    def setup_with_tools(self) -> AgentExecutor:
        """
        Setup the sales agent executor with tools. This is a placeholder for the actual
        implementation, which will configure and return an AgentExecutor instance
        using the specified tools and configurations.
        """
        # This method will be further elaborated upon reaching the specified point in your instructions.

    def setup_with_tools(self) -> AgentExecutor:
        tools = get_tools(self.knowledge_base)
        prompt = CustomPromptTemplateForTools(
            template=SALES_AGENT_TOOLS_PROMPT,
            tools_getter=lambda: tools,
            input_variables=[
                "input",
                "intermediate_steps",
                "salesperson_name",
                "salesperson_role",
                "company_name",
                "company_business",
                "company_values",
                "conversation_purpose",
                "conversation_type",
                "conversation_history",
            ],
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt, verbose=self.verbose)

        tool_names = [tool.name for tool in tools]

        # WARNING: this output parser is NOT reliable yet
        # It makes assumptions about output from LLM which can break and throw an error
        output_parser = SalesConvoOutputParser(ai_prefix=self.salesperson_name)

        sales_agent_with_tools = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names,
        )

        sales_agent_executor = AgentExecutor.from_agent_and_tools(
            agent=sales_agent_with_tools, tools=tools, verbose=self.verbose
        )
        return sales_agent_executor

    @classmethod
    @time_logger
    def from_llm(cls, llm: ChatLiteLLM, verbose: bool = False, **kwargs) -> "SalesGPT":
        """Initialize the SalesGPT Controller."""
        instance = cls(verbose=verbose, **kwargs)
        instance.llm = llm  # Assuming `llm` is an instance of ChatLiteLLM or similar
        instance.verbose = verbose
        if kwargs.get("use_tools", False):
            instance.use_tools = True
            instance.product_catalog = kwargs.get(
                'product_catalog', 'default_catalog_path.txt')
            instance.knowledge_base = setup_knowledge_base(
                instance.product_catalog)
            instance.tools = get_tools(instance.knowledge_base)
        instance.initialize_tool_executor()
        return instance
