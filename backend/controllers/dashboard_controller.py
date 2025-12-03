from flask import jsonify, g
from models import Business, Transaction, RiskScore
from datetime import datetime, timedelta
from sqlalchemy import func, extract


class DashboardController:
    @staticmethod
    def get_metrics():
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        business = Business.query.filter_by(owner_id=g.current_user.id).first()
        if not business:
            return jsonify({"error": "No business found for this user."}), 404

        business_id = business.id
        print(f"DEBUG: Dashboard metrics for User ID: {g.current_user.id}, Business ID: {business_id}")

        # --- Net Cashflow ---
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30) # Last 30 days
        
        print(f"DEBUG: Date Range: {start_date.date()} to {end_date.date()}")

        current_period_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= start_date.date(),
            Transaction.date <= end_date.date() # Changed from < to <= just in case
        ).all()
        
        print(f"DEBUG: Found {len(current_period_transactions)} transactions in period.")

        prev_start_date = start_date - timedelta(days=30)
        prev_end_date = start_date

        prev_period_transactions = Transaction.query.filter(
            Transaction.business_id == business_id,
            Transaction.date >= prev_start_date.date(),
            Transaction.date < prev_end_date.date()
        ).all()

        current_inflow = sum(t.amount for t in current_period_transactions if t.direction == 'inflow')
        current_outflow = sum(t.amount for t in current_period_transactions if t.direction == 'outflow')
        net_cashflow = float(current_inflow - current_outflow)

        prev_inflow = sum(t.amount for t in prev_period_transactions if t.direction == 'inflow')
        prev_outflow = sum(t.amount for t in prev_period_transactions if t.direction == 'outflow')
        prev_net_cashflow = float(prev_inflow - prev_outflow)

        net_cashflow_percentage_change = 0.0
        net_cashflow_trend = "neutral"
        if prev_net_cashflow != 0:
            net_cashflow_percentage_change = ((net_cashflow - prev_net_cashflow) / abs(prev_net_cashflow)) * 100
            if net_cashflow_percentage_change > 0:
                net_cashflow_trend = "up"
            elif net_cashflow_percentage_change < 0:
                net_cashflow_trend = "down"

        # --- Liquidity Score (Simplified for now) ---
        # Assuming we need current cash balance from business settings or a basic approximation
        # And average monthly expenses (from current_outflow for last 30 days)
        current_cash = business.settings.get('current_cash', 0) if business.settings else 0
        average_monthly_expenses = current_outflow # Using last 30 days outflow as proxy

        liquidity_score = 0.0
        liquidity_score_trend = "neutral"
        liquidity_score_percentage_change = 0.0

        if average_monthly_expenses > 0:
            liquidity_score = (current_cash / average_monthly_expenses) * 100
            # For trend, would need to compare with previous liquidity,
            # which requires more complex state or calculations. Keeping static for now.
            # Placeholder for trend:
            if liquidity_score > 150: # Arbitrary threshold
                liquidity_score_trend = "up"
            elif liquidity_score < 100:
                liquidity_score_trend = "down"

        # --- Cashflow Volatility (Simplified) ---
        # A rough proxy: higher difference between upper and lower bound of latest forecast, or
        # just percentage of net cashflow vs total inflow/outflow
        cashflow_volatility = 0.0
        if current_inflow + current_outflow > 0:
            cashflow_volatility = (abs(current_inflow - current_outflow) / (current_inflow + current_outflow)) * 100
        cashflow_volatility_trend = "neutral" # Needs historical volatility to calculate trend
        cashflow_volatility_percentage_change = 0.0

        # --- Projected Risk ---
        latest_risk_score = RiskScore.query.filter_by(business_id=business_id).order_by(RiskScore.assessed_at.desc()).first()
        projected_risk = latest_risk_score.details.get('overall_risk', 'Unknown') if latest_risk_score and latest_risk_score.details else 'Medium'
        projected_risk_status = latest_risk_score.details.get('recommendations', []) if latest_risk_score and latest_risk_score.details else ['Monitor']
        projected_risk_trend = "neutral" # Needs historical risk scores

        # --- Risk Breakdown (for RiskForecastPanel) ---
        risk_breakdown = []
        if latest_risk_score and latest_risk_score.details:
            # Example breakdown from details, adapt as per actual RiskScore schema
            risk_breakdown.append({"category": "Cashflow Risk", "level": float(latest_risk_score.cashflow_risk_score), "description": "Based on current net cashflow trends."})
            risk_breakdown.append({"category": "Liquidity Risk", "level": float(latest_risk_score.liquidity_score), "description": "Based on current cash vs expenses."})
            risk_breakdown.append({"category": "Volatility Index", "level": float(latest_risk_score.volatility_index * 100), "description": "Measures fluctuation of cashflow."})
        else:
            # Default or simplified risk breakdown if no RiskScore
            risk_breakdown = [
                {"category": "Cashflow Risk", "level": 50, "description": "Default risk assessment."},
                {"category": "Liquidity Risk", "level": 60, "description": "Default liquidity assessment."},
                {"category": "Burn Rate Risk", "level": 40, "description": "Default burn rate assessment."},
            ]


        return jsonify({
            "net_cashflow": net_cashflow,
            "net_cashflow_trend": net_cashflow_trend,
            "net_cashflow_percentage_change": round(net_cashflow_percentage_change, 2),
            "liquidity_score": round(liquidity_score, 2),
            "liquidity_score_trend": liquidity_score_trend,
            "liquidity_score_percentage_change": round(liquidity_score_percentage_change, 2), # Placeholder
            "cashflow_volatility": round(cashflow_volatility, 2),
            "cashflow_volatility_trend": cashflow_volatility_trend, # Placeholder
            "cashflow_volatility_percentage_change": round(cashflow_volatility_percentage_change, 2), # Placeholder
            "projected_risk": projected_risk,
            "projected_risk_trend": projected_risk_trend, # Placeholder
            "projected_risk_status": projected_risk_status,
            "risk_breakdown": risk_breakdown
        })
