import os

from dotenv import load_dotenv
from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_cors import CORS

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "database", "database.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Configure CORS to allow all origins
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


from models import db

db.init_app(app)
migrate = Migrate(app, db)

from controllers.alert_controller import AlertController
from controllers.business_controller import BusinessController
from controllers.category_controller import CategoryController
from controllers.dashboard_controller import DashboardController
from controllers.forecast_controller import ForecastController
from controllers.transaction_controller import TransactionController
from controllers.user_controller import UserController
from middleware import require_permission, self_or_admin_required, validate_json
from middleware.auth import AuthenticationMiddleware, authenticate_request
from middleware.permissions import require_role, transaction_access_required
from models import User
from utils.crypto import hash_password


# User routes
@app.route("/api/users", methods=["POST"])
@authenticate_request
@require_role("admin")
def create_user():
    return UserController().store()


@app.route("/api/users", methods=["GET"])
@authenticate_request
@require_role("admin")
@require_permission("users:read")
def get_users():
    return UserController().index()


@app.route("/api/users/<int:user_id>", methods=["GET"])
@authenticate_request
@self_or_admin_required
def get_user(user_id):
    return UserController().show(user_id)


@app.route("/api/users/<int:user_id>", methods=["PUT"])
@authenticate_request
@self_or_admin_required
@validate_json()
def update_user(user_id):
    return UserController().update(user_id)


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@authenticate_request
@self_or_admin_required
def delete_user(user_id):
    return UserController().destroy(user_id)


# Additional User Routes
@app.route("/api/users/search", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def search_users():
    """Search users"""
    return UserController().search_users()


@app.route("/api/users/role/<string:role>", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def get_users_by_role(role):
    """Get users by role"""
    return UserController().get_users_by_role(role)


# Business routes
business_controller = BusinessController()


@app.route("/api/businesses", methods=["GET"])
def get_businesses():
    return business_controller.get_businesses()


@app.route("/api/businesses/<int:business_id>", methods=["GET"])
def get_business(business_id):
    return business_controller.get_business(business_id)


@app.route("/api/businesses/<int:business_id>", methods=["PUT"])
def update_business(business_id):
    return business_controller.update_business(business_id)


@app.route("/api/businesses/<int:business_id>", methods=["DELETE"])
def delete_business(business_id):
    return business_controller.delete_business(business_id)


# Transaction routes
@app.route("/api/transactions", methods=["POST"])
@authenticate_request
@transaction_access_required
def create_transaction():
    return TransactionController.create_transaction()


@app.route("/api/transactions", methods=["GET"])
@authenticate_request
@transaction_access_required
def get_transactions():
    return TransactionController.get_transactions()


@app.route("/api/transactions/<int:transaction_id>", methods=["GET"])
@authenticate_request
@transaction_access_required
def get_transaction(transaction_id):
    return TransactionController.get_transaction(transaction_id)


@app.route("/api/transactions/<int:transaction_id>", methods=["PUT"])
@authenticate_request
@transaction_access_required
def update_transaction(transaction_id):
    return TransactionController.update_transaction(transaction_id)


@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
@authenticate_request
@transaction_access_required
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)


# Forecast routes
@app.route("/api/forecasts", methods=["POST"])
def create_forecast():
    return ForecastController.create_forecast()


@app.route("/api/forecasts", methods=["GET"])
def get_forecasts():
    return ForecastController.get_forecasts()


@app.route("/api/forecasts/<int:forecast_id>", methods=["GET"])
def get_forecast(forecast_id):
    return ForecastController.get_forecast(forecast_id)


@app.route("/api/forecasts/<int:forecast_id>", methods=["PUT"])
def update_forecast(forecast_id):
    return ForecastController.update_forecast(forecast_id)


@app.route("/api/forecasts/<int:forecast_id>", methods=["DELETE"])
def delete_forecast(forecast_id):
    return ForecastController.delete_forecast(forecast_id)


# Alert routes
@app.route("/api/alerts", methods=["POST"])
@authenticate_request
@require_role("admin")
def create_alert():
    return AlertController.create_alert()


@app.route("/api/alerts", methods=["GET"])
@authenticate_request
def get_alerts():
    return AlertController.get_alerts()


@app.route("/api/alerts/<int:alert_id>", methods=["GET"])
@authenticate_request
def get_alert(alert_id):
    return AlertController.get_alert(alert_id)


@app.route("/api/alerts/<int:alert_id>", methods=["PUT"])
@authenticate_request
@require_role("admin")
def update_alert(alert_id):
    return AlertController.update_alert(alert_id)


@app.route("/api/alerts/<int:alert_id>", methods=["DELETE"])
@authenticate_request
@require_role("admin")
def delete_alert(alert_id):
    return AlertController.delete_alert(alert_id)


# Auth routes
@app.route("/api/auth/login", methods=["POST"])
@validate_json(["email", "password"])
def login():
    """Login user and return JWT token"""
    from flask import jsonify, request

    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    hashed_password = hash_password(data["password"])

    if not user or user.password != hashed_password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = AuthenticationMiddleware.generate_token(user.id, os.getenv("SECRET_KEY"))

    return jsonify(
        {
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            },
        }
    )


@app.route("/api/auth/register", methods=["POST"])
@validate_json(["email", "password", "name"])
def register():
    """Register new user"""
    return UserController().bussinessOwnerStore()


@app.route("/api/auth/me", methods=["GET"])
@authenticate_request
def get_current_user():
    """Get current user info (requires auth token)"""
    return UserController().profile()


@app.route("/api/auth/business/register", methods=["POST"])
@authenticate_request
def register_business():
    """Register new business for the authenticated user"""
    return business_controller.create_business()


# Profile routes
@app.route("/api/profile/", methods=["GET"])
@authenticate_request
def get_profile():
    """Get current user profile"""
    return UserController().profile()


@app.route("/api/profile/", methods=["PUT"])
@authenticate_request
@validate_json()
def update_profile():
    """Update current user profile"""
    return UserController().update_profile()


@app.route("/api/profile/change-password", methods=["POST"])
@authenticate_request
@validate_json(["current_password", "new_password"])
def change_password():
    """Change current user password"""
    return UserController().change_password()


# Category routes
@app.route("/api/categories/", methods=["POST"])
@authenticate_request
def create_category():
    return CategoryController.create_category()


@app.route("/api/categories/", methods=["GET"])
@authenticate_request
def get_categories():
    return CategoryController.get_categories()


@app.route("/api/categories/<int:category_id>", methods=["GET"])
@authenticate_request
def get_category(category_id):
    return CategoryController.get_category(category_id)


@app.route("/api/categories/<int:category_id>", methods=["PUT"])
@authenticate_request
def update_category(category_id):
    return CategoryController.update_category(category_id)


@app.route("/api/categories/<int:category_id>", methods=["DELETE"])
@authenticate_request
def delete_category(category_id):
    return CategoryController.delete_category(category_id)


# Dashboard routes
@app.route("/api/dashboard/metrics", methods=["GET"])
@authenticate_request
def get_dashboard_metrics():
    return DashboardController.get_metrics()


@app.route("/")
def index():
    return {"message": "AI Cashflow Forecaster API"}


@app.route("/api/test")
def test():
    return {"message": "AI Cashflow Forecaster API works"}


if __name__ == "__main__":
    app.run(debug=os.getenv("APP_ENV", "development") != "production")
