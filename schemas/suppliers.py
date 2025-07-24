from pydantic import BaseModel
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

    class Config:
        from_attributes = True
