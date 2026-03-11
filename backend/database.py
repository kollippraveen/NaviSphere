from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017" # Update if using Atlas
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.navisphere
station_collection = database.get_collection("stations_collection")