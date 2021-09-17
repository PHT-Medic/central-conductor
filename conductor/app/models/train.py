from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import secrets
from uuid import uuid4


from conductor.app.db.base_class import Base


class Train(Base):
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=str(uuid4()))
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    proposal_id = Column(Integer, default=0)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="trains")

    key = Column(String, default=secrets.token_hex(32))

    participants = relationship("Station", secondary="train_link", backref="Station")

    state = relationship("TrainState", uselist=False, backref="trains")
    config = relationship("TrainConfig", uselist=False, backref="trains")


class TrainConfig(Base):
    __tablename__ = 'train_configs'
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey('trains.id'))
    min_participants = Column(Integer, default=0)
    dropout_allowance = Column(Float, default=0.0)
    batch_size = Column(Integer, default=8)
    epochs = Column(Integer, default=1)
    time_out = Column(Integer, default=0)


# TODO remove round finished and just move to next round once the conditions are met
class TrainState(Base):
    __tablename__ = 'train_states'
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey('trains.id'))
    iteration = Column(Integer, default=0)
    round = Column(Integer, default=0)
    round_start = Column(DateTime, default=datetime.now())
    round_k = Column(Integer, default=0)
    round_ready = Column(Boolean, default=False)
    # round_finished = Column(Boolean, default=False)
    round_messages_sent = Column(Integer, default=0)
    updated_at = Column(DateTime, nullable=True)
    epoch = Column(Integer, default=0)
    discovery_finished = Column(Boolean, default=False)

