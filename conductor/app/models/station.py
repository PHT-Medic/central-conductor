from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import secrets


from conductor.app.db.base_class import Base
from .train import Train


class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    trains = relationship(Train, secondary="train_link", backref="Train", overlaps="Station,participants")
