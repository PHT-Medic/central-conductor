from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
if os.getenv("CONDUCTOR_DB"):
    SQLALCHEMY_DATABASE_URL = os.getenv("CONDUCTOR_DB")
    print("Connecting to DB specified in env vars.")
else:
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost/pht_conductor"
    print("Connecting to default database on localhost")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}  For sqlite db
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
