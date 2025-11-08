from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os

def clean_doc(doc: dict, stringify_id=True) -> dict:
    if "_id" in doc:
        del doc["_id"]        
    return doc
        
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

db = client["sleep"]

user_col = db["users"]
auth_col = db["auth"]
coin_col = db["coin"]
money_col = db["money"]

team_col = db["teams"]
team_members_col = db["team_members"]

team_col.create_index("name", unique=True, sparse=True) 
team_members_col.create_index([("team_id", ASCENDING), ("user_id", ASCENDING)], unique=True) 
