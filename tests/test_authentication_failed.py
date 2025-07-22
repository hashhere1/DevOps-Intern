import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_authentication_failed():
    response = client.post(
        "/login/",
        data={"username": "hassaan@gmail.com",
              "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"

def test_login_nonexistent_user():
    response = client.post(
        "/login/",
        data={"username": "no_user",
              "password": "hassaan"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Credentials"