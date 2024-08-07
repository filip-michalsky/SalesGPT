---
sidebar_position: 2

---
# Internet Search

SalesGPT now has the capability to perform internet searches using DuckDuckGo through a pre-made LangChain tool. This feature allows the AI sales agent to access up-to-date information from the web during conversations, enhancing its ability to provide relevant and timely responses.

## How to Enable Internet Search

To enable the DuckDuckGo search functionality in your SalesGPT setup:

1. Ensure you have the latest version of LangChain installed.

2. Add the DuckDuckGo search tool to your tools list in the `get_tools` function within the `tools.py` file:

   ```python
   from langchain.tools import DuckDuckGoSearchRun

   def get_tools(product_catalog):
       # ... other tool configurations ...

       tools.extend([
           # ... other tools ...
           Tool(
               name="WebSearch",
               func=DuckDuckGoSearchRun().run,
               description="Useful for when you need to search the web for current information.",
           ),
       ])

       return tools
   ```

3. Make sure the `USE_TOOLS_IN_API` environment variable is set to `True` in your `.env` file:

   ```
   USE_TOOLS_IN_API=True
   ```

By adding this tool, your SalesGPT agent will be able to perform web searches when it needs to find information that isn't available in its training data or product catalog. This can be particularly useful for answering questions about current events, market trends, or competitor information.

Remember to use this tool responsibly and in compliance with DuckDuckGo's terms of service.
