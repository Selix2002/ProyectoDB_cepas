from typing import Any

from litestar.connection import ASGIConnection
from litestar.contrib.jwt import OAuth2PasswordBearerAuth, Token
from litestar.exceptions import NotFoundException
from litestar.repository import NotFoundError

from app.config import settings
from app.db import db_config
from app.models import User
from app.repositories import UserRepository


async def retrieve_user_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> User:
    session_maker = db_config.create_session_maker()
    try:
        with session_maker() as session:
            users_repo = UserRepository(session=session)
            return users_repo.get_one(username=token.sub)
    except NotFoundError as e:
        raise NotFoundException("Usuario no encontrado") from e


oauth2_auth = OAuth2PasswordBearerAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.secret_key.get_secret_value(),
    token_url="/auth/login",
    exclude=["/auth/login","/users/create","/schema"], 
)


