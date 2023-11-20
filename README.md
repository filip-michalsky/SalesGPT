# :robot: SalesGPT - Open Source AI Agent for Sales

<div align="center">
       
[Features](#features) [Performance Statistics](#performance-statistics) [Demos and Use Cases](#demos-and-use-cases) [Contact Us](#contact-us-for-suggestions-questions-or-help)

</div>

This repo demonstrates an implementation of a **context-aware** AI Agent for Sales using LLMs and can work across voice, email and texting. SalesGPT is context-aware, which means it can understand what stage of a sales conversation it is in and act accordingly.
Morever, SalesGPT has access to tools, such as your own pre-defined product knowledge base, significantly reducing hallucinations!

# Features

- Business & Product Knowledge: Reference only your business information & products and significantly reduce hallucinations
- Contextual Understanding: Sales Stage Awareness
       - Introduction: Start the conversation by introducing yourself and your company. 
       - Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service.
       - Value Proposition: Briefly explain how your product/service can benefit the prospect. 
       - Needs Analysis: Ask open-ended questions to uncover the prospect's needs and pain points. 
       - Solution Presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.
       - Objection Handling: Address any objections that the prospect may have regarding your product/service. 
       - Close: Ask for the sale by proposing a next step. 
       - End Conversation: The user does not want to continue the conversation, so end the call.
- Synchronous & Asynchronous Completion
- Synchronous & Asynchronous Streaming

# Performance Statistics

- Latency
- ...
- ...
- ...

# Demos and Use Cases

<i>Crusty AI Sales Agent Phone Call Demo - Powered by SalesGPT</i>

<div>
    <a href="https://www.loom.com/share/f0fac42954904471b266980e4948b07d">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/f0fac42954904471b266980e4948b07d-with-play.gif">
    </a>
  </div>

### To get a feel for a conversation with the AI Sales agent, you can run:

`python run.py --verbose True --config examples/example_agent_setup.json`

from your terminal.

# Contact Us for Suggestions Questions or Help

Please reach out here to chat with us: <a href="https://docs.google.com/forms/d/e/1FAIpQLSebN17aNh-HlkGu2wOKiPzhFlQuorNk_7Mk6LQO3_vFsbuOZQ/viewform?usp=sharing">Contact Form</a> 

# Quick Start

```python
import os
from salesgpt.agents import SalesGPT
from langchain.chat_models import ChatLiteLLM

from dotenv import load_dotenv
load_dotenv() # make sure you have .env file with your API keys, eg., OPENAI_API_KEY=sk-xxx

# select your model - we support 50+ LLMs via LiteLLM https://docs.litellm.ai/docs/providers
llm = ChatLiteLLM(temperature=0.4, model_name="gpt-3.5-turbo") 
                            
sales_agent = SalesGPT.from_llm(llm, use_tools=True, verbose=False,
                            product_catalog = "examples/sample_product_catalog.txt",
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
                            needs of our customers.'''
                            )
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

# user
user_input = input('Your response: ') # What pricing do you have for your mattresses?
sales_agent.human_step(user_input)

# agent
sales_agent.determine_conversation_stage() # optional for demonstration, built into the prompt
sales_agent.step()
```

> Conversation Stage: 
> Introduction: Start the conversation by introducing yourself and your company. 

> Thought: Do I need to use a tool? No <br>
> Ted Lasso: Hello, my name is Ted Lasso and I'm calling on behalf of Sleep Haven. We are a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. I was wondering if you would be interested in learning more about our products and how they can improve your sleep?

> User: Yea, sure

> Conversation Stage: 
> Value proposition: Briefly explain how your product/service can benefit the prospect. 

> Thought: Do I need to use a tool? No <br>
> Ted Lasso: Great to hear that! Our mattresses are specially designed to contour to your body shape, providing the perfect level of support and comfort for a better night's sleep. Plus, they're made with high-quality materials that are built to last. Would you like to hear more about our different mattress options?

> User:  What pricing do you have for your mattresses?

> Thought: Do I need to use a tool? Yes --> AI Agent uses tools here.<br>
> Action: ProductSearch<br>
> ActionInput pricing for mattresses<br>
> Observation: Sleep Haven offers three mattresses: the Classic Harmony Spring Mattress for $1,299, the Plush Serenity Bamboo Mattress for $2,599, and the Luxury Cloud-Comfort Memory Foam Mattress for $999. The sizes available vary by mattress.<br>
> Ted Lasso: Sleep Haven offers three mattresses at different price points. The Classic Harmony Spring Mattress is priced at $1,299, the Plush Serenity Bamboo Mattress is priced at $2,599, and the Luxury Cloud-Comfort Memory Foam Mattress is priced at $999. The prices may vary depending on the size you choose. Would you like more information about the specific sizes and features of each mattress? 

# Install Test and Deploy

### Install

Make sure your have a **python 3.10+** and run:

`pip install -r requirements.txt`

Create `.env` file and put your API keys there by specifying a line, for instance: 

`OPENAI_API_KEY=sk-xxx`

Install with pip

`pip install salesgpt`

### Test

1. `pip install -r requirements.txt`
2. `pytest`

All tests should pass.

### Deploy

We have a SalesGPT deployment demo via FastAPI.

Please refer to [README-api.md](https://github.com/filip-michalsky/SalesGPT/blob/main/README-api.md) for instructions!

# Documentation

We leverage the [`langchain`](https://github.com/hwchase17/langchain) library in this implementation, specifically [Custom Agent Configuration](https://langchain-langchain.vercel.app/docs/modules/agents/how_to/custom_agent_with_tool_retrieval) and are inspired by [BabyAGI](https://github.com/yoheinakajima/babyagi) architecture.

# Roadmap

1) Documenting the Repo
2) Documenting the API
3) Code Documentation
4) Refactor
5) Agent Parsing Reliability
7) Deployment Instructions
8) Calling Functionality
9) Security Integration via prompt-armor
10) Resolve tickets and PRs (ongoing)

# How to Contribute

Contributions are highly encouraged! Please fork and submit a PR.

# About the Team




