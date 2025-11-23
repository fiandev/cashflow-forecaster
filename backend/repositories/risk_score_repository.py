from models import RiskScore, Business, Forecast
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal


class RiskScoreRepository(BaseRepository):
    def __init__(self):
        super().__init__(RiskScore)

    def findByBusiness(self, business_id: int) -> List[RiskScore]:
        """Find risk scores by business"""
        return self.find_by(business_id=business_id)

    def findByForecast(self, forecast_id: int) -> List[RiskScore]:
        """Find risk scores by forecast"""
        return self.find_by(source_forecast_id=forecast_id)

    def findByLiquidityRange(
        self, business_id: int, min_score: Decimal, max_score: Decimal
    ) -> List[RiskScore]:
        """Find risk scores by liquidity range"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.liquidity_score >= min_score,
            self.model.liquidity_score <= max_score,
        ).all()

    def findByRiskLevel(self, business_id: int, risk_level: str) -> List[RiskScore]:
        """Find risk scores by risk level (based on cashflow risk score)"""
        if risk_level == "low":
            return self.model.query.filter(
                self.model.business_id == business_id,
                self.model.cashflow_risk_score <= 30,
            ).all()
        elif risk_level == "medium":
            return self.model.query.filter(
                self.model.business_id == business_id,
                self.model.cashflow_risk_score > 30,
                self.model.cashflow_risk_score <= 60,
            ).all()
        elif risk_level == "high":
            return self.model.query.filter(
                self.model.business_id == business_id,
                self.model.cashflow_risk_score > 60,
            ).all()
        return []

    def findRecent(self, business_id: int, days: int = 30) -> List[RiskScore]:
        """Find recent risk scores"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.assessed_at >= cutoff_date
        ).all()

    def findHighVolatility(
        self, business_id: int, threshold: Decimal = Decimal("0.2")
    ) -> List[RiskScore]:
        """Find high volatility risk scores"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.volatility_index >= threshold,
        ).all()

    def findHighDrawdownProb(
        self, business_id: int, threshold: Decimal = Decimal("0.1")
    ) -> List[RiskScore]:
        """Find high drawdown probability risk scores"""
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.drawdown_prob >= threshold
        ).all()

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> RiskScore:
        """Create risk score with business"""
        risk_data = data.copy()
        risk_data["business_id"] = business_id
        return self.create(risk_data)

    def createWithForecast(self, data: Dict[str, Any], forecast_id: int) -> RiskScore:
        """Create risk score with forecast"""
        risk_data = data.copy()
        risk_data["source_forecast_id"] = forecast_id
        return self.create(risk_data)

    def updateLiquidityScore(self, risk_id: int, score: Decimal) -> Optional[RiskScore]:
        """Update liquidity score"""
        return self.update(risk_id, {"liquidity_score": score})

    def updateCashflowRiskScore(
        self, risk_id: int, score: Decimal
    ) -> Optional[RiskScore]:
        """Update cashflow risk score"""
        return self.update(risk_id, {"cashflow_risk_score": score})

    def updateVolatilityIndex(
        self, risk_id: int, index: Decimal
    ) -> Optional[RiskScore]:
        """Update volatility index"""
        return self.update(risk_id, {"volatility_index": index})

    def updateDrawdownProb(self, risk_id: int, prob: Decimal) -> Optional[RiskScore]:
        """Update drawdown probability"""
        return self.update(risk_id, {"drawdown_prob": prob})

    def updateDetails(
        self, risk_id: int, details: Dict[str, Any]
    ) -> Optional[RiskScore]:
        """Update risk details"""
        return self.update(risk_id, {"details": details})

    def search(self, business_id: int, query: str) -> List[RiskScore]:
        """Search risk scores by details"""
        return self.model.query.filter(
            self.model.business_id == business_id,
            db.cast(self.model.details, db.Text).like(f"%{query}%"),
        ).all()

    def getWithBusiness(self, risk_id: int) -> Optional[RiskScore]:
        """Get risk score with business"""
        return (
            self.model.query.options(db.joinedload(self.model.business))
            .filter_by(id=risk_id)
            .first()
        )

    def getWithForecast(self, risk_id: int) -> Optional[RiskScore]:
        """Get risk score with forecast"""
        return (
            self.model.query.options(db.joinedload(self.model.source_forecast))
            .filter_by(id=risk_id)
            .first()
        )

    def getWithAllRelations(self, risk_id: int) -> Optional[RiskScore]:
        """Get risk score with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.business),
                db.joinedload(self.model.source_forecast),
            )
            .filter_by(id=risk_id)
            .first()
        )

    def getLatestByBusiness(self, business_id: int) -> Optional[RiskScore]:
        """Get latest risk score for business"""
        return (
            self.model.query.filter_by(business_id=business_id)
            .order_by(self.model.assessed_at.desc())
            .first()
        )

    def getRiskTrend(self, business_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get risk score trend over time"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        risk_scores = (
            self.model.query.filter(
                self.model.business_id == business_id,
                self.model.assessed_at >= cutoff_date,
            )
            .order_by(self.model.assessed_at.asc())
            .all()
        )

        return [
            {
                "date": score.assessed_at.isoformat(),
                "liquidity_score": float(score.liquidity_score)
                if score.liquidity_score
                else None,
                "cashflow_risk_score": float(score.cashflow_risk_score)
                if score.cashflow_risk_score
                else None,
                "volatility_index": float(score.volatility_index)
                if score.volatility_index
                else None,
                "drawdown_prob": float(score.drawdown_prob)
                if score.drawdown_prob
                else None,
            }
            for score in risk_scores
        ]

    def getAverageRiskScores(
        self, business_id: int, days: int = 30
    ) -> Dict[str, float]:
        """Get average risk scores for business"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = (
            db.session.query(
                db.func.avg(self.model.liquidity_score),
                db.func.avg(self.model.cashflow_risk_score),
                db.func.avg(self.model.volatility_index),
                db.func.avg(self.model.drawdown_prob),
            )
            .filter(
                self.model.business_id == business_id,
                self.model.assessed_at >= cutoff_date,
            )
            .first()
        )

        return {
            "avg_liquidity_score": float(result[0]) if result[0] else 0,
            "avg_cashflow_risk_score": float(result[1]) if result[1] else 0,
            "avg_volatility_index": float(result[2]) if result[2] else 0,
            "avg_drawdown_prob": float(result[3]) if result[3] else 0,
        }
