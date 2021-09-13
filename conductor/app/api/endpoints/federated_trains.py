from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Any

from conductor.app.crud.station import register_train_for_station
from conductor.app.protocol.token import create_train_token
from conductor.app.schemas.train import TrainState, Train, TrainCreate, TrainConfig
from conductor.app.schemas.discovery import DiscoveryResultCreate, DiscoveryResults

from conductor.app.crud.train import read_train_state, create_train, get_trains, get_train, read_train_config, update_config
from conductor.app.api.dependencies import get_db
from conductor.app.crud import trains, dl_models, discover
from conductor.app.schemas.dl_models import DLModelCreate, DLModel, DLModelUpdate

router = APIRouter()


# TODO authentication user based or with train token


@router.post("/trains", response_model=Train, tags=["Trains"])
def create_train_for_user(
        creator_id: int, train_in: TrainCreate, db: Session = Depends(get_db)
):
    db_train = trains.create_train_for_user(db, creator_id, train_in)
    return db_train


@router.get("/trains", response_model=List[Train], tags=["Trains"])
def read_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_trains = trains.get_multi(db, skip=skip, limit=limit)
    return db_trains


@router.get("/trains/{train_id}", response_model=Train, tags=["Trains"])
def read_train(train_id: int, db: Session = Depends(get_db)):
    db_train = trains.get(db, train_id)
    print(db_train.participants)

    # resp = Train(**db_train.dict())
    return db_train


@router.get("/trains/{train_id}/state", tags=["Trains"], response_model=TrainState)
def get_train_state(train_id: int, db: Session = Depends(get_db)):
    """
    Read the current state of the train, specified by **{train_id}** from the database and return it as json

    """
    state = read_train_state(db, train_id)
    return state


@router.post("/trains/{train_id}/config", response_model=TrainConfig, tags=["Trains"])
def update_train_config(train_id: int, config_in: TrainConfig, db: Session = Depends(get_db)):
    config = update_config(db, train_id, config_in)
    return config


@router.get("/trains/{train_id}/config", response_model=TrainConfig, tags=["Trains"])
def get_train_config(train_id: int, db: Session = Depends(get_db)):
    config = read_train_config(db, train_id)
    return config


@router.post("/trains/{train_id}/register")
def register_station_for_train(train_id: int, station_id: int, db: Session = Depends(get_db)):
    # TODO catch duplicate registrations
    # TODO get station id from token
    station, train = register_train_for_station(db, train_id, station_id)
    token = create_train_token(db, train_id, station_id)
    return {"token": token}


@router.post("/trains/{train_id}/model", response_model=DLModel)
def upload_model_for_train(train_id: int, model_in: DLModelCreate, db: Session = Depends(get_db)):
    train_model = dl_models.create_model_for_train(db, train_id, model_in)
    return train_model


@router.put("/trains/{train_id}/model", response_model=DLModel)
def update_train_model(train_id: int, model_in: DLModelUpdate, db: Session = Depends(get_db)):
    train_model = dl_models.get_train_model(db, train_id)

    updated_train_model = dl_models.update(db, train_model, model_in)
    return updated_train_model


@router.get("/trains/{train_id}/model", response_model=DLModel)
def read_train_model(train_id: int, db: Session = Depends(get_db)):
    train_model = dl_models.get_train_model(db, train_id)
    return train_model


@router.post("/trains/{train_id}/discovery", response_model=DiscoveryResults)
def submit_discovery_results(train_id: Any, discovery_in: DiscoveryResultCreate, db: Session = Depends(get_db)):
    print(discovery_in)
    db_discovery = discover.create_for_train(db, train_id=train_id, obj_in=discovery_in)
    return db_discovery


@router.post("/trains/{train_id}/model/aggregate")
def aggregate_model_params(train_id: int, db: Session = Depends(get_db)):
    # TODO load existing aggregate from memory/file add the received parameters, update the state
    pass
