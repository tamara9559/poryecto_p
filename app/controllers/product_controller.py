from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.product import ProductCreate, ProductRead, ProductUpdate
from ..services.product_service import ProductService

router = APIRouter()


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create(payload)


@router.get("/", response_model=List[ProductRead])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.list_all(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_or_404(product_id)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.update(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    service.delete(product_id)
    return None
