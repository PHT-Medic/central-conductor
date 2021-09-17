from sqlalchemy.orm import Session
import json
from fastapi import HTTPException
from math import floor
from typing import List

from conductor.app.schemas import protocol
from conductor.app.models.protocol import ShareKeysMessage
from conductor.app.crud.train import read_train_state, get_train, read_train_config
from conductor.app.models.train import TrainState, TrainConfig


def process_share_keys_message(db: Session, msg: protocol.SharedKeysMessage, train_id: int) -> TrainState:
    """
    Process a a message containing key cyphers coming from a station, stores the cyphers which are created for each
    station at each station with the correct association and updates the train state
    """
    sender = msg.station_id
    state = read_train_state(db, train_id)

    # Check if the message's iteration matches the conductor train state
    if state.iteration != msg.iteration:
        raise HTTPException(status_code=400, detail="Train iteration does not match")

    # store cyphers associated with stations
    for cypher in msg.cyphers:
        msg = ShareKeysMessage(
            sender=sender,
            recipient=cypher.station_id,
            cypher=cypher.cypher,
            iteration=state.iteration,
            train_id=train_id
        )
        db.add(msg)

    # Update train state
    state = _update_round_1_on_message(db, train_id, state)
    db.commit()
    db.refresh(state)
    return state


def distribute_cyphers(db: Session, train_id: int, cypher_msg: protocol.GetCyphersRequest) -> List[ShareKeysMessage]:
    # TODO check for consistent iterations
    state = read_train_state(db, train_id)
    cyphers = _get_cyphers(db, recipient=cypher_msg.station_id, iteration=state.iteration)
    # Update train state
    # _update_round_1_on_broadcast(db, train_id, state)

    return cyphers


def _update_round_1_on_message(db: Session, train_id: int, state: TrainState) -> TrainState:
    print(state.round)
    # if state.round != 1:
    #     raise HTTPException(status_code=400, detail="Train round does not match server state")

    state.round_k += 1

    db_train = get_train(db, train_id)
    db_train_config = read_train_config(db, train_id)
    assert db_train_config and db_train

    if state.round_k > floor(db_train_config.dropout_allowance * len(db_train.participants)):
        state.round_ready = True

    return state


def _get_cyphers(db: Session, recipient: int, iteration: int) -> List[ShareKeysMessage]:
    cyphers = db.query(ShareKeysMessage).filter(
        ShareKeysMessage.iteration == iteration,
        ShareKeysMessage.recipient == recipient
    ).all()

    return cyphers


def _update_round_1_on_broadcast(db: Session, train_id: int, state: TrainState):
    state.round_messages_sent += 1
    config = read_train_config(db, train_id)
    train = get_train(db, train_id)

    # TODO todo include timeout in updating train to the next round
    if state.round_messages_sent > floor(len(train.participants) * config.dropout_allowance):
        # state.round_finished = True
        state.round += 1

    db.commit()
    db.refresh(state)


