from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from exceptions import ResourceNotFoundException, DuplicateResourceException, DatabaseException


class CategoryService:
    """Servicio para gestionar categorías"""
    
    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate) -> Category:
        """Crea una nueva categoría"""
        try:
            db_category = Category(name=category_data.name)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return db_category
        except IntegrityError:
            db.rollback()
            raise DuplicateResourceException("Category", "name", category_data.name)
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error creating category: {str(e)}")
    
    @staticmethod
    def get_category(db: Session, category_id: int) -> Category:
        """Obtiene una categoría por ID"""
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise ResourceNotFoundException("Category", category_id)
        return category
    
    @staticmethod
    def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtiene todas las categorías con paginación"""
        return db.query(Category).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_category(db: Session, category_id: int, category_data: CategoryUpdate) -> Category:
        """Actualiza una categoría existente"""
        category = CategoryService.get_category(db, category_id)
        
        try:
            if category_data.name is not None:
                category.name = category_data.name
            
            db.commit()
            db.refresh(category)
            return category
        except IntegrityError:
            db.rollback()
            raise DuplicateResourceException("Category", "name", category_data.name)
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error updating category: {str(e)}")
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        """Elimina una categoría"""
        category = CategoryService.get_category(db, category_id)
        
        try:
            db.delete(category)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error deleting category: {str(e)}")
    
    @staticmethod
    def get_category_by_name(db: Session, name: str) -> Optional[Category]:
        """Obtiene una categoría por nombre"""
        return db.query(Category).filter(Category.name == name).first()