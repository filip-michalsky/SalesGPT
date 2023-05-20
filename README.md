# :robot: SalesGPT - Your Context-Aware AI Sales Assistant

This repo demonstrates an implementation of a **context-aware** AI Sales Assistant using LLMs.

SalesGPT is context-aware, which means it can understand what section of a sales conversation it is in and act accordingly.

We leverage the [`langchain`](https://github.com/hwchase17/langchain) library in this implementation and are inspired by [BabyAGI](https://github.com/yoheinakajima/babyagi) architecture .

## Our Vision: Build the Best Open-Source Autonomous Sales Agent

We are building SalesGPT to power your best Autonomous Sales Agents. Hence, we would love to learn more about use cases you are building towards which will fuel SalesGPT development roadmap.

**If you want us to build better towards your needs, please fill out our 45 seconds [SalesGPT Use Case Survey](https://5b7mfhwiany.typeform.com/to/xmJbWIjG)**

## :red_circle: Latest News

### If you looking for help building your Autonomous Sales Agents

I am currently open to freelancing opps - please contact me through [my website](https://odysseypartners.ai?utm_source=SalesGPT) if you think I can help  you.

## Quickstart

```python
import os
from sales_gpt import SalesGPT
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = 'sk-xxx' # fill me in

llm = ChatOpenAI(temperature=0.9)

sales_agent = SalesGPT.from_llm(llm, verbose=False,
                            salesperson_name="Ted Lasso",
                            salesperson_role="Sales Representative",
                            company_name="Sleep Haven",
                            company_business='''Sleep Haven 
                            is a premium mattress company that provides
                            customers with the most comfortable and
                            supportive sleeping experience possible. 
                            We offer a range of high-quality mattresses,
                            pillows, and bedding accessories 
                            that are designed to meet the unique 
                            needs of our customers.''')

sales_agent.seed_agent()
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt

# agent 
sales_agent.step()

# user
user_input = input('Your response: ') # Yea, sure
sales_agent.human_step(user_input)

# agent
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt
sales_agent.step()
```
> Conversation Stage: 
> Introduction: Start the conversation by introducing yourself and your company. 

> Ted Lasso: Hello, my name is Ted Lasso and I'm calling on behalf of Sleep Haven. We are a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. I was wondering if you would be interested in learning more about our products and how they can improve your sleep?

> User: Yea, sure

> Conversation Stage: 
> Value proposition: Briefly explain how your product/service can benefit the prospect. 

> Ted Lasso: Great to hear that! Our mattresses are specially designed to contour to your body shape, providing the perfect level of support and comfort for a better night's sleep. Plus, they're made with high-quality materials that are built to last. Would you like to hear more about our different mattress options?


## Understanding Context

The bot understands the conversation stage (you can define your own stages fitting your needs):

- Introduction: Start the conversation by introducing yourself and your company. 
- Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service.
- Value proposition: Briefly explain how your product/service can benefit the prospect. 
- Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. 
- Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.
- Objection handling: Address any objections that the prospect may have regarding your product/service. 
- Close: Ask for the sale by proposing a next step. 
- End Conversation: The user does not want to continue the conversation, so end the call.
 
As such, this agent can have a natural sales conversation with a prospect and behaves based on the conversation stage. Hence, this notebook demonstrates how we can use AI to automate sales development representatives activites, such as outbound sales calls. 


## Architecture

<img src="https://images-genai.s3.us-east-1.amazonaws.com/architecture2.png"  width="800" height="400">

## Installation

Make sure your have a python 3.10+ and run:

`pip install -r requirements.txt`

Create `.env` file and put your Open AI Key there by specifying a line: 

`OPENAI_API_KEY=sk-xxx`

## Try it out 

To get a feel for a conversation with the AI Sales agent, you can run:

`python run.py`

from your terminal.

## Contact Us

For questions, you can [contact the repo author](mailto:filipmichalsky@gmail.com).

Follow me at [@FilipMichalsky](https://twitter.com/FilipMichalsky)


## SalesGPT Roadmap

- Knowledge base for products/services a Sales Agent can offer (so that LLM does not make it up)
- Convert LLM Chains (linear workflow) to an Agent (decides what to do based on user's input)
    - What tools should the agent have? (e.g., the ability to search the internet)
    - Add the ability of Sales Agent to interact with AI plugins on your website (.well-known/ai-plugin.json)
    
~~-
 Add the ability to stop generation when user interupts the agent~~
- Add a vectorstore to incorporate a real product knowledge base vs. the LLM making it up.

## Contributing

Contributions are highly encouraged!