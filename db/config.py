import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@mongo:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client['meals_category_chefs']
