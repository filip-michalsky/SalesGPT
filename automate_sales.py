import argparse

import os
import json

from sales_gpt import SalesGPT
from langchain.chat_models import ChatOpenAI

if __name__ == "__main__":

    # import your OpenAI key (put in your .env file)
    with open('.env','r') as f:
        env_file = f.readlines()
    envs_dict = {key.strip("'"):value for key, value in [(i.split('=')) for i in env_file]}
    os.environ['OPENAI_API_KEY'] = envs_dict['OPENAI_API_KEY']

    # Initialize argparse
    parser = argparse.ArgumentParser(description='Description of your program')

    # Add arguments
    parser.add_argument('--conf', type=str, help='Path to agent config file', default='')
    parser.add_argument('--verbose', type=bool, help='Verbosity', default=False)
    parser.add_argument('--max_num_turns', type=int, help='Maximum number of turns in the sales conversation', default=5)

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    config_path = args.conf
    verbose = args.verbose
    max_num_turns = args.max_num_turns

    llm = ChatOpenAI(temperature=0.9)

    config = {
    "salesperson_name": "Ted Lasso",
    "salesperson_role": "Business Development Representative",
    "company_name": "Sleep Haven",
    "company_busines": "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.",
    "company_values": "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.",
    "conversation_purpose": "find out whether they are looking to achieve better sleep via buying a premier mattress."
}

    if config_path=='':
        print('No agent config specified, using a standard config')
        sales_agent = SalesGPT.from_llm(llm, verbose=verbose)
    else:
        with open(config_path,'r') as f:
            config = json.load(f)
        print(f'Agent config {config}')
        sales_agent = SalesGPT.from_llm(llm, verbose=verbose, **config)

    sales_agent.seed_agent()
    sales_agent.determine_conversation_stage()
    print('='*10)
    cnt = 0
    while cnt !=max_num_turns:
        
        sales_agent(inputs={})
        human_input = input('Your response: ')
        sales_agent.human_step(human_input)
        print('='*10)
        sales_agent.determine_conversation_stage()