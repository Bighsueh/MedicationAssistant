from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImageSendMessage

import requests
import os

from app.Role import User,Agent
import app.Chat as Chat
import app.Model as Model
from app.MedicationHandler import MedicationHandler
import json
from app.OCRreal import ocr_photo

app = FastAPI()

line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET")) 

rag_endpoint = os.environ.get("RAG_ENDPOINT")
# line_bot_api = LineBotApi('fcifERiOlL1tXOldxV1nVoBsrzuWjaF+LZ7W75D4JmMJtjFf3UAZoGWI7qpSLBybK1EKINUTsAHibFVebKJzZxkbac6xdhZ6MHTfXh5wlyO4jMtzAy1QsiuQ8a6gf7WXFUqbZ2xPFVp0eKVoHuKoKQdB04t89/1O/w1cDnyilFU=')
# handler = WebhookHandler('95f8ea74a89132626f6756564aa977ec')


# Line Bot config
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/getfile/<filename>')
def get_file(filename):
    file_path = f"./{filename}"
    return FileResponse(file_path)


# @app.post("/callback")
# async def callback(request: Request):
#     signature = request.headers["X-Line-Signature"]
#     body = await request.body()
#     print(body)
#     #body = request.get_data(as_text=True)                    # 取得收到的訊息內容
#     try:
#         json_data = json.loads(body)                         # json 格式化訊息內容
#         print(body)
#         tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
#         type = json_data['events'][0]['message']['type']     # 取得 LINE 收到的訊息類型
#         # 判斷如果是文字
#         if type=='text':
#             msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
#             line_id = json_data['destination']
#             #save_image_to_database(str(msg), str(line_id))
#             reply = msg
#         # 判斷如果是圖片
#         elif type == 'image':
#             msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
#             message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
#             # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
#             with open(f'{msgID}.jpg', 'wb') as fd:
#                 fd.write(message_content.content)             # 以二進位的方式寫入檔案
#             #save_image_to_database(msgID)
#             reply = str(ocr_photo(f"https://5d18-140-115-126-172.ngrok-free.app/getfile/{msgID}.jpg"))

#             #reply = '圖片儲存完成！'                             # 設定要回傳的訊息
#         else:
#             reply = '你傳的不是文字或圖片呦～'
#         print(reply)
#         line_bot_api.reply_message(tk,TextSendMessage(reply))  # 回傳訊息
#     except Exception as e:
#         print(f"Error: {e}")                                          # 如果發生錯誤，印出收到的內容
#     return 'OK'              
    


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
def handling_messages(event):
    print(event)
    if isinstance(event.message, ImageMessage):
        # line user id
        userId = event.source.user_id
        print('userId: ', userId)

        # handle image message
        image_message_content = line_bot_api.get_message_content(event.message.id)
        image_data = image_message_content.content

        # 存儲圖片到本地端
        image_filename = f"{userId}_image.jpg"  
        with open(image_filename, "wb") as file:
            file.write(image_data)

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

        if '藥' in userMessage:
            # get side effect by user id     
            sideEffectMessage = MedicationHandler().get_side_effect_message_by_user_id(str(userId))
            
            userMessage = userMessage + sideEffectMessage
        
        else:
            argSchema = requests.get(f'{rag_endpoint}/{userMessage}').text
            userMessage = f"""{userMessage}
            Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible.
            You must respond according to the following schema:
            {argSchema}
            """
        
        user = User(userId)
        agent = Agent("MedicationAssistant")

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



