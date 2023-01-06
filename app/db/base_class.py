from typing import Any
import uuid

from sqlalchemy.ext.declarative import as_declarative, declared_attr


def default_pk():
    return str(uuid.uuid4())


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
