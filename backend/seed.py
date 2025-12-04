#!/usr/bin/env python3

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeders.database_seeder import run_seeder


def main():
    print("🌱 Database Seeder")
    print("=" * 40)
    print("This script will populate your database with sample data.")
    print("⚠️  WARNING: This will delete all existing data!")
    print()

    confirm = input("Are you sure you want to continue? (yes/no): ").lower().strip()

    if confirm not in ["yes", "y"]:
        print("❌ Seeding cancelled.")
        return

    print()
    print("🚀 Starting database seeding...")

    try:
        run_seeder()
        print()
        print("✅ Database seeding completed successfully!")
        print()
        print("📊 Sample data created:")
        print("   👤 5 Users with different roles (admin, owner, manager, analyst)")
        print("   🏢 3 Businesses (TechCorp, RetailCo, CloudTech)")
        print("   📁 10 Categories (income/expense types)")
        print("   💰 45+ Transactions (realistic cash flow data)")
        print("   📄 4 OCR Documents (invoices, receipts)")
        print("   🤖 4 ML Models (LSTM, ARIMA, Prophet, Isolation Forest)")
        print("   🔄 4 Model Runs (training executions)")
        print("   📈 4 Forecasts (cash flow predictions)")
        print("   ⚠️  4 Risk Scores (liquidity, volatility metrics)")
        print("   🔔 5 Alerts (warnings, info, critical)")
        print("   🎯 4 Scenarios (business what-if analyses)")
        print("   🔑 4 API Keys (production, analytics, integration)")
        print()
        print("🔐 Test Credentials:")
        print("   Admin: admin@cashflow.com")
        print("   Owner: john.doe@techcorp.com")
        print("   Owner: jane.smith@retailco.com")
        print()
        print("🔑 Test API Keys:")
        print("   TechCorp: tk_prod_techcorp_2024")
        print("   RetailCo: rk_analytics_retailco_2024")
        print("   CloudTech: ct_integration_cloudtech_2024")

    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()