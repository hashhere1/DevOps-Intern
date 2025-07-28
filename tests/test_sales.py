from fastapi.testclient import TestClient
from app.main import app
from app.models import Sales, Products, Users

from tests.test_helpers import db

client = TestClient(app)

def create_sale_payload(product_id, user_id):
    return {
        "product_id": product_id,
        "quantity": 5,
        "selling_price": "30000",
        "user_id": user_id,
        "customer_name": "John Doe"
    }

def test_create_sale(db):
    product = db.query(Products).first()
    user = db.query(Users).first()

    response = client.post("/sales/create", json=create_sale_payload(product.product_id, user.user_id))
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["product_id"] == product.product_id
    assert data["user"]["user_id"] == user.user_id
    assert data["quantity"] == 5
    assert data["customer_name"] == "John Doe"

def test_get_all_sales(db):
    response = client.get("/sales/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_sale_by_id(db):
    sale = db.query(Sales).first()
    response = client.get(f"/sales/{sale.sale_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["sale_id"] == sale.sale_id
    assert "customer_name" in data

def test_update_sale(db):
    sale = db.query(Sales).first()
    product = db.query(Products).first()
    user = db.query(Users).first()

    update_data = {
        "product_id": product.product_id,
        "quantity": 10,
        "selling_price": "31000",
        "user_id": user.user_id,
        "customer_name": "Jane Smith"
    }

    response = client.put(f"/sales/update/{sale.sale_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 10
    assert data["customer_name"] == "Jane Smith"

def test_delete_sale(db):
    sale = db.query(Sales).first()

    response = client.delete(f"/sales/delete/{sale.sale_id}")
    assert response.status_code == 200
    assert "deleted" in response.text.lower()

    # Confirm deletion
    response = client.get(f"/sales/{sale.sale_id}")
    assert response.status_code == 404
