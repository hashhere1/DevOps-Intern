from app import models
from auth import hashing
from sqlalchemy.orm import Session
from fastapi import HTTPException,status


def create(request, db: Session):
    user = models.Users(username=request.username, password=hashing.hashing(request.password), role=request.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def show_by_id(user_id, db: Session):
    user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found"
        )
    return user

def update(user_id, request, db: Session):
    user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found"
        )
    user.username = request.username
    user.password = request.password
    user.role = request.role

    db.commit()
    db.refresh(user)
    return user

def delete(user_id, db: Session):
    user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found"
        )
    db.delete(user)
    db.commit()
    return f"User with id '{user_id}' deleted"