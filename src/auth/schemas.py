from datetime import date

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    patronymic: str
    birthday: date


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    patronymic: str
    birthday: date


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    patronymic: str
    birthday: date


class UsersList(BaseModel):
    id: int
    first_name: str
    last_name: str
