from pydantic import BaseModel


class UsersList(BaseModel):
    id: int
    first_name: str
    last_name: str
