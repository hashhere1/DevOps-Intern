from app import models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create(request, db: Session):
    check_product = db.query(models.Products).filter(models.Products.product_id == request.product_id).first()
    if check_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product with id '{request.product_id}' not found"
        )
    check_user = db.query(models.Users).filter(models.Users.user_id == request.user_id).first()
    if check_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id '{request.user_id}' not found"
        )
    add_sales = models.Sales(product_id=request.product_id, quantity=request.quantity, user_id=request.user_id,
                             selling_price=request.selling_price, customer_name=request.customer_name)
    db.add(add_sales)
    db.commit()
    db.refresh(add_sales)

    return add_sales

def show_by_id(sales_id, db: Session):
    show_sales = db.query(models.Sales).filter(models.Sales.sale_id == sales_id).first()
    if show_sales is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Sale with id '{sales_id}' not found"
        )
    return show_sales

def update(sale_id, request ,db: Session):
    update_sale = db.query(models.Sales).filter(models.Sales.sale_id == sale_id).first()
    if update_sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Sales with id '{sale_id}' not found"
        )
    update_sale.product_id = request.product_id
    update_sale.quantity = request.quantity
    update_sale.selling_price = request.selling_price
    update_sale.user_id = request.user_id
    update_sale.customer_name = request.customer_name

    db.commit()
    db.refresh(update_sale)
    return update_sale

def delete(sale_id, db: Session):
    delete_sale = db.query(models.Sales).filter(models.Sales.sale_id == sale_id).first()
    if delete_sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The sale with id '{sale_id}' not found"
        )
    db.delete(delete_sale)
    db.commit()

    return f"The sale with id '{sale_id}' deleted"
