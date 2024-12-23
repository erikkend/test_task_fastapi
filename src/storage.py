from pymongo import AsyncMongoClient
from src.config import MongoConfig

uri = f'mongodb+srv://{MongoConfig.HOST}:{MongoConfig.PASSWORD}@cluster1.4aghl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1'


mongo_client = AsyncMongoClient(uri)
db = mongo_client.logs_db
collection = db["logs"]

