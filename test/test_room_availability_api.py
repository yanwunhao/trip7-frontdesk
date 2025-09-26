import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def test_room_availability():
    """Test room availability query with dates 7 days from now"""
    # Calculate test dates (7 days from now and 2 nights stay)
    check_in_date = datetime.now() + timedelta(days=7)
    check_out_date = check_in_date + timedelta(days=2)
    
    test_params = {
        "action": "check",
        "date_from": check_in_date.strftime("%Y-%m-%d"),
        "date_to": check_out_date.strftime("%Y-%m-%d"),
        "adults": 2,
        "children": 0,
    }

    api_url = os.getenv("DB_API_URL")

    print(f"Testing room availability API: {api_url}")
    print(f"Test parameters: {json.dumps(test_params, ensure_ascii=False, indent=2)}")
    print("-" * 50)

    try:
        response = requests.get(
            api_url,
            params=test_params,
            timeout=10,
        )

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success"):
                    print("✅ Room availability test successful!")
                    print(f"Found {data.get('total_options', 0)} available options")
                    return True
                else:
                    print(
                        f"❌ API returned error: {data.get('message', 'Unknown error')}"
                    )
                    return False
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return False
        else:
            print("❌ Room availability test failed!")
            return False

    except requests.RequestException as e:
        print(f"❌ Network request failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Test exception: {str(e)}")
        return False


if __name__ == "__main__":
    test_room_availability()