from fastapi.testclient import TestClient
from faker import Faker

from app.data.models import User
from app.domain.constants import AUTH_URL
from app.main import app
from tests.domain import create_user
from tests.utils import get_db

client = TestClient(app)
fake = Faker()


def test_user_can_obtain_auth_token():
    db = get_db()
    password = fake.password()

    user = create_user(db, password)

    payload = {
        "username": user.username,
        "password": password
    }

    response = client.post(f"{AUTH_URL}/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_social_login_user_can_obtain_auth_token():
    db = get_db()

    payload = {
        "phone_number": fake.phone_number(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }

    response = client.post(f"{AUTH_URL}/external-login", json=payload)

    user_exists = db.query(User).filter(User.username == payload["phone_number"]).first()
    db.close()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert user_exists

    payload = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }

    response = client.post(f"{AUTH_URL}/external-login", json=payload)

    user_exists = db.query(User).filter(User.username == payload["email"]).first()
    db.close()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert user_exists


def test_user_can_request_password_reset():
    pass


def test_user_can_reset_password():
    pass
