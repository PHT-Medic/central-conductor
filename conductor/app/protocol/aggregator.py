from datetime import datetime
from math import floor
from typing import Any, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session
from conductor.app.crud import trains
from conductor.app.crud.train import get_train, read_train_config, read_train_state
from conductor.app.models import Train, TrainState, TrainConfig, AdvertiseKeysMessage
from conductor.app.schemas.protocol import AdvertiseKeysSchema


class Aggregator:

    # TODO more static methods?
    def get_updates_for_station(self, db: Session, station_id: Any):
        """

        :param station_id:
        :return: 
        """
        db_trains = trains.read_trains_for_station(db=db, station_id=station_id)
        return db_trains

    def get_train_info(self, db: Session, train_id: Any) -> Tuple[Train, TrainState, TrainConfig]:
        """
        Get the train from the database, as well as it's state and stored config.

        Args:
            db: sqlalchemy database session
            train_id: identifier of the train

        Returns:
            sql alchemy database objects for the train, it's state and config
        """
        db_train = get_train(db, train_id)

        return db_train, db_train.state, db_train.config

    def process_key_advertisement(self, db: Session, train_id: Any, message: AdvertiseKeysSchema):
        """
        Process a message from a station containing key advertisements (sharing key, signing_key)

        Args:
            db: sqlalchemy database session
            train_id: identifier of the train for which the message is sent
            message: message containing information about the sender and the advertised keys

        Returns:

        """

        print(message)
        train, state, config = self.get_train_info(db, train_id)

        # Check that the train is in the correct round and state to receive key advertisements
        if state.round != 0:
            raise HTTPException(status_code=400,
                                detail=f"Round mismatch - train is currently in round {state.round}")

        if state.round_k >= len(train.participants):
            raise HTTPException(status_code=400,
                                detail="Max number of key broadcast received. Check if your train is in the correct "
                                       "round or iteration.")

        # Insert the message and update the state
        db_message = self._insert_advertise_keys_message(db, message)
        state = self.update_train_state_with_key_advertisement(db, train, state, config)

        return state

    @staticmethod
    def update_train_state_with_key_advertisement(db: Session,
                                                  train: Train,
                                                  train_state: TrainState,
                                                  train_config: TrainConfig):

        # Get all messages for the train and it's current iteration
        total_key_adv = db.query(AdvertiseKeysMessage).filter(
            AdvertiseKeysMessage.train_id == train.id,
            AdvertiseKeysMessage.iteration == train_state.iteration
        ).all()

        # compare the number of messages with the registered participants
        n_participants = len(train.participants)
        n_messages = len(total_key_adv)

        print(n_participants)
        print(n_messages)

        # Mark the round as ready when the threshold has been met
        train_state.round_k = n_messages
        train_state.round_ready = (
                floor(n_messages + train_config.dropout_allowance * n_participants) >= n_participants)

        train_state.updated_at = datetime.now()
        db.commit()
        db.refresh(train_state)

        return train_state

    @staticmethod
    def _insert_advertise_keys_message(db: Session, message: AdvertiseKeysSchema) -> AdvertiseKeysMessage:
        db_message = AdvertiseKeysMessage(**message.dict())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
