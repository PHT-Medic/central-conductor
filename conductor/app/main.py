from fastapi import Depends, FastAPI, HTTPException
from conductor.app.api.api import api_router


app = FastAPI(title="PHT Conductor", version="0.1.1")


app.include_router(api_router)

