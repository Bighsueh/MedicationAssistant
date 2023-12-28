import app.MongoDB as DB
from app.Role import User,Agent

import os
import json
from datetime import datetime
from typing import List, Dict

# define chatlog
Chatlog = Dict[str,str]
ChatlogFormat = List[Chatlog]

def getHistoryChatlog(user:User,agent:Agent):
    client = DB.connectToMongoDB()
    
    db = client[os.environ.get("MONGODB_DATABASE")]
    collection = db[os.environ.get("MONGODB_COLLECTION")]
    
    historyChatlog = DB.getAllChatlog(collection, user, agent)

    client.close()
    return historyChatlog

def createNewHistoryChatlog(user:User,agent:Agent):
    client = DB.connectToMongoDB()
    
    db = client[os.environ.get("MONGODB_DATABASE")]
    collection = db[os.environ.get("MONGODB_COLLECTION")]
    
    document = {
        "agentId": agent.get_agentId(),
        "userId": user.get_userId(),
        "timestamp": datetime.now(),
        "chatlog": [
            {
                "role":"system",
                "content":agent.getAgentBackground()
            }
        ]
    }

    insertResult = collection.insert_one(document)

    print("Inserted document ID:", insertResult.inserted_id)

    client.close()

def genPrompt(tracelog: ChatlogFormat, userText: str, role:str):
    prompt = {
        "role": role,
        "content": userText,
    }
    tracelog.append(prompt)
    jsonTracelog = json.dumps(tracelog, indent=2, ensure_ascii=False)
    
    return tracelog

def updatehistoryChatlog(historyChatlog, promptText, gptResponse):
     # gpt response
    responseContent = gptResponse['choices'][0]['message']['content']

    role = "assistant"
    newHistoryChatlog = genPrompt(promptText, responseContent, role)

    # mongo object id
    objectId = historyChatlog['_id']#.binary.hex()

    # db client
    client = DB.connectToMongoDB()
    
    db = client[os.environ.get("MONGODB_DATABASE")]
    collection = db[os.environ.get("MONGODB_COLLECTION")]
    
    updateResult = collection.update_one(
        {"_id": objectId},
        {"$set": {"chatlog": newHistoryChatlog}}
    )

    print("Matched:", updateResult.matched_count)
    print("Modified:", updateResult.modified_count)

    client.close()