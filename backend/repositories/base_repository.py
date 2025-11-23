from flask_sqlalchemy import SQLAlchemy
from models import db
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal


class BaseRepository:
    def __init__(self, model):
        self.model = model
        self.db = db

    def all(self) -> List[Any]:
        """Get all records"""
        return self.model.query.all()

    def find(self, id: int) -> Optional[Any]:
        """Find record by ID"""
        return self.model.query.get(id)

    def find_by(self, **kwargs) -> List[Any]:
        """Find records by criteria"""
        return self.model.query.filter_by(**kwargs).all()

    def find_first_by(self, **kwargs) -> Optional[Any]:
        """Find first record by criteria"""
        return self.model.query.filter_by(**kwargs).first()

    def create(self, data: Dict[str, Any]) -> Any:
        """Create new record"""
        instance = self.model(**data)
        self.db.session.add(instance)
        self.db.session.commit()
        return instance

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        """Update record by ID"""
        instance = self.find(id)
        if not instance:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.db.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        """Delete record by ID"""
        instance = self.find(id)
        if not instance:
            return False

        self.db.session.delete(instance)
        self.db.session.commit()
        return True

    def where(
        self, column: str, operator: str = "=", value: Any = None
    ) -> "BaseRepository":
        """Add where clause (chainable)"""
        if operator == "=":
            self.query = self.model.query.filter(getattr(self.model, column) == value)
        elif operator == "!=":
            self.query = self.model.query.filter(getattr(self.model, column) != value)
        elif operator == ">":
            self.query = self.model.query.filter(getattr(self.model, column) > value)
        elif operator == "<":
            self.query = self.model.query.filter(getattr(self.model, column) < value)
        elif operator == ">=":
            self.query = self.model.query.filter(getattr(self.model, column) >= value)
        elif operator == "<=":
            self.query = self.model.query.filter(getattr(self.model, column) <= value)
        elif operator == "like":
            self.query = self.model.query.filter(
                getattr(self.model, column).like(value)
            )
        elif operator == "in":
            self.query = self.model.query.filter(getattr(self.model, column).in_(value))

        return self

    def where_in(self, column: str, values: List[Any]) -> "BaseRepository":
        """Add where in clause"""
        self.query = self.model.query.filter(getattr(self.model, column).in_(values))
        return self

    def where_null(self, column: str) -> "BaseRepository":
        """Add where null clause"""
        self.query = self.model.query.filter(getattr(self.model, column).is_(None))
        return self

    def where_not_null(self, column: str) -> "BaseRepository":
        """Add where not null clause"""
        self.query = self.model.query.filter(getattr(self.model, column).isnot(None))
        return self

    def order_by(self, column: str, direction: str = "asc") -> "BaseRepository":
        """Add order by clause"""
        if direction.lower() == "desc":
            self.query = self.query.order_by(getattr(self.model, column).desc())
        else:
            self.query = self.query.order_by(getattr(self.model, column).asc())
        return self

    def limit(self, limit: int) -> "BaseRepository":
        """Add limit clause"""
        self.query = self.query.limit(limit)
        return self

    def offset(self, offset: int) -> "BaseRepository":
        """Add offset clause"""
        self.query = self.query.offset(offset)
        return self

    def get(self) -> List[Any]:
        """Get results from query"""
        if hasattr(self, "query"):
            return self.query.all()
        return self.all()

    def first(self) -> Optional[Any]:
        """Get first result from query"""
        if hasattr(self, "query"):
            return self.query.first()
        return self.model.query.first()

    def count(self) -> int:
        """Count records"""
        if hasattr(self, "query"):
            return self.query.count()
        return self.model.query.count()

    def exists(self, **kwargs) -> bool:
        """Check if record exists"""
        return self.model.query.filter_by(**kwargs).first() is not None

    def paginate(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        """Paginate results"""
        if hasattr(self, "query"):
            paginated = self.query.paginate(
                page=page, per_page=per_page, error_out=False
            )
        else:
            paginated = self.model.query.paginate(
                page=page, per_page=per_page, error_out=False
            )

        return {
            "data": paginated.items,
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        }

    def with_relations(self, *relations) -> "BaseRepository":
        """Eager load relationships"""
        self.query = self.model.query.options(*relations)
        return self

    def to_dict(self, instance: Any) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        result = {}
        for column in instance.__table__.columns:
            value = getattr(instance, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, date):
                result[column.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[column.name] = float(value)
            else:
                result[column.name] = value
        return result

    def to_dict_list(self, instances: List[Any]) -> List[Dict[str, Any]]:
        """Convert list of instances to list of dictionaries"""
        return [self.to_dict(instance) for instance in instances]
