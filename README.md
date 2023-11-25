<div align="center">

# :robot: SalesGPT - Open Source AI Agent for Sales


<img src="https://demo-bucket-45.s3.amazonaws.com/filtr145_simple_robot_mascot_for_a_sales_company_professional_5282c6e6-40c1-4576-95c8-e4ba3c389f3f.png"  width="200">

![GitHub Repo stars](https://img.shields.io/github/stars/filip-michalsky/SalesGPT?style=social)
[![Downloads](https://pepy.tech/badge/salesGPT)](https://pepy.tech/project/salesgpt)
[![License](<https://img.shields.io/badge/License-MIT-brightgreen.svg>)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/salesgpt.svg)](https://badge.fury.io/py/salesgpt)
![GithubActions](https://github.com/filip-michalsky/SalesGPT/actions/workflows/unit-tests.yml/badge.svg)


</div>
<div align="center">

[Our Vision](#our-vision-build-the-best-open-source-ai-sales-agent) | [Features](#features) | [Demos and Use Cases](#demos-and-use-cases) |  [Quickstart](#quick-start) | [Setup](#setup) | [Contact Us](https://5b7mfhwiany.typeform.com/to/n6CbtxJm?utm_source=github-salesgpt&utm_medium=readme&utm_campaign=leads)

</div>

This repo is an implementation of a **context-aware** AI Agent for Sales using LLMs and can work across voice, email and texting (SMS, WhatsApp, WeChat, Weibo, Telegram, etc.). 

SalesGPT is *context-aware*, which means it can understand what stage of a sales conversation it is in and act accordingly.
Morever, SalesGPT has access to tools, such as your own pre-defined product knowledge base, significantly reducing hallucinations.

# Our Vision: Build the Best Open Source AI Sales Agent

We are building SalesGPT to power your best AI Sales Agents. Hence, we would love to learn more about use cases you are building towards which will fuel SalesGPT development roadmap, so please don't hesitate to reach out.

# Features

### Contextual Understanding: Sales Stage Awareness

The AI Sales Agent understands the conversation stage (you can define your own stages fitting your needs):

  - Introduction: Start the conversation by introducing yourself and your company. 
  - Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service.
  - Value Proposition: Briefly explain how your product/service can benefit the prospect. 
  - Needs Analysis: Ask open-ended questions to uncover the prospect's needs and pain points. 
  - Solution Presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.
  - Objection Handling: Address any objections that the prospect may have regarding your product/service. 
  - Close: Ask for the sale by proposing a next step. 
  - End Conversation: The user does not want to continue the conversation, so end the call.

### Business & Product Knowledge:
-  Reference only your business information & products and significantly reduce hallucinations!

### Use Any LLM to Power Your AI Sales Agent
- Thanks to our integration with [LiteLLM](https://github.com/BerriAI/litellm), you can choose *any closed/open-sourced LLM* to work with SalesGPT! Thanks to LiteLLM maintainers for this contribution!

### Power Real-time Sales Conversations
- Synchronous & Asynchronous Completion with LLMs
- Synchronous & Asynchronous Streaming from LLMs

### Optimized for Low Latency in Voice Channel
- Voice AI Sales Agent boasts **<1s** round trip response rate to human speakers which includes the entire pipeline - speech to text, LLM inference, and text to speech - while ensuring stability and scalability.

### Human in the loop
- For use cases where AI sales agent needs human supervision.

### Enterprise-Grade Security

- Upcoming integration with [PromptArmor](https://promptarmor.com/) to protect your AI Sales Agents against security vulnerabilities (see our roadmap).

# Demos and Use Cases

<i>Crusty AI Sales Agent Phone Call Demo - Powered by SalesGPT</i>  A New Way to Sell? 🤔

<div>
    <a href="https://www.loom.com/share/f0fac42954904471b266980e4948b07d">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/f0fac42954904471b266980e4948b07d-with-play.gif">
    </a>
  </div>


# Contact Us for Suggestions, Questions, or Help

We are building SalesGPT to power your best AI Sales Agents. Hence, we would love to learn more about use cases you are building towards which will fuel SalesGPT development roadmap.

**If you want us to build better towards your needs, or need help with your AI Sales Agents, please reach out to chat with us: [SalesGPT Use Case Intake Survey](https://5b7mfhwiany.typeform.com/to/n6CbtxJm?utm_source=github-salesgpt&utm_medium=readme&utm_campaign=leads)**

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



## Architecture

<img src="https://singularity-assets-public.s3.amazonaws.com/new_flow.png"  width="800" height="440">



## :red_circle: Latest News

- Sales Agent can now take advantage of **tools**, such as look up products in a product catalog!
- SalesGPT is now compatible with [LiteLLM](https://github.com/BerriAI/litellm), choose *any closed/open-sourced LLM* to work with SalesGPT! Thanks to LiteLLM maintainers for this contribution!
- SalesGPT works with synchronous and asynchronous completion, as well as synchronous/asynchronous streaming. Scale your Sales Agents up!



# Setup

## Install

Make sure you have a **python 3.10+** and run:

`pip install -r requirements.txt`

Create `.env` file and put your API keys there by specifying a line, for instance: 

`OPENAI_API_KEY=sk-xxx`

Install with pip

`pip install salesgpt`

## Run an Example AI Sales agent

`python run.py --verbose True --config examples/example_agent_setup.json`

from your terminal.

## Test your setup

1. Activate an environment with `python 3.10+`
2. cd `SalesGPT`
2. `pip install -r requirements.txt`
3. `pytest`

All tests should pass.

## Deploy

We have a SalesGPT deployment demo via FastAPI.

Please refer to [README-api.md](https://github.com/filip-michalsky/SalesGPT/blob/main/README-api.md) for instructions!

# Documentation

We leverage the [`langchain`](https://github.com/hwchase17/langchain) library in this implementation, specifically [Custom Agent Configuration](https://langchain-langchain.vercel.app/docs/modules/agents/how_to/custom_agent_with_tool_retrieval) and are inspired by [BabyAGI](https://github.com/yoheinakajima/babyagi) architecture.

# Roadmap

1) Documenting the Repo better
2) Documenting the API
3) Code Documentation
4) Refactor
5) Improve reliability of the parser [issue here](https://github.com/filip-michalsky/SalesGPT/issues/26) and [here](https://github.com/filip-michalsky/SalesGPT/issues/25)
7) Improve Deployment Instructions
8) Calling Functionality - sample code
9) Enterprise-Grade Security - integration with [PromptArmor](https://promptarmor.com/) to protect your AI Sales Agents against security vulnerabilities
10) LLM evaluations 
11) Resolve tickets and PRs (ongoing)
12) Add example implementation of OpenAI functions agent[issue here](https://github.com/filip-michalsky/SalesGPT/issues/17)
13) Add support for multiple tools [issue here](https://github.com/filip-michalsky/SalesGPT/issues/10)
14) Add an agent controller for when stages need to be traversed linearly without skips [issue here](https://github.com/filip-michalsky/SalesGPT/issues/19)
15) Add `tool_getter` to choose a tool based on vector distance to the tasks needed to be done
16) What tools should the agent have? (e.g., the ability to search the internet)
17) Add the ability of Sales Agent to interact with AI plugins on your website (.well-known/ai-plugin.json)
18) More SalesGPT examples


# About the Team

Lead Maintaner: Filip Michalsky 

- [Contact Email](mailto:filipmichalsky@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/filip-michalsky/)
- Follow us on X at [@FilipMichalsky](https://twitter.com/FilipMichalsky)

Our Support Team: 

- AI Engineering: Honza Michna ([LinkedIn](https://www.linkedin.com/in/jan-michna-998b78132/))

# How to Contribute

Contributions are highly encouraged! Please fork and submit a PR.



