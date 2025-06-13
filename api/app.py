import os
from logging import info 
from urllib.parse import quote_plus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_USER = os.getenv('APP_MONGO_USER') or 'root'
MONGO_PASSWORD = os.getenv('APP_MONGO_PASSWORD') or 'example'
MONGO_HOST = os.getenv('APP_MONGO_HOST') or '127.0.0.1'
MONGO_PORT = os.getenv('APP_MONGO_PORT') or 27017

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    _user = quote_plus(MONGO_USER)
    _pass = quote_plus(MONGO_PASSWORD)
    uri = f"mongodb://{_user}:{_pass}@{MONGO_HOST}"
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.database = app.mongodb_client.get_default_database('stocks')
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield

    # Shutdown
    app.mongodb_client.close()


app: FastAPI = FastAPI(
    root_path='/api/v1',
    lifespan=db_lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有源域名（生产环境需替换为具体域名）
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 显式允许 OPTIONS 方法
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Type", "Authorization"],  # 可选：暴露客户端可读的响应头
)
# app: FastAPI = FastAPI()
