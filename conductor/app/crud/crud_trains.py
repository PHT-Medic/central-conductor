from typing import Any, List
from sqlalchemy.orm import Session

from .base import CRUDBase
from conductor.app.models.train import Train, TrainState, TrainConfig
from conductor.app.schemas import TrainCreate, TrainUpdate
from ..models import Station


class CRUDTrain(CRUDBase[Train, TrainCreate, TrainUpdate]):

    # TODO allow for passing of config ids/name
    def create_train_for_user(self, db: Session, creator_id: Any, train_in: TrainCreate):
        """
        Create a train for the user identified in the database by the given id. Initializes an empty train state and
        default config for the created train.

        :param db: sql alchemy session handle
        :param creator_id: unique id of user in DB
        :param train_in: schema for train creation
        :return:
        """
        db_train = Train(
            creator_id=creator_id,
            **train_in.dict()
        )
        db.add(db_train)
        db.commit()

        # Create initial state and config

        db_train_state = TrainState(train_id=db_train.id)
        db.add(db_train_state)
        db_train_config = TrainConfig(train_id=db_train.id)
        db.add(db_train_config)
        db.commit()
        db.refresh(db_train)

        return db_train

    def read_trains_for_station(self, db: Session, station_id: Any) -> List[Train]:
        station = db.query(Station).filter(Station.id == station_id).first()
        return station.trains


trains = CRUDTrain(Train)
