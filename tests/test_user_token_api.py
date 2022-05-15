from fastapi.testclient import TestClient
from faker import Faker

from app.data.models import UserToken
from app.domain.constants import USER_TOKENS_URL
from app.main import app
from tests.domain import create_user, create_user_token
from tests.utils import get_db

client = TestClient(app)
fake = Faker()


def test_verify_user_token():
    db = get_db()

    user_token = create_user_token()

