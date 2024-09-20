---
sidebar_position: 2

---
# Pre-built Tools

SalesGPT is not limited to just custom-built tools. It can also leverage a wide range of pre-built tools available from LangChain. These tools provide additional capabilities and integrations that can enhance your AI sales agent's functionality.

## Using LangChain's Pre-built Tools

LangChain offers a variety of pre-made tools that you can easily integrate into SalesGPT. These tools cover a wide range of functionalities, from web searches to mathematical calculations.

To use these tools:

1. Set up the desired tools according to the LangChain documentation.
2. Add the configured tools to the "tools" list in your SalesGPT setup.

You can find the full list of available tools and their setup instructions in the [LangChain Tools documentation](https://python.langchain.com/v0.2/docs/integrations/tools/).

Some popular pre-built tools include:

- Search tools (e.g., SerpAPI, Google Search)
- Calculator tools
- Weather tools
- News API tools
- And many more!

By incorporating these pre-built tools, you can significantly expand the capabilities of your AI sales agent, allowing it to access real-time information, perform calculations, or integrate with various APIs as needed during sales conversations.

Remember to review the documentation for each tool you want to use, as some may require additional setup steps or API keys.


## Example: Weather Search Tool

One pre-built tool that has been implemented in SalesGPT is the weather search tool. This serves as a good example of how to set up and use a pre-built tool from LangChain. Here's how it's implemented:

1. First, ensure you have the necessary API key. For the weather tool, you need an OpenWeatherMap API key. You can get a free key that allows 1000 requests per day from [OpenWeatherMap](https://openweathermap.org/api).

2. Add the API key to your `.env` file:

   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```

3. In the `tools.py` file, import the necessary components and set up the tool:

   ```python
   from langchain.tools import OpenWeatherMapAPIWrapper
   import os

   def weather_search(query):
       OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
       weather = OpenWeatherMapAPIWrapper()
       return weather.run(query)
   ```

4. Add the weather tool to your `get_tools` function:

   ```python
   def get_tools(product_catalog):
       tools = load_tools(["openweathermap-api"])
       tools.extend([
           # ... other tools ...
           Tool(
               name="WeatherSearch",
               func=weather_search,
               description="Useful for getting current weather information for a specific location.",
           ),
       ])
       return tools
   ```

This example demonstrates how to set up a pre-built tool from LangChain. Each tool may have its own setup requirements, such as API keys or additional configurations. Always refer to the LangChain documentation for specific setup instructions for each tool you want to use.


