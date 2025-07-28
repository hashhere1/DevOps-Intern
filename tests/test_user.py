import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_helpers import db as test_db
from app.models import Users

client = TestClient(app)

# ---------- Fixture to use pre-inserted user from test_helpers ----------
@pytest.fixture
def existing_user(test_db):
    return test_db.query(Users).first()

# ---------- Test: Create User ----------
def test_create_user():
    response = client.post("/user/create", json={
        "username": "newuser@example.com",
        "password": "securepassword",
        "role": "Manager"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser@example.com"
    assert data["role"] == "Manager"
    assert "user_id" in data

# ---------- Test: Get All Users ----------
def test_get_all_users():
    response = client.get("/user/show")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# ---------- Test: Get User by ID ----------
def test_get_user_by_id(existing_user):
    response = client.get(f"/user/show_by_id/{existing_user.user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == existing_user.user_id
    assert data["username"] == existing_user.username

# ---------- Test: Update User ----------
def test_update_user(existing_user):
    response = client.put(f"/user/update/{existing_user.user_id}", json={
        "username": "updateduser@example.com",
        "password": "updatedpass123",
        "role": "Admin"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser@example.com"
    assert data["role"] == "Admin"

# ---------- Test: Delete User ----------
def test_delete_user():
    # Create a user to delete
    response = client.post("/user/create", json={
        "username": "tobedeleted@example.com",
        "password": "deletepass",
        "role": "Viewer"
    })
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    # Now delete it
    response = client.delete(f"/user/delete/{user_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["Message"]

    # Confirm deletion
    response = client.get(f"/user/show_by_id/{user_id}")
    assert response.status_code == 404
