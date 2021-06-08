from pydantic import BaseModel
from typing import List

from conductor.app.schemas.train import Train



class UserBase(BaseModel):
    email: str
    institution: str = "pht"


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    trains: List[Train] = []

    class Config:
        orm_mode = True

