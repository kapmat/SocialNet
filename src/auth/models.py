from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import BaseMeta


class User(SQLAlchemyBaseUserTable, BaseMeta):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)





