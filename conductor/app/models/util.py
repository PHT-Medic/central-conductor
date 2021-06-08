from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import secrets

from conductor.app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    institution = Column(String, default="pht")

    trains = relationship("Train", back_populates="creator")


class TrainLink(Base):
    __tablename__ = 'train_link'
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey('trains.id'))
    station_id = Column(Integer, ForeignKey('stations.id'))