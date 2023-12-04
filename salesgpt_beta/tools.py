import os, json
from typing import Any, List
from datetime import date
from pydantic import BaseModel
import serpapi


def get_tools_list():
    get_today_tool_desc = {
        'type': 'function',
        'function': eval(GetTodayTool().model_dump_json())
    }
    live_search_tool_desc = {
        'type': 'function',
        'function': eval(LiveSearchTool().model_dump_json())
    }
    tools = [get_today_tool_desc, live_search_tool_desc]
    return tools


def find_tool_by_name(tool_name: str):
    tool_map = {
        'get_today': GetTodayTool.get_today,
        'live_search': LiveSearchTool.search,
    }
    return tool_map[tool_name]


class GetTodayTool(BaseModel):
    name: str = 'get_today'
    description: str = (
        'Returns todays date, use this for any questions related to knowing todays date. '
        'The input should be always be an empty string, and this function will always return todays date.'
        'Any date mathmatics should occur outside this function.'
    )
    parameters: dict = {
        'type': 'object',
        'properties': {},
        'required': [],
    }

    @staticmethod
    def get_today() -> str:
        return str(date.today())


class LiveSearchTool(BaseModel):
    name: str = 'live_search'
    description: str = (
        "Answer questions about current events or information."
        "Input should be a search query."
    )
    parameters: dict = {
        'type': 'object',
        'properties': {
            'query': {"type": "string", "description": "the query to be searched"},
            'engine': {"type": "string", "enum": ["google", "bing", "baidu", "yahoo"]}
        },
        'required': ['query'],
    }

    @staticmethod
    def search(query: str, engine: str = 'google') -> str:
        client = serpapi.Client(api_key=os.getenv("SERPAPI_API_KEY"))
        response = client.search({
            'engine': engine,
            'q': query,
            'output': 'json'
        })
        return json.dumps(response.get("organic_results", []))


if __name__ == "__main__":
    print(get_tools_list())
