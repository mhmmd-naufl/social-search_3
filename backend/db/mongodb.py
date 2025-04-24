from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongo_url)

db = client.social_search  # nama database
search_collection = db.search_results  # nama koleksi
