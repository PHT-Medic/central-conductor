# Create a SQL alchemy session maker to be used
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost/pht_conductor"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}  For sqlite db
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
