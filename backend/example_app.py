from flask import Flask, request, jsonify
from models import db
from controllers import *
from middleware import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key-here"

db.init_app(app)


@app.route("/auth/login", methods=["POST"])
@validate_json(["email", "password"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or user.password_hash != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = AuthenticationMiddleware.generate_token(user.id, app.config["SECRET_KEY"])

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


@app.route("/profile", methods=["GET"])
@authenticate_request
def get_profile():
    """Get current user profile"""
    return UserController().profile()


@app.route("/profile", methods=["PUT"])
@authenticate_request
@validate_json()
def update_profile():
    """Update current user profile"""
    return UserController().update_profile()


@app.route("/profile/change-password", methods=["POST"])
@authenticate_request
@validate_json(["current_password", "new_password"])
def change_password():
    """Change current user password"""
    return UserController().change_password()


@app.route("/users/search", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def search_users():
    """Search users"""
    return UserController().search_users()


@app.route("/users/role/<string:role>", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def get_users_by_role(role):
    """Get users by role"""
    return UserController().get_users_by_role(role)


@app.route("/users", methods=["GET"])
@authenticate_request
@require_permission("users:read")
def get_users():
    return UserController().index()


@app.route("/users", methods=["POST"])
@validate_json(["email", "password_hash"])
def create_user():
    return UserController().store()


@app.route("/users/<int:user_id>", methods=["GET"])
@authenticate_request
@self_or_admin_required
def get_user(user_id):
    return UserController().show(user_id)


@app.route("/users/<int:user_id>", methods=["PUT"])
@authenticate_request
@self_or_admin_required
@validate_json()
def update_user(user_id):
    return UserController().update(user_id)


@app.route("/users/<int:user_id>", methods=["DELETE"])
@authenticate_request
@require_role("admin")
def delete_user(user_id):
    return UserController().destroy(user_id)


@app.route("/businesses", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def get_businesses():
    return BusinessController().index()


@app.route("/businesses", methods=["POST"])
@authenticate_request
@require_permission("businesses:write")
@validate_json(["name", "currency", "owner_id"])
def create_business():
    return BusinessController().store()


@app.route("/businesses/<int:business_id>", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def get_business(business_id):
    return BusinessController().show(business_id)


@app.route("/businesses/<int:business_id>", methods=["PUT"])
@authenticate_request
@business_owner_required
@validate_json()
def update_business(business_id):
    return BusinessController().update(business_id)


@app.route("/businesses/<int:business_id>", methods=["DELETE"])
@authenticate_request
@business_owner_required
def delete_business(business_id):
    return BusinessController().destroy(business_id)


@app.route("/my-businesses", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def my_businesses():
    """Get current user's businesses"""
    return BusinessController().my_businesses()


@app.route("/businesses/search", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def search_businesses():
    """Search businesses"""
    return BusinessController().search()


@app.route("/businesses/country/<string:country>", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def businesses_by_country(country):
    """Get businesses by country"""
    return BusinessController().by_country(country)


@app.route("/businesses/city/<string:city>", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def businesses_by_city(city):
    """Get businesses by city"""
    return BusinessController().by_city(city)


@app.route("/businesses/currency/<string:currency>", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def businesses_by_currency(currency):
    """Get businesses by currency"""
    return BusinessController().by_currency(currency)


@app.route("/businesses/<int:business_id>/details", methods=["GET"])
@authenticate_request
@require_permission("businesses:read")
def business_details(business_id):
    """Get business with all details"""
    return BusinessController().with_details(business_id)


@app.route("/businesses/<int:business_id>/settings", methods=["PUT"])
@authenticate_request
@business_owner_required
@validate_json()
def update_business_settings(business_id):
    """Update business settings"""
    return BusinessController().update_settings(business_id)


@app.route("/businesses/<int:business_id>/categories", methods=["GET"])
@authenticate_request
@require_permission("categories:read")
def get_business_categories(business_id):
    return CategoryController.get_categories_by_business(business_id)


@app.route("/businesses/<int:business_id>/transactions", methods=["GET"])
@authenticate_request
@require_permission("transactions:read")
def get_business_transactions(business_id):
    return TransactionController.get_transactions_by_business(business_id)


@app.route("/transactions", methods=["POST"])
@authenticate_request
@require_permission("transactions:write")
@validate_json(["business_id", "date", "amount", "direction"])
def create_transaction():
    return TransactionController.create_transaction()


@app.route("/transactions/<int:transaction_id>", methods=["GET"])
@authenticate_request
@require_permission("transactions:read")
def get_transaction(transaction_id):
    return TransactionController.get_transaction(transaction_id)


@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
@authenticate_request
@require_permission("transactions:write")
@validate_json()
def update_transaction(transaction_id):
    return TransactionController.update_transaction(transaction_id)


@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
@authenticate_request
@require_permission("transactions:delete")
def delete_transaction(transaction_id):
    return TransactionController.delete_transaction(transaction_id)


@app.route("/forecasts", methods=["GET"])
@authenticate_request
@require_permission("forecasts:read")
def get_forecasts():
    return ForecastController.get_forecasts()


@app.route("/forecasts", methods=["POST"])
@authenticate_request
@require_permission("forecasts:write")
@validate_json(["business_id", "granularity", "period_start", "period_end"])
def create_forecast():
    return ForecastController.create_forecast()


@app.route("/forecasts/<int:forecast_id>", methods=["GET"])
@authenticate_request
@require_permission("forecasts:read")
def get_forecast(forecast_id):
    return ForecastController.get_forecast(forecast_id)


@app.route("/alerts", methods=["GET"])
@authenticate_request
@require_permission("alerts:read")
def get_alerts():
    return AlertController.get_alerts()


@app.route("/alerts", methods=["POST"])
@authenticate_request
@require_permission("alerts:write")
@validate_json(["business_id", "level", "message"])
def create_alert():
    return AlertController.create_alert()


@app.route("/alerts/<int:alert_id>/resolve", methods=["POST"])
@authenticate_request
@require_permission("alerts:write")
def resolve_alert(alert_id):
    return AlertController.resolve_alert(alert_id)


@app.route("/api-keys", methods=["POST"])
@authenticate_request
@business_owner_required
@validate_json(["business_id"])
def create_api_key():
    return APIKeyController.create_api_key()


@app.route("/api-keys", methods=["GET"])
@authenticate_request
@require_permission("api_keys:read")
def get_api_keys():
    return APIKeyController.get_api_keys()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "timestamp": "2025-01-23T12:00:00Z"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
