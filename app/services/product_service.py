from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.product import Product
from ..models.category import Category
from ..schemas.product import ProductCreate, ProductUpdate
from ..exceptions import NotFoundException, BadRequestException


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ProductCreate) -> Product:
        category = self.db.query(Category).get(payload.category_id)
        if not category:
            raise BadRequestException(detail=f"Categoría {payload.category_id} no existe")

        product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            stock=payload.stock,
            category_id=payload.category_id,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).order_by(Product.id).all()

    def get_or_404(self, product_id: int) -> Product:
        product = self.db.query(Product).get(product_id)
        if not product:
            raise NotFoundException(detail=f"Producto con id {product_id} no encontrado")
        return product

    def update(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get_or_404(product_id)

        if payload.name is not None:
            product.name = payload.name
        if payload.description is not None:
            product.description = payload.description
        if payload.price is not None:
            product.price = payload.price
        if payload.stock is not None:
            product.stock = payload.stock
        if payload.category_id is not None:
            cat = self.db.query(Category).get(payload.category_id)
            if not cat:
                raise BadRequestException(detail=f"Categoría {payload.category_id} no existe")
            product.category_id = payload.category_id

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        product = self.get_or_404(product_id)
        self.db.delete(product)
        self.db.commit()
