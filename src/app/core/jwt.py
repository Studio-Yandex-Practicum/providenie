from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from bot.core.settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hash_password(password: str) -> str:
    """Encrypt passwords using the hash algorithm."""
    return pwd_context.hash(password)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """Password verification."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    """Generate encryption token."""
    expire = datetime.now() + timedelta(minutes=settings.token_expire_minutes)

    to_encode = {'exp': expire, 'sub': sub}

    return jwt.encode(
        to_encode,
        settings.token_secret_key,
        settings.token_algorithm,
    )


def jwt_decode(token: str) -> str:
    """Decode token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
        tg_id = int(payload.get('sub'))
        if not tg_id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return tg_id
