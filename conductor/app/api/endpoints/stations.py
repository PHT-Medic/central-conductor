from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from conductor.app.schemas.train import Train
from conductor.app.protocol import Aggregator

from conductor.app.api.dependencies import get_db
from conductor.app.crud import stations, trains
from conductor.app.schemas import StationCreate, Station

router = APIRouter()


@router.post("/station", response_model=Station)
def register_station(station_in: StationCreate, db: Session = Depends(get_db)):
    db_station = stations.create(db, obj_in=station_in)
    return db_station


@router.get("/station", response_model=List[Station])
def get_all_stations(db: Session = Depends(get_db)):
    db_stations = stations.get_multi(db)
    return db_stations


@router.get("/station/{station_id}/trains", response_model=List[Train])
def get_trains_for_station(station_id: int, db: Session = Depends(get_db)):
    db_trains = trains.read_trains_for_station(db, station_id)
    return db_trains


@router.get("/station/{station_id}/updates", response_model=List[Train])
def get_trains_for_station(station_id: int, db: Session = Depends(get_db)):
    aggregator = Aggregator()
    db_trains = aggregator.get_updates_for_station(db, station_id)
    return db_trains
