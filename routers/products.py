from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repository import product
from app import models
from app.database import get_db
from typing import List
from schemas import products
from auth.oauth2 import get_current_user

router = APIRouter(
    tags=["Products"],
    prefix="/products",
    dependencies=[Depends(get_current_user)]
)


@router.post("/create",response_model=products.ProductResponse)
def create(request: products.CreateProduct, db: Session = Depends(get_db)):
    return product.create(request, db)


@router.get("/show",response_model=List[products.ProductResponse])
def show_all(db: Session = Depends(get_db)):
    return db.query(models.Products).all()

@router.get("/show/{product_id}",response_model=products.ProductResponse)
def show(product_id: int, db: Session = Depends(get_db)):
    return product.show_by_id(product_id, db)

@router.put("/update/{product_id}",response_model=products.ProductResponse)
def update(product_id: int, request: products.UpdateProduct, db: Session = Depends(get_db)):
    return product.update(product_id, request, db)

@router.delete("/delete/{product_id}",response_model=products.ProductResponse)
def delete(product_id: int, db: Session = Depends(get_db)):
    return product.delete(product_id, db)

