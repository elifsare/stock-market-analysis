# AI-Powered Stock Market Analysis Pipeline

This project automatically analyzes financial news from Bloomberg and other sources to generate actionable trading signals using AI. It combines web scraping, natural language processing, and local AI models to provide real-time market insights.

## Features

- Real-time financial news fetching from Bloomberg
- AI-powered analysis using local LLM (Mistral)
- Specific trading signals with entry/exit points
- Automated risk management guidance
- JSON output for further processing
- 
## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) with Mistral model installed
- [SerpAPI](https://serpapi.com/) key for news fetching

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-market-ai-analysis.git
cd stock-market-ai-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install Ollama and download Mistral model:
```bash
# Install Ollama from https://ollama.ai/
ollama pull mistral
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your SerpAPI key
```

## Usage

Run the main script:
```bash
python news_stockPrice_enhanced.py
```

The script will:
1. Fetch latest financial news from Bloomberg
2. Analyze each article using AI
3. Generate trading signals with specific targets
4. Save results to JSON file

## Output Format

```json
{
  "Company/Sector": "US Markets (SPY, QQQ)",
  "Stock Impact": "UP/DOWN/NEUTRAL",
  "Trading Signal": "BUY/SELL with targets",
  "Reasoning": "Detailed analysis..."
}
```

## Configuration

- `SERPAPI_KEY`: Your SerpAPI key (required)
- News sources: Modify `bloomberg_queries` in the code
- Analysis parameters: Adjust prompt in `call_ollama_llm()`


## License

MIT

## Disclaimer

This tool is for educational purposes only. Always conduct your own research and consult with financial advisors before making investment decisions.
