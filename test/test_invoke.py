#!/usr/bin/env python3
import requests

# Test booking conversation that should trigger function call
booking_conversation = [
    {
        "role": "user",
        "content": "我想预订房间",
        "timestamp": "2025-09-29T10:00:00Z",
    },
    {
        "role": "assistant",
        "content": "好的，请问您需要几间房间，入住日期和退房日期是？",
        "timestamp": "2025-09-29T10:00:05Z",
    },
    {
        "role": "user",
        "content": "我叫董冕雄，邮箱是mx.dong@csse.muroran-it.ac.jp，电话13800138000，需要1间房，2025-10-01入住，2025-10-03退房，2个成人",
        "timestamp": "2025-09-29T10:01:00Z",
    },
]

url = "http://localhost:8000/invoke"

def test_functional_calling():
    print("Testing functional calling for booking system")
    print("=" * 50)

    try:
        response = requests.post(url, json={"data": {"conversation_history": booking_conversation}})

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result['message']}")

            # Check if function call was triggered
            response_text = result['message'].lower()
            if any(indicator in response_text for indicator in [
                "booking successful", "order reference", "预订成功", "订单号"
            ]):
                print("✅ FUNCTION CALL TRIGGERED - Booking processed")
            elif any(indicator in response_text for indicator in [
                "booking failed", "api request failed", "预订失败"
            ]):
                print("⚠️  FUNCTION CALL TRIGGERED - But booking failed")
            else:
                print("❌ NO FUNCTION CALL - Response unclear")
        else:
            print(f"❌ Error: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_functional_calling()
