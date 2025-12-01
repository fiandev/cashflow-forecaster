"""
Example usage of the LLM service
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from services.llm_service import LLMService, create_gemini_service, create_openrouter_service

def example_usage():
    # Example 1: Using the main LLMService class
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        print("Using Gemini...")
        llm_service = LLMService.create(
            provider="gemini",
            api_key=gemini_api_key,
            model="gemini-1.0-pro",
            temperature=0.7
        )
        
        response = llm_service.generate_text("Explain how cash flow forecasting helps businesses in 2 sentences.")
        print(f"Response: {response}")
    
    # Example 2: Using the convenience function
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_api_key:
        print("\nUsing OpenRouter...")
        llm_service = create_openrouter_service(
            api_key=openrouter_api_key,
            model="openai/gpt-3.5-turbo",
            temperature=0.7
        )
        
        response = llm_service.generate_text("What are the key components of a financial forecast?")
        print(f"Response: {response}")
        
        # Example of streaming
        print("\nStreaming response from OpenRouter:")
        for chunk in llm_service.generate_text_streaming("Write a short poem about financial planning."):
            print(chunk, end="", flush=True)
        print()  # New line after streaming


if __name__ == "__main__":
    example_usage()