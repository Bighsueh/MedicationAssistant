from pydantic import BaseModel
import requests
import app.Chat as Chat

class ChatInfo(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 800
    top_p : float = 0.95
    purpose :str = "none"
    api_url : str
    prompt_text : Chat.ChatlogFormat
    frequency_penalty : float = 0.8
    presence_penalty : float = 0.8
    stop :str ="stop"
    past_messages : int = 20

def callGPT(chat_info : ChatInfo):
    target_url = chat_info.api_url

    # 請求參數
    params = {
        "temperature": chat_info.temperature,
        "max_tokens": chat_info.max_tokens,
        "top_p": chat_info.top_p,
        "purpose": chat_info.purpose,
        "frequency_penalty": chat_info.frequency_penalty,
        "presence_penalty": chat_info.presence_penalty,
        "stop": chat_info.stop,
        "past_messages": chat_info.past_messages
    }

    request_body = chat_info.prompt_text

    response = requests.post(target_url, json=request_body, params=params)

    print(response)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print("request error:", response.status_code)
        return response.content
