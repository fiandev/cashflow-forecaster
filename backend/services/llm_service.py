"""
Main LLM Service that manages different LLM providers
"""
from typing import Dict, Any, Optional
from .llm_base import LLMConfig
from .gemini_provider import GeminiProvider
from .openrouter_provider import OpenRouterProvider


class LLMService:
    """Main service class to manage LLM operations"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the appropriate provider based on config"""
        if self.config.provider.lower() == "gemini":
            return GeminiProvider(
                api_key=self.config.api_key,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                **self.config.kwargs
            )
        elif self.config.provider.lower() == "openrouter":
            return OpenRouterProvider(
                api_key=self.config.api_key,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                **self.config.kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the configured provider"""
        return self.provider.generate_text(prompt, **kwargs)
    
    def generate_text_streaming(self, prompt: str, **kwargs):
        """Generate text with streaming support"""
        return self.provider.generate_text_streaming(prompt, **kwargs)
    
    def get_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get information about the current model"""
        model = model_name or self.config.model
        return self.provider.get_model_info(model)
    
    @staticmethod
    def create(provider: str, api_key: str, model: str = "default", **kwargs) -> "LLMService":
        """Factory method to create an LLMService instance"""
        config = LLMConfig(
            provider=provider,
            api_key=api_key,
            model=model,
            **kwargs
        )
        return LLMService(config)


# Convenience functions for common use cases
def create_gemini_service(api_key: str, model: str = "gemini-1.0-pro", **kwargs) -> LLMService:
    """Create a Gemini-based LLM service"""
    return LLMService.create("gemini", api_key, model, **kwargs)


def create_openrouter_service(api_key: str, model: str = "openai/gpt-3.5-turbo", **kwargs) -> LLMService:
    """Create an OpenRouter-based LLM service"""
    return LLMService.create("openrouter", api_key, model, **kwargs)