from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from app.core.auth_utils import verify_password
from app.core.config import get_settings
from app.core.database import get_session
from app.schemas.auth import TokenData
from app.services.user_services import get_user_by_email
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlmodel import Session
import uuid

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer("/api/v1/auth/token")


def authenticate_user(email: str, password: str, db=Depends(get_session)):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(
    data: dict, expires_delta: timedelta | None = None, token_type: str = "access"
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        if token_type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(days=7)
            secret_key = settings.refresh_secret_key
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                settings.access_token_expire_minutes
            )
            secret_key = settings.secret_key
    jti = str(uuid.uuid4())
    secret_key = (
        settings.refresh_secret_key if token_type == "refresh" else settings.secret_key
    )
    to_encode.update({"exp": expire, "jti": jti, "type": token_type})
    encode_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=settings.ALGORITHM,
    )
    return encode_jwt


def create_access_token(data: dict, expires_delta: timedelta = None):
    return create_token(data, token_type="access", expires_delta=expires_delta)


def create_refresh_token(data: dict, expires_delta: timedelta = None):
    return create_token(data, token_type="refresh", expires_delta=expires_delta)


def verify_access_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.ALGORITHM]
        )
        if not payload.get("jti"):
            raise InvalidTokenError("Missing JWT ID")
        if payload.get("type") != "access":
            raise InvalidTokenError("Not a refresh token")

        email = payload.get("sub", None)
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception


def verify_refresh_token(token):
    try:
        payload = jwt.decode(
            token, settings.refresh_secret_key, algorithms=[settings.ALGORITHM]
        )

        if not payload.get("jti"):
            raise InvalidTokenError("Missing JWT ID")
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Not a refresh token")

        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)
):
    token_data = verify_access_token(token)
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not admin ")
    return current_user
