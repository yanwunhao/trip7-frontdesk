import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def test_booking_api():
    test_booking_data = {
        "customer_name": "mx.dong",
        "customer_email": "1234@qq.com",
        "check_in": "2025-12-01",
        "check_out": "2025-12-03",
        "room_type_id": 1,
    }

    api_url = f"{os.getenv('DB_API_URL')}?action=book"

    print(f"Testing API URL: {api_url}")
    print(f"Test data: {json.dumps(test_booking_data, ensure_ascii=False, indent=2)}")
    print("-" * 50)

    try:
        response = requests.post(
            api_url,
            json=test_booking_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            print("✅ Test successful!")
        else:
            print("❌ Test failed!")

    except requests.RequestException as e:
        print(f"❌ Network request failed: {str(e)}")
    except Exception as e:
        print(f"❌ Test exception: {str(e)}")


if __name__ == "__main__":
    test_booking_api()
