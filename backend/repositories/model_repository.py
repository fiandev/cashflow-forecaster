from models import Model, Business
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from datetime import datetime


class ModelRepository(BaseRepository):
    def __init__(self):
        super().__init__(Model)

    def findByBusiness(self, business_id: int) -> List[Model]:
        """Find models by business"""
        return self.find_by(business_id=business_id)

    def findByType(self, model_type: str) -> List[Model]:
        """Find models by type"""
        return self.find_by(model_type=model_type)

    def findByBusinessAndType(self, business_id: int, model_type: str) -> List[Model]:
        """Find models by business and type"""
        return self.model.query.filter_by(
            business_id=business_id, model_type=model_type
        ).all()

    def findByVersion(self, version: str) -> List[Model]:
        """Find models by version"""
        return self.find_by(version=version)

    def findRecentlyTrained(self, business_id: int, days: int = 30) -> List[Model]:
        """Find recently trained models"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.last_trained_at >= cutoff_date,
        ).all()

    def findNotRecentlyTrained(self, business_id: int, days: int = 30) -> List[Model]:
        """Find models not recently trained"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.model.query.filter(
            self.model.business_id == business_id,
            db.or_(
                self.model.last_trained_at.is_(None),
                self.model.last_trained_at < cutoff_date,
            ),
        ).all()

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> Model:
        """Create model with business"""
        model_data = data.copy()
        model_data["business_id"] = business_id
        return self.create(model_data)

    def updateTrainingDate(self, model_id: int) -> Optional[Model]:
        """Update model training date"""
        return self.update(model_id, {"last_trained_at": datetime.utcnow()})

    def updateParams(self, model_id: int, params: Dict[str, Any]) -> Optional[Model]:
        """Update model parameters"""
        return self.update(model_id, {"params": params})

    def updateVersion(self, model_id: int, version: str) -> Optional[Model]:
        """Update model version"""
        return self.update(model_id, {"version": version})

    def search(self, business_id: int, query: str) -> List[Model]:
        """Search models by name"""
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.name.like(f"%{query}%")
        ).all()

    def getWithBusiness(self, model_id: int) -> Optional[Model]:
        """Get model with business"""
        return (
            self.model.query.options(db.joinedload(self.model.business))
            .filter_by(id=model_id)
            .first()
        )

    def getWithModelRuns(self, model_id: int) -> Optional[Model]:
        """Get model with model runs"""
        return (
            self.model.query.options(db.joinedload(self.model.model_runs))
            .filter_by(id=model_id)
            .first()
        )

    def getWithForecasts(self, model_id: int) -> Optional[Model]:
        """Get model with forecasts"""
        return (
            self.model.query.options(db.joinedload(self.model.forecasts))
            .filter_by(id=model_id)
            .first()
        )

    def getWithAllRelations(self, model_id: int) -> Optional[Model]:
        """Get model with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.business),
                db.joinedload(self.model.model_runs),
                db.joinedload(self.model.forecasts),
            )
            .filter_by(id=model_id)
            .first()
        )

    def getGlobalModels(self) -> List[Model]:
        """Get models not associated with specific business"""
        return self.find_by(business_id=None)

    def getActiveModels(self, business_id: int) -> List[Model]:
        """Get active models (recently trained)"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=90)
        return self.model.query.filter(
            self.model.business_id == business_id,
            self.model.last_trained_at >= cutoff_date,
        ).all()

    def getModelTypes(self, business_id: int) -> List[str]:
        """Get distinct model types for business"""
        result = (
            db.session.query(self.model.model_type)
            .filter_by(business_id=business_id)
            .distinct()
            .all()
        )
        return [row[0] for row in result]
