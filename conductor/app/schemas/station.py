from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StationBase(BaseModel):
    name: str
    class Config:
        orm_mode = True

class StationCreate(StationBase):
    pass


class StationUpdate(StationBase):
    pass


class Station(StationBase):
    id: int

