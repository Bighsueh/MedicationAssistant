import pymongo
import json
import os
from app.Role import User,Agent

def connectToMongoDB():
    try:
        connection_url = os.environ.get("MONGODB_HOST")
        client = pymongo.MongoClient(connection_url)
        print("Success connect to MongoDB！")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print("Fail to connect MongoDB！:", e)
        return None
    
def getAllChatlog(collection, user: User, agent: Agent):
    query = {
        "userId": user.get_userId(),
        "agentId": agent.get_agentId(),
    }

    documents = collection.find_one(query)
    return documents

