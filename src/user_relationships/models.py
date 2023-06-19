from sqlalchemy import Column, Integer, String, ForeignKey
from auth.models import User

from database import BaseMeta


class Status(BaseMeta):
    __tablename__ = "status"

    status_id = Column(Integer, primary_key=True)
    name = Column(String)


class Relationship(BaseMeta):
    __tablename__ = "relationship"

    id = Column(Integer, primary_key=True)
    user_1_id = Column(Integer, ForeignKey(User.id))
    user_2_id = Column(Integer, ForeignKey(User.id))
    status_id = Column(Integer, ForeignKey(Status.status_id))
