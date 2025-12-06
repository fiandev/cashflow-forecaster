# AI Cashflow Forecaster

A comprehensive financial forecasting platform that leverages AI/ML models to predict cash flow, analyze business risks, and provide actionable insights for business owners.

## 🚀 Features

- **AI-Powered Forecasting**: Multiple ML models (LSTM, ARIMA, Prophet) for accurate cash flow predictions
- **Risk Assessment**: Automated risk scoring and liquidity analysis
- **OCR Document Processing**: Extract financial data from invoices, receipts, and documents
- **Real-time Alerts**: Smart notifications for cash flow anomalies and opportunities
- **Scenario Planning**: What-if analysis for business decisions
- **Multi-business Support**: Manage multiple businesses under one account
- **Dashboard Analytics**: Comprehensive visualizations and metrics

## 🏗️ Architecture

### Backend (Flask + SQLAlchemy)
- **Framework**: Flask 3.0.0
- **Database**: SQLite with Alembic migrations
- **Authentication**: JWT-based auth with role-based permissions
- **AI/ML**: Support any models for forecasting
- **API**: RESTful API

### Frontend (React + TypeScript)
- **Framework**: React 18.3.1 with Vite
- **UI Library**: Radix UI + shadcn/ui components
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod validation

## 📁 Project Structure

```
ai-cashflow-forecaster/
├── backend/                     # Flask API server
│   ├── controllers/             # API endpoint handlers
│   │   ├── auth_controller.py
│   │   ├── business_controller.py
│   │   ├── forecast_controller.py
│   │   ├── transaction_controller.py
│   │   └── ...
│   ├── database/                # SQLite database file
│   ├── middleware/              # Authentication & permissions
│   ├── migrations/              # Database schema migrations
│   ├── models/                  # SQLAlchemy ORM models
│   ├── repositories/            # Data access layer
│   ├── routes/                  # API route definitions
│   ├── seeders/                 # Database seeding scripts
│   ├── services/                # Business logic & AI services
│   ├── utils/                   # Utility functions
│   ├── app.py                   # Flask application entry point
│   ├── models.py                # Database models definition
│   └── requirements.txt         # Python dependencies
│
├── frontend/                    # React frontend
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── ui/              # shadcn/ui components
│   │   │   └── ...              # Feature components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── lib/                 # Utility functions
│   │   ├── pages/               # Page components
│   │   ├── stores/              # Zustand state stores
│   │   ├── App.tsx              # Main app component
│   │   └── main.tsx             # App entry point
│   ├── package.json             # Node.js dependencies
│   └── vite.config.ts           # Vite configuration
│
├── essentials/                  # Documentation & diagrams
│   ├── database-schema.dbdiagram
│   └── postman_collection.json
│
├── docker-compose.yml           # Development environment
├── docker-compose.prod.yml      # Production environment
├── Dockerfile                   # Backend Docker image
├── Dockerfile.frontend          # Frontend Docker image
├── nginx.conf                   # Nginx configuration
├── docker.sh                    # Docker management script
└── README.md                    # This file
```

## 🔧 Prerequisites

- **Docker Engine**: v20.10+
- **Docker Compose**: v2.0+
- **Node.js**: v18+ (for local development)
- **Python**: v3.9+ (for local development)

## 🚀 Quick Start

### Development Environment

1. **Start services in background:**
   ```bash
   ./docker.sh up
   ```

2. **View logs:**
   ```bash
   ./docker.sh logs-follow
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:5000

4. **Stop services:**
   ```bash
   ./docker.sh down
   ```

### Production Environment

1. **Start production services:**
   ```bash
   ./docker.sh prod-up
   ```

2. **Access the application:**
   - **Application**: http://localhost (port 80)

3. **Stop production services:**
   ```bash
   ./docker.sh prod-down
   ```

## 🔑 Default Login Credentials

The application comes with pre-seeded data for testing:

### Admin Account
- **Email**: `admin@gmail.com`
- **Password**: `password`
- **Role**: System Administrator

### Business Owner Accounts
- **Email**: `user@gmail.com`
- **Password**: `password`
- **Role**: Business Owner
- **Businesses**: TechCorp Solutions, CloudTech Services

- **Email**: `jane.smith@gmail.com`
- **Password**: `password`
- **Role**: Business Owner
- **Businesses**: RetailCo Stores

### Sample Businesses
1. **TechCorp Solutions** (San Francisco, USD)
2. **RetailCo Stores** (Toronto, CAD)
3. **CloudTech Services** (New York, USD)

## 📊 Database Schema

The application uses the following main entities:

- **Users**: Authentication and user management
- **Businesses**: Multi-tenant business data
- **Transactions**: Financial transactions (income/expense)
- **Categories**: Transaction categorization
- **Forecasts**: AI-generated cash flow predictions
- **Models**: ML model configurations
- **RiskScores**: Risk assessment metrics
- **Alerts**: Smart notifications
- **OCRDocuments**: Processed financial documents
- **Scenarios**: What-if analysis results

## 🛠️ Available Commands

The `docker.sh` script provides comprehensive management:

### Basic Operations
- `up` - Start development services in background
- `up-dev` - Start development services in foreground
- `down` - Stop all services
- `logs` - View logs from all services
- `logs-follow` - View logs and follow output
- `build` - Build/rebuild service images
- `restart` - Restart all services
- `status` - Show container status

### Development Operations
- `exec-backend 'command'` - Execute command in backend container
- `exec-frontend 'command'` - Execute command in frontend container
- `shell-backend` - Start shell in backend container
- `shell-frontend` - Start shell in frontend container
- `tests` - Run backend tests

### Database Operations
- `db-backup` - Create SQLite database backup
- `db-restore file` - Restore from backup file
- `seed` - Seed database with sample data

### Production Operations
- `prod-up` - Start production services
- `prod-down` - Stop production services
- `prod-logs` - View production logs

### System Operations
- `clean` - Remove all containers, networks, and volumes

## 🔧 Environment Configuration

### Backend Environment Variables
```bash
# Database
DB_TYPE=sqlite
DB_PATH=database/database.db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# AI Services
OPENAI_API_KEY=your-openai-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend Environment Variables
```bash
# API
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000

# Features
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_SENTRY=false
```

## 🧪 Testing

### Backend Tests
```bash
./docker.sh exec-backend 'python -m pytest'
./docker.sh exec-backend 'python -m pytest tests/ -v'
```

### Frontend Tests
```bash
./docker.sh exec-frontend 'npm test'
./docker.sh exec-frontend 'npm run test:coverage'
```

## 📦 Local Development Setup

### Backend (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend (Node.js)
```bash
cd frontend
npm install
npm run dev
```

## 🗄️ Database Management

### Creating Migrations
```bash
./docker.sh exec-backend 'flask db migrate -m "migration message"'
```

### Applying Migrations
```bash
./docker.sh exec-backend 'flask db upgrade'
```

### Resetting Database
```bash
./docker.sh exec-backend 'python seed.py'
```

## 🚀 Production Deployment

### Using Docker Compose
```bash
# Build and deploy
./docker.sh prod-up

# View logs
./docker.sh prod-logs

# Scale services
docker-compose.prod.yml up -d --scale backend=3
```

### Manual Deployment
1. Build frontend: `npm run build`
2. Configure nginx: Update `nginx.conf`
3. Set environment variables
4. Run with gunicorn: `gunicorn -w 4 app:app`

## 🔍 API Documentation

### Authentication
All API endpoints require JWT authentication (except `/auth/login`).

```bash
# Login
POST /auth/login
{
  "email": "user@gmail.com",
  "password": "password"
}

# Get token (use in Authorization header)
Authorization: Bearer <jwt_token>
```

### Main Endpoints
- `GET /api/businesses` - List user businesses
- `GET /api/transactions` - List transactions
- `POST /api/forecasts` - Generate forecast
- `GET /api/alerts` - List alerts
- `POST /api/ocr/upload` - Upload document for OCR

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**:
   - Ensure ports 3000, 5000, and 80 are available
   - Use `./docker.sh clean` to reset

2. **Database connection errors**:
   - Check if database volume exists: `docker volume ls`
   - Re-seed database: `./docker.sh seed`

3. **Frontend not connecting to backend**:
   - Verify API URL in frontend environment
   - Check CORS configuration in backend

4. **AI services not working**:
   - Verify API keys in environment variables
   - Check service logs for errors

### Health Checks
```bash
# Backend health
curl http://localhost:5000/health

# Frontend availability
curl http://localhost:3000

# Database connectivity
./docker.sh exec-backend 'python -c "from app import app; print(\"DB OK\")"'
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit changes: `git commit -m "Add feature"`
5. Push to branch: `git push origin feature-name`
6. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the logs using `./docker.sh logs-follow`


---


> **Built with ❤️ by [Fiandev](https://fiandev.com) and [ErRickow](https://github.com/ErRickow)**