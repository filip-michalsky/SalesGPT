import os
import pytest
from sales_gpt import SalesGPT
from langchain.chat_models import ChatOpenAI


class TestSalesGPT():

    def test_valid_inference(self, test_data_dir, load_env):
        '''Test that the agent will start and generate the first utterance.'''

        data_dir = test_data_dir()
        load_env()
        
        llm = ChatOpenAI(temperature=0.9)

        sales_agent = SalesGPT.from_llm(llm, verbose=False,
                                    salesperson_name="Ted Lasso",
                                    salesperson_role="Sales Representative",
                                    company_name="Sleep Haven",
                                    company_business='''Sleep Haven 
                                    is a premium mattress company that provides
                                    customers with the most comfortable and
                                    supportive sleeping experience possible. 
                                    We offer a range of high-quality mattresses,
                                    pillows, and bedding accessories 
                                    that are designed to meet the unique 
                                    needs of our customers.''')

        sales_agent.seed_agent()
        sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt

        # agent output sample
        agent_output = sales_agent.step()
        assert agent_output is not None, "Agent output cannot be None."
        assert isinstance(agent_output, str), "Agent output needs to be of type str"
        assert len(agent_output) > 0, "Length of output needs to be greater than 0."
        

    



