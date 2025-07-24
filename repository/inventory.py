from sqlalchemy.orm import Session,joinedload
from app import models
from fastapi import HTTPException, status


def create(request, db: Session):
    check = db.query(models.Products).filter(models.Products.product_id == request.product_id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with product_id '{request.product_id}' not found. Add a product first"
        )
    inventory_item = models.Inventory(product_id=request.product_id, quantity=request.quantity)
    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)

    return inventory_item

def show_by_id(inventory_id, db: Session):
    inventories = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if inventories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The inventory with id '{inventory_id}' not found"
        )
    return inventories

def update(inventory_id, request ,db: Session):
    inventories = db.query(models.Inventory).filter(models.Inventory.inventory_id == inventory_id).first()
    if inventories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The inventory with id '{inventory_id}' not found"
        )
    inventories.product_id = request.product_id
    inventories.quantity = request.quantity

    db.commit()
    db.refresh(inventories)

    return inventories

def delete(inventory_id: int, db: Session):
    inventories = (
        db.query(models.Inventory)
        .options(
            joinedload(models.Inventory.product)
            .joinedload(models.Products.category),
            joinedload(models.Inventory.product)
            .joinedload(models.Products.supplier)
        )
        .filter(models.Inventory.inventory_id == inventory_id)
        .first()
    )

    if inventories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The inventory with id '{inventory_id}' not found"
        )

    db.delete(inventories)
    db.commit()

    return inventories