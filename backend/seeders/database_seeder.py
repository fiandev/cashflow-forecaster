from datetime import datetime, date, timedelta
from decimal import Decimal
from utils.crypto import hash_password
import random, hashlib

from models import (
    db,
    User,
    Business,
    Category,
    Transaction,
    OCRDocument,
    Model,
    ModelRun,
    Forecast,
    RiskScore,
    Alert,
    Scenario,
    APIKey,
)


class DatabaseSeeder:
    def __init__(self):
        self.users = []
        self.businesses = []
        self.categories = []
        self.transactions = []
        self.ocr_documents = []
        self.models = []
        self.model_runs = []
        self.forecasts = []
        self.risk_scores = []
        self.alerts = []
        self.scenarios = []
        self.api_keys = []

    def clear_all_tables(self):
        print("Clearing existing data...")
        db.session.query(Alert).delete()
        db.session.query(RiskScore).delete()
        db.session.query(Forecast).delete()
        db.session.query(ModelRun).delete()
        db.session.query(Model).delete()
        db.session.query(Transaction).delete()
        db.session.query(OCRDocument).delete()
        db.session.query(Category).delete()
        db.session.query(APIKey).delete()
        db.session.query(Scenario).delete()
        db.session.query(Business).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("All tables cleared.")

    def seed_users(self):
        print("Seeding users...")

        users_data = [
            {
                "email": "admin@gmail.com",
                "password": "password",
                "name": "System Administrator",
                "role": "admin",
            },
            {
                "email": "user@gmail.com",
                "password": "password",
                "name": "Owner Bisnis",
                "role": "business_owner",
            },
            {
                "email": "jane.smith@gmail.com",
                "password": "password",
                "name": "Jane Smith",
                "role": "business_owner",
            },
        ]

        for user_data in users_data:
            # Hash password using SHA256 with 255 character limit
            password = user_data["password"]
            hashed_password = hash_password(password)
            user_data["password"] = hashed_password

            user = User(**user_data)
            db.session.add(user)
            self.users.append(user)

        db.session.commit()
        print(f"Created {len(self.users)} users.")

    def seed_businesses(self):
        print("Seeding businesses...")

        businesses_data = [
            {
                "owner_id": self.users[1].id,  # John Doe
                "name": "TechCorp Solutions",
                "country": "United States",
                "city": "San Francisco",
                "currency": "USD",
                "timezone": "America/Los_Angeles",
                "settings": {"industry": "technology", "employees": 150},
            },
            {
                "owner_id": self.users[2].id,  # Jane Smith
                "name": "RetailCo Stores",
                "country": "Canada",
                "city": "Toronto",
                "currency": "CAD",
                "timezone": "America/Toronto",
                "settings": {"industry": "retail", "stores": 25},
            },
            {
                "owner_id": self.users[1].id,  # John Doe - second business
                "name": "CloudTech Services",
                "country": "United States",
                "city": "New York",
                "currency": "USD",
                "timezone": "America/New_York",
                "settings": {"industry": "cloud_services", "clients": 500},
            },
        ]

        for business_data in businesses_data:
            business = Business(**business_data)
            db.session.add(business)
            self.businesses.append(business)

        db.session.commit()
        print(f"Created {len(self.businesses)} businesses.")

    def seed_categories(self):
        print("Seeding categories...")

        categories_data = [
            # TechCorp Categories
            {
                "business_id": self.businesses[0].id,
                "name": "Software Revenue",
                "type": "income",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[0].id,
                "name": "Licensing",
                "type": "income",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[0].id,
                "name": "Salaries",
                "type": "expense",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[0].id,
                "name": "Office Rent",
                "type": "expense",
                "parent_id": None,
            },
            # RetailCo Categories
            {
                "business_id": self.businesses[1].id,
                "name": "Product Sales",
                "type": "income",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[1].id,
                "name": "Online Sales",
                "type": "income",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[1].id,
                "name": "Inventory",
                "type": "expense",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[1].id,
                "name": "Marketing",
                "type": "expense",
                "parent_id": None,
            },
            # CloudTech Categories
            {
                "business_id": self.businesses[2].id,
                "name": "Subscription Revenue",
                "type": "income",
                "parent_id": None,
            },
            {
                "business_id": self.businesses[2].id,
                "name": "Cloud Infrastructure",
                "type": "expense",
                "parent_id": None,
            },
        ]

        for category_data in categories_data:
            category = Category(**category_data)
            db.session.add(category)
            self.categories.append(category)

        db.session.commit()
        print(f"Created {len(self.categories)} categories.")

    def seed_transactions(self):
        print("Seeding transactions...")

        base_date = date.today() - timedelta(days=90)

        transactions_data = []

        # TechCorp transactions
        for i in range(20):
            trans_date = base_date + timedelta(days=i * 4)
            if i % 3 == 0:
                # Income
                transactions_data.append(
                    {
                        "business_id": self.businesses[0].id,
                        "date": trans_date,
                        "datetime": datetime.combine(trans_date, datetime.min.time()),
                        "description": f"Client payment #{i + 1}",
                        "amount": Decimal(str(random.uniform(5000, 25000))),
                        "direction": "inflow",
                        "category_id": self.categories[0].id,  # Software Revenue
                        "source": "bank_transfer",
                        "tags": ["client", "software"],
                    }
                )
            else:
                # Expense
                transactions_data.append(
                    {
                        "business_id": self.businesses[0].id,
                        "date": trans_date,
                        "datetime": datetime.combine(trans_date, datetime.min.time()),
                        "description": f"Salary payment #{i + 1}",
                        "amount": Decimal(str(random.uniform(8000, 15000))),
                        "direction": "outflow",
                        "category_id": self.categories[2].id,  # Salaries
                        "source": "bank_transfer",
                        "tags": ["payroll"],
                    }
                )

        # RetailCo transactions
        for i in range(15):
            trans_date = base_date + timedelta(days=i * 6)
            if i % 2 == 0:
                # Income
                transactions_data.append(
                    {
                        "business_id": self.businesses[1].id,
                        "date": trans_date,
                        "datetime": datetime.combine(trans_date, datetime.min.time()),
                        "description": f"Daily sales #{i + 1}",
                        "amount": Decimal(str(random.uniform(3000, 12000))),
                        "direction": "inflow",
                        "category_id": self.categories[4].id,  # Product Sales
                        "source": "cash_register",
                        "tags": ["retail", "sales"],
                    }
                )
            else:
                # Expense
                transactions_data.append(
                    {
                        "business_id": self.businesses[1].id,
                        "date": trans_date,
                        "datetime": datetime.combine(trans_date, datetime.min.time()),
                        "description": f"Inventory purchase #{i + 1}",
                        "amount": Decimal(str(random.uniform(2000, 8000))),
                        "direction": "outflow",
                        "category_id": self.categories[6].id,  # Inventory
                        "source": "supplier",
                        "tags": ["inventory", "purchase"],
                    }
                )

        # CloudTech transactions
        for i in range(10):
            trans_date = base_date + timedelta(days=i * 9)
            transactions_data.append(
                {
                    "business_id": self.businesses[2].id,
                    "date": trans_date,
                    "datetime": datetime.combine(trans_date, datetime.min.time()),
                    "description": f"Monthly subscription #{i + 1}",
                    "amount": Decimal(str(random.uniform(15000, 45000))),
                    "direction": "inflow",
                    "category_id": self.categories[8].id,  # Subscription Revenue
                    "source": "stripe",
                    "tags": ["subscription", "recurring"],
                }
            )

        for trans_data in transactions_data:
            transaction = Transaction(**trans_data)
            db.session.add(transaction)
            self.transactions.append(transaction)

        db.session.commit()
        print(f"Created {len(self.transactions)} transactions.")

    def seed_ocr_documents(self):
        print("Seeding OCR documents...")

        ocr_data = [
            {
                "business_id": self.businesses[0].id,
                "uploaded_by": self.users[1].id,  # John Doe
                "raw_text": "INVOICE #2024-001\nTechCorp Solutions\nAmount: $12,500.00\nDue Date: 2024-02-15",
                "parsed": {
                    "invoice_number": "2024-001",
                    "amount": 12500.00,
                    "due_date": "2024-02-15",
                },
                "confidence": Decimal("0.9542"),
                "source_image_url": "https://example.com/invoices/inv-001.jpg",
            },
            {
                "business_id": self.businesses[1].id,
                "uploaded_by": self.users[2].id,  # Jane Smith
                "raw_text": "RECEIPT #R-2024-045\nRetailCo Stores\nTotal: $3,245.67\nDate: 2024-01-20",
                "parsed": {
                    "receipt_number": "R-2024-045",
                    "amount": 3245.67,
                    "date": "2024-01-20",
                },
                "confidence": Decimal("0.9123"),
                "source_image_url": "https://example.com/receipts/rec-045.jpg",
            },
            {
                "business_id": self.businesses[0].id,
                "uploaded_by": self.users[1].id,  # John Doe
                "raw_text": "EXPENSE REPORT\nCloud Infrastructure\nAWS Services\nAmount: $8,750.00",
                "parsed": {
                    "type": "expense_report",
                    "service": "AWS",
                    "amount": 8750.00,
                },
                "confidence": Decimal("0.8891"),
                "source_image_url": "https://example.com/expenses/aws-001.jpg",
            },
            {
                "business_id": self.businesses[2].id,
                "uploaded_by": self.users[1].id,  # John Doe
                "raw_text": "CONTRACT #CT-2024-012\nCloudTech Services\nMonthly Retainer: $25,000.00",
                "parsed": {"contract_number": "CT-2024-012", "retainer": 25000.00},
                "confidence": Decimal("0.9345"),
                "source_image_url": "https://example.com/contracts/ct-012.jpg",
            },
        ]

        for doc_data in ocr_data:
            ocr_doc = OCRDocument(**doc_data)
            db.session.add(ocr_doc)
            self.ocr_documents.append(ocr_doc)

        db.session.commit()
        print(f"Created {len(self.ocr_documents)} OCR documents.")

    def seed_models(self):
        print("Seeding ML models...")

        models_data = [
            {
                "business_id": self.businesses[0].id,
                "name": "TechCorp Cash Flow Predictor",
                "model_type": "lstm",
                "params": {"layers": 3, "units": 128, "dropout": 0.2},
                "version": "v2.1.0",
                "last_trained_at": datetime.now() - timedelta(days=7),
            },
            {
                "business_id": self.businesses[1].id,
                "name": "RetailCo Sales Forecaster",
                "model_type": "arima",
                "params": {"p": 1, "d": 1, "q": 1, "seasonal": True},
                "version": "v1.5.2",
                "last_trained_at": datetime.now() - timedelta(days=3),
            },
            {
                "business_id": self.businesses[2].id,
                "name": "CloudTech Revenue Model",
                "model_type": "prophet",
                "params": {"seasonality": "monthly", "changepoints": 25},
                "version": "v3.0.1",
                "last_trained_at": datetime.now() - timedelta(days=1),
            },
            {
                "business_id": self.businesses[0].id,
                "name": "TechCorp Anomaly Detector",
                "model_type": "isolation_forest",
                "params": {"contamination": 0.1, "n_estimators": 100},
                "version": "v1.0.0",
                "last_trained_at": datetime.now() - timedelta(days=14),
            },
        ]

        for model_data in models_data:
            model = Model(**model_data)
            db.session.add(model)
            self.models.append(model)

        db.session.commit()
        print(f"Created {len(self.models)} models.")

    def seed_model_runs(self):
        print("Seeding model runs...")

        runs_data = [
            {
                "model_id": self.models[0].id,
                "input_summary": {"period": "90_days", "features": 15},
                "output_summary": {"mse": 0.0234, "mae": 0.1456},
                "run_status": "completed",
                "notes": "Successful run with improved accuracy",
            },
            {
                "model_id": self.models[1].id,
                "input_summary": {"period": "180_days", "seasonal_decomposition": True},
                "output_summary": {"aic": 1234.56, "bic": 1245.67},
                "run_status": "completed",
                "notes": "Seasonal patterns detected",
            },
            {
                "model_id": self.models[2].id,
                "input_summary": {"period": "365_days", "holidays": True},
                "output_summary": {"mape": 0.0891, "coverage": 0.95},
                "run_status": "completed",
                "notes": "Holiday effects incorporated",
            },
            {
                "model_id": self.models[0].id,
                "input_summary": {"period": "30_days", "features": 12},
                "output_summary": {"anomalies_detected": 3},
                "run_status": "failed",
                "notes": "Insufficient data for reliable prediction",
            },
        ]

        for run_data in runs_data:
            model_run = ModelRun(**run_data)
            db.session.add(model_run)
            self.model_runs.append(model_run)

        db.session.commit()
        print(f"Created {len(self.model_runs)} model runs.")

    def seed_forecasts(self):
        print("Seeding forecasts...")

        forecasts_data = [
            {
                "business_id": self.businesses[0].id,
                "model_run_id": self.model_runs[0].id,
                "model_id": self.models[0].id,
                "granularity": "monthly",
                "period_start": date.today(),
                "period_end": date.today() + timedelta(days=30),
                "predicted_value": Decimal("125000.50"),
                "lower_bound": Decimal("115000.25"),
                "upper_bound": Decimal("135000.75"),
                "forecast_metadata": {"confidence": 0.85, "trend": "increasing"},
            },
            {
                "business_id": self.businesses[1].id,
                "model_run_id": self.model_runs[1].id,
                "model_id": self.models[1].id,
                "granularity": "weekly",
                "period_start": date.today(),
                "period_end": date.today() + timedelta(days=7),
                "predicted_value": Decimal("45000.00"),
                "lower_bound": Decimal("42000.00"),
                "upper_bound": Decimal("48000.00"),
                "forecast_metadata": {"confidence": 0.78, "seasonality": "weekly"},
            },
            {
                "business_id": self.businesses[2].id,
                "model_run_id": self.model_runs[2].id,
                "model_id": self.models[2].id,
                "granularity": "daily",
                "period_start": date.today(),
                "period_end": date.today() + timedelta(days=1),
                "predicted_value": Decimal("1500.75"),
                "lower_bound": Decimal("1400.50"),
                "upper_bound": Decimal("1600.25"),
                "forecast_metadata": {"confidence": 0.92, "volatility": "low"},
            },
            {
                "business_id": self.businesses[0].id,
                "model_id": self.models[0].id,
                "granularity": "quarterly",
                "period_start": date.today(),
                "period_end": date.today() + timedelta(days=90),
                "predicted_value": Decimal("375000.00"),
                "lower_bound": Decimal("350000.00"),
                "upper_bound": Decimal("400000.00"),
                "forecast_metadata": {"confidence": 0.80, "trend": "stable"},
            },
        ]

        for forecast_data in forecasts_data:
            forecast = Forecast(**forecast_data)
            db.session.add(forecast)
            self.forecasts.append(forecast)

        db.session.commit()
        print(f"Created {len(self.forecasts)} forecasts.")

    def seed_risk_scores(self):
        print("Seeding risk scores...")

        risk_scores_data = [
            {
                "business_id": self.businesses[0].id,
                "liquidity_score": Decimal("85.50"),
                "cashflow_risk_score": Decimal("25.75"),
                "volatility_index": Decimal("0.1234"),
                "drawdown_prob": Decimal("0.0891"),
                "source_forecast_id": self.forecasts[0].id,
                "details": {
                    "overall_risk": "low",
                    "recommendations": ["maintain_current_strategy"],
                },
            },
            {
                "business_id": self.businesses[1].id,
                "liquidity_score": Decimal("72.25"),
                "cashflow_risk_score": Decimal("45.30"),
                "volatility_index": Decimal("0.2156"),
                "drawdown_prob": Decimal("0.1567"),
                "source_forecast_id": self.forecasts[1].id,
                "details": {
                    "overall_risk": "medium",
                    "recommendations": [
                        "increase_cash_reserves",
                        "monitor_seasonality",
                    ],
                },
            },
            {
                "business_id": self.businesses[2].id,
                "liquidity_score": Decimal("91.75"),
                "cashflow_risk_score": Decimal("15.20"),
                "volatility_index": Decimal("0.0891"),
                "drawdown_prob": Decimal("0.0456"),
                "source_forecast_id": self.forecasts[2].id,
                "details": {
                    "overall_risk": "very_low",
                    "recommendations": ["consider_expansion"],
                },
            },
            {
                "business_id": self.businesses[0].id,
                "liquidity_score": Decimal("68.90"),
                "cashflow_risk_score": Decimal("52.40"),
                "volatility_index": Decimal("0.3124"),
                "drawdown_prob": Decimal("0.2234"),
                "details": {
                    "overall_risk": "high",
                    "recommendations": ["reduce_expenses", "secure_funding"],
                },
            },
        ]

        for risk_data in risk_scores_data:
            risk_score = RiskScore(**risk_data)
            db.session.add(risk_score)
            self.risk_scores.append(risk_score)

        db.session.commit()
        print(f"Created {len(self.risk_scores)} risk scores.")

    def seed_alerts(self):
        print("Seeding alerts...")

        alerts_data = [
            {
                "business_id": self.businesses[0].id,
                "level": "warning",
                "message": "Cash flow projection shows 15% decrease for next month",
                "linked_forecast_id": self.forecasts[0].id,
                "resolved": False,
                "forecast_metadata": {"severity": "medium", "action_required": True},
            },
            {
                "business_id": self.businesses[1].id,
                "level": "info",
                "message": "Seasonal sales pattern detected - expected increase in Q2",
                "linked_forecast_id": self.forecasts[1].id,
                "resolved": True,
                "resolved_at": datetime.now() - timedelta(hours=2),
                "forecast_metadata": {"severity": "low", "action_required": False},
            },
            {
                "business_id": self.businesses[2].id,
                "level": "success",
                "message": "Revenue target exceeded by 12% this month",
                "linked_forecast_id": self.forecasts[2].id,
                "resolved": True,
                "resolved_at": datetime.now() - timedelta(days=1),
                "forecast_metadata": {"severity": "info", "action_required": False},
            },
            {
                "business_id": self.businesses[0].id,
                "level": "critical",
                "message": "Unusual transaction pattern detected - potential fraud",
                "linked_transaction_id": self.transactions[5].id,
                "resolved": False,
                "forecast_metadata": {
                    "severity": "high",
                    "action_required": True,
                    "auto_detected": True,
                },
            },
            {
                "business_id": self.businesses[1].id,
                "level": "warning",
                "message": "Inventory levels below optimal threshold",
                "resolved": False,
                "forecast_metadata": {"severity": "medium", "action_required": True},
            },
        ]

        for alert_data in alerts_data:
            alert = Alert(**alert_data)
            db.session.add(alert)
            self.alerts.append(alert)

        db.session.commit()
        print(f"Created {len(self.alerts)} alerts.")

    def seed_scenarios(self):
        print("Seeding scenarios...")

        scenarios_data = [
            {
                "business_id": self.businesses[0].id,
                "name": "Market Expansion Scenario",
                "params": {
                    "market_growth": 0.15,
                    "investment": 500000,
                    "timeline": "18_months",
                },
                "result_summary": {
                    "projected_roi": 0.25,
                    "break_even": "14_months",
                    "risk_level": "medium",
                },
                "run_by": self.users[1].id,  # John Doe
            },
            {
                "business_id": self.businesses[1].id,
                "name": "E-commerce Integration",
                "params": {
                    "online_channel_growth": 0.30,
                    "investment": 250000,
                    "timeline": "12_months",
                },
                "result_summary": {
                    "projected_roi": 0.40,
                    "break_even": "8_months",
                    "risk_level": "low",
                },
                "run_by": self.users[2].id,  # Jane Smith
            },
            {
                "business_id": self.businesses[2].id,
                "name": "Pricing Optimization",
                "params": {
                    "price_increase": 0.10,
                    "customer_retention": 0.85,
                    "timeline": "6_months",
                },
                "result_summary": {
                    "projected_roi": 0.18,
                    "break_even": "3_months",
                    "risk_level": "low",
                },
                "run_by": self.users[1].id,  # John Doe
            },
            {
                "business_id": self.businesses[0].id,
                "name": "Cost Reduction Initiative",
                "params": {
                    "cost_reduction_target": 0.20,
                    "areas": ["operations", "infrastructure"],
                    "timeline": "9_months",
                },
                "result_summary": {
                    "projected_savings": 300000,
                    "implementation_cost": 75000,
                    "risk_level": "low",
                },
                "run_by": self.users[1].id,  # John Doe
            },
        ]

        for scenario_data in scenarios_data:
            scenario = Scenario(**scenario_data)
            db.session.add(scenario)
            self.scenarios.append(scenario)

        db.session.commit()
        print(f"Created {len(self.scenarios)} scenarios.")

    def seed_api_keys(self):
        print("Seeding API keys...")

        api_keys_data = [
            {
                "business_id": self.businesses[0].id,
                "name": "TechCorp Production API",
                "key_hash": hashlib.sha256(
                    "tk_prod_techcorp_2024".encode()
                ).hexdigest(),
                "scopes": "read,write,admin",
                "revoked": False,
            },
            {
                "business_id": self.businesses[1].id,
                "name": "RetailCo Analytics API",
                "key_hash": hashlib.sha256(
                    "rk_analytics_retailco_2024".encode()
                ).hexdigest(),
                "scopes": "read",
                "revoked": False,
            },
            {
                "business_id": self.businesses[2].id,
                "name": "CloudTech Integration API",
                "key_hash": hashlib.sha256(
                    "ct_integration_cloudtech_2024".encode()
                ).hexdigest(),
                "scopes": "read,write",
                "revoked": False,
            },
            {
                "business_id": self.businesses[0].id,
                "name": "TechCorp Test API",
                "key_hash": hashlib.sha256(
                    "tk_test_techcorp_2024".encode()
                ).hexdigest(),
                "scopes": "read",
                "revoked": True,
            },
        ]

        for api_key_data in api_keys_data:
            api_key = APIKey(**api_key_data)
            db.session.add(api_key)
            self.api_keys.append(api_key)

        db.session.commit()
        print(f"Created {len(self.api_keys)} API keys.")

    def seed_all(self):
        print("Starting database seeding...")
        print("=" * 50)

        self.clear_all_tables()
        self.seed_users()
        self.seed_businesses()
        self.seed_categories()
        self.seed_transactions()
        self.seed_ocr_documents()
        self.seed_models()
        self.seed_model_runs()
        self.seed_forecasts()
        self.seed_risk_scores()
        self.seed_alerts()
        self.seed_scenarios()
        self.seed_api_keys()

        print("=" * 50)
        print("Database seeding completed successfully!")
        print(f"Summary:")
        print(f"- Users: {len(self.users)}")
        print(f"- Businesses: {len(self.businesses)}")
        print(f"- Categories: {len(self.categories)}")
        print(f"- Transactions: {len(self.transactions)}")
        print(f"- OCR Documents: {len(self.ocr_documents)}")
        print(f"- Models: {len(self.models)}")
        print(f"- Model Runs: {len(self.model_runs)}")
        print(f"- Forecasts: {len(self.forecasts)}")
        print(f"- Risk Scores: {len(self.risk_scores)}")
        print(f"- Alerts: {len(self.alerts)}")
        print(f"- Scenarios: {len(self.scenarios)}")
        print(f"- API Keys: {len(self.api_keys)}")


def run_seeder():
    from app import app

    with app.app_context():
        seeder = DatabaseSeeder()
        seeder.seed_all()


if __name__ == "__main__":
    run_seeder()
