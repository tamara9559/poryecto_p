from sqlalchemy.orm import Session
from typing import List

from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate
from ..exceptions import NotFoundException, ConflictException


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: CategoryCreate) -> Category:
        # evitar duplicados por nombre
        existing = self.db.query(Category).filter(Category.name == payload.name).first()
        if existing:
            raise ConflictException(detail="Ya existe una categoría con ese nombre")

        category = Category(name=payload.name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def list_all(self) -> List[Category]:
        return self.db.query(Category).order_by(Category.id).all()

    def get_or_404(self, category_id: int) -> Category:
        category = self.db.query(Category).get(category_id)
        if not category:
            raise NotFoundException(detail=f"Categoría con id {category_id} no encontrada")
        return category

    def update(self, category_id: int, payload: CategoryUpdate) -> Category:
        category = self.get_or_404(category_id)
        if payload.name is not None:
            # check uniqueness
            exists = (
                self.db.query(Category)
                .filter(Category.name == payload.name)
                .filter(Category.id != category_id)
                .first()
            )
            if exists:
                raise ConflictException(detail="Otro registro ya usa ese nombre")
            category.name = payload.name
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_or_404(category_id)
        self.db.delete(category)
        self.db.commit()
