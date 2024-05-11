import os 
from datetime import datetime
from typing import List
from bson.objectid import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument

from app.utils.default_questions import DEFAULT_QUESTIONS

uri = f"mongodb+srv://qmsoqm2:{os.environ["MONGO_DB_PASSWORD"]}@chathistory.tmp29wl.mongodb.net/?retryWrites=true&w=majority&appName=chatHistory"

def fetch_document(phone_number: str) -> dict:
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        db = client.get_database('chat_history')
        history_collection= db.get_collection('history')
        document = history_collection.find_one_and_update(
            {"phone_number": phone_number},
            {"$setOnInsert": {
                "phone_number": phone_number,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "user_info": {"age": "30"},
                "messages": [], 
                "questions": [*DEFAULT_QUESTIONS],
                "ephemeral": {}
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
    except Exception as e:
        print(e)
        return None

    return document

def update_document(phone_number: str, document: dict) -> bool:
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.get_database('chat_history')
    history_collection= db.get_collection('history')
    history_collection.update_one(
        {"phone_number": phone_number}, 
        {'$set': document}
    )

    return True

def delete_document(phone_number: str) -> bool:
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.get_database('chat_history')
    history_collection= db.get_collection('history')
    history_collection.delete_one(
        {"phone_number": phone_number}
    )

    return True