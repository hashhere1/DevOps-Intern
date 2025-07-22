import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/login/",
        data={"username": "hassaan@gmail.com",
              "password": "hassaan"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"