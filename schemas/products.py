from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime

from schemas.categories import CategoryResponse
from schemas.suppliers import SupplierResponse


class CreateProduct(BaseModel):
    name: str
    description: str
    category_id: int
    supplier_id: int
    cost_price: Decimal
    selling_price: Decimal

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    cost_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None

class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: str
    cost_price: Decimal
    selling_price: Decimal
    added_at: datetime

    category: CategoryResponse
    supplier: SupplierResponse

    model_config = ConfigDict(from_attributes=True)
