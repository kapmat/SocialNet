from pydantic import BaseModel


class AddNewFriend(BaseModel):
    requests: list = [1, 2]
