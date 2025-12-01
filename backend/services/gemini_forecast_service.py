import os
import pandas as pd
import io
from flask import current_app
from models import Business, Transaction, Forecast
from datetime import datetime, date
from decimal import Decimal
import json
import re
from services.llm_service import create_gemini_service


class GeminiForecastService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        self.service = create_gemini_service(api_key, model='gemini-1.0-pro')
    
    def prepare_business_data(self, business_id, period_start, period_end):
        """
        Prepare business data for forecasting including transactions and previous forecasts
        """
        business = Business.query.get(business_id)
        if not business:
            raise ValueError(f"Business with id {business_id} not found")
        
        # Get historical transactions for the business
        transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date <= period_start
        ).order_by(Transaction.date).all()
        
        # Get previous forecasts for the business
        previous_forecasts = Forecast.query.filter(
            Forecast.business_id == business_id,
            Forecast.period_end <= period_start
        ).order_by(Forecast.period_end).all()
        
        # Convert transactions to CSV format
        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                'date': transaction.date.isoformat() if isinstance(transaction.date, date) else str(transaction.date),
                'amount': float(transaction.amount) if transaction.amount else 0.0,
                'description': transaction.description or '',
                'category': transaction.category.name if transaction.category else '',
                'direction': transaction.direction or ''
            })
        
        transactions_df = pd.DataFrame(transaction_data)
        transactions_csv = transactions_df.to_csv(index=False)
        
        # Convert previous forecasts to CSV format
        forecast_data = []
        for forecast in previous_forecasts:
            forecast_data.append({
                'period_start': forecast.period_start.isoformat() if isinstance(forecast.period_start, date) else str(forecast.period_start),
                'period_end': forecast.period_end.isoformat() if isinstance(forecast.period_end, date) else str(forecast.period_end),
                'predicted_value': float(forecast.predicted_value) if forecast.predicted_value else 0.0,
                'lower_bound': float(forecast.lower_bound) if forecast.lower_bound else 0.0,
                'upper_bound': float(forecast.upper_bound) if forecast.upper_bound else 0.0,
                'granularity': forecast.granularity or ''
            })
        
        forecasts_df = pd.DataFrame(forecast_data)
        forecasts_csv = forecasts_df.to_csv(index=False) if not forecasts_df.empty else ""
        
        return {
            'business': {
                'name': business.name,
                'country': business.country,
                'currency': business.currency,
                'timezone': business.timezone,
                'settings': json.dumps(business.settings) if business.settings else '{}'
            },
            'transactions_csv': transactions_csv,
            'forecasts_csv': forecasts_csv,
            'period_start': period_start.isoformat() if isinstance(period_start, date) else str(period_start),
            'period_end': period_end.isoformat() if isinstance(period_end, date) else str(period_end)
        }

    def generate_forecast_with_gemini(self, business_id, period_start, period_end, granularity):
        """
        Generate a cash flow forecast using Gemini LLM
        """
        # Prepare the data for the LLM
        data = self.prepare_business_data(business_id, period_start, period_end)

        # Read the prompt template
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'cashflow_forecasting_prompt.txt')
        with open(prompt_path, 'r') as f:
            base_prompt = f.read()

        # Create the full prompt with actual data
        full_prompt = f"""
{base_prompt}

BUSINESS INFORMATION:
{json.dumps(data['business'], indent=2)}

HISTORICAL TRANSACTIONS (CSV format):
{data['transactions_csv']}

PREVIOUS FORECASTS (CSV format, if any):
{data['forecasts_csv']}

FORECAST PERIOD:
Start: {data['period_start']}
End: {data['period_end']}
Granularity: {granularity}

Please provide your forecast in CSV format as specified in the output requirements.
"""

        try:
            # Generate content using the LLM service
            response_text = self.service.generate_text(full_prompt).strip()

            # Try to parse as CSV first
            forecast_result = self._parse_forecast_response_csv(response_text)

            if forecast_result is not None:
                return forecast_result
            else:
                # If CSV fails, try JSON format
                current_app.logger.warning("CSV parsing failed, attempting JSON fallback")
                return self._parse_forecast_response_json(response_text)

        except Exception as e:
            # If both CSV and JSON parsing fail, return default values
            current_app.logger.error(f"Error generating forecast with Gemini: {str(e)}")
            return {
                'predicted_value': Decimal('0.00'),
                'lower_bound': Decimal('0.00'),
                'upper_bound': Decimal('0.00'),
                'confidence_score': 0,
                'explanation': 'Error generating forecast',
                'risk_factors': 'Error in forecasting process'
            }

    def _parse_forecast_response_csv(self, response_text):
        """
        Parse the LLM response as CSV format
        """
        try:
            # Extract CSV content from the response (if it contains markdown formatting)
            csv_content = self._extract_csv_content(response_text)

            if not csv_content:
                return None

            # Parse the CSV response
            csv_io = io.StringIO(csv_content)
            df = pd.read_csv(csv_io)

            # Extract forecast values from the first row
            row = df.iloc[0]  # Get the first row
            forecast_result = {
                'predicted_value': Decimal(str(row['predicted_value'])),
                'lower_bound': Decimal(str(row['lower_bound'])),
                'upper_bound': Decimal(str(row['upper_bound'])),
                'confidence_score': int(row['confidence_score']) if 'confidence_score' in row else 0,
                'explanation': str(row['explanation']) if 'explanation' in row else '',
                'risk_factors': str(row['risk_factors']) if 'risk_factors' in row else ''
            }

            return forecast_result
        except Exception as e:
            current_app.logger.error(f"Error parsing CSV response: {str(e)}")
            return None

    def _parse_forecast_response_json(self, response_text):
        """
        Parse the LLM response as JSON format as fallback
        """
        try:
            # Try to find JSON content in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                json_data = json.loads(json_str)

                forecast_result = {
                    'predicted_value': Decimal(str(json_data.get('predicted_value', 0.0))),
                    'lower_bound': Decimal(str(json_data.get('lower_bound', 0.0))),
                    'upper_bound': Decimal(str(json_data.get('upper_bound', 0.0))),
                    'confidence_score': int(json_data.get('confidence_score', 0)),
                    'explanation': str(json_data.get('explanation', '')),
                    'risk_factors': str(json_data.get('risk_factors', ''))
                }

                return forecast_result
            else:
                # If no JSON found, try to extract individual values
                return self._extract_values_from_text(response_text)
        except Exception as e:
            current_app.logger.error(f"Error parsing JSON response: {str(e)}")
            return self._extract_values_from_text(response_text)

    def _extract_csv_content(self, response_text):
        """
        Extract CSV content from the response, handling markdown formatting
        """
        # Check for CSV markdown block
        csv_pattern = r'```csv\s*\n(.*?)\n```'
        csv_match = re.search(csv_pattern, response_text, re.DOTALL)
        if csv_match:
            return csv_match.group(1).strip()

        # Check for generic code block
        code_pattern = r'```\s*\n(.*?)\n```'
        code_match = re.search(code_pattern, response_text, re.DOTALL)
        if code_match:
            content = code_match.group(1).strip()
            # Check if it looks like CSV (has commas and headers)
            if ',' in content and '\n' in content:
                first_line = content.split('\n')[0]
                if all(col in first_line for col in ['predicted_value', 'lower_bound', 'upper_bound']):
                    return content

        # If no code blocks, return the full response (might already be CSV)
        return response_text.strip()

    def _extract_values_from_text(self, response_text):
        """
        Extract forecast values from plain text response as final fallback
        """
        try:
            # Look for common patterns in the response
            import re

            # Try to find values using regex
            predicted_pattern = r'predicted[ _]?value[ :]*([+-]?\d*\.?\d+)'
            lower_pattern = r'lower[ _]?bound[ :]*([+-]?\d*\.?\d+)'
            upper_pattern = r'upper[ _]?bound[ :]*([+-]?\d*\.?\d+)'

            predicted_match = re.search(predicted_pattern, response_text, re.IGNORECASE)
            lower_match = re.search(lower_pattern, response_text, re.IGNORECASE)
            upper_match = re.search(upper_pattern, response_text, re.IGNORECASE)

            predicted_value = Decimal(predicted_match.group(1)) if predicted_match else Decimal('0.00')
            lower_bound = Decimal(lower_match.group(1)) if lower_match else Decimal('0.00')
            upper_bound = Decimal(upper_match.group(1)) if upper_match else Decimal('0.00')

            return {
                'predicted_value': predicted_value,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'confidence_score': 0,
                'explanation': response_text[:200] + "..." if len(response_text) > 200 else response_text,
                'risk_factors': 'Values extracted from text response'
            }
        except Exception as e:
            current_app.logger.error(f"Error extracting values from text: {str(e)}")
            return {
                'predicted_value': Decimal('0.00'),
                'lower_bound': Decimal('0.00'),
                'upper_bound': Decimal('0.00'),
                'confidence_score': 0,
                'explanation': 'Error extracting forecast values',
                'risk_factors': 'Error in text parsing'
            }