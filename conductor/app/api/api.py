from fastapi import APIRouter
from conductor.app.api.endpoints import trains, util, stations, protocol

api_router = APIRouter(prefix="/api")

api_router.include_router(trains.router, tags=["Trains"])
api_router.include_router(stations.router, tags=["Stations"])
api_router.include_router(util.router, tags=["Admin"])
api_router.include_router(protocol.router, tags=["Protocol"])
