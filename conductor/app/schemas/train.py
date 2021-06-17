from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

from .station import StationBase


class TrainBase(BaseModel):
    description: str
    proposal_id: Optional[int] = 0


class TrainCreate(TrainBase):
    pass


class TrainUpdate(TrainBase):
    pass


class TrainInfo(BaseModel):
    pass


class TrainState(BaseModel):
    train_id: int
    iteration: int
    round: int
    round_start: datetime
    round_k: int
    round_ready: bool
    updated_at: Optional[datetime] = None
    discovery_finished: bool

    class Config:
        orm_mode = True


class TrainConfig(BaseModel):
    train_id: int
    min_participants: int
    dropout_allowance: float
    batch_size: int
    epochs: int
    time_out: int

    class Config:
        orm_mode = True


class Train(TrainBase):
    id: int
    is_active: bool
    participants: List[StationBase] = None
    state: Optional[TrainState] = None

    class Config:
        orm_mode = True


class Station(StationBase):
    id: int
    trains: List[Train] = []


class DiscoveryResult(BaseModel):
    n_samples: int
    station_id: Any
