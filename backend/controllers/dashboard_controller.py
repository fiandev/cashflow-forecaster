from flask import request, jsonify
from models import db, Transaction, Forecast, Alert, Business, Category, RiskScore
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from decimal import Decimal


class DashboardController:
    @staticmethod
    def get_dashboard_data(business_id):
        """
        Get comprehensive dashboard data including metrics, charts, and alerts
        """
        try:
            # Check if business exists
            business = Business.query.get(business_id)
            if not business:
                return jsonify({"error": "Business not found"}), 404

            # Get metric card data
            metrics_data = DashboardController._get_metric_card_data(business_id)
            
            # Get cashflow chart data
            cashflow_chart_data = DashboardController._get_cashflow_chart_data(business_id)
            
            # Get risk forecast data
            risk_forecast_data = DashboardController._get_risk_forecast_data(business_id)
            
            # Get expense chart data
            expense_chart_data = DashboardController._get_expense_chart_data(business_id)
            
            # Get income chart data
            income_chart_data = DashboardController._get_income_chart_data(business_id)
            
            # Get AI alerts data
            ai_alerts_data = DashboardController._get_ai_alerts_data(business_id)
            
            # Get recent transactions data
            transactions_data = DashboardController._get_transactions_data(business_id)
            
            return jsonify({
                "metrics": metrics_data,
                "cashflow_chart": cashflow_chart_data,
                "risk_forecast": risk_forecast_data,
                "expense_chart": expense_chart_data,
                "income_chart": income_chart_data,
                "ai_alerts": ai_alerts_data,
                "transactions": transactions_data
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @staticmethod
    def _get_metric_card_data(business_id):
        """
        Calculate metric card data:
        - Net Cashflow
        - Liquidity Score 
        - Cashflow Volatility
        - Projected Risk
        """
        # Calculate net cashflow for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= thirty_days_ago
        ).all()
        
        net_cashflow = 0
        total_inflow = 0
        total_outflow = 0
        
        for transaction in transactions:
            if transaction.direction == 'inflow':
                total_inflow += float(transaction.amount) if transaction.amount else 0
            else:
                total_outflow += float(transaction.amount) if transaction.amount else 0
        
        net_cashflow = total_inflow - total_outflow
        
        # Calculate liquidity score (simplified: ratio of inflow to outflow)
        liquidity_score = 0
        if total_outflow > 0:
            liquidity_score = round((total_inflow / total_outflow) * 72, 2)  # Scale to 0-100 range
            if liquidity_score > 100:
                liquidity_score = 100
        
        # Calculate cashflow volatility (simplified: standard deviation of daily net flows)
        daily_flows = {}
        for transaction in transactions:
            date_key = transaction.date.strftime('%Y-%m-%d')
            if date_key not in daily_flows:
                daily_flows[date_key] = 0
            if transaction.direction == 'inflow':
                daily_flows[date_key] += float(transaction.amount) if transaction.amount else 0
            else:
                daily_flows[date_key] -= float(transaction.amount) if transaction.amount else 0
        
        daily_values = list(daily_flows.values())
        if len(daily_values) > 1:
            mean_flow = sum(daily_values) / len(daily_values)
            variance = sum((x - mean_flow) ** 2 for x in daily_values) / len(daily_values)
            volatility = (variance ** 0.5) / abs(mean_flow) * 100 if mean_flow != 0 else 0
            volatility = round(volatility, 1)
        else:
            volatility = 0
        
        # Projected risk based on recent patterns
        projected_risk = "Low"
        if net_cashflow < 0:
            projected_risk = "High"
        elif volatility > 20:
            projected_risk = "Medium"
        
        return {
            "net_cashflow": f"${net_cashflow:,.2f}",
            "net_cashflow_trend": "up" if net_cashflow >= 0 else "down",
            "net_cashflow_trend_value": f"+{abs(net_cashflow/100):.1f}%" if net_cashflow >= 0 else f"-{abs(net_cashflow/100):.1f}%",
            "net_cashflow_risk": "low" if net_cashflow > 0 else "high",
            
            "liquidity_score": f"{liquidity_score}/100",
            "liquidity_score_trend": "up" if liquidity_score > 70 else "down",
            "liquidity_score_trend_value": f"+{(liquidity_score-60):.1f}%" if liquidity_score > 60 else f"-{abs(liquidity_score-60):.1f}%",
            "liquidity_score_risk": "low" if liquidity_score > 60 else ("medium" if liquidity_score > 30 else "high"),
            
            "cashflow_volatility": f"{volatility}%",
            "cashflow_volatility_trend": "up" if volatility > 15 else "down", 
            "cashflow_volatility_trend_value": f"+{volatility/5:.1f}%" if volatility > 15 else f"-{abs(volatility-15):.1f}%",
            "cashflow_volatility_risk": "high" if volatility > 20 else ("medium" if volatility > 10 else "low"),
            
            "projected_risk": projected_risk,
            "projected_risk_trend": "up" if projected_risk == "High" else "down",
            "projected_risk_trend_value": "Critical" if projected_risk == "High" else "Stable",
            "projected_risk_risk": "high" if projected_risk == "High" else ("medium" if projected_risk == "Medium" else "low")
        }

    @staticmethod
    def _get_cashflow_chart_data(business_id):
        """
        Get cashflow chart data showing inflows and outflows over time
        """
        # Get recent transactions for daily view
        # First try to get transactions from last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        daily_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= seven_days_ago
        ).order_by(Transaction.date).all()

        # If no transactions in last 7 days, try to get at least some recent transactions
        # to ensure the daily chart isn't completely empty
        if not daily_transactions:
            # Get transactions from the last 30 days as fallback
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            daily_transactions = Transaction.query.filter(
                Transaction.business_id == business_id,
                Transaction.date >= thirty_days_ago
            ).order_by(Transaction.date).all()

        # Group by date
        daily_data = {}
        for transaction in daily_transactions:
            date_key = transaction.date.strftime('%a')  # Mon, Tue, etc.
            if date_key not in daily_data:
                daily_data[date_key] = {"cashIn": 0, "cashOut": 0, "anomaly": transaction.is_anomalous or False}

            if transaction.direction == 'inflow':
                daily_data[date_key]["cashIn"] += float(transaction.amount) if transaction.amount else 0
            else:
                daily_data[date_key]["cashOut"] += float(transaction.amount) if transaction.amount else 0

        # Convert to array format with proper chronological day order
        day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_array = []
        for day in day_order:
            if day in daily_data:
                daily_array.append({
                    "date": day,
                    "cashIn": daily_data[day]["cashIn"],
                    "cashOut": daily_data[day]["cashOut"],
                    "anomaly": daily_data[day]["anomaly"]
                })

        # Get weekly data (last 4 weeks)
        four_weeks_ago = datetime.utcnow() - timedelta(days=28)
        weekly_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= four_weeks_ago
        ).all()

        # Group by week
        weekly_data = {}
        for transaction in weekly_transactions:
            week_start = transaction.date - timedelta(days=transaction.date.weekday())
            week_key = week_start.strftime('Week %U')
            if week_key not in weekly_data:
                weekly_data[week_key] = {"cashIn": 0, "cashOut": 0, "anomaly": False}

            if transaction.direction == 'inflow':
                weekly_data[week_key]["cashIn"] += float(transaction.amount) if transaction.amount else 0
            else:
                weekly_data[week_key]["cashOut"] += float(transaction.amount) if transaction.amount else 0

            # Update anomaly flag if any transaction in this week is anomalous
            if transaction.is_anomalous:
                weekly_data[week_key]["anomaly"] = True

        # Convert weekly data to array format
        weekly_array = []
        for week_key in sorted(weekly_data.keys(), key=lambda x: int(x.split()[1])):
            weekly_array.append({
                "date": week_key,
                "cashIn": weekly_data[week_key]["cashIn"],
                "cashOut": weekly_data[week_key]["cashOut"],
                "anomaly": weekly_data[week_key]["anomaly"]
            })

        # Get monthly data (last 6 months)
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        monthly_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= six_months_ago
        ).all()

        # Group by month
        monthly_data = {}
        for transaction in monthly_transactions:
            month_key = transaction.date.strftime('%b')  # Jan, Feb, etc.
            if month_key not in monthly_data:
                monthly_data[month_key] = {"cashIn": 0, "cashOut": 0, "anomaly": False}

            if transaction.direction == 'inflow':
                monthly_data[month_key]["cashIn"] += float(transaction.amount) if transaction.amount else 0
            else:
                monthly_data[month_key]["cashOut"] += float(transaction.amount) if transaction.amount else 0

            # Update anomaly flag if any transaction in this month is anomalous
            if transaction.is_anomalous:
                monthly_data[month_key]["anomaly"] = True

        # Convert monthly data to array format
        monthly_array = []
        # Sort months properly (by actual date order, not alphabetically)
        for month_key in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if month_key in monthly_data:
                monthly_array.append({
                    "date": month_key,
                    "cashIn": monthly_data[month_key]["cashIn"],
                    "cashOut": monthly_data[month_key]["cashOut"],
                    "anomaly": monthly_data[month_key]["anomaly"]
                })

        return {
            "daily": daily_array,
            "weekly": weekly_array,
            "monthly": monthly_array
        }

    @staticmethod
    def _get_risk_forecast_data(business_id):
        """
        Get risk forecast data
        """
        # Get the most recent risk scores from the database
        risk_scores = RiskScore.query.filter_by(business_id=business_id).order_by(RiskScore.created_at.desc()).limit(1).all()

        if risk_scores:
            latest_risk = risk_scores[0]  # Get the most recent risk score

            risk_items = [
                {
                    "category": "Cashflow Risk",
                    "level": float(latest_risk.cashflow_risk_score) if latest_risk.cashflow_risk_score else 0,
                    "description": f"{'High' if latest_risk.cashflow_risk_score and latest_risk.cashflow_risk_score > 70 else 'Moderate' if latest_risk.cashflow_risk_score and latest_risk.cashflow_risk_score > 40 else 'Low'} risk of negative cashflow"
                },
                {
                    "category": "Liquidity Score",
                    "level": float(latest_risk.liquidity_score) if latest_risk.liquidity_score else 0,
                    "description": f"Liquidity score of {latest_risk.liquidity_score:.1f}" if latest_risk.liquidity_score else "Liquidity score not calculated"
                },
                {
                    "category": "Volatility Index",
                    "level": float(latest_risk.volatility_index) if latest_risk.volatility_index else 0,
                    "description": f"Cashflow volatility index of {latest_risk.volatility_index:.1f}" if latest_risk.volatility_index else "Volatility index not calculated"
                },
                {
                    "category": "Drawdown Probability",
                    "level": float(latest_risk.drawdown_prob) if latest_risk.drawdown_prob else 0,
                    "description": f"{(latest_risk.drawdown_prob or 0)*100:.1f}% probability of needing emergency funds"
                }
            ]
        else:
            # Fallback to calculating risk metrics based on transactions if no RiskScore records exist
            # This uses the same method as get_actual_stats_after_forecast
            all_transactions = Transaction.query.filter_by(business_id=business_id).all()
            risk_metrics = DashboardController._calculate_risk_metrics_from_transactions(all_transactions)

            risk_items = [
                {
                    "category": "Cashflow Risk",
                    "level": min(100, risk_metrics["volatility"] / 10) if risk_metrics["volatility"] else 30,
                    "description": f"Risk based on cashflow volatility of {risk_metrics['volatility']:.2f}" if risk_metrics["volatility"] else "Risk calculated from transaction patterns"
                },
                {
                    "category": "Liquidity Score",
                    "level": min(100, risk_metrics["liquidity_ratio"] * 10) if risk_metrics["liquidity_ratio"] and risk_metrics["liquidity_ratio"] != float('inf') else 70,
                    "description": f"Liquidity ratio of {risk_metrics['liquidity_ratio']:.2f}" if risk_metrics["liquidity_ratio"] and risk_metrics["liquidity_ratio"] != float('inf') else "Sufficient inflows relative to outflows"
                },
                {
                    "category": "Volatility Index",
                    "level": min(100, risk_metrics["volatility"] / 5) if risk_metrics["volatility"] else 20,
                    "description": f"Based on transaction volatility of {risk_metrics['volatility']:.2f}" if risk_metrics["volatility"] else "Low transaction volatility"
                },
                {
                    "category": "Drawdown Probability",
                    "level": 30,  # Default estimate when no risk score exists
                    "description": "Estimated probability based on transaction patterns"
                }
            ]

        return risk_items

    @staticmethod
    def _get_expense_chart_data(business_id):
        """
        Get expense composition data
        """
        # Get expenses by category for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        expenses = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.direction == 'outflow',
            Transaction.date >= thirty_days_ago
        ).all()

        # Group by category
        category_totals = {}
        for transaction in expenses:
            category = transaction.category.name if transaction.category else "Uncategorized"
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += float(transaction.amount) if transaction.amount else 0

        # Convert to the required format - return empty array if no expense data
        total_expenses = sum(category_totals.values())
        chart_data = []

        for category, amount in category_totals.items():
            percentage = round((amount / total_expenses) * 100, 2) if total_expenses > 0 else 0
            chart_data.append({
                "name": category,
                "value": percentage
            })

        return chart_data

    @staticmethod
    def _get_income_chart_data(business_id):
        """
        Get income stream breakdown data
        """
        # Get income by category for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        income = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.direction == 'inflow',
            Transaction.date >= thirty_days_ago
        ).all()

        # Group by category
        category_totals = {}
        for transaction in income:
            category = transaction.category.name if transaction.category else "Uncategorized"
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += float(transaction.amount) if transaction.amount else 0

        # Convert to the required format - return empty array if no income data
        chart_data = []

        for source, amount in category_totals.items():
            chart_data.append({
                "source": source,
                "amount": amount
            })

        return chart_data

    @staticmethod
    def _get_ai_alerts_data(business_id):
        """
        Get AI alerts data
        """
        # Get alerts for this business
        alerts = Alert.query.filter_by(business_id=business_id).order_by(Alert.created_at.desc()).limit(10).all()

        alerts_data = []
        for alert in alerts:
            alert_type = "info"
            if alert.level.lower() in ["critical", "high"]:
                alert_type = "critical"
            elif alert.level.lower() in ["warning", "medium"]:
                alert_type = "warning"

            time_diff = datetime.utcnow() - alert.created_at
            if time_diff.days > 0:
                timestamp = f"{time_diff.days} days ago"
            elif time_diff.seconds // 3600 > 0:
                timestamp = f"{time_diff.seconds // 3600} hours ago"
            else:
                timestamp = f"{time_diff.seconds // 60} minutes ago"

            alerts_data.append({
                "id": alert.id,
                "type": alert_type,
                "message": alert.message,
                "timestamp": timestamp
            })

        return alerts_data

    @staticmethod
    def generate_ai_alerts(business_id):
        """
        Generate AI-powered alerts based on transaction patterns and business data
        """
        try:
            # Check if business exists
            business = Business.query.get(business_id)
            if not business:
                return jsonify({"error": "Business not found"}), 404

            # Get recent transactions for analysis
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_transactions = Transaction.query.filter(
                Transaction.business_id == business_id,
                Transaction.date >= thirty_days_ago
            ).order_by(Transaction.date.desc()).all()

            # Get recent forecasts for context
            recent_forecasts = Forecast.query.filter(
                Forecast.business_id == business_id,
                Forecast.created_at >= thirty_days_ago
            ).order_by(Forecast.created_at.desc()).limit(5).all()

            # Get recent risk scores
            recent_risk_scores = RiskScore.query.filter(
                RiskScore.business_id == business_id,
                RiskScore.created_at >= thirty_days_ago
            ).order_by(RiskScore.created_at.desc()).limit(5).all()

            # Prepare data for AI analysis
            transaction_data = []
            for transaction in recent_transactions:
                transaction_data.append({
                    "date": transaction.date.isoformat() if transaction.date else "N/A",
                    "direction": transaction.direction,
                    "amount": float(transaction.amount) if transaction.amount else 0,
                    "description": transaction.description or "",
                    "category": transaction.category.name if transaction.category else "N/A",
                    "is_anomalous": transaction.is_anomalous
                })

            forecast_data = []
            for forecast in recent_forecasts:
                forecast_data.append({
                    "period_start": forecast.period_start.isoformat() if forecast.period_start else "N/A",
                    "period_end": forecast.period_end.isoformat() if forecast.period_end else "N/A",
                    "predicted_value": float(forecast.predicted_value) if forecast.predicted_value else 0,
                    "lower_bound": float(forecast.lower_bound) if forecast.lower_bound else 0,
                    "upper_bound": float(forecast.upper_bound) if forecast.upper_bound else 0,
                    "granularity": forecast.granularity
                })

            risk_data = []
            for risk_score in recent_risk_scores:
                risk_data.append({
                    "liquidity_score": float(risk_score.liquidity_score) if risk_score.liquidity_score else 0,
                    "cashflow_risk_score": float(risk_score.cashflow_risk_score) if risk_score.cashflow_risk_score else 0,
                    "volatility_index": float(risk_score.volatility_index) if risk_score.volatility_index else 0,
                    "drawdown_prob": float(risk_score.drawdown_prob) if risk_score.drawdown_prob else 0
                })

            # Prepare prompt for AI alert generation
            prompt = f"""
You are a financial risk analyst examining a business's cashflow patterns. Analyze the following data and generate 3-5 critical AI alerts with recommendations.

BUSINESS INFORMATION:
- Business Name: {business.name}
- Currency: {business.currency}
- Country: {business.country}

RECENT TRANSACTIONS (last 30 days):
{str(transaction_data[:10])}  # Limit to first 10 for prompt brevity

RECENT FORECASTS:
{str(forecast_data)}

RECENT RISK SCORES:
{str(risk_data)}

Based on this data, identify potential financial risks, anomalies, or opportunities. Create alerts with the following format as a JSON array:
[
  {{
    "type": "critical|warning|info|success",
    "message": "Alert message with specific financial insight",
    "severity": "high|medium|low",
    "category": "cashflow|risk|expense|income|anomaly",
    "recommendation": "Specific recommendation to address this alert",
    "confidence": "high|medium|low"
  }}
]

Important: Only return the JSON array with no additional text or explanation.
"""

            import os
            import json
            import re

            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                # If API key is not available, return default alerts
                ai_alerts = [
                    {
                        "type": "warning",
                        "message": "Potential cashflow issue detected in recent transactions",
                        "severity": "medium",
                        "category": "cashflow",
                        "recommendation": "Review upcoming expenses and income projections",
                        "confidence": "medium"
                    },
                    {
                        "type": "info",
                        "message": "Income patterns show seasonal trend alignment",
                        "severity": "low",
                        "category": "income",
                        "recommendation": "Continue current revenue strategy",
                        "confidence": "high"
                    }
                ]
            else:
                from services.llm_service import create_gemini_service
                # Use the existing LLM service to generate alerts
                service = create_gemini_service(api_key, model='gemini-1.0-pro')
                response_text = service.generate_text(prompt)

                # Extract JSON array from the response
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    try:
                        ai_alerts = json.loads(json_str)
                        # Validate and ensure each alert has required fields
                        validated_alerts = []
                        for alert in ai_alerts:
                            if isinstance(alert, dict):
                                validated_alert = {
                                    "type": alert.get('type', 'info'),
                                    "message": alert.get('message', 'Financial insight detected'),
                                    "severity": alert.get('severity', 'medium'),
                                    "category": alert.get('category', 'general'),
                                    "recommendation": alert.get('recommendation', 'Review this financial aspect'),
                                    "confidence": alert.get('confidence', 'medium')
                                }
                                validated_alerts.append(validated_alert)
                        ai_alerts = validated_alerts
                    except json.JSONDecodeError:
                        # If JSON parsing fails, return default alerts
                        ai_alerts = [
                            {
                                "type": "info",
                                "message": "AI analysis completed but could not parse detailed insights",
                                "severity": "low",
                                "category": "analysis",
                                "recommendation": "Check transaction data for anomalies",
                                "confidence": "low"
                            }
                        ]
                else:
                    ai_alerts = [
                        {
                            "type": "info",
                            "message": "No specific AI alerts generated from current data",
                            "severity": "low",
                            "category": "analysis",
                            "recommendation": "Continue monitoring financial patterns",
                            "confidence": "low"
                        }
                    ]

            # Create and save alerts to database
            created_alerts = []
            for alert_data in ai_alerts:
                # Create Alert instance and save to database
                new_alert = Alert(
                    business_id=business_id,
                    level=alert_data['severity'],
                    message=alert_data['message']
                )

                db.session.add(new_alert)
                db.session.commit()

                created_alerts.append({
                    "id": new_alert.id,
                    "type": alert_data['type'],
                    "message": alert_data['message'],
                    "severity": alert_data['severity'],
                    "category": alert_data['category'],
                    "recommendation": alert_data['recommendation'],
                    "confidence": alert_data['confidence'],
                    "created_at": new_alert.created_at.isoformat()
                })

            return jsonify({
                "business_id": business_id,
                "ai_generated_alerts": created_alerts,
                "analysis_timestamp": datetime.utcnow().isoformat()
            })

        except Exception as e:
            return jsonify({"error": f"Error generating AI alerts: {str(e)}"}), 500

    @staticmethod
    def _get_transactions_data(business_id):
        """
        Get recent transactions data
        """
        # Get recent transactions for this business
        recent_transactions = Transaction.query.filter_by(
            business_id=business_id
        ).order_by(Transaction.date.desc()).limit(10).all()

        transactions_data = []
        for transaction in recent_transactions:
            amount = float(transaction.amount) if transaction.amount else 0
            ai_tag = "Normal"  # Default AI tag, could be enhanced with more logic

            # Update AI tag based on transaction properties
            if transaction.is_anomalous:
                ai_tag = "Anomalous"
            elif transaction.amount and transaction.amount > 10000:  # High value transaction
                ai_tag = "High Value"
            elif transaction.category and transaction.category.name.lower() in ['tax', 'penalty', 'fine']:
                ai_tag = "Attention Required"

            transactions_data.append({
                "id": transaction.id,
                "date": transaction.date.strftime('%Y-%m-%d') if transaction.date else "N/A",
                "description": transaction.description or "N/A",
                "inflow": amount if transaction.direction == 'inflow' else 0,
                "outflow": amount if transaction.direction == 'outflow' else 0,
                "category": transaction.category.name if transaction.category else "Uncategorized",
                "aiTag": ai_tag
            })

        return transactions_data

    @staticmethod
    def get_actual_stats_after_forecast(business_id):
        """
        Get actual stats and calculated metrics after forecast, derived from transaction data
        """
        try:
            # Check if business exists
            business = Business.query.get(business_id)
            if not business:
                return jsonify({"error": "Business not found"}), 404

            # Get all transactions for this business
            all_transactions = Transaction.query.filter_by(business_id=business_id).all()

            # Calculate various metrics from transaction data
            total_income = sum(float(t.amount) for t in all_transactions if t.direction == 'inflow')
            total_expenses = sum(float(t.amount) for t in all_transactions if t.direction == 'outflow')
            net_cashflow = total_income - total_expenses

            # Calculate transaction counts
            income_transaction_count = len([t for t in all_transactions if t.direction == 'inflow'])
            expense_transaction_count = len([t for t in all_transactions if t.direction == 'outflow'])

            # Find date range of transactions
            dates = [t.date for t in all_transactions if t.date]
            if dates:
                min_date = min(dates)
                max_date = max(dates)
            else:
                min_date = max_date = None

            # Calculate monthly averages if we have date range
            monthly_income_avg = 0
            monthly_expense_avg = 0
            if min_date and max_date:
                days_diff = (max_date - min_date).days
                months_diff = max(1, days_diff / 30.44)  # Average days in a month
                monthly_income_avg = total_income / months_diff if months_diff > 0 else 0
                monthly_expense_avg = total_expenses / months_diff if months_diff > 0 else 0

            # Calculate risk metrics based on transaction patterns
            # This includes volatility, liquidity ratios, etc.
            risk_metrics = DashboardController._calculate_risk_metrics_from_transactions(all_transactions)

            # Get recent forecasts for this business
            recent_forecasts = Forecast.query.filter_by(business_id=business_id).order_by(Forecast.created_at.desc()).limit(5).all()

            recent_forecast_data = []
            for forecast in recent_forecasts:
                recent_forecast_data.append({
                    "id": forecast.id,
                    "granularity": forecast.granularity,
                    "period_start": forecast.period_start.isoformat() if forecast.period_start else None,
                    "period_end": forecast.period_end.isoformat() if forecast.period_end else None,
                    "predicted_value": float(forecast.predicted_value) if forecast.predicted_value else 0,
                    "lower_bound": float(forecast.lower_bound) if forecast.lower_bound else 0,
                    "upper_bound": float(forecast.upper_bound) if forecast.upper_bound else 0,
                    "created_at": forecast.created_at.isoformat() if forecast.created_at else None
                })

            # Get recent risk scores
            recent_risk_scores = RiskScore.query.filter_by(business_id=business_id).order_by(RiskScore.created_at.desc()).limit(5).all()

            risk_score_data = []
            for risk_score in recent_risk_scores:
                risk_score_data.append({
                    "id": risk_score.id,
                    "assessed_at": risk_score.assessed_at.isoformat() if risk_score.assessed_at else None,
                    "liquidity_score": float(risk_score.liquidity_score) if risk_score.liquidity_score else 0,
                    "cashflow_risk_score": float(risk_score.cashflow_risk_score) if risk_score.cashflow_risk_score else 0,
                    "volatility_index": float(risk_score.volatility_index) if risk_score.volatility_index else 0,
                    "drawdown_prob": float(risk_score.drawdown_prob) if risk_score.drawdown_prob else 0,
                    "created_at": risk_score.created_at.isoformat() if risk_score.created_at else None
                })

            # Prepare response with actual metrics derived from transactions and forecasts
            response_data = {
                "business_id": business_id,
                "transaction_summary": {
                    "total_income": total_income,
                    "total_expenses": total_expenses,
                    "net_cashflow": net_cashflow,
                    "income_transaction_count": income_transaction_count,
                    "expense_transaction_count": expense_transaction_count,
                    "date_range": {
                        "start": min_date.isoformat() if min_date else None,
                        "end": max_date.isoformat() if max_date else None
                    },
                    "monthly_averages": {
                        "income": round(monthly_income_avg, 2),
                        "expense": round(monthly_expense_avg, 2)
                    }
                },
                "risk_metrics": risk_metrics,
                "recent_forecasts": recent_forecast_data,
                "recent_risk_scores": risk_score_data,
                "calculation_timestamp": datetime.utcnow().isoformat()
            }

            return jsonify(response_data)

        except Exception as e:
            return jsonify({"error": f"Error getting actual stats after forecast: {str(e)}"}), 500

    @staticmethod
    def _calculate_risk_metrics_from_transactions(transactions):
        """
        Calculate risk metrics based on transaction patterns
        """
        if not transactions:
            return {
                "volatility": 0,
                "liquidity_ratio": 0,
                "expense_concentration": 0,
                "cashflow_trend": "neutral",
                "payment_frequency": 0
            }

        # Calculate daily cashflows
        daily_flows = {}
        for transaction in transactions:
            if not transaction.date:
                continue
            date_key = transaction.date.isoformat()
            if date_key not in daily_flows:
                daily_flows[date_key] = 0

            if transaction.direction == 'inflow':
                daily_flows[date_key] += float(transaction.amount) if transaction.amount else 0
            else:
                daily_flows[date_key] -= float(transaction.amount) if transaction.amount else 0

        daily_values = list(daily_flows.values())

        # Calculate volatility (standard deviation of daily flows)
        if len(daily_values) > 1:
            mean_flow = sum(daily_values) / len(daily_values)
            variance = sum((x - mean_flow) ** 2 for x in daily_values) / len(daily_values)
            volatility = (variance ** 0.5)
        else:
            volatility = 0

        # Calculate liquidity ratio (income / expenses)
        total_income = sum(float(t.amount) for t in transactions if t.direction == 'inflow')
        total_expenses = sum(float(t.amount) for t in transactions if t.direction == 'outflow')
        liquidity_ratio = (total_income / total_expenses) if total_expenses > 0 else float('inf')

        # Calculate expense concentration (how much is spent on top categories)
        expense_by_category = {}
        for transaction in [t for t in transactions if t.direction == 'outflow']:
            category = transaction.category.name if transaction.category else "Uncategorized"
            if category not in expense_by_category:
                expense_by_category[category] = 0
            expense_by_category[category] += float(transaction.amount) if transaction.amount else 0

        if expense_by_category:
            total_expenses_by_cat = sum(expense_by_category.values())
            if total_expenses_by_cat > 0:
                top_categories = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)
                top_expense_concentration = sum(amt for _, amt in top_categories[:3]) / total_expenses_by_cat
            else:
                top_expense_concentration = 0
        else:
            top_expense_concentration = 0

        # Determine cashflow trend
        cashflow_trend = "neutral"
        if len(daily_values) >= 2:
            recent_avg = sum(daily_values[-max(1, len(daily_values)//4):]) / len(daily_values[-max(1, len(daily_values)//4):])
            earlier_avg = sum(daily_values[:max(1, len(daily_values)//4)]) / len(daily_values[:max(1, len(daily_values)//4)])
            if recent_avg > earlier_avg * 1.1:
                cashflow_trend = "improving"
            elif recent_avg < earlier_avg * 0.9:
                cashflow_trend = "declining"

        # Calculate payment frequency (for recurring income)
        income_dates = [t.date for t in transactions if t.direction == 'inflow' and t.date]
        if len(income_dates) >= 2:
            income_dates.sort()
            intervals = [(income_dates[i+1] - income_dates[i]).days for i in range(len(income_dates)-1)]
            avg_interval = sum(intervals) / len(intervals) if intervals else 0
            payment_frequency = avg_interval
        else:
            payment_frequency = 0

        return {
            "volatility": round(volatility, 2),
            "liquidity_ratio": round(liquidity_ratio, 2),
            "expense_concentration": round(top_expense_concentration * 100, 2),
            "cashflow_trend": cashflow_trend,
            "payment_frequency_days": round(payment_frequency, 1),
            "transaction_count": len(transactions),
            "active_days": len(daily_values)
        }