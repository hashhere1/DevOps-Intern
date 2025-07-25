from fastapi import APIRouter,Depends
from repository import inventory
from auth.oauth2 import get_current_user
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from schemas import inventories
from typing import List


router = APIRouter(
    tags=["Inventory"],
    prefix="/inventory",
    dependencies=[Depends(get_current_user)]
)


@router.post("/create", response_model=inventories.InventoryResponse)
def create(request: inventories.CreateInventory, db: Session = Depends(get_db)):
    return inventory.create(request, db)

@router.get("/",response_model=List[inventories.InventoryResponse])
def show(db: Session = Depends(get_db)):
    return db.query(models.Inventory).all()

@router.get("/{inventory_id}",response_model=inventories.InventoryResponse)
def show_by_id(inventory_id: int, db: Session = Depends(get_db)):
    return inventory.show_by_id(inventory_id, db)

@router.put("/update/{inventory_id}",response_model=inventories.InventoryResponse)
def update(inventory_id: int, request: inventories.UpdateInventory, db: Session = Depends(get_db)):
    return inventory.update(inventory_id, request, db)

@router.delete("/delete/{inventory_id}",response_model=inventories.InventoryResponse)
def delete(inventory_id: int, db: Session = Depends(get_db)):
    return inventory.delete(inventory_id, db)