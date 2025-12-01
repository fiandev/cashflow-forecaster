"""
Gemini LLM Provider implementation
"""
import google.generativeai as genai
from typing import Dict, Any, Generator
from .llm_base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini API provider implementation"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.0-pro", **kwargs):
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # Extract generation config parameters
        self.generation_config = {
            "temperature": kwargs.get("temperature", 0.7),
            "max_output_tokens": kwargs.get("max_tokens", 2048),
            "top_p": kwargs.get("top_p", 0.9),
            "top_k": kwargs.get("top_k", 40),
        }
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Gemini API"""
        generation_config = self.generation_config.copy()
        
        # Override with any specific kwargs for this call
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            generation_config["max_output_tokens"] = kwargs["max_tokens"]
            
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def generate_text_streaming(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate text with streaming support using Gemini API"""
        generation_config = self.generation_config.copy()
        
        # Override with any specific kwargs for this call
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            generation_config["max_output_tokens"] = kwargs["max_tokens"]
            
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config,
            stream=True
        )
        
        for chunk in response:
            yield chunk.text or ""
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific Gemini model"""
        # For now, return basic info; would need to call model API for detailed info
        return {
            "name": model_name,
            "provider": "gemini",
            "capabilities": ["text-generation", "code-generation"],
            "max_input_tokens": 30720,  # Typical for Gemini models
            "max_output_tokens": 2048,
        }