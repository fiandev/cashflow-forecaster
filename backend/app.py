from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "database", "database.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Enable CORS for development (allow frontend origin for Docker)
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3001")
CORS(app, resources={r"/*": {"origins": [frontend_origin, "http://localhost:3000", "http://localhost:3001"]}})

from models import (
    db,
    User,
    Business,
    Category,
    Transaction,
    OCRDocument,
    Model,
    ModelRun,
    Forecast,
    RiskScore,
    Alert,
    Scenario,
    APIKey,
)
from routes import register_routes

db.init_app(app)
migrate = Migrate(app, db)

register_routes(app)


@app.route("/")
def index():
    return {"message": "AI Cashflow Forecaster API"}


if __name__ == "__main__":
    app.run(debug=os.getenv("APP_ENV", "development") != "production")
