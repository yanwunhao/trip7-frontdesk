import json
import os
import requests
from langchain_core.tools import tool
from typing import Optional


@tool
def create_hotel_booking(
    customer_name: str,
    customer_email: str,
    check_in: str,
    check_out: str,
    room_type_id: int,
    customer_phone: Optional[str] = None,
    adults: Optional[int] = None,
    children: Optional[int] = None,
) -> str:
    """
    Create a new hotel booking directly through the API.
    Use this tool when the customer has confirmed their booking details.

    Args:
        customer_name: Customer's full name
        customer_email: Customer's email address
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        room_type_id: Room type ID
        customer_phone: Customer's phone number (optional)
        adults: Number of adult guests (optional, defaults to 1)
        children: Number of children (optional, defaults to 0)

    Returns:
        String containing booking confirmation or error message
    """
    try:
        # Prepare booking data according to API documentation
        booking_data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "check_in": check_in,
            "check_out": check_out,
            "room_type_id": room_type_id,
        }

        # Add optional fields only if provided
        if customer_phone:
            booking_data["customer_phone"] = customer_phone
        if adults is not None:
            booking_data["adults"] = adults
        if children is not None:
            booking_data["children"] = children

        # Use the configured API URL from environment
        api_url = f"{os.getenv('DB_API_URL')}?action=book"

        response = requests.post(
            api_url,
            json=booking_data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                order_info = result.get("order", {})
                order_ref = order_info.get("order_reference", "N/A")
                room_num = order_info.get("room", {}).get("room_number", "N/A")
                total_amount = order_info.get("booking_details", {}).get(
                    "total_amount", 0
                )

                return f"Booking successful! Order reference: {order_ref}, Customer: {customer_name}, Room: {room_num}, Total: {total_amount} CNY"
            else:
                return f"Booking failed: {result.get('message', 'Unknown error')}"
        else:
            return f"API request failed with status code: {response.status_code}"

    except requests.RequestException as e:
        return f"Network request failed: {str(e)}"
    except Exception as e:
        return f"Booking creation failed: {str(e)}"
