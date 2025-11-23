from models import ModelRun, Model
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any
from datetime import datetime


class ModelRunRepository(BaseRepository):
    def __init__(self):
        super().__init__(ModelRun)

    def findByModel(self, model_id: int) -> List[ModelRun]:
        """Find model runs by model"""
        return self.find_by(model_id=model_id)

    def findByStatus(self, run_status: str) -> List[ModelRun]:
        """Find model runs by status"""
        return self.find_by(run_status=run_status)

    def findByModelAndStatus(self, model_id: int, run_status: str) -> List[ModelRun]:
        """Find model runs by model and status"""
        return self.model.query.filter_by(
            model_id=model_id, run_status=run_status
        ).all()

    def findRecent(self, model_id: int, hours: int = 24) -> List[ModelRun]:
        """Find recent model runs"""
        from datetime import datetime, timedelta

        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return self.model.query.filter(
            self.model.model_id == model_id, self.model.run_at >= cutoff_time
        ).all()

    def findSuccessful(self, model_id: int) -> List[ModelRun]:
        """Find successful model runs"""
        return self.findByModelAndStatus(model_id, "completed")

    def findFailed(self, model_id: int) -> List[ModelRun]:
        """Find failed model runs"""
        return self.findByModelAndStatus(model_id, "failed")

    def findRunning(self, model_id: int) -> List[ModelRun]:
        """Find running model runs"""
        return self.findByModelAndStatus(model_id, "running")

    def createWithModel(self, data: Dict[str, Any], model_id: int) -> ModelRun:
        """Create model run with model"""
        run_data = data.copy()
        run_data["model_id"] = model_id
        return self.create(run_data)

    def updateStatus(self, run_id: int, status: str) -> Optional[ModelRun]:
        """Update model run status"""
        return self.update(run_id, {"run_status": status})

    def updateInputSummary(
        self, run_id: int, input_summary: Dict[str, Any]
    ) -> Optional[ModelRun]:
        """Update input summary"""
        return self.update(run_id, {"input_summary": input_summary})

    def updateOutputSummary(
        self, run_id: int, output_summary: Dict[str, Any]
    ) -> Optional[ModelRun]:
        """Update output summary"""
        return self.update(run_id, {"output_summary": output_summary})

    def updateNotes(self, run_id: int, notes: str) -> Optional[ModelRun]:
        """Update notes"""
        return self.update(run_id, {"notes": notes})

    def search(self, model_id: int, query: str) -> List[ModelRun]:
        """Search model runs by notes"""
        return self.model.query.filter(
            self.model.model_id == model_id, self.model.notes.like(f"%{query}%")
        ).all()

    def getWithModel(self, run_id: int) -> Optional[ModelRun]:
        """Get model run with model"""
        return (
            self.model.query.options(db.joinedload(self.model.model))
            .filter_by(id=run_id)
            .first()
        )

    def getWithForecasts(self, run_id: int) -> Optional[ModelRun]:
        """Get model run with forecasts"""
        return (
            self.model.query.options(db.joinedload(self.model.forecasts))
            .filter_by(id=run_id)
            .first()
        )

    def getWithAllRelations(self, run_id: int) -> Optional[ModelRun]:
        """Get model run with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.model), db.joinedload(self.model.forecasts)
            )
            .filter_by(id=run_id)
            .first()
        )

    def getLatestRun(self, model_id: int) -> Optional[ModelRun]:
        """Get latest model run"""
        return (
            self.model.query.filter_by(model_id=model_id)
            .order_by(self.model.run_at.desc())
            .first()
        )

    def getRunStats(self, model_id: int) -> Dict[str, Any]:
        """Get model run statistics"""
        total_runs = self.model.query.filter_by(model_id=model_id).count()
        successful_runs = self.model.query.filter_by(
            model_id=model_id, run_status="completed"
        ).count()
        failed_runs = self.model.query.filter_by(
            model_id=model_id, run_status="failed"
        ).count()

        return {
            "total": total_runs,
            "successful": successful_runs,
            "failed": failed_runs,
            "success_rate": (successful_runs / total_runs * 100)
            if total_runs > 0
            else 0,
        }

    def getRunsByDateRange(
        self, model_id: int, start_date: datetime, end_date: datetime
    ) -> List[ModelRun]:
        """Get model runs within date range"""
        return self.model.query.filter(
            self.model.model_id == model_id,
            self.model.run_at >= start_date,
            self.model.run_at <= end_date,
        ).all()
