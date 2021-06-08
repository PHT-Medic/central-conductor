import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase, CreateSchemaType, ModelType
from conductor.app.models.discovery import DiscoveryResult
from conductor.app.schemas import discovery


class CRUDDiscoveryResults(CRUDBase[DiscoveryResult, discovery.DiscoveryResultCreate, discovery.DiscoveryResultsUpdate]):

    def create_for_train(self, db: Session, *, train_id: Any, obj_in: CreateSchemaType) -> ModelType:
        obj_in_dict = obj_in.dict()
        obj_in_dict["results"] = json.dumps(obj_in_dict["results"])
        db_results = self.model(**obj_in_dict)
        db_results.train_id = train_id
        db.add(db_results)
        db.commit()
        db.refresh(db_results)
        return db_results


discover = CRUDDiscoveryResults(DiscoveryResult)
