from openai import OpenAI
import os
import json

class AIService:
    def __init__(self):
        self.api_key = os.getenv("KOLOSAL_API_KEY")
        self.base_url = os.getenv("KOLOSAL_BASE_URL", "https://api.kolosal.ai/v1")
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
            print("Warning: KOLOSAL_API_KEY not set. AI features will be disabled.")

    def get_market_sentiment(self, sector="general"):
        """
        Simulates fetching real-time market sentiment data.
        In a real app, this would call an external financial news API.
        """
        print(f"DEBUG: Executing tool 'get_market_sentiment' for sector: {sector}")
        
        # Simulated dynamic response based on sector
        if "tech" in sector.lower():
            return json.dumps({
                "sector": "Technology",
                "sentiment": "Volatile",
                "trend": "Correction phase",
                "interest_rates": "High impact",
                "advice": "Conservative cash buffers recommended due to market fluctuations."
            })
        elif "retail" in sector.lower():
             return json.dumps({
                "sector": "Retail",
                "sentiment": "Positive",
                "trend": "Seasonal Uptrend",
                "consumer_confidence": "Rising",
                "advice": "Good time to invest in inventory."
            })
        else:
            return json.dumps({
                "sector": "General Market",
                "sentiment": "Neutral",
                "trend": "Stable",
                "inflation": "Moderating",
                "advice": "Standard cashflow management applies."
            })

    def generate_forecast_insight(self, forecast_data):
        """
        Generates a textual insight/analysis for a cashflow forecast, potentially using tool calls.
        """
        if not self.client:
            return "AI analysis unavailable (API Key missing)."

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_market_sentiment",
                    "description": "Get current market sentiment and economic trends for a specific business sector to inform financial advice.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sector": {
                                "type": "string",
                                "description": "The business sector, e.g., 'technology', 'retail', 'manufacturing', or 'general'.",
                            }
                        },
                        "required": ["sector"],
                    },
                },
            }
        ]

        try:
            # Construct a prompt based on the forecast data
            prompt = f"""
            Analyze the following cashflow forecast data and provide a strategic insight.
            
            Forecast Details:
            - Period: {forecast_data.get('period_start')} to {forecast_data.get('period_end')}
            - Granularity: {forecast_data.get('granularity')}
            - Predicted Cashflow: {forecast_data.get('predicted_value')}
            - Lower Bound: {forecast_data.get('lower_bound')}
            - Upper Bound: {forecast_data.get('upper_bound')}
            
            If you need context on the broader economic environment to give better advice, use the available tool to check market sentiment.
            
            Please provide:
            1. A summary of the outlook.
            2. Key risks or opportunities.
            3. One actionable recommendation.
            """

            messages = [
                {"role": "system", "content": "You are a financial analyst AI assistant. You have access to real-time market data tools. Use them if relevant to provide context-aware advice."},
                {"role": "user", "content": prompt}
            ]

            # First API Call: Ask the model
            response = self.client.chat.completions.create(
                model="Llama 4 Maverick",
                messages=messages,
                tools=tools,
                tool_choice="auto", # Let the model decide whether to call a tool
                max_tokens=500
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Check if the model wants to call a tool
            if tool_calls:
                print("DEBUG: AI initiated tool call.")
                
                # Append the model's request to the conversation history
                messages.append(response_message)

                # Process each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "get_market_sentiment":
                        function_response = self.get_market_sentiment(
                            sector=function_args.get("sector", "general")
                        )
                        
                        # Append the tool result to the conversation history
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })

                # Second API Call: Get the final answer with tool data
                second_response = self.client.chat.completions.create(
                    model="Llama 4 Maverick",
                    messages=messages,
                    tools=tools, # Keep tools available in context
                    max_tokens=500
                )
                return second_response.choices[0].message.content.strip()
            
            else:
                # No tool call needed, return direct response
                return response_message.content.strip()

        except Exception as e:
            print(f"Error generating AI insight: {e}")
            return f"AI analysis failed: {str(e)}"

    def analyze_transaction_anomaly(self, transaction_data):
         """
         Analyzes a transaction to determine if it's anomalous and why.
         Returns a dictionary with keys: is_anomalous, tag, reason.
         """
         if not self.client:
             return {"is_anomalous": False, "tag": "AI Unavailable", "reason": "API Key missing"}
         
         try:
             prompt = f"""
             Analyze this transaction for potential anomalies or fraud:
             - Description: {transaction_data.get('description')}
             - Amount: {transaction_data.get('amount')}
             - Date: {transaction_data.get('date')}
             - Category: {transaction_data.get('category')}
             - Direction: {transaction_data.get('direction')}
             
             Determine if this is unusual.
             
             You must respond in valid JSON format only, with no extra text.
             JSON Schema:
             {{
                "is_anomalous": boolean,
                "tag": "string (Short classification, e.g. 'High Value', 'Unusual Category', 'Normal')",
                "reason": "string (Brief explanation)"
             }}
             """
             
             response = self.client.chat.completions.create(
                model="Llama 4 Maverick",
                messages=[
                    {"role": "system", "content": "You are a fraud detection AI. Respond only in JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
             
             content = response.choices[0].message.content.strip()
             
             # Clean up markdown code blocks if present
             if content.startswith("```json"):
                 content = content[7:]
             if content.endswith("```"):
                 content = content[:-3]
                 
             return json.loads(content.strip())
             
         except Exception as e:
             print(f"AI Anomaly Analysis Error: {e}")
             return {"is_anomalous": False, "tag": "Analysis Failed", "reason": str(e)}
