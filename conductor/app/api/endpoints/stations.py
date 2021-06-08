from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from conductor.app.crud.station import create_station, register_train_for_station, read_trains_for_station
from conductor.app.protocol.token import create_train_token
from conductor.app.schemas.train import Train

from conductor.app.api.dependencies import get_db
from conductor.app.crud import stations
from conductor.app.schemas import StationCreate, Station

router = APIRouter()


@router.post("/stations", response_model=Station)
def register_station(station_in: StationCreate, db: Session = Depends(get_db)):
    db_station = stations.create(db, obj_in=station_in)
    return db_station


@router.get("/stations", response_model=List[Station])
def get_all_stations(db: Session = Depends(get_db)):
    db_stations = stations.get_multi(db)
    return db_stations


@router.get("/stations/{station_id}/trains", response_model=List[Train])
def get_trains_for_station(station_id: int, db: Session = Depends(get_db)):
    trains = read_trains_for_station(db, station_id)
    return trains
