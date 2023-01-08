from pydantic import BaseModel
from fastapi import FastAPI
import motor.motor_asyncio
from . import schema
from ...config import MONGO_DB_CONN_STRING

DB_NAME = "devices"

app = FastAPI()

schema.map_routers(app, DB_NAME)
