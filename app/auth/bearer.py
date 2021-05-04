from fastapi import Request
from fastapi.security.http import HTTPBearer

from app.data import models
from app.domain.database import SessionLocal
from app.exceptions.app_exceptions import UnauthorizedRequestException
from app.services import jwt_service


class BearerAuth(HTTPBearer):

    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        scheme, token = request.headers.get("Authorization").split(" ")

        if not scheme or not token:
            raise UnauthorizedRequestException("Missing or malformed authorization header")

        if scheme.lower() != "bearer":
            raise UnauthorizedRequestException("Invalid authentication scheme")

        if not self.verify_jwt(token):
            raise UnauthorizedRequestException("Invalid or expired token")

        return True

    def verify_jwt(self, jwtoken: str) -> bool:

        db = SessionLocal()

        try:
            payload = jwt_service.decode_jwt(jwtoken)
        except:
            payload = None

        if not payload:
            return False

        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user:
            return False

        return True
