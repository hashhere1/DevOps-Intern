import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from tests.test_db import override_get_db, TestingSessionLocal
from tests.test_helpers import setup_foreign_keys
from auth.oauth2 import get_current_user
from sqlalchemy.orm import Session
from app.models import Products, Inventory, Suppliers, Categories
import tests.test_db

app.dependency_overrides[get_db] = override_get_db

def override_get_current_user():
    return {"username": "testuser", "user_id": 1}
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_inventory_dependencies():
    db: Session = TestingSessionLocal()

    db.query(Inventory).delete()
    db.query(Products).delete()
    db.query(Categories).delete()
    db.query(Suppliers).delete()

    setup_foreign_keys(db)

    db.close()

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
    assert response.json()["name"] == "Test Product"

def test_get_all_products():
    create_product()
    response = client.get("/products/show")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Test Product"

def test_get_product_by_id():
    response = create_product()
    product_id = response.json()["product_id"]
    response = client.get(f"/products/show/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

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
    assert response.json()["name"] == "Updated Product"

def test_delete_product():
    product_id = create_product().json()["product_id"]
    assert client.delete(f"/products/delete/{product_id}").status_code == 200

    products = client.get("/products/show").json()
    assert not any(p["product_id"] == product_id for p in products)

