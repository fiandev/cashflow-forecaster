from models import User
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def findByEmail(self, email: str) -> Optional[User]:
        """Find user by email"""
        return self.find_first_by(email=email)

    def findByRole(self, role: str) -> List[User]:
        """Find users by role"""
        return self.find_by(role=role)

    def createWithPassword(self, data: Dict[str, Any], password: str) -> User:
        """Create user with password hash"""
        user_data = data.copy()
        user_data["password_hash"] = password
        return self.create(user_data)

    def updateLastLogin(self, user_id: int) -> Optional[User]:
        """Update user last login"""
        from datetime import datetime

        return self.update(user_id, {"last_login": datetime.utcnow()})

    def search(self, query: str) -> List[User]:
        """Search users by name or email"""
        return self.model.query.filter(
            (self.model.name.like(f"%{query}%")) | (self.model.email.like(f"%{query}%"))
        ).all()

    def getWithBusinesses(self, user_id: int) -> Optional[User]:
        """Get user with their businesses"""
        return (
            self.model.query.options(db.joinedload(self.model.businesses))
            .filter_by(id=user_id)
            .first()
        )

    def getWithScenarios(self, user_id: int) -> Optional[User]:
        """Get user with their scenarios"""
        return (
            self.model.query.options(db.joinedload(self.model.scenarios))
            .filter_by(id=user_id)
            .first()
        )
