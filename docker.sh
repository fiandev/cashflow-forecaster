#!/bin/bash

# Docker utility script for AI Cashflow Forecaster
# Provides commands for common Docker operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="docker-compose.yml"
COMPOSE_PROD_FILE="docker-compose.prod.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display usage
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  up                    Start development services in the background"
    echo "  up-dev               Start development services in foreground"
    echo "  down                 Stop all services"
    echo "  logs                 View logs from all services"
    echo "  logs-follow          View logs from all services and follow"
    echo "  build                Build/rebuild service images"
    echo "  restart              Restart all services"
    echo "  exec-backend         Execute a command in the backend container"
    echo "  exec-frontend        Execute a command in the frontend container"
    echo "  shell-backend        Start a shell in the backend container"
    echo "  shell-frontend       Start a shell in the frontend container"
    echo "  prod-up              Start production services"
    echo "  prod-down            Stop production services"
    echo "  prod-restart         Restart production services with updated frontend"
    echo "  prod-logs            View logs from production services"
    echo "  prod-build-frontend  Build/rebuild the production frontend service"
    echo "  db-backup            Create a backup of the SQLite database"
    echo "  db-restore           Restore the SQLite database from backup"
    echo "  seed                 Seed the database with sample data"
    echo "  tests                Run tests in the backend container"
    echo "  clean                Remove all containers, networks, and volumes"
    echo "  status               Show status of containers"
    echo ""
    echo "Examples:"
    echo "  $0 up                # Start development environment"
    echo "  $0 prod-up           # Start production environment"
    echo "  $0 shell-backend     # Access backend container shell"
    echo "  $0 db-backup         # Backup the database"
}

# Check if docker-compose is available
check_docker_compose() {
    if ! [ -x "$(command -v docker-compose)" ]; then
        if ! [ -x "$(command -v docker)" ] || ! docker compose version >/dev/null 2>&1; then
            print_error "Neither docker-compose nor 'docker compose' is available."
            exit 1
        fi
    fi
}

# Function to run docker-compose command
run_compose() {
    local cmd=$1
    shift
    check_docker_compose
    
    if [ -x "$(command -v docker-compose)" ]; then
        docker-compose $cmd "$@"
    else
        docker compose $cmd "$@"
    fi
}

# Function to run production docker-compose command
run_compose_prod() {
    local cmd=$1
    shift
    check_docker_compose
    
    if [ -x "$(command -v docker-compose)" ]; then
        docker-compose -f $COMPOSE_PROD_FILE $cmd "$@"
    else
        docker compose -f $COMPOSE_PROD_FILE $cmd "$@"
    fi
}

# Main command execution
case "$1" in
    up)
        print_info "Starting development services in background..."
        run_compose up -d
        print_success "Development services started in background."
        print_info "Backend API: http://localhost:5000"
        print_info "Frontend: http://localhost:3000"
        ;;
    
    up-dev)
        print_info "Starting development services in foreground..."
        run_compose up
        ;;
    
    down)
        print_info "Stopping all services..."
        run_compose down
        print_success "All services stopped."
        ;;
    
    logs)
        print_info "Showing logs from all services..."
        run_compose logs
        ;;
    
    logs-follow)
        print_info "Showing logs from all services (following)..."
        run_compose logs -f
        ;;
    
    build)
        print_info "Building service images..."
        run_compose build
        print_success "Service images built."
        ;;
    
    restart)
        print_info "Restarting all services..."
        run_compose restart
        print_success "All services restarted."
        ;;
    
    exec-backend)
        if [ -z "$2" ]; then
            print_error "Please specify a command to execute in the backend container."
            echo "Example: $0 exec-backend 'python manage.py shell'"
            exit 1
        fi
        run_compose exec backend $2
        ;;
    
    exec-frontend)
        if [ -z "$2" ]; then
            print_error "Please specify a command to execute in the frontend container."
            echo "Example: $0 exec-frontend 'npm run build'"
            exit 1
        fi
        run_compose exec frontend $2
        ;;
    
    shell-backend)
        print_info "Opening shell in backend container..."
        run_compose exec backend bash
        ;;
    
    shell-frontend)
        print_info "Opening shell in frontend container..."
        run_compose exec frontend bash
        ;;
    
    prod-up)
        print_info "Starting production services..."
        run_compose_prod up -d
        print_success "Production services started."
        print_info "Application: http://localhost"
        ;;
    
    prod-down)
        print_info "Stopping production services..."
        run_compose_prod down
        print_success "Production services stopped."
        ;;

    prod-restart)
        print_info "Stopping production services..."
        run_compose_prod down
        print_info "Building production frontend service..."
        run_compose_prod build frontend
        print_info "Starting production services..."
        run_compose_prod up -d
        print_success "Production services restarted with updated frontend."
        print_info "Application: http://localhost"
        ;;

    prod-logs)
        print_info "Showing logs from production services..."
        run_compose_prod logs
        ;;

    prod-build-frontend)
        print_info "Building production frontend service..."
        run_compose_prod build frontend
        print_success "Production frontend service built."
        ;;
    
    db-backup)
        print_info "Creating database backup..."
        BACKUP_DIR="backups"
        mkdir -p $BACKUP_DIR
        BACKUP_FILE="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).db"
        
        run_compose exec backend bash -c "cp database/database.db /tmp/backup.db"
        run_compose cp backend:/tmp/backup.db "./$BACKUP_FILE"
        run_compose exec backend bash -c "rm /tmp/backup.db"
        
        print_success "Database backed up to $BACKUP_FILE"
        ;;
    
    db-restore)
        if [ -z "$2" ]; then
            print_error "Please specify the backup file to restore."
            echo "Example: $0 db-restore backups/db_backup_20231201_120000.db"
            exit 1
        fi
        
        if [ ! -f "$2" ]; then
            print_error "Backup file $2 does not exist."
            exit 1
        fi
        
        print_info "Restoring database from $2..."
        run_compose cp "$2" backend:/tmp/restore.db
        run_compose exec backend bash -c "cp /tmp/restore.db database/database.db && rm /tmp/restore.db"
        print_success "Database restored from $2"
        ;;
    
    seed)
        print_info "Seeding database with sample data..."
        run_compose exec backend bash -c "
            python -c \"
import os
os.environ['DB_TYPE'] = 'sqlite'
os.environ['DB_PATH'] = 'database/database.db'
from seeders.database_seeder import run_seeder
run_seeder()
print('✅ Database seeded successfully!')
\"
        "
        print_success "Database seeded with sample data."
        ;;
    
    tests)
        print_info "Running tests in backend container..."
        run_compose exec backend bash -c "python -m pytest tests/ -v"
        ;;
    
    clean)
        print_warning "This will remove ALL containers, networks, and volumes!"
        read -p "Are you sure you want to continue? (yes/no): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing all Docker resources..."
            run_compose down -v --remove-orphans
            run_compose_prod down -v --remove-orphans
            print_success "All Docker resources cleaned up."
        else
            print_info "Clean operation cancelled."
        fi
        ;;
    
    status)
        print_info "Container status:"
        run_compose ps
        ;;
    
    *)
        if [ -z "$1" ]; then
            print_error "No command specified."
            echo ""
            usage
        else
            print_error "Unknown command: $1"
            echo ""
            usage
        fi
        ;;
esac