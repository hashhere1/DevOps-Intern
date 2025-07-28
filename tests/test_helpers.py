import pytest
from tests.conftest import TestingSessionLocal, engine
from app.models import Base, Categories, Suppliers, Users, Products, Sales
from datetime import datetime

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        # Setup
        category = Categories(name="Electronics", description="All gadgets")
        supplier = Suppliers(name="Hassaan", phone="0319", email="hassaan@gmail.com", address="Lahore")
        user = Users(username="hassaan@gmail.com",password= "testuser123" ,role="Distributor", created_at=datetime.utcnow())

        session.add_all([category, supplier, user])
        session.commit()

        product = Products(
            name="Phone",
            description="Samsung",
            cost_price="25000",
            selling_price="30000",
            added_at=datetime.utcnow(),
            category_id=category.category_id,
            supplier_id=supplier.supplier_id
        )
        session.add(product)
        session.commit()

        sale = Sales(
            quantity=0,
            selling_price="30000",
            sale_date=datetime.utcnow(),
            customer_name="Hash",
            product_id=product.product_id,
            user_id=user.user_id
        )
        session.add(sale)
        session.commit()

        yield session  # used in tests

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
