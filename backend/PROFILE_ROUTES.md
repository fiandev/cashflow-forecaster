# API Routes Documentation

## 📍 Profile Routes Location

The profile routes are now properly organized in the Flask application structure:

### **File:** `/home/fiandev/projects/ai-cashflow-forecaster/backend/routes/profile_routes.py`

### **Registered in:** `/home/fiandev/projects/ai-cashflow-forecaster/backend/routes/__init__.py`

## 🚀 Available Profile Endpoints

| Method | Endpoint | Description | Authentication |
|---------|-----------|-------------|----------------|
| `GET` | `/api/profile/` | Get current user profile | Required |
| `PUT` | `/api/profile/` | Update current user profile | Required |
| `POST` | `/api/profile/change-password` | Change password | Required |

## 🔐 Authentication Routes

| Method | Endpoint | Description | Authentication |
|---------|-----------|-------------|----------------|
| `POST` | `/api/auth/login` | Login and get JWT token | None |
| `POST` | `/api/auth/register` | Register new user | None |
| `GET` | `/api/auth/me` | Get current user info | Required |

## 📋 Usage Examples

### **Login**
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"email": "john.doe@techcorp.com", "password": "password"}' \
     http://localhost:5000/api/auth/login
```

### **Get Profile**
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/api/profile/
```

### **Update Profile**
```bash
curl -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated Doe"}' \
     http://localhost:5000/api/profile/
```

### **Change Password**
```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"current_password": "oldpass", "new_password": "newpass"}' \
     http://localhost:5000/api/profile/change-password
```

## 🏗️ App Structure

```
backend/
├── app.py                    # Main Flask app
├── routes/
│   ├── __init__.py           # Route registration
│   ├── auth_routes.py        # Authentication routes
│   ├── profile_routes.py      # Profile routes ⭐
│   ├── user_routes.py        # User management
│   ├── business_routes.py     # Business management
│   ├── transaction_routes.py  # Transaction management
│   ├── forecast_routes.py     # Forecast management
│   └── alert_routes.py       # Alert management
├── controllers/              # Controllers with repositories
├── repositories/             # Repository pattern
├── middleware/              # Auth & permissions
└── models.py                # Database models
```

The profile routes are now properly organized in the Flask application structure at `/api/profile/`!