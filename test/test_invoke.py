#!/usr/bin/env python3
import requests
import json
import uuid
from datetime import datetime

# Base conversation history for all tests
base_conversation = [
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
]

# Test cases for different languages
test_cases = [
    {
        "name": "Chinese Test",
        "lang": "cn",
        "data": {"conversation_history": base_conversation, "lang": "cn"},
    },
    {
        "name": "Japanese Test (default)",
        "lang": "jp",
        "data": {"conversation_history": base_conversation, "lang": "jp"},
    },
    {
        "name": "English Test",
        "lang": "en",
        "data": {"conversation_history": base_conversation, "lang": "en"},
    },
    {
        "name": "Invalid Language Test (should default to Japanese)",
        "lang": "fr",
        "data": {"conversation_history": base_conversation, "lang": "fr"},
    },
    {
        "name": "No Language Parameter Test (should default to Japanese)",
        "lang": None,
        "data": {"conversation_history": base_conversation},
    },
]

# API endpoint
url = "http://localhost:8000/invoke"


def test_language_support():
    print("Testing language support for /invoke endpoint")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Language parameter: {test_case['lang']}")
        print("-" * 30)

        try:
            response = requests.post(url, json={"data": test_case["data"]})

            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result['message'][:100]}...")
            else:
                print(f"Error Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print(
                "Error: Could not connect to the server. Make sure the FastAPI server is running."
            )
        except Exception as e:
            print(f"Error: {e}")

        print()


if __name__ == "__main__":
    test_language_support()
