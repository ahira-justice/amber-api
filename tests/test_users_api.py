from fastapi.testclient import TestClient
from faker import Faker

from app.data.models import User
from app.domain.constants import USERS_URL
from app.main import app
from tests.utils import get_db

client = TestClient(app)
fake = Faker()


def test_can_create_user():
    db = get_db()

    payload = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": fake.password()
    }

    response = client.post(f"{USERS_URL}", json=payload)

    user_exists = db.query(User).filter(User.username == payload["email"]).first()
    db.close()

    assert response.status_code == 200
    assert response.json().get("username") == payload["email"]
    assert user_exists
