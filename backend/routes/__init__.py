from .alert_routes import alert_bp
from .auth_routes import auth_bp
from .business_routes import business_bp
from .category_routes import category_bp
from .dashboard_routes import dashboard_bp
from .forecast_routes import forecast_bp
from .profile_routes import profile_bp
from .transaction_routes import transaction_bp
from .user_routes import user_bp


def register_routes(app):
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(business_bp, url_prefix="/businesses")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    app.register_blueprint(forecast_bp, url_prefix="/forecasts")
    app.register_blueprint(alert_bp, url_prefix="/alerts")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
