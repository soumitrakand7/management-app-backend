from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from ... import crud
from .. import deps
from ...core import security
from ...core.config import settings
from jose import jwt


router = APIRouter()


@router.post("/login/auth")
def login(
    response: Response, db: Session = Depends(deps.get_db), *, form_data: Dict
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data["username"], password=form_data["password"]
    )
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=403,
            detail="Inactive user, please activate your account by verifying your email",
        )
    token = jwt.encode({"sub": user.email}, settings.SECRET_KEY)
    response = JSONResponse({"success": 1, "session": token})
    response.set_cookie("session", token)

    return response


@router.post("/login/access-token")
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/activate-user")
def activate_user(
    db: Session = Depends(deps.get_db),
    *,
    activation_details: Dict
) -> Any:
    activation_code = activation_details.get('activation_code')
    email = activation_details.get('email')
    user_obj = crud.user.get_by_email(db=db, email=email)
    if crud.user.activate_user(db=db, user_obj=user_obj, activation_code=activation_code):
        token = jwt.encode({"sub": user_obj.email}, settings.SECRET_KEY)
        response = JSONResponse({"success": 1, "session": token})
        response.set_cookie("session", token)
        return response
    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid OTP or Validity Expired",
        )
