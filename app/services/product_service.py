from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from exceptions import ResourceNotFoundException, DatabaseException, InvalidOperationException


class ProductService:
    """Servicio para gestionar productos"""
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Crea un nuevo producto"""
        # Verificar que la categoría exista
        from app.services.category_service import CategoryService
        CategoryService.get_category(db, product_data.category_id)
        
        try:
            db_product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                stock=product_data.stock,
                category_id=product_data.category_id
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error creating product: {str(e)}")
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        """Obtiene un producto por ID"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ResourceNotFoundException("Product", product_id)
        return product
    
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None) -> List[Product]:
        """Obtiene todos los productos con paginación y filtro por categoría"""
        query = db.query(Product)
        
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
        """Actualiza un producto existente"""
        product = ProductService.get_product(db, product_id)
        
        # Si se actualiza la categoría, verificar que exista
        if product_data.category_id is not None:
            from app.services.category_service import CategoryService
            CategoryService.get_category(db, product_data.category_id)
        
        try:
            update_data = product_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)
            
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error updating product: {str(e)}")
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Elimina un producto"""
        product = ProductService.get_product(db, product_id)
        
        try:
            db.delete(product)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error deleting product: {str(e)}")
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity: int) -> Product:
        """Actualiza el stock de un producto"""
        product = ProductService.get_product(db, product_id)
        
        new_stock = product.stock + quantity
        if new_stock < 0:
            raise InvalidOperationException("Insufficient stock")
        
        try:
            product.stock = new_stock
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error updating stock: {str(e)}")