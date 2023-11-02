import asyncio, uuid
from tortoise.queryset import Q
from typing import Any, Dict, List, Tuple
from salesgpt.models import ChatMessage


class SalesChat:
    chat_live_id: str = None
    salesperson_name: str = "Ted Lasso"
    customer_name: str = "Alice Yu"
    chat_live_history: List[str] = []
    loop: Any = None
    end_of_turn: str = '<END_OF_TURN>'
    end_of_call: str = '<END_OF_CALL>'

    def __init__(self, salesperson_name: str = None, customer_name: str = None):
        self.chat_live_id = uuid.uuid4().hex
        self.salesperson_name = salesperson_name if salesperson_name is not None else self.salesperson_name
        self.customer_name = customer_name if customer_name is not None else self.customer_name

    def get_salesperson_name(self):
        return self.salesperson_name

    def get_customer_name(self):
        return self.customer_name

    def get_live_chat_id(self):
        return self.chat_live_id

    def append(self, name: str, content: str) -> None:
        assert name == self.customer_name or name == self.salesperson_name
        if self.end_of_turn not in content:
            if self.end_of_call not in content:
                content = f"{content} {self.end_of_turn}"
            else:
                content = content.replace(self.end_of_call, "")
                content = f"{content} {self.end_of_turn} {self.end_of_call}"
        self.chat_live_history.append(f"{name}: {content}")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ChatMessage.create(chat_id=self.chat_live_id, name=name, content=content))

    def get_live_history(self) -> List[str]:
        return self.chat_live_history

    def is_live_ended(self) -> bool:
        return self.chat_live_history[-1].endswith(self.end_of_call)

    def query_history(self, chat_id: str) -> List[str]:
        loop = asyncio.get_event_loop()
        chat_msgs = loop.run_until_complete(ChatMessage.filter(
            Q(chat_id=chat_id) & Q(name__in=[self.customer_name, self.salesperson_name])).order_by('id').all())
        chat_history = [f"{msg.name}: {msg.content}" for msg in chat_msgs]
        return chat_history

    def query_last_history(self) -> List[str]:
        loop = asyncio.get_event_loop()
        last_msg = loop.run_until_complete(ChatMessage.filter(name=self.customer_name).order_by('-id').first())
        last_chat_msgs = loop.run_until_complete(ChatMessage.filter(chat_id=last_msg.chat_id).order_by('id').all())
        last_chat_history = [f"{msg.name}: {msg.content}" for msg in last_chat_msgs]
        return last_chat_history

    def query_all_history(self) -> List[str]:
        loop = asyncio.get_event_loop()
        chat_id_list = loop.run_until_complete(ChatMessage.filter(name=self.customer_name)
                                               .order_by('id').values_list("chat_id"))
        chat_id_list = [t[0] for t in list(dict.fromkeys(chat_id_list))]
        all_chat_msgs = loop.run_until_complete(ChatMessage.filter(chat_id__in=chat_id_list).order_by('id').all())
        all_chat_history = [f"{msg.name}: {msg.content}" for msg in all_chat_msgs]
        return all_chat_history

    def delete_all_history(self):
        loop = asyncio.get_event_loop()
        chat_id_list = loop.run_until_complete(ChatMessage.filter(name=self.customer_name)
                                               .order_by('id').values_list("chat_id"))
        chat_id_list = [t[0] for t in list(dict.fromkeys(chat_id_list))]
        loop.run_until_complete(ChatMessage.filter(chat_id__in=chat_id_list).delete())
