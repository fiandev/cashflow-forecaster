import os

from dotenv import load_dotenv
from flask import Flask, make_response, request
from flask_migrate import Migrate

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "database", "database.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


from models import db

db.init_app(app)
migrate = Migrate(app, db)


# Custom CORS middleware - allow all origins
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type,Authorization,X-Requested-With,Accept,Origin",
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,HEAD"
    )
    return response


# Handle preflight OPTIONS requests for all routes
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,X-Requested-With,Accept,Origin",
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,HEAD"
        )
        return response


@app.route("/")
def index():
    return {"message": "AI Cashflow Forecaster API"}


if __name__ == "__main__":
    app.run(debug=os.getenv("APP_ENV", "development") != "production")
