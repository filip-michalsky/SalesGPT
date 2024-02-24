from pydantic import BaseModel

class Chat(BaseModel):
    messages: list[str]