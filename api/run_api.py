import os
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from api.config import ApiKeySettings
from salesgpt.salesgptapi import SalesGPTAPI

api_settings = ApiKeySettings()
app = FastAPI()

GPT_MODEL = "gpt-3.5-turbo-0613"
# GPT_MODEL_16K = "gpt-3.5-turbo-16k-0613"


@app.get("/")
async def say_hello():
    return {"message": "Hello World"}


class MessageList(BaseModel):
    conversation_history: List[str]
    human_say: str


@app.post("/chat")
async def chat_with_sales_agent(req: MessageList):
    sales_api = SalesGPTAPI(
        config_path="examples/example_agent_setup.json", verbose=True
    )
    name, reply = sales_api.do(req.conversation_history, req.human_say)
    res = {"name": name, "say": reply}
    return res



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
