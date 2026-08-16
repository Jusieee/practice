from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class CartItemCreate(BaseModel):
    product_id: int = Field(
        gt=0,
        description="ID товара",
    )
    quantity: int = Field(
        gt=0,
        description="Количество товара",
    )


class ProductUpdate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    total_price: float


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float