from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateSupplier(BaseModel):
    name: str
    phone: str
    email: str
    address: str

class UpdateSupplier(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class SupplierResponse(BaseModel):
    supplier_id: int
    name: str
    phone: str
    email: str
    address: str

    model_config = ConfigDict(from_attributes=True)
