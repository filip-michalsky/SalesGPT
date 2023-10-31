import os
import argparse
import json

from langchain.chat_models import ChatLiteLLM
from salesgpt.agents import SalesGPT

from dotenv import load_dotenv
load_dotenv()  # loads .env file


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
    parser.add_argument("--use_tools", type=bool,
                        help="Use tools or not", default=False)
    parser.add_argument("--product_catalog", type=str,
                        help="Product catalog location (examples/sample_product_catalog.txt)",
                        default=None)
    parser.add_argument("--max_num_turns", type=int,
                        help="Maximum number of turns in the sales conversation",
                        default=10)

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    config_path = args.config
    verbose = args.verbose
    salesperson_name = args.salesperson_name
    use_tools = args.use_tools
    max_num_turns = args.max_num_turns
    product_catalog = args.product_catalog

    llm = ChatLiteLLM(temperature=0, model_name=os.environ.get('MODEL_NAME'))

    if config_path == "":
        print("No agent config specified, using a standard config")
        # keep boolean as string to be consistent with JSON configs.
        sales_agent = SalesGPT.from_llm(
            llm, use_tools=use_tools,
            product_catalog=product_catalog,
            salesperson_name=salesperson_name,
            verbose=verbose,
        )
    else:
        with open(config_path, "r", encoding=os.environ.get('ENCODING')) as f:
            config = json.load(f)
        print(f"Agent config {config}")
        sales_agent = SalesGPT.from_llm(llm, verbose=verbose, **config)

    sales_agent.seed_agent()
    print("=" * 10)
    cnt = 0
    while cnt != max_num_turns:
        cnt += 1
        if cnt == max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            break
        sales_agent.step()

        # end conversation
        if "<END_OF_CALL>" in sales_agent.conversation_history[-1]:
            print("Sales Agent determined it is time to end the conversation.")
            break
        human_input = input("Your response: ")
        sales_agent.human_step(human_input)
        print("=" * 10)
