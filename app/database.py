from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
    client.server_info() 
    print("✅ Connected to MongoDB Atlas!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

db = client["sample_mflix"]
users_collection = db["users"]
shows_collection = db["movies"]
