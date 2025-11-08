from pymongo import MongoClient
from dotenv import load_dotenv
import os

def clean_doc(doc: dict, stringify_id=True) -> dict:
    if "_id" in doc:
        del doc["_id"]        
        
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

db = client["sleep"]

user_col = db["users"]
auth_col = db["auth"]