from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, decode_token, hash_password, verify_password
from app.models import User


# fmt: off
class AuthUserAlreadyExistsError(Exception): ...
class AuthInvalidCredentialsError(Exception): ...
class AuthInactiveUserError(Exception): ...
class AuthInvalidTokenError(Exception): ...
# fmt: on


async def register_user(db: AsyncSession, email: str, password: str, full_name: str) -> User:
    existing = await _get_user_by_email(db, email)
    if existing is not None:
        raise AuthUserAlreadyExistsError(f"Email {email} is already registered")

    user = User(
        email=email.lower().strip(),
        hashed_password=hash_password(password),
        full_name=full_name,
        is_active=True,
        is_verified=False,  # extend with email verification at a later date
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> str:
    user = await _get_user_by_email(db, email)
    if user is None:
        raise AuthInvalidCredentialsError("Invalid email or password")

    valid, new_hash = verify_password(password, user.hashed_password)
    if not valid:
        raise AuthInvalidCredentialsError("Invalid email or password")

    if new_hash is not None:
        user.hashed_password = new_hash
        await db.commit()
        await db.refresh(user)

    if not user.is_active:
        raise AuthInactiveUserError("Account is deactivated")

    access_token = create_access_token(subject=str(user.id))
    return access_token


async def get_user_from_token(db: AsyncSession, token: str) -> User:
    payload = decode_token(token)
    if payload is None:
        raise AuthInvalidTokenError("Access token is invalid or expired")

    user_id = int(payload.get("sub"))
    user = await _get_user_by_id(db, user_id)

    if user is None:
        raise AuthInvalidTokenError("User not found")
    if not user.is_active:
        raise AuthInvalidTokenError("Account is deactivated")

    return user


# TODO: determine if should block if it has portfolios or should cascade
async def delete_user(db: AsyncSession, id: int):
    user = await db.scalar(select(User).where(User.id == id))
    if user:
        db.delete(user)
        await db.commit()


async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email.lower().strip()))


async def _get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.scalar(select(User).where(User.id == user_id))
