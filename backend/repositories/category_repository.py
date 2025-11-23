from models import Category, Business
from repositories.base_repository import BaseRepository
from typing import List, Optional, Dict, Any


class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Category)

    def findByBusiness(self, business_id: int) -> List[Category]:
        """Find categories by business"""
        return self.find_by(business_id=business_id)

    def findByType(self, category_type: str) -> List[Category]:
        """Find categories by type"""
        return self.find_by(type=category_type)

    def findByBusinessAndType(
        self, business_id: int, category_type: str
    ) -> List[Category]:
        """Find categories by business and type"""
        return self.model.query.filter_by(
            business_id=business_id, type=category_type
        ).all()

    def findRootCategories(self, business_id: int) -> List[Category]:
        """Find root categories (no parent)"""
        return self.model.query.filter_by(business_id=business_id, parent_id=None).all()

    def findChildCategories(self, parent_id: int) -> List[Category]:
        """Find child categories"""
        return self.find_by(parent_id=parent_id)

    def createWithBusiness(self, data: Dict[str, Any], business_id: int) -> Category:
        """Create category with business"""
        category_data = data.copy()
        category_data["business_id"] = business_id
        return self.create(category_data)

    def createChild(self, data: Dict[str, Any], parent_id: int) -> Category:
        """Create child category"""
        category_data = data.copy()
        category_data["parent_id"] = parent_id
        return self.create(category_data)

    def search(self, business_id: int, query: str) -> List[Category]:
        """Search categories by name within business"""
        return self.model.query.filter(
            self.model.business_id == business_id, self.model.name.like(f"%{query}%")
        ).all()

    def getWithParent(self, category_id: int) -> Optional[Category]:
        """Get category with parent"""
        return (
            self.model.query.options(db.joinedload(self.model.parent))
            .filter_by(id=category_id)
            .first()
        )

    def getWithChildren(self, category_id: int) -> Optional[Category]:
        """Get category with children"""
        return (
            self.model.query.options(db.joinedload(self.model.children))
            .filter_by(id=category_id)
            .first()
        )

    def getWithTransactions(self, category_id: int) -> Optional[Category]:
        """Get category with transactions"""
        return (
            self.model.query.options(db.joinedload(self.model.transactions))
            .filter_by(id=category_id)
            .first()
        )

    def getWithAllRelations(self, category_id: int) -> Optional[Category]:
        """Get category with all relationships"""
        return (
            self.model.query.options(
                db.joinedload(self.model.parent),
                db.joinedload(self.model.children),
                db.joinedload(self.model.transactions),
                db.joinedload(self.model.business),
            )
            .filter_by(id=category_id)
            .first()
        )

    def getIncomeCategories(self, business_id: int) -> List[Category]:
        """Get income categories for business"""
        return self.findByBusinessAndType(business_id, "income")

    def getExpenseCategories(self, business_id: int) -> List[Category]:
        """Get expense categories for business"""
        return self.findByBusinessAndType(business_id, "expense")
