# API Routes for User Profile and Authentication

## Authentication
- `POST /auth/login` - Login user and get JWT token

## User Profile
- `GET /profile` - Get current user profile with businesses, scenarios, and permissions
- `PUT /profile` - Update current user profile (name, email)
- `POST /profile/change-password` - Change current user password

## User Management
- `GET /users` - Get all users (requires users:read permission)
- `POST /users` - Create new user
- `GET /users/<id>` - Get specific user (self or admin)
- `PUT /users/<id>` - Update user (self or admin)
- `DELETE /users/<id>` - Delete user (admin only)
- `GET /users/search?q=query` - Search users (requires users:read permission)
- `GET /users/role/<role>` - Get users by role (requires users:read permission)

## Business Management
- `GET /businesses` - Get all businesses (requires businesses:read permission)
- `POST /businesses` - Create new business (requires businesses:write permission)
- `GET /businesses/<id>` - Get specific business (requires businesses:read permission)
- `PUT /businesses/<id>` - Update business (business owner only)
- `DELETE /businesses/<id>` - Delete business (business owner only)
- `GET /my-businesses` - Get current user's businesses
- `GET /businesses/search?q=query` - Search businesses
- `GET /businesses/country/<country>` - Get businesses by country
- `GET /businesses/city/<city>` - Get businesses by city
- `GET /businesses/currency/<currency>` - Get businesses by currency
- `GET /businesses/<id>/details` - Get business with all related data
- `PUT /businesses/<id>/settings` - Update business settings

## Profile Response Example

```json
{
  "id": 1,
  "email": "john.doe@techcorp.com",
  "name": "John Doe",
  "role": "owner",
  "created_at": "2024-01-15T10:30:00",
  "last_login": "2024-01-23T14:20:00",
  "businesses": [
    {
      "id": 1,
      "name": "TechCorp Solutions",
      "country": "United States",
      "city": "San Francisco",
      "currency": "USD",
      "created_at": "2024-01-15T11:00:00"
    }
  ],
  "scenarios": [
    {
      "id": 1,
      "name": "Market Expansion Scenario",
      "created_at": "2024-01-20T09:15:00"
    }
  ],
  "permissions": [
    "businesses:read",
    "businesses:write",
    "categories:read",
    "categories:write",
    "categories:delete",
    "transactions:read",
    "transactions:write",
    "transactions:delete",
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
    "api_keys:delete"
  ],
  "auth_method": "token"
}
```

## Usage Examples

### Get Profile
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/profile
```

### Update Profile
```bash
curl -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated Doe"}' \
     http://localhost:5000/profile
```

### Change Password
```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"current_password": "oldpass", "new_password": "newpass"}' \
     http://localhost:5000/profile/change-password
```

### Get My Businesses
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/my-businesses
```

### Search Users
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/users/search?q=john
```