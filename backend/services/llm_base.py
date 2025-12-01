"""
Base classes and interfaces for LLM service providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text based on the provided prompt"""
        pass
    
    @abstractmethod
    def generate_text_streaming(self, prompt: str, **kwargs) -> Any:
        """Generate text with streaming support"""
        pass

    @abstractmethod
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        pass


class LLMConfig:
    """Configuration for LLM service"""
    def __init__(self, provider: str, api_key: str, model: str = "default", temperature: float = 0.7, max_tokens: int = 1000, **kwargs):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs