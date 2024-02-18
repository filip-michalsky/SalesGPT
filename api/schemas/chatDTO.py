from pydantic import BaseModel

class Chat(BaseModel):
    telegram_id: str
    messages: list[str]