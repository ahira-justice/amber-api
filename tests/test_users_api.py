from fastapi.testclient import TestClient

from app.data import models
from app.domain.constants import *
from app.main import app
from tests.domain import create_user
from tests.utils import get_db


client = TestClient(app)


def test_can_create_user():

    db = get_db()

    payload = {
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "password"
    }

    response = client.post(f"{USERS_URL}", json=payload)

    user_exists = db.query(models.User).filter(models.User.username == payload["email"]).first()
    db.close()

    assert response.status_code == 200
    assert response.json().get("username") == payload["email"]
    assert user_exists


def test_user_can_obtain_auth_token():

    db = get_db()
    create_user(db)

    payload = {
        "username": "user@example.com",
        "password": "password"
    }

    response = client.post(f"{USERS_URL}/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_social_login_user_can_obtain_auth_token():
    db = get_db()

    payload = {
        "phone_number": "08001234567",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post(f"{USERS_URL}/externallogin", json=payload)

    user_exists = db.query(models.User).filter(models.User.username == payload["phone_number"]).first()
    db.close()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert user_exists

    payload = {
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post(f"{USERS_URL}/externallogin", json=payload)

    user_exists = db.query(models.User).filter(models.User.username == payload["email"]).first()
    db.close()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert user_exists


def test_user_can_request_password_reset():
    pass


def test_user_can_reset_password():
    pass
