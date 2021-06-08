from fastapi.testclient import TestClient
from dotenv import load_dotenv, find_dotenv
from fixtures import SessionLocal

# Initialize environment variables
load_dotenv(find_dotenv())

from conductor.app.main import app


# Setup test client and db session
client = TestClient(app)
session = SessionLocal()

def test_read_trains():
    response = client.get("/api/trains")
    assert response.status_code == 200