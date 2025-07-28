import pytest
from sqlalchemy.orm import Session
from app.models import Users
from auth.hashing import hashing
from tests.conftest import TestingSessionLocal


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


def test_login_success(client):
    add_test_user("hassaan", "test123")
    response = client.post("/login/", data={
        "username": "hassaan",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_login_invalid_password(client):
    add_test_user("hassaan2", "realpass")
    response = client.post("/login/", data={
        "username": "hassaan2",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"


def test_login_user_not_found(client):
    response = client.post("/login/", data={
        "username": "nouser",
        "password": "any"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"
