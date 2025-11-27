from pydantic import BaseModel, Field, confloat, conint
from typing import Optional
from category import CategoryRead


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: confloat(ge=0) = 0.0
    stock: conint(ge=0) = 0


class ProductCreate(ProductBase):
    category_id: int = Field(..., gt=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[confloat(ge=0)] = None
    stock: Optional[conint(ge=0)] = None
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    category: CategoryRead

    model_config = {"from_attributes": True}
