# :robot: SalesGPT - Your Context-Aware AI Sales Assistant

This repo demonstrates an implementation of a **context-aware** AI Sales Assistant using LLMs.

SalesGPT is context-aware, which means it can understand what section of a sales conversation it is in and act accordingly.
Morever, SalesGPT has access to tools, such as your own pre-defined product knowledge base, significantly reducing hallucinations!

We leverage the [`langchain`](https://github.com/hwchase17/langchain) library in this implementation, specifically [Custom Agent Configuration](https://langchain-langchain.vercel.app/docs/modules/agents/how_to/custom_agent_with_tool_retrieval) and are inspired by [BabyAGI](https://github.com/yoheinakajima/babyagi) architecture.

## Our Vision: Build the Best Open-Source Autonomous Sales Agent

We are building SalesGPT to power your best Autonomous Sales Agents. Hence, we would love to learn more about use cases you are building towards which will fuel SalesGPT development roadmap.

**If you want us to build better towards your needs, please fill out our 45 seconds [SalesGPT Use Case Survey](https://5b7mfhwiany.typeform.com/to/xmJbWIjG)**

### If you looking for help building your Autonomous Sales Agents

Please send an email to [the repo author](mailto:filipmichalsky@gmail.com).

## :red_circle: Latest News

- Sales Agent can now take advantage of **tools**, such as look up products in a product catalog!

### Demo: Outbound Prospecting from Crusty AI: A New Way to Sell? 🤔

<i>Crusty AI Sales Agent Phone Call Demo - Powered by SalesGPT</i>

<div>
    <a href="https://www.loom.com/share/f0fac42954904471b266980e4948b07d">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/f0fac42954904471b266980e4948b07d-with-play.gif">
    </a>
  </div>


## Quickstart

```python
import os
from salesgpt.agents import SalesGPT
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = 'sk-xxx' # fill me in

llm = ChatOpenAI(temperature=0.4)
                            
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

## Product Knowledge Base

The AI Sales Agent has access to tools, such as your internal Product Knowledge base.
This allows the agent to only talk about your own products and significantly reduces hallucinations.

## Understanding Context

The AI Sales Agent understands the conversation stage (you can define your own stages fitting your needs):

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

<img src="https://singularity-assets-public.s3.amazonaws.com/new_flow.png"  width="800" height="440">

## Installation

Make sure your have a python 3.10+ and run:

`pip install -r requirements.txt`

Create `.env` file and put your Open AI Key there by specifying a line: 

`OPENAI_API_KEY=sk-xxx`

Install with pip

`pip install salesgpt`

## Try it out 

To get a feel for a conversation with the AI Sales agent, you can run:

`python run.py --verbose True --config examples/example_agent_setup.json`

from your terminal.

## Contact Us

For questions, you can [contact the repo author](mailto:filipmichalsky@gmail.com).

Follow me at [@FilipMichalsky](https://twitter.com/FilipMichalsky)


## SalesGPT Roadmap


- Add the ability of Sales Agent to interact with AI plugins on your website (.well-known/ai-plugin.json)

- What tools should the agent have? (e.g., the ability to search the internet)

~~-
 Add the ability to stop generation when user interupts the agent~~

~~- Add a vectorstore to incorporate a real product knowledge base vs. the LLM making it up.~~

~~- Knowledge base for products/services a Sales Agent can offer (so that LLM does not make it up)~~

~~- Convert LLM Chains (linear workflow) to an Agent (decides what to do based on user's input)~~



## Contributing

Contributions are highly encouraged! Please fork and submit a PR.
