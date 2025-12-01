"""
OpenRouter LLM Provider implementation
"""
from openai import OpenAI
from typing import Dict, Any, Generator
from .llm_base import LLMProvider


class OpenRouterProvider(LLMProvider):
    """OpenRouter API provider implementation"""
    
    def __init__(self, api_key: str, model: str = "openai/gpt-3.5-turbo", **kwargs):
        self.api_key = api_key
        self.model_name = model
        
        # Initialize OpenAI client with OpenRouter base URL
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Extract generation config parameters
        self.temperature = kwargs.get("temperature", 0.7)
        self.max_tokens = kwargs.get("max_tokens", 1000)
        self.top_p = kwargs.get("top_p", 1.0)
        self.frequency_penalty = kwargs.get("frequency_penalty", 0.0)
        self.presence_penalty = kwargs.get("presence_penalty", 0.0)
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenRouter API"""
        # Prepare the messages for chat completion
        messages = [{"role": "user", "content": prompt}]
        
        # Prepare parameters with potential overrides from kwargs
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        top_p = kwargs.get("top_p", self.top_p)
        frequency_penalty = kwargs.get("frequency_penalty", self.frequency_penalty)
        presence_penalty = kwargs.get("presence_penalty", self.presence_penalty)
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        
        return response.choices[0].message.content or ""
    
    def generate_text_streaming(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate text with streaming support using OpenRouter API"""
        # Prepare the messages for chat completion
        messages = [{"role": "user", "content": prompt}]
        
        # Prepare parameters with potential overrides from kwargs
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        top_p = kwargs.get("top_p", self.top_p)
        frequency_penalty = kwargs.get("frequency_penalty", self.frequency_penalty)
        presence_penalty = kwargs.get("presence_penalty", self.presence_penalty)
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=True
        )
        
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific OpenRouter model"""
        # For now, return basic info; would need to call model API for detailed info
        return {
            "name": model_name,
            "provider": "openrouter",
            "capabilities": ["text-generation", "code-generation", "chat"],
            "max_input_tokens": 4096,  # Typical for GPT models, but varies by model
        }