import json
import os
import requests


def write_booking_to_database(json_data):
    try:
        booking_data = json.loads(json_data)
        booking_data["room_type_id"] = 1

        api_url = f"{os.getenv('DB_API_URL')}?action=book"

        response = requests.post(
            api_url,
            json=booking_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            return f"Booking saved successfully, customer: {booking_data.get('customer_name', 'N/A')}"
        else:
            return f"Database write failed, status code: {response.status_code}"

    except json.JSONDecodeError as e:
        return f"JSON parsing failed: {str(e)}"
    except requests.RequestException as e:
        return f"Network request failed: {str(e)}"
    except Exception as e:
        return f"Write failed: {str(e)}"