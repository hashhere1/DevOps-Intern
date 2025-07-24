import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from tests.test_db import override_get_db,TestingSessionLocal
from auth.oauth2 import get_current_user
from sqlalchemy.orm import Session
from app.models import Categories

app.dependency_overrides[get_db] = override_get_db

def override_get_current_user():
    return {"username": "testuser", "user_id": 1}

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tables():
    db: Session = TestingSessionLocal()
    db.query(Categories).delete()
    db.commit()
    db.close()

def create_category():
    return client.post(
        "/category/create",
        json={"name": "Electronics",
              "description": "All electronic items"
              }
    )

def test_create_category():
    response = create_category()
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_get_all_categories():
    create_category()
    response = client.get(
        "/category/"
    )
    assert response.status_code == 200
    assert isinstance(response.json(),list)
    assert response.json()[0]["name"] == "Electronics"

def test_category_by_id():
    create_category()
    response = client.get("/category/by_id/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_update_category():
    create_category()
    response = client.put("/category/update/1",
                          json={"name": "UpdatedElectronics",
                                "description": "Updated Electronic items"}
                          )
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedElectronics"

def test_delete_category():
    create_category()
    response = client.delete("/category/delete/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

    response = client.get("/category/")
    assert response.json() == []
