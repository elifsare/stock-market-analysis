# 📈 AI-Powered Stock Market Analysis Pipeline

An intelligent system that combines real-time financial news analysis with AI to generate actionable trading signals. Using Bloomberg news, local LLM processing (Mistral), and Slack integration, it provides instant market insights with specific entry/exit points.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.0.329-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

- 📰 Real-time financial news fetching from Bloomberg
- 🤖 AI-powered analysis using local LLM (Mistral)
- 💹 Specific trading signals with entry/exit points
- ⚠️ Automated risk management guidance
- 📊 Structured JSON output with historical storage
- 💬 Real-time Slack notifications
- 📁 Organized daily analysis archives
## 📋 Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) with Mistral model installed
- [SerpAPI](https://serpapi.com/) key for news fetching
- Slack workspace with a bot

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/elifsare/stock-market-analysis.git
cd stock-market-analysis
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

## 🚀 Usage

1. Create a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac
```

2. Run the analysis pipeline:
```bash
python main.py
```

The system will:
1. 📰 Fetch latest Bloomberg financial news
2. 🤖 Analyze each article using Mistral AI
3. 📊 Generate detailed trading signals
4. 💬 Send analyses to Slack
5. 💾 Save structured outputs to dated directories

## 📈 Analysis Output

The system generates three types of outputs:

1. **Slack Notifications**:
```
📰 News Analysis Alert
Title: S&P 500 Hits New Highs
Analysis:
MARKET DIRECTION: BULLISH (>5% upside)
PRIMARY TRADE:
- Tickers: SPY, QQQ
- Action: BUY
- Entry: Current levels
- Target: +5% from entry
- Stop: -3% from entry
```

2. **Individual JSON Files**:
```json
{
  "news": {
    "title": "S&P 500 Hits New Highs",
    "link": "https://bloomberg.com/...",
    "snippet": "..."
  },
  "analysis": {
    "market_direction": "BULLISH",
    "primary_trade": {
      "tickers": ["SPY", "QQQ"],
      "action": "BUY",
      "targets": {...}
    }
  },
  "timestamp": "2025-07-26 17:23:49"
}
```

3. **Daily Combined Analysis**:
```json
{
  "analyses": [...],
  "metadata": {
    "analysis_date": "20250726",
    "total_articles": 5,
    "generated_at": "20250726_172349"
  }
}
```

## ⚙️ Configuration

Create a `.env` file with:
```bash
SERPAPI_KEY=your_serp_api_key
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL=#your-channel
```

## 📂 Project Structure

```
stock-market-analysis/
├── main.py              # Main pipeline
├── tools/
│   ├── __init__.py
│   └── news_api.py     # News fetching tool
├── outputs/            # Analysis storage
│   └── YYYYMMDD/      # Daily directories
├── requirements.txt    # Dependencies
└── .env               # Configuration
```

## 🤝 Contributing

Pull requests are welcome! For major changes:
1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)

## ⚠️ Disclaimer

This tool is for educational purposes only. The trading signals and analyses generated are not financial advice. Always:
- Conduct your own research
- Verify signals independently
- Consult with licensed financial advisors
- Never trade with money you can't afford to lose

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=elifsare/stock-market-analysis&type=Date)](https://star-history.com/#elifsare/stock-market-analysis&Date)

## 📬 Contact

- Created by [@elifsare](https://github.com/elifsare)
- LinkedIn: [Elif Şile](https://www.linkedin.com/in/elif-%C5%9File-8140311ab/)
