import pytest
import os
from langchain.chat_models import ChatOpenAI

from salesgpt.agents import SalesGPT


class TestSalesGPT:

    def test_valid_inference_no_tools(self, load_env):
        """Test that the agent will start and generate the first utterance."""

        llm = ChatOpenAI(temperature=0.9)

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
        sales_agent.determine_conversation_stage()  # optional for demonstration, built into the prompt

        # agent output sample
        sales_agent.step()

        agent_output = sales_agent.conversation_history[-1]
        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."


    def test_valid_inference_with_tools(self, load_env):
        """Test that the agent will start and generate the first utterance."""

        llm = ChatOpenAI(temperature=0.9)

        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

        sales_agent = SalesGPT.from_llm(
            llm,
            verbose=False,
            use_tools=True,
            product_catalog = f"{data_dir}/sample_product_catalog.txt",
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

        llm = ChatOpenAI(temperature=0.9)
        model_name = 'gpt-3.5-turbo'

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
        stream_generator = sales_agent.step(return_streaming_generator=True, model_name=model_name)
        agent_output=''
        for chunk in stream_generator:
            token = chunk["choices"][0]["delta"].get("content", "")
            agent_output += token

        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."
