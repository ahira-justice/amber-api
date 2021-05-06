import os

from dotenv import load_dotenv


load_dotenv()


SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SIGNING_ALGORITHM = os.environ.get("JWT_SIGNING_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
LOG_LEVEL_CONFIG = os.environ.get("LOG_LEVEL_CONFIG", "DEBUG")
JSON_LOGS_CONFIG = os.environ.get("JSON_LOGS_CONFIG", "0")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME")
ADMIN_LAST_NAME = os.environ.get("ADMIN_LAST_NAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
RESET_CODE_EXPIRE_MINUTES= os.environ.get("RESET_CODE_EXPIRE_MINUTES")
