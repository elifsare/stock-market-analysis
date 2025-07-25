import requests
import subprocess
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
SERPAPI_KEY = os.getenv('SERPAPI_KEY')

if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY not found in environment variables. Please check your .env file.")

def fetch_financial_news(api_key):
    # Specific queries for Bloomberg
    bloomberg_queries = [
        "site:bloomberg.com stocks",
        "site:bloomberg.com markets",
        "site:bloomberg.com earnings"
    ]
    
    all_news = []
    
    # First try to get Bloomberg news
    for query in bloomberg_queries:
        params = {
            "engine": "google",
            "q": query,
            "tbm": "nws",
            "num": 5,  # Request more to ensure we get some results
            "api_key": api_key,
            "time": "d"  # Last 24 hours to get fresh news
        }
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            if 'news_results' in data:
                # Filter to ensure we only get Bloomberg results
                bloomberg_news = [
                    news for news in data['news_results']
                    if 'bloomberg.com' in news.get('link', '').lower()
                ]
                all_news.extend(bloomberg_news)
                print(f"Found {len(bloomberg_news)} Bloomberg articles for query: {query}")
        except Exception as e:
            print(f"Error fetching news: {e}")
    
    # If we don't have enough Bloomberg news, add general financial news
    if len(all_news) < 3:
        general_query = "financial news stocks market analysis"
        params = {
            "engine": "google",
            "q": general_query,
            "tbm": "nws",
            "num": 5,
            "api_key": api_key,
            "time": "d"
        }
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            if 'news_results' in data:
                all_news.extend(data['news_results'])
        except Exception as e:
            print(f"Error fetching general news: {e}")
    
    # Remove duplicates based on title
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        title = news.get('title', '')
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_news.append(news)
    
    return unique_news[:5]  # Return top 5 most relevant unique news items

def call_ollama_llm(news_snippet):
    prompt = f"""You are an experienced financial analyst. Analyze this news and provide actionable insights using these rules:

1. Provide trading signals in these cases:
   a) News mentions specific companies (Use stock symbols: AAPL, MSFT, etc.)
   b) News affects specific sectors (Tech, Finance, Healthcare, etc.)
   c) Major market events (Fed decisions, market trends, bubbles)
   d) Economic indicators that impact stocks
   e) Regulatory changes affecting industries

2. Trading Signal Requirements:
   - ALWAYS include specific tradeable symbols (stocks or ETFs)
   - For company news: Use the company's stock symbol (e.g., AAPL, MSFT)
   - For sector news: List relevant ETFs (e.g., XLF for banking, XLK for tech)
   - For market news: Use index ETFs (e.g., SPY for S&P 500, QQQ for Nasdaq)
   - For regional news: Use country ETFs (e.g., EWJ for Japan, FXI for China)
   
   Signal types:
   - UP + BUY: Clear positive catalyst with >5% upside potential
   - DOWN + SELL: Clear negative catalyst with >5% downside risk
   - NEUTRAL + HOLD: Limited price movement expected (±5%)
   - NOT APPLICABLE: Only if absolutely no tradeable angle exists

3. Format your response EXACTLY as follows:

REQUIRED FORMAT (You must follow this exactly):

Company/Sector: [MUST include specific symbols. Examples:
  - Individual stock: "Apple Inc. (AAPL)"
  - Sector: "Banking Sector (XLF, JPM, BAC)"
  - Market: "US Markets (SPY, QQQ)"
  - Region: "Japan (EWJ, DXJ)"]

Key Event: [One clear sentence about what happened]

Stock Impact: [MUST be one of: UP (>5% expected), DOWN (>5% expected), NEUTRAL (±5% range)]

Trading Signal: [MUST include specific symbols. Examples:
  - "BUY AAPL, MSFT Target: $200, Stop: $180"
  - "SELL SPY, BUY SH Target: SPY 420, Stop: 460"
  - "HOLD XLF, Add at 32, Exit at 28"]

Reasoning: [MUST include:
  1. Primary trade setup with entry/exit
  2. Expected timeline (days/weeks/months)
  3. Key metrics/catalysts to watch
  4. Risk factors and stop loss levels]

For news WITHOUT direct stock implications:
Company Name: No direct stock market implications
Key Event: [One clear sentence about what happened]
Stock Impact: NOT APPLICABLE
Trading Signal: NO SIGNAL
Reasoning: [Explain why this news, while important, doesn't warrant specific stock trading actions]

Examples of proper analysis:

1. Company-specific news:
Company Name: Apple Inc. (AAPL)
Key Event: Apple announces new AI chip development
Stock Impact: UP
Trading Signal: BUY AAPL, BUY SMH
Reasoning: Direct positive catalyst for AAPL (primary trade, 15% upside target) and semiconductor ETF SMH (secondary trade, 8% upside target). AI chip development typically adds $100-150B to market cap over 6-12 months based on previous announcements.

2. Sector news:
Company Name: US Banking Sector
Key Event: Fed signals faster rate cuts than expected
Stock Impact: UP
Trading Signal: BUY XLF, BUY JPM, BAC
Reasoning: Trade setup: Primary - XLF ETF (10% upside target), Secondary - JPM and BAC (12-15% upside each). Banks historically outperform by 15% in 6 months after Fed pivot. JPM and BAC have highest rate sensitivity among large banks.

3. Market warning news:
Company Name: US Market Indices
Key Event: Technical indicators suggest market bubble risk
Stock Impact: DOWN
Trading Signal: SELL SPY, BUY SH
Reasoning: Trade setup: 1) Reduce SPY exposure (12% downside risk), 2) Consider SH (ProShares Short S&P500 ETF) as hedge. Similar conditions in 2024 led to 15% correction. Set stop loss at 5% above entry for SH position.

4. Non-market news:
Company Name: No direct stock market implications
Key Event: Local infrastructure announcement
Stock Impact: NOT APPLICABLE
Trading Signal: NO SIGNAL
Reasoning: No clear tradeable securities or ETFs impacted by this news. Local project without material impact on any public companies.

News Snippet: {news_snippet}
"""
    process = subprocess.Popen(
        ['ollama', 'run', 'mistral'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    stdout, stderr = process.communicate(input=prompt)

    if stderr:
        print(f"Error: {stderr}")
    return stdout

def parse_llm_response(response_text):
    lines = response_text.split('\n')
    extracted = {}
    current_key = None
    reasoning_lines = []
    
    for line in lines:
        if line.strip():
            if line.startswith("Company Name:"):
                extracted['Company Name'] = line.split(":",1)[1].strip()
            elif line.startswith("Key Event:"):
                extracted['Key Event'] = line.split(":",1)[1].strip()
            elif line.startswith("Stock Impact:"):
                extracted['Stock Impact'] = line.split(":",1)[1].strip()
            elif line.startswith("Trading Signal:"):
                extracted['Trading Signal'] = line.split(":",1)[1].strip()
            elif line.startswith("Reasoning:"):
                current_key = "Reasoning"
                reasoning_text = line.split(":",1)[1].strip()
                if reasoning_text:
                    reasoning_lines.append(reasoning_text)
            elif current_key == "Reasoning":
                reasoning_lines.append(line.strip())
    
    if reasoning_lines:
        extracted['Reasoning'] = ' '.join(reasoning_lines)
    
    return extracted

def pipeline():
    news_list = fetch_financial_news(SERPAPI_KEY)
    all_analyses = []
    
    for news in news_list:
        title = news.get('title')
        snippet = news.get('snippet')
        link = news.get('link')

        print(f"\n📰 Analyzing: {title}")
        
        # Enhance the news context for better analysis
        enhanced_snippet = f"""
Title: {title}
Full Context: {snippet}
Source: {link.split('/')[2] if link else 'Unknown'}
        """
        
        llm_output = call_ollama_llm(enhanced_snippet)
        parsed_data = parse_llm_response(llm_output)
        
        # Validate the analysis
        if not parsed_data or len(parsed_data) < 4:  # Must have all 4 key fields
            print("⚠️ Warning: Analysis incomplete, retrying...")
            time.sleep(1)
            llm_output = call_ollama_llm(enhanced_snippet)  # Retry once
            parsed_data = parse_llm_response(llm_output)
        
        # Add source information to the analysis
        analysis = {
            "news": {
                "title": title,
                "link": link,
                "snippet": snippet
            },
            "analysis": parsed_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        all_analyses.append(analysis)
        
        # Print real-time analysis
        print("\n📊 Analysis Result:")
        print(json.dumps(analysis, indent=2))
        print("\n" + "="*80)
        
        time.sleep(2)  # Rate limiting for Ollama
    
    # Save all analyses to a JSON file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"market_analysis_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump({"analyses": all_analyses}, f, indent=2)
    
    print(f"\n✅ Analysis complete! Results saved to {output_file}")

if __name__ == "__main__":
    pipeline()
