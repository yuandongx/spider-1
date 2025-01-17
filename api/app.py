import os
from logging import info 
from urllib.parse import quote_plus
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_USER = os.getenv('MONGO_USER') or 'root'
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD') or 'example'
MONGO_HOST = os.getenv('MONGO_HOST') or '123.249.37.220'
MONGO_PORT = os.getenv('MONGO_PORT') or 27017

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    _user = quote_plus(MONGO_USER)
    _pass = quote_plus(MONGO_PASSWORD)
    uri = f"mongodb://{_user}:{_pass}@{MONGO_HOST}"
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.database = app.mongodb_client.get_default_database('stock')
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield

    # Shutdown
    app.mongodb_client.close()


# app: FastAPI = FastAPI(lifespan=db_lifespan)
app: FastAPI = FastAPI()
