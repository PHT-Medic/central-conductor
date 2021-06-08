import uvicorn
from conductor.app.db.setup_db import setup_db, populate_db_for_testing, reset_db
from dotenv import load_dotenv, find_dotenv
import os

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    setup_db()
    # reset_db()
    # populate_db_for_testing()
    uvicorn.run("app.main:app", host="0.0.0.0", reload=os.getenv("ENVIRONMENT") != "prod")

