from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImageSendMessage


import os

from app.Role import User,Agent
import app.Chat as Chat
import app.Model as Model
from app.PostgreModel import save_record_to_database, save_record_detail_to_db
import json
from app.OCRreal import ocr_photo
from app.SendPhoto import send_image, token, user_id, image_urls, text_message
import random

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def send_random_image_task():
    random_image_url = random.choice(image_urls)  # 隨機選擇一個圖片URL
    send_image(token, user_id, random_image_url, text_message)

app = FastAPI()
scheduler = AsyncIOScheduler()
# 設定靜態文件目錄，這樣 FastAPI 才知道從哪裡提供文件
app.mount("/static", StaticFiles(directory="static"), name="static")

line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET")) 
# line_bot_api = LineBotApi('fcifERiOlL1tXOldxV1nVoBsrzuWjaF+LZ7W75D4JmMJtjFf3UAZoGWI7qpSLBybK1EKINUTsAHibFVebKJzZxkbac6xdhZ6MHTfXh5wlyO4jMtzAy1QsiuQ8a6gf7WXFUqbZ2xPFVp0eKVoHuKoKQdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('95f8ea74a89132626f6756564aa977ec')


@app.on_event("startup")
async def startup_event():
    # 在啟動時添加定時任務
    # 每小時執行一次檢查
    scheduler.add_job(send_random_image_task, 'interval', minutes=2)
    scheduler.start()

# Line Bot config
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/getfile/<filename>')
def get_file(filename):
    file_path = f"./static/{filename}"
    print(file_path)
    return FileResponse(file_path)


@app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"


@handler.add(MessageEvent, message=ImageMessage)
def shitt(event):
    print(event)
    if isinstance(event.message, ImageMessage):
        # line user id
        userId = event.source.user_id
        print('userId: ', userId)

        # handle image message
        image_message_content = line_bot_api.get_message_content(event.message.id)
        image_data = image_message_content.content

        # 存儲圖片到本地端
        image_filename = f"static/{event.message.id}.jpg"  
        #image_filename = f"{event.message.id}.jpg"  
        with open(image_filename, "wb") as file:
            file.write(image_data)
        print(image_filename)

        test = ocr_photo(f"https://6b88-140-115-126-172.ngrok-free.app/getfile/{event.message.id}.jpg")
        #test = ocr_photo(f"https://6b88-140-115-126-172.ngrok-free.app/{event.message.id}.jpg")
        
        record_id = save_record_to_database(userId, test)
        save_record_detail_to_db(record_id, test)
        print('圖片儲存完成！')                   

        # 回覆訊息
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"local image path：{image_filename}"))
    # # line user id
    # userId = event.source.user_id
    # tk = event.reply_token            # 取得回傳訊息的 Token
    # print(event)

    # msgID = event.message.id  # 取得訊息 id
    # print(msgID)

    # message_content = line_bot_api.get_message_content(msgID)
    # print(message_content)
    # try:
    #     with open(f'{msgID}.jpg', 'wb') as fd:
    #         fd.write(message_content.iter_content())
    #     print("Image saved successfully.")
    # except Exception as e:
    #     print(f"Error saving image: {e}")
    #save_image_to_database(msgID)
    #reply = str(ocr_photo(f"https://5ca0-140-115-126-172.ngrok-free.app/getfile/{msgID}.jpg"))
        # reply = '收到圖片!'
        # print(reply)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(reply)))




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

