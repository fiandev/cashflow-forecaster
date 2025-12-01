from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(200))
    role = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)

    businesses = db.relationship("Business", backref="owner", lazy=True)
    scenarios = db.relationship("Scenario", backref="run_by_user", lazy=True)


class Business(db.Model):
    __tablename__ = "businesses"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    currency = db.Column(db.String(10), nullable=False)
    timezone = db.Column(db.String(64), nullable=False, default="Asia/Jakarta")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    settings = db.Column(db.JSON)

    categories = db.relationship("Category", backref="business", lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", backref="business", lazy=True, cascade="all, delete-orphan")
    ocr_documents = db.relationship("OCRDocument", backref="business", lazy=True, cascade="all, delete-orphan")
    models = db.relationship("Model", backref="business", lazy=True, cascade="all, delete-orphan")
    forecasts = db.relationship("Forecast", backref="business", lazy=True, cascade="all, delete-orphan")
    risk_scores = db.relationship("RiskScore", backref="business", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="business", lazy=True, cascade="all, delete-orphan")
    scenarios = db.relationship("Scenario", backref="business", lazy=True, cascade="all, delete-orphan")
    api_keys = db.relationship("APIKey", backref="business", lazy=True, cascade="all, delete-orphan")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    children = db.relationship(
        "Category", backref=db.backref("parent", remote_side=[id]), cascade="all, delete-orphan"
    )
    transactions = db.relationship("Transaction", backref="category", lazy=True, cascade="all, delete-orphan")


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    datetime = db.Column(db.DateTime)
    description = db.Column(db.Text)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    direction = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"))
    source = db.Column(db.String(100))
    ocr_document_id = db.Column(db.Integer, db.ForeignKey("ocr_documents.id", ondelete="CASCADE"))
    tags = db.Column(db.JSON)
    is_anomalous = db.Column(db.Boolean, default=False)
    ai_tag = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime)

    alerts = db.relationship("Alert", backref="linked_transaction", lazy=True, cascade="all, delete-orphan")


class OCRDocument(db.Model):
    __tablename__ = "ocr_documents"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())
    raw_text = db.Column(db.Text)
    parsed = db.Column(db.JSON)
    confidence = db.Column(db.Numeric(6, 4))
    source_image_url = db.Column(db.String(1024))

    transactions = db.relationship("Transaction", backref="ocr_document", lazy=True, cascade="all, delete-orphan")


class Model(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"))
    name = db.Column(db.String(200), nullable=False)
    model_type = db.Column(db.String(100), nullable=False)
    params = db.Column(db.JSON)
    version = db.Column(db.String(50))
    last_trained_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    model_runs = db.relationship("ModelRun", backref="model", lazy=True, cascade="all, delete-orphan")
    forecasts = db.relationship("Forecast", backref="model_ref", lazy=True, cascade="all, delete-orphan")


class ModelRun(db.Model):
    __tablename__ = "model_runs"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("models.id", ondelete="CASCADE"), nullable=False)
    run_at = db.Column(db.DateTime, server_default=db.func.now())
    input_summary = db.Column(db.JSON)
    output_summary = db.Column(db.JSON)
    run_status = db.Column(db.String(50), default="completed")
    notes = db.Column(db.Text)

    forecasts = db.relationship("Forecast", backref="model_run", lazy=True, cascade="all, delete-orphan")


class Forecast(db.Model):
    __tablename__ = "forecasts"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    model_run_id = db.Column(db.Integer, db.ForeignKey("model_runs.id", ondelete="CASCADE"))
    model_id = db.Column(db.Integer, db.ForeignKey("models.id", ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    granularity = db.Column(db.String(20), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    predicted_value = db.Column(db.Numeric(14, 2))
    lower_bound = db.Column(db.Numeric(14, 2))
    upper_bound = db.Column(db.Numeric(14, 2))
    forecast_metadata = db.Column(db.JSON)

    risk_scores = db.relationship("RiskScore", backref="source_forecast", lazy=True, cascade="all, delete-orphan")
    alerts = db.relationship("Alert", backref="linked_forecast", lazy=True, cascade="all, delete-orphan")


class RiskScore(db.Model):
    __tablename__ = "risk_scores"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    assessed_at = db.Column(db.DateTime, server_default=db.func.now())
    liquidity_score = db.Column(db.Numeric(5, 2))
    cashflow_risk_score = db.Column(db.Numeric(5, 2))
    volatility_index = db.Column(db.Numeric(10, 4))
    drawdown_prob = db.Column(db.Numeric(10, 4))
    source_forecast_id = db.Column(db.Integer, db.ForeignKey("forecasts.id", ondelete="CASCADE"))
    details = db.Column(db.JSON)


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    linked_transaction_id = db.Column(db.Integer, db.ForeignKey("transactions.id", ondelete="CASCADE"))
    linked_forecast_id = db.Column(db.Integer, db.ForeignKey("forecasts.id", ondelete="CASCADE"))
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    forecast_metadata = db.Column(db.JSON)


class Scenario(db.Model):
    __tablename__ = "scenarios"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    params = db.Column(db.JSON)
    result_summary = db.Column(db.JSON)
    run_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))


class APIKey(db.Model):
    __tablename__ = "api_keys"
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(200))
    key_hash = db.Column(db.String(255))
    scopes = db.Column(db.Text)
    revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
