from fastapi import HTTPException, status
from app import models
from sqlalchemy.orm import Session

def create(request, db: Session):
    check = db.query(models.Suppliers).filter(models.Suppliers.supplier_id == request.supplier_id).first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The supplier with id '{request.supplier_id}' not created. Add a Supplier First!"
        )
    check2 = db.query(models.Categories).filter(models.Categories.category_id == request.category_id).first()
    if check2 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The category with id '{request.category_id}' not created. Add a Category First!"
        )
    product = models.Products(name=request.name, description=request.description, category_id=request.category_id,
                              supplier_id=request.supplier_id, cost_price=request.cost_price,
                              selling_price=request.selling_price)
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def show_by_id(product_id, db: Session):
    product = db.query(models.Products).filter(models.Products.product_id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product with id '{product_id}' not found"
        )
    return product

def update(product_id, request, db: Session):
    update_product = db.query(models.Products).filter(models.Products.product_id == product_id).first()
    if update_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product with id '{product_id}' not found"
        )
    category_exists = db.query(models.Categories).filter(models.Categories.category_id == request.category_id).first()
    if category_exists is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with id '{request.category_id}' does not exist"
        )


    supplier_exists = db.query(models.Suppliers).filter(models.Suppliers.supplier_id == request.supplier_id).first()
    if supplier_exists is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Supplier with id '{request.supplier_id}' does not exist"
        )
    update_product.name = request.name
    update_product.description = request.description
    update_product.category_id = request.category_id
    update_product.supplier_id = request.supplier_id
    update_product.cost_price = request.cost_price
    update_product.selling_price = request.selling_price

    db.commit()
    db.refresh(update_product)
    return update_product

def delete(product_id, db: Session):
    delete_product = db.query(models.Products).filter(models.Products.product_id == product_id).first()
    if delete_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product with id '{product_id}' not found"
        )
    db.delete(delete_product)
    db.commit()

    return f"The product with id '{product_id}' deleted"