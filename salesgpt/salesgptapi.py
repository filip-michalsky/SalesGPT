import json

from langchain_community.chat_models import ChatLiteLLM
import asyncio
from salesgpt.agents import SalesGPT
import re
GPT_MODEL = "gpt-3.5-turbo"

class SalesGPTAPI:
    USE_TOOLS = True

    def __init__(self, config_path: str, verbose: bool = False, max_num_turns: int = 20,use_tools=True):
        self.config_path = config_path
        self.verbose = verbose
        self.max_num_turns = max_num_turns
        self.llm = ChatLiteLLM(temperature=0.2, model_name=GPT_MODEL)
        self.conversation_history = []
        self.use_tools = use_tools
        self.sales_agent = self.initialize_agent()
        self.current_turn = 0
    def initialize_agent(self):
        if self.config_path == "":
            print("No agent config specified, using a standard config")
            if self.use_tools:
                print("USING TOOLS")
                sales_agent = SalesGPT.from_llm(
                    self.llm,
                    use_tools=True,
                    product_catalog="examples/sample_product_catalog.txt",
                    salesperson_name="Ted Lasso",
                    verbose=self.verbose,
                )
            else:
                sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose)
        else:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            if self.verbose:
                print(f"Agent config {config}")
            if self.use_tools:
                print("USING TOOLS")
                config["use_tools"] = True
                config["product_catalog"] = "examples/sample_product_catalog.txt"
            else:
                config.pop("use_tools", None)  # Remove the use_tools key from config if it exists
            sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose, **config)
        print(f"SalesGPT use_tools: {sales_agent.use_tools}")  # Print the use_tools value of the SalesGPT instance
        sales_agent.seed_agent()
        return sales_agent

    def do(self, human_input=None):
        self.current_turn+=1
        current_turns = self.current_turn
        if current_turns >= self.max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            return ["BOT","In case you'll have any questions - just text me one more time!"]

        #self.sales_agent.seed_agent() why do we seeding at each turn? put to agent_init
        #self.sales_agent.conversation_history = conversation_history

        if human_input is not None:
            self.sales_agent.human_step(human_input)

        ai_log = self.sales_agent.step(stream=False)
        self.sales_agent.determine_conversation_stage()
        if "<END_OF_CALL>" in self.sales_agent.conversation_history[-1]:
            print("Sales Agent determined it is time to end the conversation.")
            return ["BOT","In case you'll have any questions - just text me one more time!"]

        reply = self.sales_agent.conversation_history[-1]

        if self.verbose:
            print("=" * 10)
        ''''''
        if ai_log['intermediate_steps'][1]['outputs']['intermediate_steps'] is not []:
            try:
                res_str = ai_log['intermediate_steps'][1]['outputs']['intermediate_steps'][0]
                tool_search_result = res_str[0]
                agent_action = res_str[0]
                tool,tool_input,log = agent_action.tool, agent_action.tool_input, agent_action.log
                actions = re.search(r"Action: (.*?)[\n]*Action Input: (.*)",log)
                action_input= actions.group(2)
                action_output = ai_log['intermediate_steps'][1]['outputs']['intermediate_steps'][0][1]
            except:
                tool,tool_input,action,action_input,action_output = "","","","",""
        else:   
            tool,tool_input,action,action_input,action_output = "","","","",""
        return {
            "bot_name": reply.split(": ")[0],
            "response": reply.split(": ")[1].rstrip('<END_OF_TURN>'),
            "conversational_stage": self.sales_agent.current_conversation_stage,
            "tool": tool,
            "tool_input": tool_input,
            "action_output": action_output,
            "action_input": action_input
        }

    async def do_stream(self, conversation_history: [str], human_input=None):
        current_turns = len(conversation_history) + 1
        if current_turns >= self.max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            yield ["BOT","In case you'll have any questions - just text me one more time!"]
            raise StopAsyncIteration

        self.sales_agent.seed_agent()
        self.sales_agent.conversation_history = conversation_history

        if human_input is not None:
            self.sales_agent.human_step(human_input)

        stream_gen = self.sales_agent.astep(stream=True)
        for model_response in stream_gen:
            for choice in model_response.choices:
                message = choice['delta']['content']
                if message is not None:
                    if "<END_OF_CALL>" in message:
                        print("Sales Agent determined it is time to end the conversation.")
                        yield ["BOT","In case you'll have any questions - just text me one more time!"]
                    yield message
                else:
                    continue