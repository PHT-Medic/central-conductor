from conductor.app.db.base import Base
from conductor.app.db.session import engine, SessionLocal
from conductor.app.models.station import Station
from conductor.app.models import User


def setup_db():
    Base.metadata.create_all(bind=engine)


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def populate_db_for_testing():
    print("Populating DB with test data")
    session = SessionLocal()

    # Create the three stations defined in the docker compose
    # TODO handle station ids/name better
    station_1 = Station(name="station_1")
    station_2 = Station(name="station_2")
    station_3 = Station(name="station_3")

    session.add(station_1)
    session.add(station_2)
    session.add(station_3)

    test_user = User(email="test@pht.com", hashed_password="start123!")

    session.add(test_user)

    session.commit()
    session.close()


if __name__ == '__main__':
    # Base.metadata.drop_all(bind=engine)
    setup_db()
