from app import models
from fastapi import HTTPException,status
from sqlalchemy.orm import Session

def create(request, db: Session):
    category = models.Categories(name=request.name, description=request.description)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def show_by_id(category_id, db: Session):
    category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id '{category_id}' not found"
        )
    return category

def update(category_id, request, db: Session):
    update_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if update_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id '{category_id}' not found"
        )
    update_category.name = request.name
    update_category.description = request.description

    db.commit()
    db.refresh(update_category)
    return update_category

def delete(category_id, db: Session):
    delete_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if delete_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id '{category_id}' not found"
        )
    db.delete(delete_category)
    db.commit()
    return delete_category