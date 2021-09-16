from datetime import datetime
from math import floor, ceil
from typing import Any, Tuple, List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from conductor.app.crud import trains
from conductor.app.crud.train import get_train, read_train_config, read_train_state
from conductor.app.models import Train, TrainState, TrainConfig, AdvertiseKeysMessage
from conductor.app.schemas.protocol import AdvertiseKeysSchema, BroadCastKeysMessage


class Aggregator:

    def get_updates_for_station(self, db: Session, station_id: Any) -> List[Train]:
        """

        :param station_id:
        :return: 
        """
        db_trains = trains.read_trains_for_station(db=db, station_id=station_id)
        ready_trains = []
        for train in db_trains:
            state = train.state
            if state.round_ready:
                ready_trains.append(train)
        return ready_trains

    def get_train_info(self, db: Session, train_id: Any) -> Tuple[Train, TrainState, TrainConfig]:
        """
        Get the train from the database, as well as it's state and stored config.

        Args:
            db: sqlalchemy database session
            train_id: identifier of the train

        Returns:
            sql alchemy database objects for the train, it's state and config
        """
        db_train = trains.get(db, train_id)

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
        state = self._update_train_state_with_key_advertisement(db, train, state, config)

        return state

    def broadcast_keys(self, db: Session, train_id: Any) -> BroadCastKeysMessage:
        """
        Collect all key advertisements in the for the given train in the current iteration and package them into
        a message to send to participant

        Args:
            db: sqlalchemy database session
            train_id: identifier of the train

        Returns:
            Message to be sent to a participant after a request
        """
        train, state, config = self.get_train_info(db, train_id)
        n_participants = len(train.participants)

        # Check for states and that no additional messages will be sent
        if not state.round_ready:
            raise HTTPException(status_code=403,
                                detail=f"Train {train_id} is not ready."
                                       f" Collected {state.round_k}/{n_participants} messages")

        if state.round_messages_sent >= n_participants:
            raise HTTPException(status_code=403, detail=f"Maximum number of key broadcasts performed for "
                                                        f"train {train_id}")

        # Get all key advertisements for the selected train in the current iteration
        messages = db.query(AdvertiseKeysMessage).filter(
            AdvertiseKeysMessage.train_id == train.id,
            AdvertiseKeysMessage.iteration == state.iteration
        ).all()

        # Create key broadcast message based on the key advertisements in the db
        broadcast_message = BroadCastKeysMessage(train_id=train_id,
                                                 iteration=state.iteration,
                                                 keys=messages)

        # Update the state based on the new message
        state.round_messages_sent += 1
        if state.round_messages_sent >= ceil(n_participants * config.dropout_allowance):
            print(f"Moving train {train_id} to round 1")
            state.round = 1
            state.round_k = 0
            state.round_messages_sent = 0

        db.commit()
        db.refresh(state)

        return broadcast_message

    def process_shared_keys(self):

        pass

    @staticmethod
    def _update_train_state_with_key_advertisement(db: Session,
                                                   train: Train,
                                                   train_state: TrainState,
                                                   train_config: TrainConfig) -> TrainState:

        """
        Update the train state after receiving a key advertisement from a participant

        Args:
            db: database session
            train: db train object
            train_state: db train state
            train_config: db train config

        Returns:
            the updated state of the train
        """

        # Get all messages for the train and it's current iteration
        total_key_adv = db.query(AdvertiseKeysMessage).filter(
            AdvertiseKeysMessage.train_id == train.id,
            AdvertiseKeysMessage.iteration == train_state.iteration
        ).all()

        # compare the number of messages with the registered participants
        n_participants = len(train.participants)
        n_messages = len(total_key_adv)

        # Mark the round as ready when the threshold has been met
        train_state.round_k = n_messages
        train_state.round_ready = (n_messages >= ceil(train_config.dropout_allowance * n_participants))

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
