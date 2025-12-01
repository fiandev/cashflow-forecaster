# Basic tests for backend
import pytest
from unittest.mock import patch


def test_app_import():
    """Test that the main app can be imported without errors."""
    try:
        from app import app
        assert app is not None
        print("Successfully imported app")
    except ImportError as e:
        print(f"Failed to import app: {e}")
        assert False, f"Import error: {e}"


def test_models_import():
    """Test that models can be imported."""
    try:
        from models import User, Business, Category, Transaction, OCRDocument, Model, ModelRun, Forecast, RiskScore, Alert, Scenario, APIKey
        print("Successfully imported all models")

        # Test that we can instantiate a User model (without DB connection)
        user = User(email="test@example.com", password="password123", name="Test User")
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        print("Successfully instantiated User model")
    except ImportError as e:
        print(f"Could not import models: {e}")
        assert False, f"Import error: {e}"


def test_database_connection_import():
    """Test that database connection can be imported."""
    try:
        from models import db
        print("Successfully imported database connection")
    except ImportError as e:
        print(f"Could not import database connection: {e}")
        assert False, f"Import error: {e}"