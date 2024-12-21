import os
from logging import info 
from urllib.parse import quote_plus
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    uri = "mongodb://%s:%s@%s" % (
    quote_plus(MONGO_USER), quote_plus(MONGO_PASSWORD), MONGO_HOST)
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield

    # Shutdown
    app.mongodb_client.close()


app: FastAPI = FastAPI(lifespan=db_lifespan)
