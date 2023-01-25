from datetime import timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from ... import crud, models
from .. import deps
from ...core import security
import jinja2
from ...core.config import settings
from jose import jwt
import random

router = APIRouter()


@router.post("/auth")
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


@router.post("/access-token")
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
        response = crud.user.send_verification_otp(db=db, user_obj=user)
        raise HTTPException(
            status_code=400, detail="Inactive user. Please activate user to login")
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


@router.post("/send-forgot-password-otp")
def send_forgot_paasword_otp(
    *,
    db: Session = Depends(deps.get_db),
    email: Dict
) -> Any:
    user_obj = crud.user.get_by_email(db=db, email=email["email"])
    if user_obj is None:
        raise HTTPException(
            status_code=400,
            detail="The username does not exists",
        )
    reset_code = random.randint(1000, 9999)

    response = crud.reset_password_request.create(
        db, email=email["email"], reset_code=reset_code)
    return response


@router.post("/validate-reset-password-otp")
def validate_otp(
    *,
    db: Session = Depends(deps.get_db),
    reset_details: Dict,
) -> Any:
    email = reset_details["email"]
    reset_code = reset_details["reset_code"]
    is_valid = crud.reset_password_request.validate_reset_code(
        db, email=email, reset_code=reset_code
    )
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid / Expired Code"
        )
        # return {"status": False, "msg": }
    else:
        token = jwt.encode(
            {"sub": reset_details["email"]}, settings.SECRET_KEY)
        response = JSONResponse({"success": 1, "session": token})
        response.set_cookie("session", token)
        return response

     # user_obj = crud.user.get_by_email(db, email=email)
        # crud.user.update(db, db_obj=user_obj, obj_in={
        #     "password": new_password})
        # return {"status": True, "msg": "Password Updated Successfully"}


@router.post("/reset-password")
def reset_password(
    *,
    db: Session = Depends(deps.get_db),
    reset_details: Dict,
    current_user: models.Users = Depends(deps.get_current_user)
):
    user = crud.user.get_by_email(db=db, email=current_user)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email")
    user_obj = crud.user.get_by_email(db, email=current_user)
    crud.user.update(db, db_obj=user_obj, obj_in={
        "password": reset_details.get('new_password')})
    return {"status": True, "msg": "Password Updated Successfully"}
