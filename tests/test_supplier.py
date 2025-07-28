import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_helpers import db as test_db  # your fixture with initial data
from app.models import Suppliers

client = TestClient(app)

# Use existing supplier from test_helpers
@pytest.fixture
def existing_supplier(test_db):
    return test_db.query(Suppliers).first()

# ---------- Test: Create Supplier ----------
def test_create_supplier(test_db):
    response = client.post("/suppliers/create", json={
        "name": "Test Supplier",
        "phone": "1234567890",
        "email": "test@example.com",
        "address": "Test Address"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Supplier"
    assert data["email"] == "test@example.com"
    assert data["phone"] == "1234567890"
    assert data["address"] == "Test Address"

# ---------- Test: Get All Suppliers ----------
def test_get_all_suppliers():
    response = client.get("/suppliers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# ---------- Test: Get Supplier by ID ----------
def test_get_supplier_by_id(existing_supplier):
    response = client.get(f"/suppliers/by_id/{existing_supplier.supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["supplier_id"] == existing_supplier.supplier_id
    assert data["name"] == existing_supplier.name

# ---------- Test: Update Supplier ----------
def test_update_supplier(existing_supplier):
    response = client.put(f"/suppliers/update/{existing_supplier.supplier_id}", json={
        "name": "Updated Supplier",
        "phone": "9999999999",
        "email": "updated@example.com",
        "address": "Updated Address"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Supplier"
    assert data["phone"] == "9999999999"
    assert data["email"] == "updated@example.com"
    assert data["address"] == "Updated Address"

# ---------- Test: Delete Supplier ----------
def test_delete_supplier():
    # First, create a supplier to delete
    response = client.post("/suppliers/create", json={
        "name": "To Be Deleted",
        "phone": "0000000000",
        "email": "delete@example.com",
        "address": "Nowhere"
    })
    assert response.status_code == 200
    supplier_id = response.json()["supplier_id"]

    # Now delete it
    response = client.delete(f"/suppliers/delete/{supplier_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["Message"]

    # Try to fetch again
    response = client.get(f"/suppliers/by_id/{supplier_id}")
    assert response.status_code == 404
