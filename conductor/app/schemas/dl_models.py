from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Union, Dict, Any


class DLModelBase(BaseModel):
    model_type: str
    model_name: str
    model_src: str


class DLModelCreate(DLModelBase):
    pass


class DLModelUpdate(DLModelBase):
    pass


class DLModel(DLModelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    train_id: Optional[int]

    class Config:
        orm_mode = True
