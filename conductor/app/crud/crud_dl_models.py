from typing import Any
from sqlalchemy.orm import Session

from .base import CRUDBase

from conductor.app.schemas.dl_models import DLModelCreate, DLModelUpdate
from conductor.app.models import DLModel


class CRUDDLModels(CRUDBase[DLModel, DLModelCreate, DLModelUpdate]):

    def create_model_for_train(self, db: Session, train_id: Any, model_in: DLModelCreate) -> DLModel:
        db_model = DLModel(
            train_id=train_id,
            **model_in.dict()
        )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)

        return db_model

    def get_train_model(self, db: Session, train_id: Any) -> DLModel:
        db_model = db.query(DLModel).filter(DLModel.train_id == train_id).first()
        return db_model


dl_models = CRUDDLModels(DLModel)
