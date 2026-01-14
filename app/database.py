# Import AsyncIOMotorClient for asynchronous MongoDB operations
from motor.motor_asyncio import AsyncIOMotorClient
# Import config to read environment variables from .env file
from decouple import config

# Get MongoDB connection URI from environment variable or use default
MONGO_DETAILS = config("MONGO_URI", default="mongodb://localhost:27017")

# Create an asynchronous MongoDB client
client = AsyncIOMotorClient(MONGO_DETAILS)

# Access the 'asset_tracker' database
db = client.asset_tracker