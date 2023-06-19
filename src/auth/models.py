from datetime import date, datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseMeta


class User(SQLAlchemyBaseUserTable, BaseMeta):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow())








