from typing import Any
from sqlalchemy.orm import Session
from conductor.app.crud import trains


class Aggregator:

    def get_updates_for_station(self, db: Session, station_id: Any):
        """

        :param station_id:
        :return: 
        """
        db_trains = trains.read_trains_for_station(db=db, station_id=station_id)
        return db_trains
