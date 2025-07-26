from typing import Dict, List
import json
import time
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
import ollama

# Load environment variables
load_dotenv()

class MarketAnalyst:
    def __init__(self):
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        self.slack_token = os.getenv('SLACK_BOT_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL')
        
    def fetch_news(self) -> List[Dict]:
        from tools import NewsAPI
        news_tool = NewsAPI()
        return news_tool._run("market analysis stocks finance")
        
    def analyze_news(self, news_item: Dict) -> Dict:
        prompt = f"""You are an expert financial analyst. Analyze this news and provide SPECIFIC trading signals and actionable insights:

Title: {news_item.get('title')}
Snippet: {news_item.get('snippet')}
Source: {news_item.get('link', 'Unknown')}

Provide your analysis in this EXACT format:

MARKET DIRECTION: [MUST be one of: BULLISH (>5% upside), BEARISH (>5% downside), or NEUTRAL (±5% range)]

PRIMARY TRADE:
- Tickers: [SPECIFIC stock symbols or ETFs, e.g., "SPY, QQQ, AAPL"]
- Action: [BUY or SELL]
- Entry: [Current price level]
- Target: [Price target with % gain]
- Stop: [Stop loss level with % risk]
- Timeframe: [Days, Weeks, or Months]

KEY CATALYSTS:
[List 2-3 specific events/factors that could move the market]

RISK FACTORS:
[List 2-3 specific risks that could affect the trade]

CONFIDENCE: [HIGH, MEDIUM, or LOW - based on available data and clarity of signals]
"""
        # Call Ollama
        response = ollama.chat(model='mistral', messages=[{
            'role': 'user',
            'content': prompt
        }])
        
        return {
            'news': news_item,
            'analysis': response['message']['content'],
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def save_analysis_json(self, analysis: Dict, output_dir: Path) -> Path:
        """Save individual analysis to a JSON file"""
        # Create a filename from the title (clean it up for filesystem)
        title = analysis['news']['title']
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:50]  # Limit length
        
        timestamp = analysis['timestamp'].replace(':', '-').replace(' ', '_')
        filename = f"{timestamp}_{safe_title}.json"
        
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
            
        return filepath

    def send_to_slack(self, analysis: Dict, json_file: Path = None):
        """Send analysis to Slack with file path information"""
        from slack_sdk import WebClient
        client = WebClient(token=self.slack_token)
        
        message = f"""
*News Analysis Alert* 📰
*Title:* {analysis['news']['title']}
*Analysis:* 
{analysis['analysis']}
*Source:* {analysis['news'].get('link', 'N/A')}
*Time:* {analysis['timestamp']}

💾 *Analysis saved to:* `{json_file if json_file else 'N/A'}`
"""
        
        try:
            client.chat_postMessage(
                channel=self.slack_channel,
                text=message,
                parse='mrkdwn'
            )
        except Exception as e:
            print(f"⚠️ Failed to send message to Slack: {e}")
    
    def run_pipeline(self):
        # Create dated output directory
        date_str = time.strftime("%Y%m%d")
        base_output_dir = Path("outputs")
        output_dir = base_output_dir / date_str
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Fetch news
        print("🔍 Fetching latest news...")
        news_items = self.fetch_news()
        
        analyses = []
        for news in news_items:
            print(f"\n📊 Analyzing: {news['title']}")
            
            # Analyze
            analysis = self.analyze_news(news)
            analyses.append(analysis)
            
            # Save individual JSON
            json_file = self.save_analysis_json(analysis, output_dir)
            print(f"💾 Saved analysis to {json_file}")
            
            # Send to Slack with JSON attachment
            print("📤 Sending to Slack...")
            self.send_to_slack(analysis, json_file)
            
            # Rate limiting
            time.sleep(2)
        
        # Save combined analysis
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        combined_file = output_dir / f"market_analysis_{timestamp}_combined.json"
        
        with open(combined_file, "w", encoding='utf-8') as f:
            json.dump({
                "analyses": analyses,
                "metadata": {
                    "analysis_date": date_str,
                    "total_articles": len(analyses),
                    "generated_at": timestamp
                }
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Analysis complete!")
        print(f"📁 Individual analyses saved to: {output_dir}")
        print(f"📊 Combined analysis saved to: {combined_file}")

if __name__ == "__main__":
    analyst = MarketAnalyst()
    analyst.run_pipeline()
