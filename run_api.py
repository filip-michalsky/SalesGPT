import json
import os
from typing import List, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from salesgpt.salesgptapi import SalesGPTAPI

# Load environment variables
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CORS_ORIGINS = ["http://localhost:3000", 
                "http://react-frontend:80",
                "https://sales-gpt-frontend-git-main-filip-odysseypartns-projects.vercel.app",
                "https://sales-gpt-frontend.vercel.app"]
CORS_METHODS = ["GET", "POST"]

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

class AuthenticatedResponse(BaseModel):
    message: str

def get_auth_key(authorization: str = Header(...)) -> None:
    auth_key = os.getenv("AUTH_KEY")
    if not auth_key:
        raise HTTPException(status_code=500, detail="AUTH_KEY not configured")
    expected_header = f"Bearer {auth_key}"
    if authorization != expected_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
async def say_hello():
    return {"message": "Hello World"}


class MessageList(BaseModel):
    session_id: str
    human_say: str


sessions = {}


@app.get("/botname", response_model=None)
async def get_bot_name(authorization: Optional[str] = Header(None)):
    load_dotenv()
    if os.getenv("ENVIRONMENT") == "production":
        get_auth_key(authorization)
        
    sales_api = SalesGPTAPI(
        config_path=os.getenv("CONFIG_PATH", "examples/example_agent_setup.json"),
        product_catalog=os.getenv(
            "PRODUCT_CATALOG", "examples/sample_product_catalog.txt"
        ),
        verbose=True,
        model_name=os.getenv("GPT_MODEL", "gpt-3.5-turbo-0613"),
    )
    name = sales_api.sales_agent.salesperson_name
    return {"name": name, "model": sales_api.sales_agent.model_name}


@app.post("/chat")
async def chat_with_sales_agent(req: MessageList, stream: bool = Query(False), authorization: Optional[str] = Header(None)):
    """
    Handles chat interactions with the sales agent.

    This endpoint receives a message from the user and returns the sales agent's response. It supports session management to maintain context across multiple interactions with the same user.

    Args:
        req (MessageList): A request object containing the session ID and the message from the human user.
        stream (bool, optional): A flag to indicate if the response should be streamed. Currently, streaming is not implemented.

    Returns:
        If streaming is requested, it returns a StreamingResponse object (not yet implemented). Otherwise, it returns the sales agent's response to the user's message.

    Note:
        Streaming functionality is planned but not yet available. The current implementation only supports synchronous responses.
    """
    sales_api = None
    if os.getenv("ENVIRONMENT") == "production":
        get_auth_key(authorization)
    # print(f"Received request: {req}")
    if req.session_id in sessions:
        print("Session is found!")
        sales_api = sessions[req.session_id]
        print(f"Are tools activated: {sales_api.sales_agent.use_tools}")
        print(f"Session id: {req.session_id}")
    else:
        print("Creating new session")
        sales_api = SalesGPTAPI(
            config_path=os.getenv("CONFIG_PATH", "examples/example_agent_setup.json"),
            verbose=True,
            product_catalog=os.getenv(
                "PRODUCT_CATALOG", "examples/sample_product_catalog.txt"
            ),
            model_name=os.getenv("GPT_MODEL", "gpt-3.5-turbo-0613"),
            use_tools=os.getenv("USE_TOOLS_IN_API", "True").lower()
            in ["true", "1", "t"],
        )
        print(f"TOOLS?: {sales_api.sales_agent.use_tools}")
        sessions[req.session_id] = sales_api

    # TODO stream not working
    if stream:

        async def stream_response():
            stream_gen = sales_api.do_stream(req.conversation_history, req.human_say)
            async for message in stream_gen:
                data = {"token": message}
                yield json.dumps(data).encode("utf-8") + b"\n"

        return StreamingResponse(stream_response())
    else:
        response = await sales_api.do(req.human_say)
        return response


# Main entry point
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
