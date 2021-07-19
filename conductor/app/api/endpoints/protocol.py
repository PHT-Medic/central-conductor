from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from conductor.app.schemas.train import TrainState, Train, TrainCreate, TrainConfig
from conductor.app.schemas.protocol import AdvertiseKeysSchema, BroadCastKeysSchema, PostSharedKeys, GetCyphersRequest, \
    DistributeCypher
from conductor.app.crud import trains
from conductor.app.protocol.broadcast_keys import (update_round_0_on_message,
                                                   update_round_0_on_broadcast,
                                                   create_advertise_keys_message)
from conductor.app.protocol.share_keys import process_share_keys_message, distribute_cyphers
from conductor.app.api.dependencies import get_db

router = APIRouter()


@router.post("/trains/{train_id}/advertiseKeys", tags=["Protocol"], response_model=TrainState)
def collect_key_advertisements(train_id: int, message: AdvertiseKeysSchema, db: Session = Depends(get_db)):
    """
    Route for participants to advertise keys when the protocol for the specified train is in round 0
    """
    # db_message = create_advertise_keys_message(db, message)

    db_train = trains.get(db, id=train_id)
    if not db_train:
        raise HTTPException(status_code=403, detail="Train does not exist")
    db_state: TrainState = db_train.state
    if db_state.round != 0:
        raise HTTPException(status_code=403, detail="Train is not in the correct round of the protocol")

    if db_state.round_k >= len(db_train.participants):
        raise HTTPException(status_code=403, detail="Maximum number of key advertisements sent in.")

    state = update_round_0_on_message(db, train_id, message)
    return state


@router.get("/trains/{train_id}/broadcastKeys", tags=["Protocol"], response_model=BroadCastKeysSchema)
def distribute_collected_keys(train_id: int, db: Session = Depends(get_db)):
    """
    When the advertisement round of an iteration is finished receive a list of user associated key pairs
    """
    broadcast = update_round_0_on_broadcast(db, train_id=train_id)
    return broadcast


@router.post("/trains/{train_id}/shareKeys", tags=["Protocol"], response_model=TrainState)
def collect_key_shares(train_id: int, msg: PostSharedKeys, db: Session = Depends(get_db)):

    db_train = trains.get(db, id=train_id)

    if not db_train:
        raise HTTPException(status_code=403, detail="Train does not exist")

    db_state: TrainState = db_train.state
    if db_state.round != 1:
        raise HTTPException(status_code=403, detail="Train is not in the correct round of the protocol")

    if db_state.round_k >= len(db_train.participants):
        raise HTTPException(status_code=403, detail="Maximum number of shared keys have been uploaded.")

    state = process_share_keys_message(db, msg, train_id)
    return state


@router.post("/trains/{train_id}/cyphers", response_model=List[DistributeCypher], tags=["Protocol"])
def distribute_collected_cyphers(train_id: int, cypher_msg: GetCyphersRequest, db: Session = Depends(get_db)):
    cyphers = distribute_cyphers(db, train_id, cypher_msg)
    return cyphers
