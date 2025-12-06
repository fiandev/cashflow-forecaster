# AI Cashflow Forecaster

[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A comprehensive financial forecasting platform that leverages AI/ML models to predict cash flow, analyze business risks, and provide actionable insights for business owners. Built for modern financial planning with intuitive dashboards, automated data processing, and powerful predictive analytics.

## ✨ Key Features

### 🧠 AI-Powered Insights
- **Predictive Forecasting**: Multiple ML models (LSTM, ARIMA, Prophet) for accurate cash flow predictions
- **Risk Assessment**: Automated risk scoring and liquidity analysis with probability modeling
- **AI Document Processing**: OCR technology to extract financial data from invoices, receipts, and documents
- **Smart Recommendations**: Actionable insights based on historical trends and market patterns

### 📊 Analytics & Visualization
- **Interactive Dashboards**: Comprehensive visualizations and real-time metrics
- **Scenario Planning**: What-if analysis for business decisions with multiple forecasting models
- **Performance Tracking**: Monitor KPIs, trends, and financial health indicators
- **Custom Reports**: Generate and export detailed financial reports

### 🔐 Security & Management
- **Multi-business Support**: Manage multiple businesses under one account with role-based access
- **Real-time Alerts**: Smart notifications for cash flow anomalies, opportunities, and deadlines
- **Secure Authentication**: JWT-based auth with role-based permissions and audit trails
- **Data Encryption**: End-to-end encryption for sensitive financial information

## 🏗️ Technology Stack

### Backend (Python/Flask)
| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Flask 3.0.0** | Web framework and API |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Primary database with Alembic migrations |
| **Pandas** | Data processing and analysis |
| **Gunicorn** | Production WSGI server |

### Frontend (React/TypeScript)
| Technology | Purpose |
|------------|---------|
| **React 18.3.1** | Component-based UI framework |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first styling |
| **Radix UI** | Accessible UI primitives |
| **shadcn/ui** | Pre-built component library |
| **Zustand** | State management |
| **Recharts** | Interactive data visualization |
| **React Hook Form** | Form management |
| **Zod** | Schema validation |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Nginx** | Reverse proxy and load balancing |
| **OpenAI API** | Advanced AI capabilities |
| **Google AI** | Enhanced ML features |

## 🚀 Quick Start

### Prerequisites
- Docker Engine v20.10+
- Docker Compose v2.0+

### Development Setup
```bash
# Clone the repository
git clone https://github.com/fiandev/cashflow-forecaster.git
cd cashflow-forecaster

# Start development services in background
./docker.sh up

# View application logs
./docker.sh logs-follow
```

### Application Access
| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:5000 |
| **Health Check** | http://localhost:5000/health |

### Common Commands
```bash
# Stop services
./docker.sh down

# Build/rebuild services
./docker.sh build

# Run tests
./docker.sh tests

# Database seed (for sample data)
./docker.sh seed
```

## 🎯 Project Goals & Vision

### Mission
To democratize financial planning and forecasting for businesses of all sizes by providing accessible, accurate, and intuitive cash flow prediction tools powered by artificial intelligence.

### Core Objectives
- **Accessibility**: Make advanced financial forecasting tools available to small and medium businesses
- **Accuracy**: Deliver reliable predictions using sophisticated ML models and comprehensive data analysis
- **Usability**: Provide an intuitive interface that doesn't require financial expertise
- **Scalability**: Support businesses from startup to enterprise with flexible architecture

## 🗺️ Roadmap & Future Features

### Phase 1: Foundation (Current)
- ✅ Basic cash flow forecasting
- ✅ Multi-business management
- ✅ Transaction categorization
- ✅ Dashboard analytics

### Phase 2: Intelligence (Planned)
- 🔄 Enhanced AI models with seasonal adjustment
- 🔄 Integration with accounting software (QuickBooks, Xero)
- 🔄 Advanced scenario planning tools
- 🔄 Automated financial insights

### Phase 3: Expansion (Future)
- 📅 Predictive invoicing and payment tracking
- 🌐 Multi-currency support
- 📈 Integration with banking APIs
- 🤖 AI-powered financial advisor chatbot
- 📱 Mobile applications (iOS/Android)

## 🔐 Default Login Credentials

> **⚠️ Security Note**: These credentials are for development and testing only. Never use in production environments.

| Role | Email | Password | Access |
|------|-------|----------|---------|
| **Admin** | `admin@gmail.com` | `password` | Full system administration |
| **Business Owner** | `user@gmail.com` | `password` | Multi-business management |
| **Business Owner** | `jane.smith@gmail.com` | `password` | Single business access |

### Sample Businesses
- **TechCorp Solutions** (San Francisco, USD)
- **RetailCo Stores** (Toronto, CAD) 
- **CloudTech Services** (New York, USD)

### Additional Entities
- **Forecasts**: AI-generated cash flow predictions
- **Models**: ML model configurations and performance metrics
- **RiskScores**: Risk assessment and probability calculations
- **Alerts**: Smart notifications and triggers
- **OCRDocuments**: Processed financial documents
- **Scenarios**: What-if analysis results

## 🛠️ Development Commands

### Docker Management
| Command | Description |
|---------|-------------|
| `./docker.sh up` | Start development services in background |
| `./docker.sh up-dev` | Start development services in foreground |
| `./docker.sh down` | Stop all services |
| `./docker.sh logs-follow` | View logs and follow output |
| `./docker.sh build` | Build/rebuild service images |
| `./docker.sh restart` | Restart all services |
| `./docker.sh status` | Show container status |

### Development Operations
| Command | Description |
|---------|-------------|
| `./docker.sh exec-backend 'command'` | Execute command in backend container |
| `./docker.sh exec-frontend 'command'` | Execute command in frontend container |
| `./docker.sh shell-backend` | Start shell in backend container |
| `./docker.sh shell-frontend` | Start shell in frontend container |
| `./docker.sh tests` | Run backend tests |

### Database Operations
| Command | Description |
|---------|-------------|
| `./docker.sh db-backup` | Create SQLite database backup |
| `./docker.sh db-restore file` | Restore from backup file |
| `./docker.sh seed` | Seed database with sample data |

### Production Operations
| Command | Description |
|---------|-------------|
| `./docker.sh prod-up` | Start production services |
| `./docker.sh prod-down` | Stop production services |
| `./docker.sh prod-logs` | View production logs |

## 🔧 Environment Configuration

### Backend Environment Variables (`.env.docker.example`)
```bash
# Database Configuration
DB_TYPE=sqlite
DB_PATH=database/database.db

# Security Settings
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# AI Services
OPENAI_API_KEY=your-openai-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

### Frontend Environment Variables (`.env.docker.example`)
```bash
# API Configuration
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_SENTRY=false

# UI Settings
VITE_DEFAULT_CURRENCY=USD
VITE_DATE_FORMAT=MM/DD/YYYY
```

## 🧪 Testing Strategy

### Backend Testing
```bash
# Run all backend tests
./docker.sh exec-backend 'python -m pytest'

# Run tests with verbose output
./docker.sh exec-backend 'python -m pytest tests/ -v'

# Run tests with coverage report
./docker.sh exec-backend 'python -m pytest --cov=app --cov-report=html'
```

### Frontend Testing
```bash
# Run all frontend tests
./docker.sh exec-frontend 'npm test'

# Run tests with coverage report
./docker.sh exec-frontend 'npm run test:coverage'

# Run tests in watch mode
./docker.sh exec-frontend 'npm run test:watch'
```

### Test Structure
- **Unit Tests**: Individual functions and components
- **Integration Tests**: API endpoints and database operations
- **End-to-End Tests**: Complete user workflows
- **Performance Tests**: Load and stress testing

## 📦 Local Development Setup

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Database Management
```bash
# Create new migration
./docker.sh exec-backend 'flask db migrate -m "Add new feature"'

# Apply migrations
./docker.sh exec-backend 'flask db upgrade'

# Reset database with seed data
./docker.sh exec-backend 'python seed.py'
```

## 🚀 Production Deployment

### Docker Production Setup
```bash
# Build and deploy production services
./docker.sh prod-up

# View production logs
./docker.sh prod-logs

# Scale backend services
docker-compose.prod.yml up -d --scale backend=3

# Stop production services
./docker.sh prod-down
```

### Manual Production Deployment
1. Build frontend: `cd frontend && npm run build`
2. Configure nginx: Update `nginx.conf` with production settings
3. Set production environment variables
4. Deploy with Gunicorn: `gunicorn -w 4 --bind 0.0.0.0:5000 app:app`

### Deployment Checklist
- [ ] Environment variables configured securely
- [ ] SSL certificates installed
- [ ] Database connection optimized
- [ ] Monitoring and logging enabled
- [ ] Backup procedures established
- [ ] Performance settings applied

## 🔍 API Documentation

### Authentication
All API endpoints require JWT authentication (except `/auth/login` and `/health`).

#### Login Example
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@gmail.com",
    "password": "password"
  }'
```

#### API Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "role": "business_owner"
  }
}
```

#### Using the Token
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  http://localhost:5000/api/businesses
```

### Core API Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Authenticate user |
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/refresh` | Refresh access token |

#### Business Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/businesses` | List user businesses |
| `POST` | `/api/businesses` | Create new business |
| `PUT` | `/api/businesses/{id}` | Update business |
| `DELETE` | `/api/businesses/{id}` | Delete business |

#### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/transactions` | List transactions |
| `POST` | `/api/transactions` | Create new transaction |
| `PUT` | `/api/transactions/{id}` | Update transaction |
| `DELETE` | `/api/transactions/{id}` | Delete transaction |

#### Forecasting
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/forecasts` | Generate forecast |
| `GET` | `/api/forecasts/{business_id}` | Get forecasts for business |
| `GET` | `/api/models` | List available ML models |

#### OCR & Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ocr/upload` | Upload document for processing |
| `GET` | `/api/documents` | List processed documents |
| `GET` | `/api/documents/{id}` | Get document details |

## 🧭 API Error Handling

### Error Response Format
```json
{
  "error": "Error message",
  "status_code": 400,
  "timestamp": "2023-01-01T10:00:00Z",
  "details": {}
}
```

### Common Status Codes
- `200`: Success
- `400`: Bad request (validation errors)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not found
- `500`: Internal server error

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Docker Issues
| Issue | Solution |
|-------|----------|
| **Port conflicts** | Ensure ports 3000, 5000, and 80 are available; use `./docker.sh clean` to reset |
| **Container won't start** | Check logs with `./docker.sh logs-follow`; verify environment variables |
| **Database connection errors** | Check if database volume exists: `docker volume ls`; re-seed with `./docker.sh seed` |

#### Development Issues
| Issue | Solution |
|-------|----------|
| **Frontend not connecting to backend** | Verify API URL in frontend environment; check CORS configuration in backend |
| **AI services not working** | Verify API keys in environment variables; check service logs for errors |
| **Database migration errors** | Reset with `./docker.sh seed` or apply migrations manually with `flask db upgrade` |

#### Performance Issues
| Issue | Solution |
|-------|----------|
| **Slow application** | Check resource usage; optimize database queries; enable caching |
| **High memory usage** | Monitor container resources; adjust Gunicorn workers as needed |

### Health Checks
```bash
# Backend health endpoint
curl http://localhost:5000/health

# Frontend availability
curl http://localhost:3000

# Database connectivity
./docker.sh exec-backend 'python -c "from app import app; from app.database import db; with app.app_context(): db.engine.execute(\"SELECT 1\"); print(\"DB OK\")"'
```

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/cashflow-forecaster.git`
3. **Create feature branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** and test thoroughly
5. **Commit changes**: `git add . && git commit -m "Add amazing feature"`
6. **Push** to branch: `git push origin feature/amazing-feature`
7. **Submit** pull request

### Code Standards
- **Python**: Follow PEP 8 style guide with Black formatting
- **JavaScript/TypeScript**: Use ESLint with recommended settings
- **Documentation**: Update README and code comments as needed
- **Testing**: Add tests for new features and ensure all tests pass

### Local Development Setup
- Use proper virtual environments
- Run linting and formatting tools before committing
- Follow existing code style and patterns
- Write meaningful commit messages

### Pull Request Guidelines
- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation as needed
- Reference related issues in your PR description
- Ensure all CI checks pass

## 🛡️ Security

### Security Practices
- **Input Validation**: All user inputs are validated and sanitized
- **Authentication**: JWT tokens with proper expiration and refresh mechanisms
- **Authorization**: Role-based access control for all endpoints
- **Data Protection**: Encryption for sensitive data at rest and in transit
- **Dependency Scanning**: Regular security scanning of dependencies

### Security Reporting
For security vulnerabilities, please contact us directly rather than opening a public issue.

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check the README and project documentation
- **Issues**: Create an issue in the GitHub repository for bugs and feature requests
- **Logs**: Review application logs using `./docker.sh logs-follow`
- **Community**: Reach out through GitHub Discussions (if enabled)

### System Requirements
- **Development**: 4GB RAM minimum, 2 CPU cores, 2GB free disk space
- **Production**: 8GB RAM recommended, 4 CPU cores, SSD storage recommended
- **Docker**: Ensure Docker has adequate resources allocated

---
<div align="center">

**AI Cashflow Forecaster**  
*Built with ❤️ by [Fiandev](https://fiandev.com) and [ErRickow](https://github.com/ErRickow)*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/fiandev/cashflow-forecaster)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/company/fiandev)

</div>
