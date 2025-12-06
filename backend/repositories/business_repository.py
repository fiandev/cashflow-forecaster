from models import Business, User
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any


class BusinessRepository(BaseRepository):
    def __init__(self):
        super().__init__(Business)

    def findByOwner(self, owner_id: int) -> List[Business]:
        """Find businesses by owner"""
        return self.find_by(owner_id=owner_id)

    def findByCountry(self, country: str) -> List[Business]:
        """Find businesses by country"""
        return self.find_by(country=country)

    def findByCity(self, city: str) -> List[Business]:
        """Find businesses by city"""
        return self.find_by(city=city)

    def findByCurrency(self, currency: str) -> List[Business]:
        """Find businesses by currency"""
        return self.find_by(currency=currency)

    def createWithOwner(self, data: Dict[str, Any], owner_id: int) -> Business:
        """Create business with owner"""
        business_data = data.copy()
        business_data["owner_id"] = owner_id
        return self.create(business_data)

    def updateSettings(
        self, business_id: int, settings: Dict[str, Any]
    ) -> Optional[Business]:
        """Update business settings"""
        return self.update(business_id, {"settings": settings})

    def search(self, query: str) -> List[Business]:
        """Search businesses by name"""
        return self.model.query.filter(self.model.name.like(f"%{query}%")).all()

    def getWithCategories(self, business_id: int) -> Optional[Business]:
        """Get business with categories"""
        return (
            self.model.query.options(db.joinedload(self.model.categories))
            .filter_by(id=business_id)
            .first()
        )

    def getWithTransactions(self, business_id: int) -> Optional[Business]:
        """Get business with transactions"""
        return (
            self.model.query.options(db.joinedload(self.model.transactions))
            .filter_by(id=business_id)
            .first()
        )

    def getWithOwner(self, business_id: int) -> Optional[Business]:
        """Get business with owner"""
        return (
            self.model.query.options(db.joinedload(self.model.owner))
            .filter_by(id=business_id)
            .first()
        )

    def getWithAllRelations(self, business_id: int) -> Optional[Business]:
        """Get business with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.owner),
                db.joinedload(self.model.categories),
                db.joinedload(self.model.transactions),
                db.joinedload(self.model.forecasts),
                db.joinedload(self.model.alerts),
            )
            .filter_by(id=business_id)
            .first()
        )
