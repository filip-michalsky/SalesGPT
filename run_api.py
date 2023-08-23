import os
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from salesgpt.salesgptapi import SalesGPTAPI

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


def _set_env():
    with open(".env", "r") as f:
        env_file = f.readlines()
    envs_dict = {
        key.strip("'"): value.strip("\n")
        for key, value in [(i.split("=")) for i in env_file]
    }
    os.environ["OPENAI_API_KEY"] = envs_dict["OPENAI_API_KEY"]


if __name__ == "__main__":
    _set_env()
    uvicorn.run(app, host="127.0.0.1", port=8000)
