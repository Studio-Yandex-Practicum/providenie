from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from bot.core.settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hash_password(password: str) -> str:
    """Encrypt passwords using the hash algorithm."""
    return pwd_context.hash(password) if password else ''


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """Password verification."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: dict) -> str:
    """Generate encryption token."""
    expire = datetime.now() + timedelta(minutes=settings.token_expire_minutes)

    to_encode = {'exp': expire, 'sub': sub}

    return jwt.encode(
        to_encode,
        settings.token_secret_key,
        settings.token_algorithm,
    )


def jwt_decode(token: str) -> dict:
    """Decode token."""
    response = {
        'status': 'error',
    }

    try:
        payload = jwt.decode(
            token,
            settings.token_secret_key,
            algorithms=[settings.token_algorithm],
        )
        sub = payload.get('sub')
        if sub is None:
            response['error'] = 'Token does not contain valid subject'
            return response

        response['status'] = 'ok'
        response['data'] = sub
    except InvalidTokenError:
        response['error'] = 'Could not validate credentials'

    return response
