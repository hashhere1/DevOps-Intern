from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from repository import supplier
from app import models
from app.database import get_db
from schemas import suppliers
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    tags=["Suppliers"],
    prefix="/suppliers",
    dependencies=[Depends(get_current_user)]
)

@router.post("/create", response_model=suppliers.SupplierResponse)
def create(request: suppliers.CreateSupplier, db: Session = Depends(get_db)):
    return supplier.create(request, db)

@router.get("/", response_model=List[suppliers.SupplierResponse])
def show(db: Session = Depends(get_db)):
   return db.query(models.Suppliers).all()

@router.get("/by_id/{supplier_id}", response_model=suppliers.SupplierResponse)
def show_by_id(supplier_id: int, db: Session = Depends(get_db)):
    return supplier.show_by_id(supplier_id, db)

@router.put("/update/{supplier_id}", response_model=suppliers.SupplierResponse)
def update(supplier_id: int, request: suppliers.UpdateSupplier, db: Session = Depends(get_db)):
    return supplier.update(supplier_id, request, db)

@router.delete("/delete/{supplier_id}", response_model=suppliers.SupplierResponse)
def delete(supplier_id: int, db: Session = Depends(get_db)):
    return supplier.delete(supplier_id, db)

