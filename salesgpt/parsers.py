import re
from typing import Union

from langchain.agents.agent import AgentOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish  # OutputParserException


class SalesConvoOutputParser(AgentOutputParser):
    react_regex = r"Action: (.*?)[\n]*Action Input: (.*)"
    ai_prefix: str = "AI"  # change for salesperson_name
    verbose: bool = False

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        if self.verbose:
            print("TEXT")
            print(text)
            print("-------")
        if f"{self.ai_prefix}:" in text:
            pure_text = text.split(f"{self.ai_prefix}:")[-1].strip()
            return AgentFinish(
                {"output": pure_text}, text
            )
        match = re.search(self.react_regex, text)
        if not match:
            return AgentFinish(
                {"output": text}, text,
            )
        action = match.group(1)
        action_input = match.group(2)
        return AgentAction(action.strip(), action_input.strip(" ").strip('"'), text)

    @property
    def _type(self) -> str:
        return "sales-agent"
