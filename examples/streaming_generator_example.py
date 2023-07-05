import os
from salesgpt.agents import SalesGPT

from langchain.chat_models import ChatOpenAI

with open('.env','r') as f:
    env_file = f.readlines()
envs_dict = {key.strip("'") :value.strip("\n") for key, value in [(i.split('=')) for i in env_file]}
os.environ['OPENAI_API_KEY'] = envs_dict['OPENAI_API_KEY']

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

# get generator of the LLM output
generator = sales_agent.step(return_streaming_generator=True, model_name="gpt-3.5-turbo-0613")

# operate on streaming LLM output in near-real time
# for instance, do something after each full sentence is generated
for chunk in generator: 
    print(chunk)