from sqlalchemy.orm import Session
from typing import List

from conductor.app.models.train import Train, TrainState, TrainConfig
from conductor.app.schemas import train


def get_train(db: Session, train_id: int) -> Train:
    return db.query(Train).get(train_id)


def get_trains(db: Session, skip: int = 0, limit: int = 100) -> List[Train]:
    return db.query(Train).offset(skip).limit(limit).all()


def create_train(db: Session, train: train.TrainCreate, creator_id: int):
    db_train = Train(**train.dict(), creator_id=creator_id)
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    # Create initial state and config
    # TODO check if this should be separated
    db_train_state = TrainState(train_id=db_train.id)
    db.add(db_train_state)
    db_train_config = TrainConfig(train_id=db_train.id)
    db.add(db_train_config)
    db.commit()
    return db_train


def read_train_state(db: Session, train_id: int) -> TrainState:
    db_train_state = db.query(TrainState).filter(TrainState.train_id == train_id).first()
    return db_train_state


def read_train_config(db: Session, train_id: int) -> TrainConfig:
    db_train_config = db.query(TrainConfig).filter(TrainConfig.train_id == train_id).first()
    return db_train_config


def update_config(db: Session, train_id: int, config: train.TrainConfig):
    db_config = read_train_config(db, train_id)
    for key, val in config.dict().items():
        setattr(db_config, key, val)

    db.commit()
    db.refresh(db_config)
    return db_config
