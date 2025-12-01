from flask import request, jsonify, g
from functools import wraps
from models import Business, User, Transaction

class PermissionPolicies:
    ROLE_PERMISSIONS = {
        "admin": [
            "users:read",
            "users:write",
            "users:delete",
            "businesses:read",
            "businesses:write",
            "businesses:delete",
            "categories:read",
            "categories:write",
            "categories:delete",
            "transactions:read",
            "transactions:write",
            "transactions:delete",
            "ocr_documents:read",
            "ocr_documents:write",
            "ocr_documents:delete",
            "models:read",
            "models:write",
            "models:delete",
            "model_runs:read",
            "model_runs:write",
            "model_runs:delete",
            "forecasts:read",
            "forecasts:write",
            "forecasts:delete",
            "risk_scores:read",
            "risk_scores:write",
            "risk_scores:delete",
            "alerts:read",
            "alerts:write",
            "alerts:delete",
            "scenarios:read",
            "scenarios:write",
            "scenarios:delete",
            "api_keys:read",
            "api_keys:write",
            "api_keys:delete",
        ],
        "owner": [
            "businesses:read",
            "businesses:write",
            "categories:read",
            "categories:write",
            "categories:delete",
            "transactions:read",
            "transactions:write",
            "transactions:delete",
            "ocr_documents:read",
            "ocr_documents:write",
            "ocr_documents:delete",
            "models:read",
            "models:write",
            "models:delete",
            "model_runs:read",
            "model_runs:write",
            "model_runs:delete",
            "forecasts:read",
            "forecasts:write",
            "forecasts:delete",
            "risk_scores:read",
            "risk_scores:write",
            "risk_scores:delete",
            "alerts:read",
            "alerts:write",
            "alerts:delete",
            "scenarios:read",
            "scenarios:write",
            "scenarios:delete",
            "api_keys:read",
            "api_keys:write",
            "api_keys:delete",
        ],
        "manager": [
            "categories:read",
            "categories:write",
            "transactions:read",
            "transactions:write",
            "ocr_documents:read",
            "ocr_documents:write",
            "models:read",
            "models:write",
            "model_runs:read",
            "model_runs:write",
            "forecasts:read",
            "forecasts:write",
            "risk_scores:read",
            "risk_scores:write",
            "alerts:read",
            "alerts:write",
            "scenarios:read",
            "scenarios:write",
        ],
        "analyst": [
            "categories:read",
            "transactions:read",
            "ocr_documents:read",
            "models:read",
            "model_runs:read",
            "forecasts:read",
            "risk_scores:read",
            "alerts:read",
            "scenarios:read",
        ],
        "viewer": [
            "categories:read",
            "transactions:read",
            "forecasts:read",
            "risk_scores:read",
            "alerts:read",
        ],
    }

    API_KEY_SCOPES = {
        "read": [
            "categories:read",
            "transactions:read",
            "ocr_documents:read",
            "models:read",
            "model_runs:read",
            "forecasts:read",
            "risk_scores:read",
            "alerts:read",
            "scenarios:read",
        ],
        "write": [
            "categories:write",
            "transactions:write",
            "ocr_documents:write",
            "models:write",
            "model_runs:write",
            "forecasts:write",
            "risk_scores:write",
            "alerts:write",
            "scenarios:write",
        ],
        "delete": [
            "categories:delete",
            "transactions:delete",
            "ocr_documents:delete",
            "models:delete",
            "model_runs:delete",
            "forecasts:delete",
            "risk_scores:delete",
            "alerts:delete",
            "scenarios:delete",
        ],
        "admin": [
            "businesses:read",
            "businesses:write",
            "businesses:delete",
            "api_keys:read",
            "api_keys:write",
            "api_keys:delete",
        ],
    }

    @classmethod
    def get_user_permissions(cls, user):
        if not user:
            return []

        role = user.role or "viewer"
        return cls.ROLE_PERMISSIONS.get(role, [])

    @classmethod
    def get_api_key_permissions(cls, scopes):
        if not scopes:
            return []

        permissions = []
        for scope in scopes:
            if scope in cls.API_KEY_SCOPES:
                permissions.extend(cls.API_KEY_SCOPES[scope])

        return list(set(permissions))

    @classmethod
    def has_permission(cls, user, permission, business_id=None):
        if not user:
            return False

        user_permissions = cls.get_user_permissions(user)

        if permission in user_permissions:
            if business_id and user.role != "admin":
                business = Business.query.get(business_id)
                if business and business.owner_id != user.id:
                    return False
            return True

        return False

    @classmethod
    def has_api_key_permission(cls, scopes, permission, business_id=None):
        if not scopes:
            return False

        api_permissions = cls.get_api_key_permissions(scopes)

        if permission in api_permissions:
            return True

        return False


def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, "current_user") or not g.current_user:
                return jsonify({"error": "Authentication required"}), 401

            business_id = kwargs.get("business_id") or request.view_args.get(
                "business_id"
            )

            if g.auth_method == "api_key":
                scopes = getattr(g, "scopes", [])
                if not PermissionPolicies.has_api_key_permission(
                    scopes, permission, business_id
                ):
                    return jsonify({"error": "Insufficient permissions"}), 403
            else:
                if not PermissionPolicies.has_permission(
                    g.current_user, permission, business_id
                ):
                    return jsonify({"error": "Insufficient permissions"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, "current_user") or not g.current_user:
                return jsonify({"error": "Authentication required"}), 401

            if g.current_user.role != role:
                return jsonify({"error": f"{role} role required"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def business_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        business_id = kwargs.get("business_id") or request.view_args.get("business_id")

        if not business_id:
            return jsonify({"error": "Business ID required"}), 400

        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "Business owner access required"}), 403

        g.current_business = business
        return f(*args, **kwargs)

    return decorated_function


def transaction_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        transaction_id = kwargs.get("transaction_id") or request.view_args.get("transaction_id")

        if not transaction_id:
            return f(*args, **kwargs)  # Allow for create operations that don't have transaction_id yet

        # Get the transaction to check ownership
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        # Allow access if user is admin or owner of the business that owns the transaction
        if g.current_user.role != "admin" and transaction.business.owner_id != g.current_user.id:
            return jsonify({"error": "Transaction access denied"}), 403

        g.current_transaction = transaction
        return f(*args, **kwargs)

    return decorated_function


def self_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        user_id = kwargs.get("user_id") or request.view_args.get("user_id")

        if (
            user_id
            and str(user_id) != str(g.current_user.id)
            and g.current_user.role != "admin"
        ):
            return jsonify({"error": "Self or admin access required"}), 403

        return f(*args, **kwargs)

    return decorated_function

def business_owner_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "current_user") or not g.current_user:
            return jsonify({"error": "Authentication required"}), 401

        business_id = kwargs.get("business_id") or request.view_args.get("business_id")

        if not business_id:
            if g.current_user.role == "admin":
                return f(*args, **kwargs)
            else:
                # Attempt to infer business_id for non-admin users if not provided
                owned_businesses = Business.query.filter_by(owner_id=g.current_user.id).all()
                if len(owned_businesses) == 1:
                    business_id = owned_businesses[0].id
                else:
                    return jsonify({"error": "Business ID required"}), 400

        business = Business.query.get(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404

        if business.owner_id != g.current_user.id and g.current_user.role != "admin":
            return jsonify({"error": "Business owner access required"}), 403

        g.current_business = business
        return f(*args, **kwargs)

    return decorated_function