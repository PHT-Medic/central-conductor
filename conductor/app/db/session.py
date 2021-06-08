from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# TODO store db credentials in environment variables

if not os.getenv("ENVIRONMENT") == "prod":
    print("Running in development environment")
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost/pht_conductor"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:admin@postgres/pht_conductor"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}  For sqlite db
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
