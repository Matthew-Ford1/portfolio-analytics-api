from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.security import hash_password, verify_password, create_access_token, decode_token


class UserAlreadyExistsError(Exception): ...


class InvalidCredentialsError(Exception): ...


class InactiveUserError(Exception): ...


class InvalidTokenError(Exception): ...


async def register_user(db: AsyncSession, email: str, password: str, full_name: str) -> User:
    existing = await _get_user_by_email(db, email)
    if existing is not None:
        raise UserAlreadyExistsError(f"Email {email} is already registered")

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
        raise InvalidCredentialsError("Invalid email or password")

    valid, new_hash = verify_password(password, user.hashed_password)
    if not valid:
        raise InvalidCredentialsError("Invalid email or password")

    if new_hash is not None:
        print("#########UPDATING PASSWORD HASH############")
        user.hashed_password = new_hash
        await db.commit()
        await db.refresh(user)

    if not user.is_active:
        raise InactiveUserError("Account is deactivated")

    access_token = create_access_token(subject=str(user.id))
    return access_token


async def get_user_from_token(db: AsyncSession, token: str) -> User:
    payload = decode_token(token)
    if payload is None:
        raise InvalidTokenError("Access token is invalid or expired")

    user_id = int(payload.get("sub"))
    user = await _get_user_by_id(db, user_id)

    if user is None:
        raise InvalidTokenError("User not found")
    if not user.is_active:
        raise InvalidTokenError("Account is deactivated")

    return user


async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email.lower().strip()))


async def _get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.scalar(select(User).where(User.id == user_id))
