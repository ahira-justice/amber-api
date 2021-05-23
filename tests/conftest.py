import pytest
import os

from app.domain.constants import TEST_DATABASE_FILE
from tests.utils import get_db, setup, clear_db_data


@pytest.hookimpl()
def pytest_sessionstart(session):
    setup()


@pytest.hookimpl()
def pytest_runtest_teardown(item, nextitem):
    db = get_db()
    clear_db_data(db)


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    os.remove(TEST_DATABASE_FILE)
