from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGO_DETAILS = config("MONGO_URI", default="mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.asset_tracker