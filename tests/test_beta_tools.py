import os, json
from salesgpt_beta.tools import LiveSearchTool


class TestBetaTools:

    def testSearchApi(self, load_env):
        search = LiveSearchTool()
        response = search.search('Sleep Haven')
        print(response)
        assert response is not None, "Agent output cannot be None."

