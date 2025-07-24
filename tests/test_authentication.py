import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models import Users
from auth.hashing import hashing
from app.database import get_db
from tests.test_db import override_get_db, TestingSessionLocal

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    db: Session = TestingSessionLocal()
    db.query(Users).delete()
    db.commit()
    db.close()


def add_test_user(username: str, password: str):
    db: Session = TestingSessionLocal()
    hashed = hashing(password)
    user = Users(username=username, password=hashed, role="user")
    db.add(user)
    db.commit()
    db.close()


def test_login_success():
    add_test_user("hassaan", "test123")
    response = client.post("/login/", data={
        "username": "hassaan",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_login_invalid_password():
    add_test_user("hassaan2", "realpass")
    response = client.post("/login/", data={
        "username": "hassaan2",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"


def test_login_user_not_found():
    response = client.post("/login/", data={
        "username": "nouser",
        "password": "any"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"
