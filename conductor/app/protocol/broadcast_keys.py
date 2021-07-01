from sqlalchemy.orm import Session
from conductor.app.schemas import protocol
from math import floor
from datetime import datetime
from fastapi import HTTPException

from conductor.app.models.train import Train, TrainState, TrainConfig
from conductor.app.models.protocol import AdvertiseKeysMessage
from conductor.app.schemas.protocol import BroadCastKeysSchema, AdvertiseKeysSchema
from conductor.app.crud.train import get_train, read_train_config, read_train_state


def update_round_0_on_message(db: Session, train_id: int, message: AdvertiseKeysSchema):

    # TODO check that the message is valid - no duplicates etc
    # store the message in db
    msg = create_advertise_keys_message(db, message)

    db_train = get_train(db, train_id)
    db_train_state = read_train_state(db, train_id)
    db_train_config = read_train_config(db, train_id)
    # check if train is currently in round 0
    if db_train_state.round != 0:
        raise HTTPException(status_code=400,
                            detail=f"Round mismatch - train is currently in round {db_train_state.round}")

    key_advertise_messages = db.query(AdvertiseKeysMessage). \
        filter(AdvertiseKeysMessage.train_id == train_id,
               AdvertiseKeysMessage.iteration == db_train_state.iteration).all()

    n_participants = len(db_train.participants)
    n_messages = len(key_advertise_messages)
    db_train_state.round_k = n_messages

    db_train_state.round_ready = (
            floor(n_messages + db_train_config.dropout_allowance * n_participants) >= n_participants)

    db_train_state.updated_at = datetime.now()
    db.commit()
    db.refresh(db_train_state)

    return db_train_state


def update_round_0_on_broadcast(db: Session, train_id: int) -> protocol.BroadCastKeysSchema:
    db_train = db.query(Train).get(train_id)
    assert db_train
    db_train_state = db.query(TrainState).filter(TrainState.train_id == train_id).first()
    n_participants = len(db_train.participants)

    # if db_train_state.round != 0:
    #     raise HTTPException(status_code=400,
    #                         detail=f"Round mismatch - train {train_id} is currently in round {db_train_state.round}")

    if not db_train_state.round_ready:
        raise HTTPException(status_code=400,
                            detail=f"Train {train_id} is not ready."
                                   f" Collected {db_train_state.round_k}/{n_participants} messages")
    messages = db.query(AdvertiseKeysMessage).filter(
        AdvertiseKeysMessage.train_id == train_id,
        AdvertiseKeysMessage.iteration == db_train_state.iteration
    ).all()

    db_train_state.round_messages_sent += 1

    config = read_train_config(db, train_id)


    if db_train_state.round_messages_sent > floor(
            len(db_train.participants) - (len(db_train.participants) * config.dropout_allowance)):
        # db_train_state.round_finished = True
        print(f"Moving to next round: {db_train_state.round} -> {db_train_state.round + 1}")
        db_train_state.round += 1

    db.commit()

    broad_cast_message = BroadCastKeysSchema(train_id=train_id,
                                             iteration=db_train_state.iteration,
                                             keys=messages)
    return broad_cast_message


def create_advertise_keys_message(db: Session, ak_msg: AdvertiseKeysSchema):
    db_message = AdvertiseKeysMessage(**ak_msg.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
