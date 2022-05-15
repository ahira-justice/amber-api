import os

import pytest

from app.domain.config import ENVIRONMENT
from app.domain.constants import TEST_DATABASE_FILE
from tests.utils import setup


@pytest.hookimpl()
def pytest_sessionstart(session):
    setup()


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    if ENVIRONMENT == "TEST":
        os.remove(TEST_DATABASE_FILE)
