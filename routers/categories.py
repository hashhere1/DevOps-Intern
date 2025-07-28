from fastapi import APIRouter, Depends
from repository import category
from app import models
from schemas import categories
from app.database import get_db
from typing import List
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user

router = APIRouter(
    tags=["Categories"],
    prefix="/category",
    # dependencies=[Depends(get_current_user)]
)


@router.post("/create", response_model=categories.CategoryResponse)
def create(request: categories.CreateCategory, db: Session = Depends(get_db)):
    return category.create(request, db)


@router.get("/", response_model=List[categories.CategoryResponse])
def show(db: Session = Depends(get_db)):
    return db.query(models.Categories).all()


@router.get("/by_id/{category_id}", response_model=categories.CategoryResponse)
def show_by_id(category_id: int, db: Session = Depends(get_db)):
    return category.show_by_id(category_id, db)

@router.put("/update/{category_id}",response_model=categories.CategoryResponse)
def update(category_id: int, request: categories.UpdateCategory, db: Session = Depends(get_db)):
    return category.update(category_id, request, db)

@router.delete("/delete/{category_id}", response_model=categories.CategoryResponse)
def delete(category_id: int, db: Session = Depends(get_db)):
    return category.delete(category_id, db)