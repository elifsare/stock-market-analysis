from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM

class LLMFactory:
    @staticmethod
    def get_llm(provider: str = "ollama", model: str = "mistral") -> BaseLLM:
        if provider == "ollama":
            return Ollama(model=model)
        elif provider == "openai":
            return ChatOpenAI(model_name="gpt-3.5-turbo")
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
