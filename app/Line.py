from fastapi import FastAPI, Request, HTTPException

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import app.postgresql as postgre

import os

from app.Role import User,Agent
import app.Chat as Chat
import app.Model as Model

app = FastAPI()

postgre.create_tables()

line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET")) 

# Line Bot config
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handling_message(event):
    if isinstance(event.message, TextMessage):
        # line user id
        userId = event.source.user_id    

        # line user input message        
        userMessage = event.message.text

        user = User(userId)
        agent = Agent("facilator")

        # get history chatlog
        historyChatlog = Chat.getHistoryChatlog(user,agent)

        # if history chatlog not exist, create a new one
        if historyChatlog is None:
            Chat.createNewHistoryChatlog(user,agent)
            historyChatlog = Chat.getHistoryChatlog(user,agent)

        chatlogJson: Chat.ChatlogFormat = historyChatlog['chatlog']

        # combine userMessage as prompt
        role: str = "user"
        promptText = Chat.genPrompt(chatlogJson,userMessage,role)

        # send prompt to GPT
        chatInfo = Model.ChatInfo(
            api_url= os.environ.get("GPT_API_URL"), 
            prompt_text=promptText,
            purpose="none"
        )
        gptResponse = Model.callGPT(chatInfo)

        responseContent = gptResponse['choices'][0]['message']['content']

        # update response to db
        Chat.updatehistoryChatlog(historyChatlog,promptText,gptResponse)
        
        userMessage = str(responseContent)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=userMessage))



