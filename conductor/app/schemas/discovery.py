from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Union, Dict, Any


class ClassDiscoveryItem(BaseModel):
    class_name: str
    n_items: int


class DiscoveryResultCreate(BaseModel):
    station_id: int
    results: Union[List[ClassDiscoveryItem], str]


class DiscoveryResultsUpdate(DiscoveryResultCreate):
    pass


class DiscoveryResults(DiscoveryResultCreate):
    id: int
    train_id: Any
    created_at: datetime

    class Config:
        orm_mode = True
