import json
import time
from pathlib import Path
from src.agents.market_analysis_agent import MarketAnalysisAgent

def save_analysis(analyses: list, output_dir: str = "outputs"):
    """Save analyses to a JSON file with timestamp"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"market_analysis_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump({"analyses": analyses}, f, indent=2)
    
    return output_file

def main():
    # Initialize the agent with Ollama/Mistral
    agent = MarketAnalysisAgent()
    
    # Run market analysis
    analyses = agent.analyze_market_news()
    
    # Save results
    output_file = save_analysis(analyses)
    print(f"\n✅ Analysis complete! Results saved to {output_file}")

if __name__ == "__main__":
    main()
