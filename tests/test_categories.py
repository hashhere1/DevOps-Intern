import pytest
from sqlalchemy.orm import Session
from app.models import Categories
from tests.conftest import client, TestingSessionLocal


@pytest.fixture(autouse=True)
def clear_categories():
    """Clear the categories table before each test."""
    db: Session = TestingSessionLocal()
    db.query(Categories).delete()
    db.commit()
    db.close()


def create_category(client):
    return client.post(
        "/category/create",
        json={
            "name": "Electronics",
            "description": "All electronic items"
        }
    )


def test_create_category(client):
    response = create_category(client)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["description"] == "All electronic items"


def test_get_all_categories(client):
    create_category(client)
    response = client.get("/category/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Electronics"


def test_category_by_id(client):
    create_category(client)
    response = client.get("/category/by_id/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["description"] == "All electronic items"


def test_update_category(client):
    create_category(client)
    response = client.put(
        "/category/update/1",
        json={
            "name": "UpdatedElectronics",
            "description": "Updated Electronic items"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "UpdatedElectronics"


def test_delete_category(client):
    create_category(client)
    response = client.delete("/category/delete/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"

    response = client.get("/category/")
    assert response.status_code == 200
    assert response.json() == []
