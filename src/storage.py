import time

from pymongo import AsyncMongoClient

mongo_client = AsyncMongoClient(f"mongodb://mongodb:27017/")
db = mongo_client.logs_db
collection = db["logs"]

async def save_message_log(message_id):
    await collection.insert_one({"saved_message_id": f"{message_id}", "timestamp": f"{time.time()}","status": "ok"})
