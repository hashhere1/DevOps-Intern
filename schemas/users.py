from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    username: str
    password: str
    role: str


class UpdateUser(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
