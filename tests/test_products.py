import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app import models
from tests.test_helpers import db  # your fixture with seeded data



client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_products_and_inventory(db: Session):
    # Clean products and inventory before each test to avoid conflicts
    db.query(models.Inventory).delete()
    db.query(models.Products).delete()
    db.commit()

def create_product():
    response = client.post("/products/create", json={
        "name": "Test Product",
        "description": "Sample description",
        "category_id": 1,
        "supplier_id": 1,
        "cost_price": 10.5,
        "selling_price": 15.0
    })
    return response

def test_create_product():
    response = create_product()
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["category"]["category_id"] == 1
    assert data["supplier"]["supplier_id"] == 1

def test_get_all_products():
    create_product()
    response = client.get("/products/show")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["name"] == "Test Product" for p in data)

def test_get_product_by_id():
    response = create_product()
    product_id = response.json()["product_id"]
    response = client.get(f"/products/show/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id
    assert data["name"] == "Test Product"

def test_update_product():
    response = create_product()
    product_id = response.json()["product_id"]
    response = client.put(f"/products/update/{product_id}", json={
        "name": "Updated Product",
        "description": "Updated description",
        "category_id": 1,
        "supplier_id": 1,
        "cost_price": 12.0,
        "selling_price": 18.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert float(data["cost_price"]) == 12.0
    assert float(data["selling_price"]) == 18.0

def test_delete_product():
    product_id = create_product().json()["product_id"]
    delete_response = client.delete(f"/products/delete/{product_id}")
    assert delete_response.status_code == 200

    response = client.get("/products/show")
    data = response.json()
    assert not any(p["product_id"] == product_id for p in data)
