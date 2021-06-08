from typing import Any

from sqlalchemy.orm import Session

from .base import CRUDBase, CreateSchemaType, ModelType
from conductor.app.models.train import TrainState


class CRUDTrainState:
    @staticmethod
    def get_train_state(db: Session, train_id: Any) -> TrainState:
        db_train_state = db.query(TrainState).filter(TrainState.train_id == train_id).first()
        return db_train_state

    def update_discovery_state(self):
        pass
