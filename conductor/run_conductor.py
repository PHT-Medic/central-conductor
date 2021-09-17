import uvicorn
from conductor.app.db.setup_db import setup_db, reset_db
from dotenv import load_dotenv, find_dotenv
import os

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    setup_db()
    # reset_db(dev=True)
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run("app.main:app", host="0.0.0.0", reload=os.getenv("ENVIRONMENT") != "prod", log_config=log_config)

