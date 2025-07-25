from pydantic import BaseModel
from typing import Optional

class CreateCategory(BaseModel):
    name: str
    description: str


class UpdateCategory(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    description: str

    class Config:
        from_attributes = True


