from functools import wraps
from flask import request, jsonify, g
from .auth import authenticate_request, optional_authenticate
from .permissions import (
    require_permission,
    require_role,
    business_owner_required,
    self_or_admin_required,
)


def rate_limit(max_requests=100, window_seconds=3600):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, "rate_limit_store"):
                g.rate_limit_store = {}

            client_ip = request.remote_addr
            current_time = int(time.time())
            window_start = current_time - window_seconds

            if client_ip not in g.rate_limit_store:
                g.rate_limit_store[client_ip] = []

            g.rate_limit_store[client_ip] = [
                timestamp
                for timestamp in g.rate_limit_store[client_ip]
                if timestamp > window_start
            ]

            if len(g.rate_limit_store[client_ip]) >= max_requests:
                return jsonify({"error": "Rate limit exceeded"}), 429

            g.rate_limit_store[client_ip].append(current_time)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_json(required_fields=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400

            data = request.get_json()

            if not data:
                return jsonify({"error": "No JSON data provided"}), 400

            if required_fields:
                missing_fields = [
                    field for field in required_fields if field not in data
                ]
                if missing_fields:
                    return jsonify(
                        {
                            "error": "Missing required fields",
                            "missing_fields": missing_fields,
                        }
                    ), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        import logging

        logger = logging.getLogger(__name__)

        user_info = None
        if hasattr(g, "current_user") and g.current_user:
            user_info = f"User: {g.current_user.email} (Role: {g.current_user.role})"

        logger.info(f"{request.method} {request.path} - {user_info}")

        return f(*args, **kwargs)

    return decorated_function


def cors(allowed_origins=None, allowed_methods=None, allowed_headers=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "OPTIONS":
                response = jsonify({"status": "ok"})
            else:
                response = f(*args, **kwargs)

            if allowed_origins:
                origin = request.headers.get("Origin")
                if origin in allowed_origins or "*" in allowed_origins:
                    response.headers["Access-Control-Allow-Origin"] = origin
            else:
                response.headers["Access-Control-Allow-Origin"] = "*"

            if allowed_methods:
                response.headers["Access-Control-Allow-Methods"] = ", ".join(
                    allowed_methods
                )
            else:
                response.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, OPTIONS"
                )

            if allowed_headers:
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    allowed_headers
                )
            else:
                response.headers["Access-Control-Allow-Headers"] = (
                    "Content-Type, Authorization, X-API-Key"
                )

            return response

        return decorated_function

    return decorator


class Decorators:
    auth = authenticate_request
    optional_auth = optional_authenticate
    permission = require_permission
    role = require_role
    business_owner = business_owner_required
    self_or_admin = self_or_admin_required
    rate_limit = rate_limit
    validate_json = validate_json
    log = log_request
    cors = cors


def secure_endpoint(
    permission=None,
    role=None,
    require_business_owner=False,
    require_self_or_admin=False,
    rate_limit_max=None,
    validate_fields=None,
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            decorators = []

            decorators.append(authenticate_request)

            if permission:
                decorators.append(require_permission(permission))

            if role:
                decorators.append(require_role(role))

            if require_business_owner:
                decorators.append(business_owner_required)

            if require_self_or_admin:
                decorators.append(self_or_admin_required)

            if rate_limit_max:
                decorators.append(rate_limit(rate_limit_max))

            if validate_fields:
                decorators.append(validate_json(validate_fields))

            decorated = f
            for dec in reversed(decorators):
                decorated = dec(decorated)

            return decorated(*args, **kwargs)

        return decorated_function

    return decorator


import time
