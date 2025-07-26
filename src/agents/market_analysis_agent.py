from typing import List, Dict
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from src.models.llm_provider import LLMFactory
from src.tools.news_api import NewsAPI

class MarketAnalysisAgent:
    def __init__(self, llm_provider: str = "ollama", model: str = "mistral"):
        self.llm = LLMFactory.get_llm(llm_provider, model)
        self.tools = [NewsAPI()]
        
        # Define the agent prompt
        prompt = PromptTemplate.from_template(
            """You are an expert financial analyst. Analyze the provided information and take appropriate actions.
            
            Consider:
            1. If news requires additional context, use the news_api tool
            2. For each news item, provide:
               - Company/Sector analysis
               - Trading signals
               - Risk assessment
               - Action items
            
            Current task: {input}
            {agent_scratchpad}
            """
        )
        
        # Create the agent
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    
    def analyze(self, task: str) -> Dict:
        """Run the agent with a specific task"""
        return self.agent_executor.invoke({"input": task})

    def analyze_market_news(self) -> List[Dict]:
        """Analyze current market news and generate insights"""
        # First, get recent news
        news_tool = NewsAPI()
        news_items = news_tool._run("stocks market analysis")
        
        analyses = []
        for news in news_items:
            result = self.analyze(
                f"Analyze this news and provide trading signals: {news['title']} - {news.get('snippet', '')}"
            )
            analyses.append({
                "news": news,
                "analysis": result
            })
        
        return analyses
