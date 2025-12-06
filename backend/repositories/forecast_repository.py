from models import Forecast, Business, Model, ModelRun
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal


class ForecastRepository(BaseRepository):
    def __init__(self):
        super().__init__(Forecast)

    def findByBusiness(self, business_id: int) -> List[Forecast]:
        """Find forecasts by business"""
        return self.find_by(business_id=business_id)

    def findByModel(self, model_id: int) -> List[Forecast]:
        """Find forecasts by model"""
        return self.find_by(model_id=model_id)

    def findByModelRun(self, model_run_id: int) -> List[Forecast]:
        """Find forecasts by model run"""
        return self.find_by(model_run_id=model_run_id)

    def findByGranularity(self, granularity: str) -> List[Forecast]:
        """Find forecasts by granularity"""
        return self.find_by(granularity=granularity)

    def findByDateRange(
        self, business_id: int, start_date: date, end_date: date
    ) -> List[Forecast]:
        """Find forecasts within date range"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.period_start >= start_date,
            self.model.period_end <= end_date,
        ).all()

    def findActive(self, business_id: int) -> List[Forecast]:
        """Find active forecasts (future dates)"""
        today = date.today()
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.period_end >= today
        ).all()

    def findExpired(self, business_id: int) -> List[Forecast]:
        """Find expired forecasts (past dates)"""
        today = date.today()
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.period_end < today
        ).all()

    def findByPeriod(
        self, business_id: int, period_start: date, period_end: date
    ) -> List[Forecast]:
        """Find forecasts by specific period"""
        return self.model.query.filter_by(
            business_id=business_id, period_start=period_start, period_end=period_end
        ).all()

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> Forecast:
        """Create forecast with business"""
        forecast_data = data.copy()
        forecast_data["business_id"] = business_id
        return self.create(forecast_data)

    def createWithModel(self, data: Dict[str, Any], model_id: int) -> Forecast:
        """Create forecast with model"""
        forecast_data = data.copy()
        forecast_data["model_id"] = model_id
        return self.create(forecast_data)

    def createWithModelRun(self, data: Dict[str, Any], model_run_id: int) -> Forecast:
        """Create forecast with model run"""
        forecast_data = data.copy()
        forecast_data["model_run_id"] = model_run_id
        return self.create(forecast_data)

    def updatePrediction(
        self, forecast_id: int, predicted_value: Decimal
    ) -> Optional[Forecast]:
        """Update predicted value"""
        return self.update(forecast_id, {"predicted_value": predicted_value})

    def updateBounds(
        self, forecast_id: int, lower_bound: Decimal, upper_bound: Decimal
    ) -> Optional[Forecast]:
        """Update confidence bounds"""
        return self.update(
            forecast_id, {"lower_bound": lower_bound, "upper_bound": upper_bound}
        )

    def updateMetadata(
        self, forecast_id: int, metadata: Dict[str, Any]
    ) -> Optional[Forecast]:
        """Update forecast metadata"""
        return self.update(forecast_id, {"forecast_metadata": metadata})

    def search(self, business_id: int, query: str) -> List[Forecast]:
        """Search forecasts by metadata"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            db.cast(self.model.forecast_metadata, db.Text).like(f"%{query}%"),
        ).all()

    def getWithBusiness(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with business"""
        return (
            self.model.query.options(db.joinedload(self.model.business))
            .filter_by(id=forecast_id)
            .first()
        )

    def getWithModel(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with model"""
        return (
            self.model.query.options(db.joinedload(self.model.model_ref))
            .filter_by(id=forecast_id)
            .first()
        )

    def getWithModelRun(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with model run"""
        return (
            self.model.query.options(db.joinedload(self.model.model_run))
            .filter_by(id=forecast_id)
            .first()
        )

    def getWithRiskScores(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with risk scores"""
        return (
            self.model.query.options(db.joinedload(self.model.risk_scores))
            .filter_by(id=forecast_id)
            .first()
        )

    def getWithAlerts(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with alerts"""
        return (
            self.model.query.options(db.joinedload(self.model.alerts))
            .filter_by(id=forecast_id)
            .first()
        )

    def getWithAllRelations(self, forecast_id: int) -> Optional[Forecast]:
        """Get forecast with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.business),
                db.joinedload(self.model.model_ref),
                db.joinedload(self.model.model_run),
                db.joinedload(self.model.risk_scores),
                db.joinedload(self.model.alerts),
            )
            .filter_by(id=forecast_id)
            .first()
        )

    def getLatestByBusiness(self, business_id: int, limit: int = 10) -> List[Forecast]:
        """Get latest forecasts for business"""
        return (
            self.model.query.filter_by(business_id=business_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )

    def getForecastAccuracy(self, model_id: int) -> Dict[str, Any]:
        """Calculate forecast accuracy for model"""
        # This would compare actual vs predicted values
        # For now, return placeholder
        return {
            "model_id": model_id,
            "mape": 0.15,  # Mean Absolute Percentage Error
            "rmse": 1250.50,  # Root Mean Square Error
            "samples": 50,
        }

    def getForecastSummary(
        self, business_id: int, start_date: date, end_date: date
    ) -> Dict[str, Any]:
        """Get forecast summary for business and date range"""
        forecasts = self.findByDateRange(business_id, start_date, end_date)

        total_predicted = sum(f.predicted_value or 0 for f in forecasts)
        total_lower = sum(f.lower_bound or 0 for f in forecasts)
        total_upper = sum(f.upper_bound or 0 for f in forecasts)

        return {
            "business_id": business_id,
            "period": f"{start_date} to {end_date}",
            "total_forecasts": len(forecasts),
            "total_predicted": total_predicted,
            "total_lower_bound": total_lower,
            "total_upper_bound": total_upper,
            "average_predicted": total_predicted / len(forecasts) if forecasts else 0,
        }
