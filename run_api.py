import os
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from salesgpt.salesgptapi import SalesGPTAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



GPT_MODEL = "gpt-3.5-turbo-0613"
# GPT_MODEL_16K = "gpt-3.5-turbo-16k-0613"


@app.get("/")
async def say_hello():
    return {"message": "Hello World"}


class MessageList(BaseModel):
    session_id: str
    conversation_history: List[str]
    human_say: str

sessions = {}

@app.post("/chat")
async def chat_with_sales_agent(req: MessageList):
    if req.session_id in sessions:
        sales_api = sessions[req.session_id]
    else:
        sales_api = SalesGPTAPI(
            config_path="examples/example_agent_setup.json", verbose=True
        )
        sessions[req.session_id] = sales_api
    name, reply = sales_api.do(req.conversation_history, req.human_say)
    res = {"name": name, "say": reply.rstrip('<END_OF_TURN>')}
    return res


def _set_env():
    with open(".env", "r") as f:
        env_file = f.readlines()
    envs_dict = {
        key.strip("'").strip('"'): value.strip("\n").strip("'").strip('"')
        for key, value in [(i.split("=")) for i in env_file]
    }
    os.environ["OPENAI_API_KEY"] =envs_dict["OPENAI_API_KEY"]


if __name__ == "__main__":
    _set_env()
    uvicorn.run(app, host="127.0.0.1", port=8000)
