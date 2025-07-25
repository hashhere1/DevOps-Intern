from sqlalchemy.orm import Session
from app.models import Categories, Suppliers, Products
from datetime import datetime
from decimal import Decimal

def setup_foreign_keys(db: Session):
    category = Categories(name="TestCategory", description="Test Desc")
    supplier = Suppliers(name="TestSupplier", phone="1234567890", email="test@supplier.com", address="Somewhere")

    db.add(category)
    db.add(supplier)
    db.commit()

    product = Products(
        name="Test Product",
        description="Test Desc",
        category_id=category.category_id,
        supplier_id=supplier.supplier_id,
        cost_price=Decimal("10.0"),
        selling_price=Decimal("15.0"),
        added_at=datetime.utcnow()
    )
    db.add(product)

    db.commit()

