import asyncio, uuid
from typing import Any, Dict, List, Tuple
from salesgpt.models import ChatMessage


class SalesChat:
    chat_id: str = None
    salesperson_name: str = "Ted Lasso"
    customer_name: str = "Alice Yu"
    chat_history: List[str] = []
    loop: Any = None
    end_of_turn: str = '<END_OF_TURN>'
    end_of_call: str = '<END_OF_CALL>'

    def __init__(self, salesperson_name: str, customer_name: str):
        self.chat_id = uuid.uuid4().hex
        self.salesperson_name = salesperson_name
        self.customer_name = customer_name
        self.loop = asyncio.new_event_loop()

    def append(self, name: str, content: str) -> None:
        assert name == self.customer_name or name == self.salesperson_name
        if self.end_of_turn not in content:
            content = f"{content} {self.end_of_turn}"
        self.chat_history.append(f"{name}: {content}")
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(ChatMessage.create(chat_id=self.chat_id, name=name, content=content))

    def get_history(self) -> List[str]:
        return self.chat_history

    def end(self) -> bool:
        return self.chat_history[-1].endswith(self.end_of_call)
