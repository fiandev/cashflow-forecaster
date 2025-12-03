from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

client = OpenAI(
    api_key=os.getenv("KOLOSAL_API_KEY"),
    base_url=os.getenv("KOLOSAL_BASE_URL")
)

# Define a simple tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

print("Testing tool call support for model: Llama 4 Maverick")

try:
    response = client.chat.completions.create(
        model="Llama 4 Maverick",
        messages=[{"role": "user", "content": "What is the weather like in San Francisco?"}],
        tools=tools,
        tool_choice="auto",
    )

    print("\nResponse received:")
    print(response)
    
    if response.choices[0].message.tool_calls:
        print("\n✅ Tool calls appear to be SUPPORTED!")
        print(response.choices[0].message.tool_calls)
    else:
        print("\n⚠️  No tool call generated (might be supported but model chose not to use it, or ignored parameters).")

except Exception as e:
    print(f"\n❌ Error (Likely NOT supported): {e}")
