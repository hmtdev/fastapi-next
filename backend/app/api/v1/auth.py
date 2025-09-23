from app.core.database import get_session
from app.schemas.auth import Token, TokenRefresh
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    verify_refresh_token,
    create_refresh_token,
    verify_access_token,
)
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi.responses import Response
from app.services.user_services import get_user_by_email

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/token")
async def login_for_access_token(
    response: Response,
    db: Session = Depends(get_session),
    form: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(form.username, form.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=60 * 60 * 24 * 30,
    )
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/refresh")
async def refresh_token(refresh_token, db: Session = Depends(get_session)):
    token_data = verify_refresh_token(refresh_token)
    user = get_user_by_email(db, token_data.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token invalid"
        )
    access_token = create_access_token(data={"sub": user.email})
    return TokenRefresh(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/verify")
async def verify_token(
    token: str,
    type: str = Query("access", enum=["access", "refresh"]),
):
    if type == "access":
        token_data = verify_access_token(token)
    elif type == "refresh":
        token_data = verify_refresh_token(token)
    else:
        raise HTTPException(status_code=400, detail="Invalid token type")
    return {"token_data": token_data}
