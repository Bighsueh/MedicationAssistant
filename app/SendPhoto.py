# import psycopg2
# import requests
# import datetime
# import random  # 導入random模組

# def send_image(token, to, image_url, text):
#     headers = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json',
#     }

#     data = {
#         'to': to,
#         'messages': [
#             {
#                 'type': 'text',
#                 'text': text
#             },
#             {
#                 'type': 'image',
#                 'originalContentUrl': image_url,
#                 'previewImageUrl': image_url
#             }
#         ]
#     }
#     try:
#         response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
#         print(response)
#     except:
#         print('err')
    
#     return response.json()

# # 替換成你的Line Channel Access Token和用戶ID
# token = 'Y5inqLI3ZsckR5j1L7JdHAG4zpC+6W5yLjsUMRC+Y3ZzPs+pw1kqpPjXZsw+mbBXK1EKINUTsAHibFVebKJzZxkbac6xdhZ6MHTfXh5wlyN7lpn5BtEESPDn7gQOVEWuJEkd10/mydXXIU8KPyATuQdB04t89/1O/w1cDnyilFU='
# user_id = 'U88a6808255645177d906c8c49880fe25'

# # 圖片URL列表
# image_urls = [
#     'https://drive.google.com/uc?export=view&id=1_rNsxmPi4_j2BLpqcncfslpMFZazsHmP',
#     'https://drive.google.com/uc?export=view&id=1n3fWG1H2qXB9bu3oVnBBoNRRqbutqFs8',
#     'https://drive.google.com/uc?export=view&id=1ojk__flEsrYVqGfaaRH6KWPIzVZj6ggv',
#     'https://drive.google.com/uc?export=view&id=1Pa_YY5DsbOShi7wqsCJyFOWH2cGAAuam',
#     'https://drive.google.com/uc?export=view&id=1wj8kqzJJGi3nPOQr-rtCsiLwzIn67ztT',
#     'https://drive.google.com/uc?export=view&id=1lm8TAdvuJTSs3X3Zq1P9d-mnb8WQRa7W',
#     'https://drive.google.com/uc?export=view&id=10mO0kdydtHuZSbFGXWLs4AqX24yoLy53'
# ]

# # 隨機選擇一個圖片URL
# random_image_url = random.choice(image_urls)

# # 要發送的文字訊息
# text_message = "這是今天的隨機圖片"

# # 發送隨機選擇的圖片
# send_image(token, user_id, random_image_url, text_message)


import psycopg2
import requests
import datetime
import random
from app.PostgreModel import PostgreSQLConnector

def get_medication_reminders():
    pg_connector = PostgreSQLConnector()
    pg_connector.connect()

    current_hour = datetime.datetime.now().hour
   
    sql_query_find_user = """
    SELECT user_id from medication_schema.medication_records;
    """
    pg_connector.execute_query(sql_query_find_user)
    all_user_id = pg_connector.fetch_all()
    user_list = [item[0] for item in all_user_id]
    print(user_list)
    for user in user_list:

    # 執行用藥提醒查詢
        sql_query = f"""
        SELECT 
            medication_schema.medication_record_detail.trade_name, 
            medication_schema.medication_record_detail.dose_per_time, 
            medication_schema.medication_record_detail.morning, 
            medication_schema.medication_record_detail.noon, 
            medication_schema.medication_record_detail.night, 
            medication_schema.medication_record_detail.bed 
        FROM 
            medication_schema.medication_records
        JOIN 
            medication_schema.medication_record_detail ON medication_schema.medication_records.record_id = medication_schema.medication_record_detail.record_id 
        WHERE 
            medication_schema.medication_records.user_id = '{user}';
        """

        pg_connector.execute_query(sql_query)
        
        records = pg_connector.fetch_all()
        print(records)
        # 關閉連接
        reminders = []
        for record in records:
            trade_name, dose_per_time, morning, noon, night, bed = record
            if (current_hour == 8 and morning) or \
            (current_hour == 12 and noon) or \
            (current_hour == 18 and night) or \
            (current_hour == 24 and bed):
                reminders.append((trade_name, dose_per_time))

        for trade_name, dose_per_time in reminders:
            random_image_url = random.choice(image_urls)
            text_message = f"提醒用藥: {trade_name}, 每次劑量: {dose_per_time}"
            send_image(token, 'U88a6808255645177d906c8c49880fe25', random_image_url, text_message)

        
    
    pg_connector.close_connection()

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
token = 'Y5inqLI3ZsckR5j1L7JdHAG4zpC+6W5yLjsUMRC+Y3ZzPs+pw1kqpPjXZsw+mbBXK1EKINUTsAHibFVebKJzZxkbac6xdhZ6MHTfXh5wlyN7lpn5BtEESPDn7gQOVEWuJEkd10/mydXXIU8KPyATuQdB04t89/1O/w1cDnyilFU='
user_id = 'U88a6808255645177d906c8c49880fe25'

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

# 使用 PostgreSQLConnector 進行資料庫操作


# 獲取用藥提醒
# reminders = get_medication_reminders(user_id)

get_medication_reminders()
# # 為每個提醒發送Line消息
# for trade_name, dose_per_time in reminders:
#     random_image_url = random.choice(image_urls)
#     text_message = f"提醒用藥: {trade_name}, 每次劑量: {dose_per_time}"
#     send_image(token, 'U88a6808255645177d906c8c49880fe25', random_image_url, text_message)
