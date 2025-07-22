import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    response = client.post(
        "/login/",
        data={"username": "hassaan@gmail.com", "password": "hassaan"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def created_category(auth_headers):
    response = client.post(
        "/category/create",
        json={"name": "Electronics", "description": "Devices and gadgets"},
        headers=auth_headers
    )
    assert response.status_code == 200
    return response.json()["category_id"]

def test_create_category(auth_headers):
    response = client.post(
        "/category/create",
        json={"name": "Books", "description": "Reading materials"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Books"

def test_get_all_categories(auth_headers):
    response = client.get("/category/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_category_by_id(auth_headers, created_category):
    response = client.get(f"/category/by_id/{created_category}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["category_id"] == created_category

def test_update_category(auth_headers, created_category):
    response = client.put(
        f"/category/update/{created_category}",
        json={"name": "Updated Category", "description": "Updated description"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Category"

def test_delete_category(auth_headers, created_category):
    response = client.delete(
        f"/category/delete/{created_category}",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["category_id"] == created_category
