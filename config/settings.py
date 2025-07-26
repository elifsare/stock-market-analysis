# LLM Configuration
LLM_PROVIDER = "ollama"  # or "openai"
LLM_MODEL = "mistral"    # or "gpt-3.5-turbo" for OpenAI

# API Configuration
NEWS_SOURCES = [
    "bloomberg.com",
    "reuters.com",
    "ft.com"
]

# Output Configuration
OUTPUT_DIR = "outputs"
MAX_NEWS_ITEMS = 5
RATE_LIMIT_DELAY = 2  # seconds between API calls
