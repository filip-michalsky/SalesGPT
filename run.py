import os
import argparse
import json
from tortoise import Tortoise, run_async
from langchain.chat_models import ChatLiteLLM
from salesgpt.agents import SalesGPT

from dotenv import load_dotenv

load_dotenv()


async def init_db():
    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['salesgpt.models']},
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
    parser.add_argument("--use_tools", type=bool,
                        help="Use tools or not", default=False)
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
    use_tools = args.use_tools
    product_catalog = args.product_catalog

    # Init database
    run_async(init_db())

    llm = ChatLiteLLM(temperature=0, model_name=os.environ.get('MODEL_NAME'))

    if config_path == "":
        print("No agent config specified, using a standard config")
        # keep boolean as string to be consistent with JSON configs.
        sales_agent = SalesGPT.from_llm(
            llm, use_tools=use_tools,
            product_catalog=product_catalog,
            salesperson_name=salesperson_name,
            customer_name=customer_name,
            verbose=verbose,
        )
    else:
        print(f"Agent config specified according to {config_path}")
        with open(config_path, "r", encoding=os.environ.get('ENCODING')) as f:
            config = json.load(f)
        print(f"Agent config {config}")
        sales_agent = SalesGPT.from_llm(llm, verbose=verbose, **config)

    sales_agent.seed_agent()
    print("=" * 10)
    cnt = 0
    while True:

        sales_agent.step()

        # end conversation
        if sales_agent.sales_chat.end():
            print("Sales Agent determined it is time to end the conversation.")
            break
        human_input = input("Your response: ")
        sales_agent.human_step(human_input)
        print("=" * 10)
