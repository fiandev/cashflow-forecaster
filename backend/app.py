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

# Enable CORS for localhost:5173
CORS(app, 
    origins=["http://localhost:5173/", "http://127.0.0.1:5173/"]
)

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
