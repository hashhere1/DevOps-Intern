from pydantic import BaseModel
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

    class Config:
        from_attributes = True
