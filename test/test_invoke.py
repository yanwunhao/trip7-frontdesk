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
                "content": "你好，我想预订一间房间",
                "timestamp": "2025-08-28T10:00:00Z",
            },
            {
                "role": "assistant",
                "content": "您好！欢迎来到我们酒店。我很乐意帮您预订房间。请问您需要什么类型的房间，以及入住和退房的日期是什么时候？",
                "timestamp": "2025-08-28T10:00:05Z",
            },
            {
                "role": "user",
                "content": "我需要一间标准双人房，8月29日入住，8月31日退房",
                "timestamp": "2025-08-28T10:01:00Z",
            },
            {
                "role": "assistant",
                "content": "好的，让我为您查询8月29日到8月31日的标准双人房。我们有房间可用，价格是每晚380元。请问您需要预订吗？还需要其他服务吗？",
                "timestamp": "2025-08-28T10:01:10Z",
            },
            {
                "role": "user",
                "content": "价格可以接受，请帮我预订。另外想问一下早餐是否包含在内？",
                "timestamp": "2025-08-28T10:02:00Z",
            },
        ],
    },
    "timestamp": datetime.now().isoformat() + "Z",
}

# API endpoint
url = "http://localhost:8000/invoke"

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
