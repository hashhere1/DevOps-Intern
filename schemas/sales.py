from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

from schemas.products import ProductResponse
from schemas.users import UserResponse


class CreateSales(BaseModel):
    product_id: int
    quantity: int
    selling_price: Decimal
    user_id: int
    customer_name: str

class UpdateSale(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    selling_price: Optional[Decimal] = None
    user_id: Optional[int] = None
    customer_name: Optional[str] = None

class SaleResponse(BaseModel):
    sale_id: int
    quantity: int
    selling_price: Decimal
    sale_date: datetime
    customer_name: str

    product: ProductResponse
    user: UserResponse

    class Config:
        from_attributes = True
