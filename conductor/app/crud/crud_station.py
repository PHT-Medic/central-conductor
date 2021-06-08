from .base import CRUDBase
from conductor.app.models.station import Station
from conductor.app.schemas import StationCreate, StationUpdate


class CRUDStation(CRUDBase[Station, StationCreate, StationUpdate]):
    pass


stations = CRUDStation(Station)