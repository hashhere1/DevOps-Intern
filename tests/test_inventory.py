import pytest
from fastapi.testclient import TestClient
from app.main import app
from auth.oauth2 import get_current_user
from app.models import Inventory
from tests.test_helpers import db  # fixture

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_inventory(db):
    db.query(Inventory).delete()
    db.commit()

def create_inventory():
    return client.post(
        "/inventory/create",
        json={
            "product_id": 1,  # If unsure, get actual ID in test
            "quantity": 50
        }
    )

def test_create_inventory():
    response = create_inventory()
    assert response.status_code == 200
    assert response.json()["product"]["product_id"] == 1
    assert response.json()["quantity"] == 50

def test_get_all_inventory():
    create_inventory()
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["quantity"] == 50

def test_get_inventory_by_id():
    create_inventory()
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.json()["quantity"] == 50

def test_update_inventory():
    create_inventory()
    response = client.put(
        "/inventory/update/1",
        json={
            "product_id": 1,
            "quantity": 100
        }
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 100

def test_delete_inventory():
    create_inventory()
    response = client.delete("/inventory/delete/1")
    assert response.status_code == 200
    assert response.json()["product"]["product_id"] == 1

    response = client.get("/inventory/")
    assert response.json() == []
