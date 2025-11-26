from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la categoría")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True


class CategoryWithProducts(CategoryResponse):
    products: list = []
    
    class Config:
        from_attributes = True