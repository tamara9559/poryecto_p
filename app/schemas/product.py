from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    stock: int = Field(..., ge=0, description="Cantidad en stock")
    category_id: int = Field(..., description="ID de la categoría")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    
    class Config:
        from_attributes = True


class ProductWithCategory(ProductResponse):
    category: dict = {}
    
    class Config:
        from_attributes = True