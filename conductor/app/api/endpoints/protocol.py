from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from conductor.app.schemas.train import TrainState, Train, TrainCreate, TrainConfig
from conductor.app.schemas.protocol import AdvertiseKeysSchema, BroadCastKeysSchema, PostSharedKeys, GetCyphersRequest, \
    DistributeCypher
from conductor.app.crud.train import read_train_state, create_train, get_trains, get_train, read_train_config, \
    update_config
from conductor.app.protocol.broadcast_keys import (update_round_0_on_message,
                                                   update_round_0_on_broadcast,
                                                   create_advertise_keys_message)
from conductor.app.protocol.share_keys import process_share_keys_message, distribute_cyphers
from conductor.app.api.dependencies import get_db
from conductor.app.protocol.aggregator import Aggregator

router = APIRouter()


@router.post("/trains/{train_id}/advertiseKeys", response_model=TrainState)
def collect_key_advertisements(train_id: int, message: AdvertiseKeysSchema, db: Session = Depends(get_db)):
    """
    Route for participants to advertise keys when the protocol for the specified train is in round 0
    """
    # state = update_round_0_on_message(db, train_id, message)
    aggregator = Aggregator()
    state = aggregator.process_key_advertisement(db, train_id, message)
    return state


@router.get("/trains/{train_id}/broadcastKeys", response_model=BroadCastKeysSchema)
def distribute_collected_keys(train_id: int, db: Session = Depends(get_db)):
    """
    When the advertisement round of an iteration is finished receive a list of user associated key pairs
    """
    broadcast = update_round_0_on_broadcast(db, train_id=train_id)
    return broadcast


@router.post("/trains/{train_id}/shareKeys", response_model=TrainState)
def collect_key_shares(train_id: int, msg: PostSharedKeys, db: Session = Depends(get_db)):
    state = process_share_keys_message(db, msg, train_id)
    return state


@router.post("/trains/{train_id}/cyphers", response_model=List[DistributeCypher])
def distribute_collected_cyphers(train_id: int, cypher_msg: GetCyphersRequest, db: Session = Depends(get_db)):
    cyphers = distribute_cyphers(db, train_id, cypher_msg)
    return cyphers
