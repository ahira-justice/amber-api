from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.auth.bearer import BearerAuth
from app.domain.constants import USER_TOKENS_URL
from app.domain.database import get_db
from app.dtos import error_dtos, user_token_dtos
from app.services import user_token_service


controller = APIRouter(
    prefix=USER_TOKENS_URL,
    tags=["User Tokens"]
)


@controller.post(
    path="/verify",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {
            "model": bool
        },
        401: {
            "model": error_dtos.ErrorResponse
        },
        422: {
            "model": error_dtos.ValidationErrorResponse
        }
    }
)
async def verify_user_token(
    request: user_token_dtos.VerifyUserTokenRequest,
    db: Session = Depends(get_db)
):
    """Verify user token"""

    return user_token_service.verify_user_token(db, request)
