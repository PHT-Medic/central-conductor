import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import secrets

from conductor.app.db.base_class import Base


class AdvertiseKeysMessage(Base):
    __tablename__ = 'msg_advertise_keys'

    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    name = Column(String, default=str(uuid.uuid4()))
    station_id = Column(Integer, ForeignKey("stations.id"))
    iteration = Column(Integer)
    # TODO add unique constraints
    signing_key = Column(String)
    sharing_key = Column(String)
    key_signature = Column(String, nullable=True)

    received_at = Column(DateTime, default=datetime.now())


class ShareKeysMessage(Base):
    __tablename__ = "msg_share_keys"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"))
    sender = Column(Integer, ForeignKey("stations.id"))
    recipient = Column(Integer)
    cypher = Column(String)
    iteration = Column(Integer)
