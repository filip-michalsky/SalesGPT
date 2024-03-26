import json
import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from langchain_community.chat_models import ChatLiteLLM
from salesgpt.models import BedrockCustomModel

from salesgpt.agents import SalesGPT

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# Mock response for the API call
MOCK_RESPONSE = {
    "choices": [
        {
            "text": "Ted Lasso: Hey, good morning! This is a mock response to test when you don't have access to LLM API gods. <END_OF_TURN>"
        }
    ]
}


MOCK_STREAM_RESPONSE = [
    {"choices": [{"delta": {"content": "This is "}}]},
    {"choices": [{"delta": {"content": "a mock "}}]},
    {"choices": [{"delta": {"content": "streaming response. <END_OF_TURN>"}}]},
]


class TestSalesGPT:
    @pytest.fixture(autouse=True)
    def load_env(self):
        # Setup for each test
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("OPENAI_API_KEY not found, proceeding with mock testing.")

    def _test_inference_with_mock_or_real_api(self, use_mock_api):
        """Helper method to test inference with either mock or real API based on the use_mock_api flag."""
        if use_mock_api:
            self.api_key = None  # Force the use of mock API by unsetting the API key

        llm = ChatLiteLLM(temperature=0.9, model="gpt-4-0125-preview")

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools=False,
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.""",
        )

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage()

        if use_mock_api:
            with patch("salesgpt.agents.SalesGPT._call", return_value=MOCK_RESPONSE):
                sales_agent.step()
                output = MOCK_RESPONSE["choices"][0]["text"]
                sales_agent.conversation_history.append(output)
        else:
            sales_agent.step()

        agent_output = sales_agent.conversation_history[-1]
        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."
        if use_mock_api:
            assert (
                "mock response" in agent_output
            ), "Mock response not found in agent output."
        else:
            assert (
                "mock response" not in agent_output
            ), "Mock response found in agent output."

    def test_inference_with_mock_api(self, load_env):
        """Test that the agent uses the mock response when the API key is not set."""
        self._test_inference_with_mock_or_real_api(use_mock_api=True)

    def test_inference_with_real_api(self, load_env):
        """Test that the agent uses the real API when the API key is set."""
        # This test will use the real API if OPENAI_API_KEY is set in the environment.
        self._test_inference_with_mock_or_real_api(use_mock_api=False)

    def test_valid_inference_with_tools(self, load_env):
        """Test that the agent will start and generate the first utterance."""

        llm = ChatLiteLLM(temperature=0.9)

        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools="True",
            product_catalog=f"{data_dir}/sample_product_catalog.txt",
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.""",
        )

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage()  # optional for demonstration, built into the prompt

        # agent output sample
        sales_agent.step()

        agent_output = sales_agent.conversation_history[-1]
        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."

    def test_valid_inference_with_tools_anthropic(self, load_env):
        """Test that the agent will start and generate the first utterance."""

        
        llm = BedrockCustomModel(type='bedrock-model', model="anthropic.claude-3-sonnet-20240229-v1:0", system_prompt="You are a helpful assistant.")

        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools="True",
            product_catalog=f"{data_dir}/sample_product_catalog.txt",
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.""",
        )

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage()  # optional for demonstration, built into the prompt

        # agent output sample
        sales_agent.step()

        agent_output = sales_agent.conversation_history[-1]
        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."


    def test_valid_inference_stream(self, load_env):
        """Test that the agent will start and generate the first utterance when streaming."""

        llm = ChatLiteLLM(temperature=0.9)

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.""",
        )

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage()  # optional for demonstration, built into the prompt

        # agent output sample
        # if use_mock_api:
        #     with patch('salesgpt.agents.SalesGPT._streaming_generator', return_value=iter(MOCK_STREAM_RESPONSE)):
        #         stream_generator = sales_agent.step(stream=True)
        #         agent_output = ""
        #         for chunk in stream_generator:
        #             token = chunk["choices"][0]["delta"].get("content", "") or ""
        #             agent_output += token

        stream_generator = sales_agent.step(stream=True)
        agent_output = ""
        for chunk in stream_generator:
            token = chunk["choices"][0]["delta"].get("content", "") or ""
            agent_output += token

        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."

    @pytest.mark.asyncio
    async def test_valid_async_inference_stream(self, load_env):
        llm = ChatLiteLLM(temperature=0.9)
        model_name = "gpt-3.5-turbo"

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.""",
        )

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage()  # optional for demonstration, built into the prompt

        # agent output sample
        astream_generator = await sales_agent.astep(stream=True)
        import inspect

        is_async_generator = inspect.isasyncgen(astream_generator)
        assert (
            is_async_generator == True
        ), f"This needs to be an async generator, got {type(astream_generator)}"
        agent_output = ""
        async for chunk in astream_generator:
            token = chunk["choices"][0]["delta"].get("content", "") or ""
            agent_output += token

        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."

    def test_accept_json_or_args_config(self, load_env):
        llm = ChatLiteLLM()

        sales_agent_passing_str = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools="True",
            product_catalog="tests/test_data/sample_product_catalog.txt",
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible.
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories
                                    that are designed to meet the unique
                                    needs of our customers.""",
        )  # Passing use_tools="True" as arg
        assert isinstance(sales_agent_passing_str, SalesGPT)
        assert sales_agent_passing_str.seed_agent() is None
        output = sales_agent_passing_str.step()

        keys_expected = [
            "input",
            "conversation_stage",
            "conversation_history",
            "salesperson_name",
            "salesperson_role",
            "company_name",
            "company_business",
            "company_values",
            "conversation_purpose",
            "conversation_type",
            "output",
            "intermediate_steps",
        ]

        assert output is not None
        for key in keys_expected:
            assert (
                key in output.keys()
            ), f"Expected key {key} in output, got {output.keys()}"

        sales_agent_passing_bool = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools=True,
            product_catalog="tests/test_data/sample_product_catalog.txt",
            salesperson_name="Ted Lasso",
            salesperson_role="Sales Representative",
            company_name="Sleep Haven",
            company_business="""Sleep Haven
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible.
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories
                                    that are designed to meet the unique
                                    needs of our customers.""",
        )  # Passing use_tools=True as arg
        assert isinstance(sales_agent_passing_bool, SalesGPT)
        assert sales_agent_passing_bool.seed_agent() is None

        output = sales_agent_passing_bool.step()

        keys_expected = [
            "input",
            "conversation_stage",
            "conversation_history",
            "salesperson_name",
            "salesperson_role",
            "company_name",
            "company_business",
            "company_values",
            "conversation_purpose",
            "conversation_type",
            "output",
            "intermediate_steps",
        ]

        assert output is not None, "Output cannot be None"
        for key in keys_expected:
            assert (
                key in output.keys()
            ), f"Expected key {key} in output, got {output.keys()}"
