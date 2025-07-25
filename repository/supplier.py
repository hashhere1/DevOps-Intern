from app import models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create(request, db: Session):
    supplier = models.Suppliers(name=request.name, phone=request.phone, email=request.email, address=request.address)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier

def show_by_id(supplier_id, db: Session):
    supplier = db.query(models.Suppliers).filter(models.Suppliers.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id '{supplier_id}' not found"
        )
    return supplier

def update(supplier_id, request, db: Session):
    supplier = db.query(models.Suppliers).filter(models.Suppliers.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id '{supplier_id}' not found"
        )
    supplier.name = request.name
    supplier.phone = request.phone
    supplier.email = request.email
    supplier.address = request.address

    db.commit()
    db.refresh(supplier)
    return supplier

def delete(supplier_id, db: Session):
    supplier = db.query(models.Suppliers).filter(models.Suppliers.supplier_id == supplier_id).first()
    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with id '{supplier_id}' not found"
        )
    db.delete(supplier)
    db.commit()
    return f"Supplier with id '{supplier_id}' deleted"