import os
import sys
from app import app
from models import db
from seeders.database_seeder import run_seeder

def init_db():
    """Initialize the database with tables and sample data."""
    print("🚀 Initializing database...")

    # Set environment variables for SQLite database
    os.environ.setdefault('DB_TYPE', 'sqlite')
    os.environ.setdefault('DB_PATH', 'database/database.db')

    # Set the database URI in the app config
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'database', 'database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with app.app_context():
        # Create the database tables
        print("📦 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

        # Seed the database with sample data
        print("🌱 Seeding database with sample data...")
        run_seeder()
        print("✅ Database seeded successfully!")

    print("🎯 Database initialization completed!")

if __name__ == "__main__":
    init_db()