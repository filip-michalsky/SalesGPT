import os
from typing import List

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from salesgpt.salesgptapi import SalesGPTAPI
from fastapi.responses import Response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GPT_MODEL = "gpt-3.5-turbo-0613"

# Global variable to store conversation state
conversation_state = {
    "greeted": False,
    "history": []
}

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
    os.environ["TWILIO_ACCOUNT_SID"] = envs_dict["TWILIO_ACCOUNT_SID"]
    os.environ["TWILIO_AUTH_TOKEN"] = envs_dict["TWILIO_AUTH_TOKEN"]
    os.environ["TWILIO_PHONE_NUMBER"] = envs_dict["TWILIO_PHONE_NUMBER"]

def get_phone_number():
    return input("Enter the phone number to dial: ")

def initiate_call(to_number):
    client = Client()
    call = client.calls.create(
        to=to_number,
        from_=os.environ["TWILIO_PHONE_NUMBER"],
        url="https://8ead-74-65-4-51.ngrok-free.app/twiml_endpoint"
    )
    return call.sid

@app.post("/twiml_endpoint")
def twiml_response():
    response = VoiceResponse()
    if not conversation_state["greeted"]:
        with response.gather(input='speech', action='/handle_input', method='POST', timeout=5) as gather:
            gather.say("Hi there! This is Ted Lasso from Sleep Haven. I heard you're looking to buy a mattress. How can I assist you in finding the perfect mattress for a better night's sleep?")
            conversation_state["greeted"] = True
    else:
        response.pause(length=2)  # Pause for 2 seconds to give the user some time
        with response.gather(input='speech', action='/handle_input', method='POST', timeout=5) as gather:
            gather.say("Sorry, I didn't catch that. Can you please repeat?")
        response.redirect('/twiml_endpoint')  # Redirect to the same endpoint if no input is captured
    return Response(content=str(response), media_type="text/xml")

@app.post("/handle_input")
async def handle_input(request: Request):
    try:
        form_data = await request.form()
        user_input = form_data.get('SpeechResult')

        # Get response from SalesGPT using the captured input
        sales_api = SalesGPTAPI(config_path="examples/example_agent_setup.json", verbose=True)
        _, reply = sales_api.do([], user_input)  # Assuming no conversation history for simplicity

        # Generate TwiML response with SalesGPT's reply
        response = VoiceResponse()
        response.say(reply)
        response.redirect('/twiml_endpoint')  # Redirect to the main endpoint to continue the conversation
        return Response(content=str(response), media_type="text/xml")
    except Exception as e:
        # Handle any exceptions and return a default TwiML response
        response = VoiceResponse()
        response.say("Sorry, there was an error processing your request. Please try again.")
        return Response(content=str(response), media_type="text/xml")



if __name__ == "__main__":
    _set_env()
    phone_number = get_phone_number()
    initiate_call(phone_number)
    uvicorn.run(app, host="127.0.0.1", port=8000)
