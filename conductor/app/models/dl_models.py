from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from conductor.app.db.base_class import Base


class ModelCheckpoint(Base):
    __tablename__ = "model_checkpoints"
    id = Column(Integer, primary_key=True, index=True)
    dl_model_id = Column(Integer, ForeignKey('dl_models.id'))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    checkpoint_path = Column(String, nullable=True)


class DLModel(Base):
    __tablename__ = "dl_models"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey('trains.id'), nullable=True)
    model_id = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    model_type = Column(String)
    model_name = Column(String)
    model_src = Column(String)
    model_logs = Column(String, nullable=True)
    checkpoints = relationship(ModelCheckpoint, backref="dl_models.id")
