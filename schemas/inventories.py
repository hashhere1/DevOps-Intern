from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from schemas.products import ProductResponse


class CreateInventory(BaseModel):
    product_id: int
    quantity: int

class UpdateInventory(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class InventoryResponse(BaseModel):
    inventory_id: int
    quantity: int
    last_updated: datetime

    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)
