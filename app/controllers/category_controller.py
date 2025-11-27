from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from ..services.category_service import CategoryService

router = APIRouter()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(payload)


@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.list_all()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_or_404(category_id)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    service.delete(category_id)
    return None
