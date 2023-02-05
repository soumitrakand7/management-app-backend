from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models.reset_password_request import ResetPasswordRequest
from datetime import datetime, timedelta
import jinja2
from integrations import mailer
from backports.zoneinfo import ZoneInfo


class CRUDResetPasswordRequest(CRUDBase):
    def create(
        self,
        db: Session,
        *,
        email: str,
        reset_code: int,
    ):
        reset_pass_obj = ResetPasswordRequest(
            user_email=email,
            reset_code=reset_code,
            validity=datetime.now(tz=ZoneInfo(
                'Asia/Kolkata')) + timedelta(hours=30)
        )
        db.add(reset_pass_obj)
        db.commit()
        db.refresh(reset_pass_obj)

        with open("templates/reset-password.html", "r") as f:
            template_string = f.read()
        template = jinja2.Template(template_string)
        registration_template = template.render(
            reset_code=reset_code, full_name=reset_pass_obj.user.full_name)
        response = mailer.send_email(
            receiver_email=reset_pass_obj.user_email, subject="OTP for Password Reset", email_content=registration_template)
        print(response)

        return reset_pass_obj

    def validate_reset_code(
        self,
        db: Session,
        *,
        email: str,
        reset_code: int
    ):
        password_reset_requests = db.query(ResetPasswordRequest) \
            .filter(ResetPasswordRequest.user_email == email) \
            .filter(ResetPasswordRequest.reset_code == reset_code) \
            .filter(ResetPasswordRequest.validity >= datetime.now(tz=ZoneInfo('Asia/Kolkata'))).all()
        if len(password_reset_requests) > 0:
            return True
        else:
            return False


reset_password_request = CRUDResetPasswordRequest()
