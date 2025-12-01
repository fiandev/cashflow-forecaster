# LLM Service

The LLM (Large Language Model) service provides an abstraction layer over different LLM providers, currently supporting:
- Google Gemini
- OpenRouter

## Setup

### Installation

The service requires additional dependencies that are included in the `requirements.txt`:
- `google-generativeai` for Gemini support
- `openai` for OpenRouter support (uses OpenAI-compatible API)

### Environment Variables

Add the following variables to your `.env` file:

```bash
# For Google Gemini
GEMINI_API_KEY=your-gemini-api-key-here

# For OpenRouter
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

## Usage

### Basic Usage

```python
from services.llm_service import LLMService

# Initialize with Gemini
llm_service = LLMService.create(
    provider="gemini",
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-1.0-pro",
    temperature=0.7
)

# Generate text
response = llm_service.generate_text("Your prompt here")
print(response)
```

### Using Convenience Functions

```python
from services.llm_service import create_gemini_service, create_openrouter_service

# Create Gemini service
gemini_service = create_gemini_service(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-1.0-pro"
)

# Create OpenRouter service
openrouter_service = create_openrouter_service(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-3.5-turbo"
)
```

### Streaming Responses

```python
# Streaming with OpenRouter
for chunk in openrouter_service.generate_text_streaming("Write a story..."):
    print(chunk, end="", flush=True)
```

## Configuration

The service accepts the following configuration parameters:

- `provider`: "gemini" or "openrouter"
- `api_key`: Your API key for the selected provider
- `model`: The model to use (defaults vary by provider)
- `temperature`: Controls randomness (0.0 to 1.0, default 0.7)
- `max_tokens`: Maximum tokens in the response (default 1000)

## Architecture

The service follows a provider pattern:

- `LLMProvider`: Abstract base class defining the interface
- `GeminiProvider`: Google Gemini implementation
- `OpenRouterProvider`: OpenRouter implementation (uses OpenAI-compatible API)
- `LLMService`: Main service class that manages providers