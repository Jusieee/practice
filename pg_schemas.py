from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)