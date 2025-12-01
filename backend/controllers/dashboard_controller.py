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
        # Get the last 7 days of transactions for daily view
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        daily_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= seven_days_ago
        ).order_by(Transaction.date).all()
        
        # Group by date
        daily_data = {}
        for transaction in daily_transactions:
            date_key = transaction.date.strftime('%a')  # Mon, Tue, etc.
            if date_key not in daily_data:
                daily_data[date_key] = {"cashIn": 0, "cashOut": 0, "anomaly": False}
            
            if transaction.direction == 'inflow':
                daily_data[date_key]["cashIn"] += float(transaction.amount) if transaction.amount else 0
            else:
                daily_data[date_key]["cashOut"] += float(transaction.amount) if transaction.amount else 0
        
        # Convert to array format
        daily_array = []
        for date_key in sorted(daily_data.keys()):
            daily_array.append({
                "date": date_key,
                "cashIn": daily_data[date_key]["cashIn"],
                "cashOut": daily_data[date_key]["cashOut"],
                "anomaly": daily_data[date_key]["anomaly"]  # This would be determined by a more complex logic in real implementation
            })
        
        # For simplicity, adding sample data for weekly and monthly
        return {
            "daily": daily_array,
            "weekly": [
                {"date": "Week 1", "cashIn": 85000, "cashOut": 62000, "anomaly": False},
                {"date": "Week 2", "cashIn": 92000, "cashOut": 68000, "anomaly": False},
                {"date": "Week 3", "cashIn": 78000, "cashOut": 85000, "anomaly": True},
                {"date": "Week 4", "cashIn": 105000, "cashOut": 72000, "anomaly": False},
            ],
            "monthly": [
                {"date": "Jan", "cashIn": 340000, "cashOut": 280000, "anomaly": False},
                {"date": "Feb", "cashIn": 360000, "cashOut": 295000, "anomaly": False},
                {"date": "Mar", "cashIn": 320000, "cashOut": 310000, "anomaly": True},
                {"date": "Apr", "cashIn": 395000, "cashOut": 285000, "anomaly": False},
            ]
        }

    @staticmethod
    def _get_risk_forecast_data(business_id):
        """
        Get risk forecast data
        """
        # Calculate risk scores from the RiskScore model
        risk_scores = RiskScore.query.filter_by(business_id=business_id).order_by(RiskScore.created_at.desc()).limit(10).all()
        
        risk_items = [
            {
                "category": "Cashflow Risk",
                "level": 35,
                "description": "Moderate risk of negative cashflow in next 2 weeks"
            },
            {
                "category": "Debt Risk", 
                "level": 15,
                "description": "Low debt exposure relative to revenue"
            },
            {
                "category": "Burn Rate Risk",
                "level": 65, 
                "description": "Current spending rate may exceed income"
            },
            {
                "category": "Drawdown Probability",
                "level": 45,
                "description": "Medium probability of needing emergency funds"
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
            category = transaction.category.name if transaction.category else "Other"
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += float(transaction.amount) if transaction.amount else 0
        
        # If no transaction categories, use default values
        if not category_totals:
            category_totals = {
                "Operations": 35000,
                "Payroll": 30000,
                "Marketing": 15000,
                "Utilities": 12000,
                "Other": 8000
            }
        
        # Convert to the required format
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
            category = transaction.category.name if transaction.category else "Other"
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += float(transaction.amount) if transaction.amount else 0
        
        # If no transaction categories, use default values
        if not category_totals:
            category_totals = {
                "Product Sales": 45000,
                "Services": 32000,
                "Subscriptions": 18000,
                "Consulting": 12000
            }
        
        # Convert to the required format
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
        
        # If no alerts in DB, use default values
        if not alerts:
            alerts_data = [
                {
                    "id": 1,
                    "type": "warning",
                    "message": "Potential negative cashflow next week",
                    "timestamp": "2 hours ago",
                },
                {
                    "id": 2,
                    "type": "critical",
                    "message": "Unusual spike in operational expenses",
                    "timestamp": "5 hours ago",
                },
                {
                    "id": 3,
                    "type": "warning",
                    "message": "Low liquidity window expected in 14 days",
                    "timestamp": "1 day ago",
                },
                {
                    "id": 4,
                    "type": "info",
                    "message": "Income pattern aligned with seasonal trends",
                    "timestamp": "2 days ago",
                },
            ]
        else:
            alerts_data = []
            for alert in alerts[:4]:  # Take only first 4
                alert_type = "info"
                if alert.level.lower() in ["critical", "high"]:
                    alert_type = "critical"
                elif alert.level.lower() in ["warning", "medium"]:
                    alert_type = "warning"
                    
                alerts_data.append({
                    "id": alert.id,
                    "type": alert_type,
                    "message": alert.message,
                    "timestamp": f"{(datetime.utcnow() - alert.created_at).days} days ago"
                })
        
        return alerts_data

    @staticmethod
    def _get_transactions_data(business_id):
        """
        Get recent transactions data
        """
        # Get recent transactions for this business
        recent_transactions = Transaction.query.filter_by(
            business_id=business_id
        ).order_by(Transaction.date.desc()).limit(10).all()
        
        # If no transactions in DB, use default values
        if not recent_transactions:
            transactions_data = [
                {
                    "id": 1,
                    "date": "2025-01-20",
                    "description": "Client Payment - Invoice #1234",
                    "inflow": 15000,
                    "outflow": 0,
                    "category": "Revenue",
                    "aiTag": "Normal",
                },
                {
                    "id": 2,
                    "date": "2025-01-20",
                    "description": "Office Supplies",
                    "inflow": 0,
                    "outflow": 850,
                    "category": "Operations",
                    "aiTag": "Normal",
                },
                {
                    "id": 3,
                    "date": "2025-01-19",
                    "description": "Marketing Campaign",
                    "inflow": 0,
                    "outflow": 5200,
                    "category": "Marketing",
                    "aiTag": "Unusual",
                },
                {
                    "id": 4,
                    "date": "2025-01-19",
                    "description": "Subscription Revenue",
                    "inflow": 2400,
                    "outflow": 0,
                    "category": "Revenue",
                    "aiTag": "Normal",
                },
                {
                    "id": 5,
                    "date": "2025-01-18",
                    "description": "Payroll",
                    "inflow": 0,
                    "outflow": 12000,
                    "category": "Payroll",
                    "aiTag": "Normal",
                },
            ]
        else:
            transactions_data = []
            for idx, transaction in enumerate(recent_transactions[:5]):  # Take only first 5
                amount = float(transaction.amount) if transaction.amount else 0
                ai_tag = "Normal"  # Default AI tag
                
                transactions_data.append({
                    "id": transaction.id or (idx + 1),
                    "date": transaction.date.strftime('%Y-%m-%d') if transaction.date else "N/A",
                    "description": transaction.description or "N/A",
                    "inflow": amount if transaction.direction == 'inflow' else 0,
                    "outflow": amount if transaction.direction == 'outflow' else 0,
                    "category": transaction.category.name if transaction.category else "N/A",
                    "aiTag": ai_tag
                })
        
        return transactions_data