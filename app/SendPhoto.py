import psycopg2
import requests
import datetime
import random  # 導入random模組

def send_image(token, to, image_url, text):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    data = {
        'to': to,
        'messages': [
            {
                'type': 'text',
                'text': text
            },
            {
                'type': 'image',
                'originalContentUrl': image_url,
                'previewImageUrl': image_url
            }
        ]
    }

    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
    return response.json()

# 替換成你的Line Channel Access Token和用戶ID
token = 'fcifERiOlL1tXOldxV1nVoBsrzuWjaF+LZ7W75D4JmMJtjFf3UAZoGWI7qpSLBybK1EKINUTsAHibFVebKJzZxkbac6xdhZ6MHTfXh5wlyO4jMtzAy1QsiuQ8a6gf7WXFUqbZ2xPFVp0eKVoHuKoKQdB04t89/1O/w1cDnyilFU='
user_id = 'U211c923e33a8c72357c0683d322a1b10'

# 圖片URL列表
image_urls = [
    'https://drive.google.com/uc?export=view&id=1_rNsxmPi4_j2BLpqcncfslpMFZazsHmP',
    'https://drive.google.com/uc?export=view&id=1n3fWG1H2qXB9bu3oVnBBoNRRqbutqFs8',
    'https://drive.google.com/uc?export=view&id=1ojk__flEsrYVqGfaaRH6KWPIzVZj6ggv',
    'https://drive.google.com/uc?export=view&id=1Pa_YY5DsbOShi7wqsCJyFOWH2cGAAuam',
    'https://drive.google.com/uc?export=view&id=1wj8kqzJJGi3nPOQr-rtCsiLwzIn67ztT',
    'https://drive.google.com/uc?export=view&id=1lm8TAdvuJTSs3X3Zq1P9d-mnb8WQRa7W',
    'https://drive.google.com/uc?export=view&id=10mO0kdydtHuZSbFGXWLs4AqX24yoLy53'
]

# 隨機選擇一個圖片URL
random_image_url = random.choice(image_urls)

# 要發送的文字訊息
text_message = "這是今天的隨機圖片"

# 發送隨機選擇的圖片
send_image(token, user_id, random_image_url, text_message)