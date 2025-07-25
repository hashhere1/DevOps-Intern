from fastapi import APIRouter, Depends
from schemas import users
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from typing import List
from repository import user
from auth.oauth2 import get_current_user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post("/create", response_model=users.UserResponse)
def create(request: users.CreateUser, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/show", response_model=List[users.UserResponse])
def show_all(db: Session = Depends(get_db),current_user: users = Depends(get_current_user)):
    return db.query(models.Users).all()


@router.get("/show_by_id/{user_id}", response_model=users.UserResponse)
def show(user_id: int, db: Session = Depends(get_db),current_user: users = Depends(get_current_user)):
    return user.show_by_id(user_id, db)


@router.put("/update/{user_id}", response_model=users.UserResponse)
def update(user_id: int, request: users.UpdateUser, db: Session = Depends(get_db),current_user: users = Depends(get_current_user)):
    return user.update(user_id, request, db)


@router.delete("/delete/{user_id}", response_model=users.UserResponse)
def delete(user_id: int, db: Session = Depends(get_db),current_user: users = Depends(get_current_user)):
    return user.delete(user_id, db)
