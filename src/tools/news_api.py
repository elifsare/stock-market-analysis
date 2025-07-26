from typing import Dict, List
from langchain.tools import BaseTool
from langchain.agents import Tool
import requests
import os

class NewsAPI(BaseTool):
    name = "financial_news"
    description = "Get the latest financial news from Bloomberg and other sources"

    def _run(self, query: str) -> List[Dict]:
        api_key = os.getenv('SERPAPI_KEY')
        if not api_key:
            raise ValueError("SERPAPI_KEY not found in environment")

        params = {
            "engine": "google",
            "q": f"site:bloomberg.com {query}",
            "tbm": "nws",
            "num": 5,
            "api_key": api_key,
            "time": "d"
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        if 'news_results' not in data:
            return []
            
        return data['news_results']

    async def _arun(self, query: str) -> List[Dict]:
        # Async implementation if needed
        raise NotImplementedError("Async not implemented")
