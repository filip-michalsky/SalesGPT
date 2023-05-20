import os
from sales_gpt import SalesGPT
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = 'sk-xxx' # fill me in

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

# agent 
sales_agent.step()

# user
user_input = input('Your response: ')
sales_agent.human_step(user_input)

# agent
sales_agent.step()
