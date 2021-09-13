from typing import Any, Tuple
from sqlalchemy.orm import Session
from conductor.app.crud import trains
from conductor.app.crud.train import get_train, read_train_config, read_train_state
from conductor.app.models import Train, TrainState, TrainConfig


class Aggregator:

    def get_updates_for_station(self, db: Session, station_id: Any):
        """

        :param station_id:
        :return: 
        """
        db_trains = trains.read_trains_for_station(db=db, station_id=station_id)
        return db_trains

    def get_train_info(self, db: Session, train_id: Any) -> Tuple[Train, TrainState, TrainConfig]:
        db_train = get_train(db, train_id)

        return db_train, db_train.state, db_train.config

    def process_key_broadcast(self, db: Session, train_id: Any):
        train, state, config = self.get_train_info(db, train_id)
