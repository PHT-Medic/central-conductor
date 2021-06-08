from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import jwt
from conductor.app.models.train import Train, TrainConfig


def create_train_token(db: Session, train_id: int, station_id: int):
    db_train = db.query(Train).get(train_id)
    db_train_config = db.query(TrainConfig).filter(TrainConfig.train_id == train_id).first()

    if db_train_config.time_out > 0:
        # TODO add expiry date to token
        pass

    token_payload = {
        "station_id": station_id
    }

    token = jwt.encode(token_payload, key=db_train.key, algorithm="HS256")
    return token

