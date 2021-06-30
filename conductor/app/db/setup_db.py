from conductor.app.db.base import Base
from conductor.app.db.session import engine, SessionLocal
from conductor.app.models.station import Station
from conductor.app.models import User
from conductor.app.crud import trains
from conductor.app.schemas.train import TrainCreate
from fastapi.logger import logger




def setup_db():
    Base.metadata.create_all(bind=engine)
    seed_db_for_testing()


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_db_for_testing()


def seed_db_for_testing():
    logger.info("Checking for database seed")
    session = SessionLocal()

    # Create the three stations defined in the docker compose
    # TODO handle station ids/name better

    stations = session.query(Station).all()
    if not stations:
        print("Creating test stations...")
        station_1 = Station(name="station_1")
        station_2 = Station(name="station_2")
        station_3 = Station(name="station_3")

        session.add(station_1)
        session.add(station_2)
        session.add(station_3)

    users = session.query(User).all()
    if not users:
        print("Creating test user")
        test_user = User(email="test@pht.com", hashed_password="start123!")

        session.add(test_user)

    db_trains = trains.get_multi(session)
    if not db_trains:
        print("Creating test trains")
        test_train_create = TrainCreate(description="test train 1")
        db_train_1 = trains.create_train_for_user(db=session, train_in=test_train_create, creator_id=1)
        test_train_2_create = TrainCreate(description="test train 2")
        db_train_2 = trains.create_train_for_user(db=session, train_in=test_train_2_create, creator_id=1)
        test_train_3_create = TrainCreate(description="test train 3")
        db_train_3 = trains.create_train_for_user(db=session, train_in=test_train_3_create, creator_id=1)

    session.commit()
    session.close()


if __name__ == '__main__':
    # Base.metadata.drop_all(bind=engine)
    setup_db()
