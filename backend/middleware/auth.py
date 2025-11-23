from flask import request, jsonify, g
from functools import wraps
import jwt
from datetime import datetime, timedelta
from models import User, APIKey
import hashlib
import hmac


class AuthenticationMiddleware:
    @staticmethod
    def generate_token(user_id, secret_key, expires_in_hours=24):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def verify_token(token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def hash_api_key(api_key):
        return hashlib.sha256(api_key.encode()).hexdigest()

    @staticmethod
    def verify_api_key(api_key_hash, provided_key):
        provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
        return hmac.compare_digest(api_key_hash, provided_hash)


def authenticate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        api_key_header = request.headers.get("X-API-Key")

        user = None
        auth_method = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = AuthenticationMiddleware.verify_token(
                token, "your-secret-key-here"
            )

            if payload:
                user = User.query.get(payload["user_id"])
                auth_method = "token"

        elif api_key_header:
            api_key = APIKey.query.filter_by(
                key_hash=AuthenticationMiddleware.hash_api_key(api_key_header),
                revoked=False,
            ).first()

            if api_key:
                business = api_key.business
                if business and business.owner:
                    user = business.owner
                    auth_method = "api_key"
                    g.api_key = api_key
                    g.scopes = api_key.scopes.split(",") if api_key.scopes else []

        if not user:
            return jsonify({"error": "Authentication required"}), 401

        g.current_user = user
        g.auth_method = auth_method

        return f(*args, **kwargs)

    return decorated_function


def optional_authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        api_key_header = request.headers.get("X-API-Key")

        user = None
        auth_method = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = AuthenticationMiddleware.verify_token(
                token, "your-secret-key-here"
            )

            if payload:
                user = User.query.get(payload["user_id"])
                auth_method = "token"

        elif api_key_header:
            api_key = APIKey.query.filter_by(
                key_hash=AuthenticationMiddleware.hash_api_key(api_key_header),
                revoked=False,
            ).first()

            if api_key:
                business = api_key.business
                if business and business.owner:
                    user = business.owner
                    auth_method = "api_key"
                    g.api_key = api_key
                    g.scopes = api_key.scopes.split(",") if api_key.scopes else []

        g.current_user = user
        g.auth_method = auth_method

        return f(*args, **kwargs)

    return decorated_function
