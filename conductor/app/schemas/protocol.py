from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AdvertiseKeysSchema(BaseModel):
    """
    Schema for receiving a key advertisement message (Round 0)
    """
    train_id: int
    station_id: int
    iteration: int
    signing_key: str
    sharing_key: str
    key_signature: Optional[str] = None


class StationKeys(BaseModel):
    station_id: int
    signing_key: str
    sharing_key: str
    key_signature: Optional[str] = None

    class Config:
        orm_mode = True


class BroadCastKeysMessage(BaseModel):
    train_id: int
    iteration: int
    keys: List[StationKeys]


class KeyCypher(BaseModel):
    station_id: int
    cypher: str


class SharedKeysMessage(BaseModel):
    station_id: int
    created_at: datetime
    iteration: int
    cyphers: List[KeyCypher]


class GetCyphersRequest(BaseModel):
    station_id: int
    iteration: int


class DistributeCypher(BaseModel):
    sender: int
    cypher: str

    class Config:
        orm_mode = True
