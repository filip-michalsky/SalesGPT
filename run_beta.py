import os
import argparse
import json
from tortoise import Tortoise, run_async
from openai import OpenAI
from salesgpt_beta.agents import SalesGPT

from dotenv import load_dotenv

load_dotenv()


async def init_db():
    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['salesgpt_beta.models']},
    )


if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Description of your program")

    # Add arguments
    parser.add_argument(
        "--config", type=str,
        help="Path to agent config file",
        default=""
    )
    parser.add_argument("--verbose", type=bool,
                        help="Verbosity", default=False)
    parser.add_argument("--salesperson_name", type=str,
                        help="The salesperson name", default="Ted Lasso")
    parser.add_argument("--customer_name", type=str,
                        help="The customer name", default="Alice Yu")
    parser.add_argument("--customer_phone", type=str,
                        help="The customer phone", default="+8613911118888")
    parser.add_argument("--product_catalog", type=str,
                        help="Product catalog location",
                        default='examples/sample_product_catalog.txt')

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    config_path = args.config
    verbose = args.verbose
    salesperson_name = args.salesperson_name
    customer_name = args.customer_name
    customer_phone = args.customer_phone
    product_catalog = args.product_catalog

    # Init database
    run_async(init_db())

    openAI = OpenAI()

    if config_path == "":
        print("No agent config specified, using a standard config")
        # keep boolean as string to be consistent with JSON configs.
        sales_agent = SalesGPT.from_llm(
            llm=openAI,
            customer_name=customer_name,
            customer_phone=customer_phone,
            salesperson_name=salesperson_name,
            product_catalog=product_catalog,
            verbose=verbose,
        )
    else:
        print(f"Agent config specified according to {config_path}")
        with open(config_path, "r", encoding=os.environ.get('ENCODING')) as f:
            config = json.load(f)
        print(f"Agent config {config}")
        sales_agent = SalesGPT.from_llm(llm=openAI, verbose=verbose, **config)

    sales_agent.seed_agent()
    print("=" * 10)
    cnt = 0
    while True:

        response = sales_agent.step()
        print(response)

        # end conversation
        if sales_agent.chatDao.is_live_ended():
            print("Sales Agent determined it is time to end the conversation.")
            break
        human_input = input("Your response: ")
        sales_agent.human_step(human_input)
        print("=" * 10)
