from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import jwt
from sqlalchemy.orm import Session
from .. import crud, models
from ..core.config import settings
from ..db.session import SessionLocal
from ..core import security

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

cookie_sec = APIKeyCookie(name="session", auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Users:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = payload
    except (jwt.JWTError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = payload["sub"]
    user_obj = crud.user.get_by_email(db, email=user)
    if not crud.user.is_active(user_obj):
        raise HTTPException(status_code=400, detail="Inactive user")
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_cookie_affiliate(
    db: Session = Depends(get_db), session: str = Depends(cookie_sec)
):
    try:
        print(settings.SECRET_KEY)
        payload = jwt.decode(session, settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        affiliate = payload["sub"]
        affiliate_obj = crud.user.get_by_email(db, email=affiliate)
        if not crud.user.is_active(affiliate_obj):
            raise HTTPException(status_code=400, detail="Inactive Affiliate")
        return affiliate
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )
