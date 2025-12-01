# AI Cashflow Forecaster

## Prerequisites

- Docker Engine (v20.10+)
- Docker Compose (v2.0+)

## Quick Start

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
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

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
   - Application: http://localhost (port 80)

3. **Stop production services:**
   ```bash
   ./docker.sh prod-down
   ```

## Available Commands

The `docker.sh` script provides the following commands:

### Basic Operations:
- `up` - Start development services in the background
- `up-dev` - Start development services in foreground
- `down` - Stop all services
- `logs` - View logs from all services
- `logs-follow` - View logs from all services and follow
- `build` - Build/rebuild service images
- `restart` - Restart all services
- `status` - Show status of containers

### Development Operations:
- `exec-backend 'command'` - Execute a command in the backend container
- `exec-frontend 'command'` - Execute a command in the frontend container
- `shell-backend` - Start a shell in the backend container
- `shell-frontend` - Start a shell in the frontend container
- `tests` - Run tests in the backend container

### Database Operations:
- `db-backup` - Create a backup of the SQLite database
- `db-restore file` - Restore the SQLite database from backup
- `seed` - Seed the database with sample data

### Production Operations:
- `prod-up` - Start production services
- `prod-down` - Stop production services
- `prod-logs` - View logs from production services

### System Operations:
- `clean` - Remove all containers, networks, and volumes

## Architecture

The Docker setup consists of:

1. **Backend Service**:
   - Flask application running on port 5000
   - Uses SQLite database stored in a named volume
   - Automatically creates database tables on startup
   - Initializes with sample data if needed

2. **Frontend Service**:
   - React application running on port 3000 (dev) or served via nginx (prod)
   - Communicates with backend API
   - Uses Vite for development

3. **Database**:
   - SQLite database file stored in a Docker named volume
   - Persists data between container restarts

## Database Management

### Backing up the database:
```bash
./docker.sh db-backup
```

### Restoring the database:
```bash
./docker.sh db-restore backups/db_backup_YYYYMMDD_HHMMSS.db
```

### Seeding with sample data:
```bash
./docker.sh seed
```

## Environment Configuration

The application uses the following environment variables:

### Backend:
- `DB_TYPE` - Database type (set to 'sqlite')
- `DB_PATH` - Path to SQLite database file
- `SECRET_KEY` - Secret key for Flask application

## Customization

### For Development:
The development environment uses `docker-compose.yml` and runs both services with hot-reloading.

### For Production:
The production environment uses `docker-compose.prod.yml` and serves the frontend through nginx with the backend API behind a reverse proxy.

## Troubleshooting

1. **Port already in use**:
   - Make sure no other services are using ports 3000, 5000, or 80
   - Stop conflicting services or change ports in the compose files

2. **Database connection issues**:
   - Ensure the db service is running before the backend
   - Check that database files are mounted correctly

3. **Frontend not connecting to backend**:
   - In development, the frontend uses environment variables to connect to the backend
   - In production, nginx proxies API requests to the backend

## Production Deployment

For production deployment, use the production compose file:

```bash
./docker.sh prod-up
```

This will:
- Build optimized frontend assets
- Serve them through nginx
- Run multiple backend workers
- Configure proper proxying between frontend and backend