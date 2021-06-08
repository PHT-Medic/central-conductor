from sqlalchemy.orm import Session
from pydantic import BaseModel


def update_train_on_message(db: Session, train_id: int, msg: BaseModel):
    pass