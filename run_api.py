import os
from typing import List
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from salesgpt.salesgptapi import SalesGPTAPI
import json

# Load environment variables
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CORS_ORIGINS = ["http://localhost:3000","http://react-frontend:80"]
CORS_METHODS = ["GET","POST"]
# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS, 
    allow_headers=["*"],
)

# API configuration and routes
CONFIG_PATH = "examples/example_agent_setup.json"
print(f"Config path: {CONFIG_PATH}")
GPT_MODEL = "gpt-3.5-turbo-0613"

@app.get("/")
async def say_hello():
    return {"message": "Hello World"}

class MessageList(BaseModel):
    session_id: str
    human_say: str

sessions = {}

@app.get("/botname")
async def get_bot_name():
    sales_api = SalesGPTAPI(config_path=CONFIG_PATH, verbose=True)
    name = sales_api.sales_agent.salesperson_name
    return {"name": name}

@app.post("/chat")
async def chat_with_sales_agent(req: MessageList, stream: bool = Query(False)):
    '''
    Response is of type:
    '''
    sales_api = None
    #print(f"Received request: {req}")
    if req.session_id in sessions:
        print("Session is found!")
        sales_api = sessions[req.session_id]
        print(f"Are tools activated: {sales_api.sales_agent.use_tools}")
        print(f"Session id: {req.session_id}")
    else:
        print("Creating new session")
        sales_api = SalesGPTAPI(config_path=CONFIG_PATH, verbose=True,use_tools=True)
        print(f"TOOLS?: {sales_api.sales_agent.use_tools}")
        sessions[req.session_id] = sales_api


    #TODO stream not working
    if stream:
        async def stream_response():
            stream_gen = sales_api.do_stream(req.conversation_history, req.human_say)
            async for message in stream_gen:
                data = {"token": message}
                yield json.dumps(data).encode('utf-8') + b'\n'
        return StreamingResponse(stream_response())
    else:
        response = sales_api.do(req.human_say)
        return response

# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
