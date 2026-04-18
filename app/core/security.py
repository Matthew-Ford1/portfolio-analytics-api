from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import config


# verifies using all algorithms in list and provides updated hash if
# first one wasn't used
password_hash = PasswordHash((Argon2Hasher(),))
_ALGORITHM = "HS256"


def hash_password(plaintext: str) -> str:
    return password_hash.hash(plaintext)


def verify_password(plaintext: str, hashed: str) -> tuple[bool, str]:
    return password_hash.verify_and_update(plaintext, hashed)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expires_delta = expires_delta or timedelta(minutes=config.TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + expires_delta
    to_encode = {"expire": expire.timestamp(), "sub": subject}
    encode_jwt = jwt.encode(to_encode, config.SECRET_KEY.get_secret_value(), algorithm=_ALGORITHM)
    return encode_jwt


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.SECRET_KEY.get_secret_value(), algorithms=[_ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
