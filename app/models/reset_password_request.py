from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from ..db.base_class import default_pk
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class ResetPasswordRequest(Base):
    id = Column(String(36), primary_key=True, default=default_pk)
    user_email = Column(String(32), ForeignKey("users.email"), index=True)
    reset_code = Column(Float, index=True)
    validity = Column(DateTime)

    user = relationship("Users", foreign_keys=[user_email])
