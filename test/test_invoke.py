#!/usr/bin/env python3
import requests
import json
import uuid
from datetime import datetime

# Test data - random JSON payload
test_data = {
    "action": "test",
    "data": {
        "id": str(uuid.uuid4()),
        "conversation_history": [
            {
                "role": "user",
                "content": "你好，我想预约一下你们家酒店，两个人，后天下午入住，待三天。",
                "timestamp": "2025-08-28T10:00:00Z",
            },
            {
                "role": "assistant",
                "content": "您好，欢迎来到Trip7箱根仙石原温泉ホテル！很高兴为您服务。您提到要预约两人入住，后天下午入住，待三天。请问您的联系人姓名是？",
                "timestamp": "2025-08-28T10:00:05Z",
            },
            {
                "role": "user",
                "content": "董冕雄。",
                "timestamp": "2025-08-28T10:01:00Z",
            },
            {
                "role": "assistant",
                "content": "好的，联系人姓名是董冕雄。请问您需要早餐服务吗？",
                "timestamp": "2025-08-28T10:01:10Z",
            },
            {
                "role": "user",
                "content": "不是",
                "timestamp": "2025-08-28T10:02:00Z",
            },
        ],
    },
    "timestamp": datetime.now().isoformat() + "Z",
}

# API endpoint
url = "http://160.16.67.238:10021/invoke"

try:
    # Send POST request
    response = requests.post(url, json=test_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

except requests.exceptions.ConnectionError:
    print(
        "Error: Could not connect to the server. Make sure the FastAPI server is running on localhost:8000"
    )
except Exception as e:
    print(f"Error: {e}")
