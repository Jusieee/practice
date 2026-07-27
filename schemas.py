from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)