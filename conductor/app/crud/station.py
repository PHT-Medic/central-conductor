from sqlalchemy.orm import Session

from conductor.app.models.train import Train
from conductor.app.models.station import Station

from conductor.app.crud.train import get_train
from fastapi.exceptions import HTTPException


def create_station(db: Session, name: str):
    db_station = Station(name=name)
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station


def register_train_for_station(db: Session, train_id: int, station_id: int):
    print(f"Train id: {train_id}, Station ID {station_id}")
    db_train = get_train(db, train_id)

    db_station = db.query(Station).get(station_id)
    if station_id in db_train.participants:
        raise HTTPException(status_code=403, detail=f"Your station is already registered for train: {train_id}")
    db_train.participants.append(db_station)
    db_station.trains.append(db_train)

    db.commit()
    db.refresh(db_train)
    db.refresh(db_station)

    return db_station, db_train


def read_trains_for_station(db: Session, station_id: int):
    db_station = db.query(Station).get(station_id)
    return db_station.trains
