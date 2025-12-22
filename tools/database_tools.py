import json
import os
import requests
from langchain_core.tools import tool
from typing import Optional, List, Dict

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def search_available_rooms(
    checkin: str,
    checkout: str,
    adults: int,
    rooms: int = 1,
    children: int = 0,
) -> str:
    """
    Search for available hotel rooms based on check-in/check-out dates and guest count.
    Use this tool when customers ask about room availability or want to search for rooms.

    Args:
        checkin: Check-in date in YYYY-MM-DD format (e.g., "2025-11-21")
        checkout: Check-out date in YYYY-MM-DD format (e.g., "2025-11-22")
        adults: Number of adult guests (required)
        rooms: Number of rooms needed (defaults to 1)
        children: Number of children (defaults to 0)

    Returns:
        JSON string containing available room information or error message
    """
    logger.info(f"[TOOL] search_available_rooms called: checkin={checkin}, checkout={checkout}, adults={adults}, rooms={rooms}, children={children}")
    try:
        # Prepare search parameters
        params = {
            "checkin": checkin,
            "checkout": checkout,
            "adults": adults,
            "rooms": rooms,
            "children": children,
        }

        # Build API URL
        api_url = f"{os.getenv('DB_API_URL')}/api/rooms/search"

        response = requests.get(
            api_url,
            params=params,
            timeout=10,
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                # Return the result as JSON string for the LLM to process
                return json.dumps(result, ensure_ascii=False)
            else:
                return json.dumps(
                    {
                        "success": False,
                        "message": result.get("message", "Search failed"),
                    },
                    ensure_ascii=False,
                )
        else:
            return json.dumps(
                {
                    "success": False,
                    "message": f"API request failed with status code: {response.status_code}",
                },
                ensure_ascii=False,
            )

    except requests.RequestException as e:
        return json.dumps(
            {"success": False, "message": f"Network request failed: {str(e)}"},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps(
            {"success": False, "message": f"Room search failed: {str(e)}"},
            ensure_ascii=False,
        )


@tool
def format_rooms_html(
    rooms_json,
    checkin: str = "",
    checkout: str = "",
    adults: int = 0,
    rooms: int = 1,
    children: int = 0,
) -> str:
    """
    Format room search results into HTML for display to the user.
    Use this tool AFTER search_available_rooms to present the results in a user-friendly format.

    Args:
        rooms_json: JSON string or dict from search_available_rooms containing room data
        checkin: Check-in date (YYYY-MM-DD) for generating booking link
        checkout: Check-out date (YYYY-MM-DD) for generating booking link
        adults: Number of adults for generating booking link
        rooms: Number of rooms for generating booking link (default 1)
        children: Number of children for generating booking link (default 0)

    Returns:
        HTML formatted string with room information, images, details and booking link
    """
    logger.info(f"[TOOL] format_rooms_html called")
    try:
        # Parse the JSON data - handle both string and dict input
        if isinstance(rooms_json, str):
            data = json.loads(rooms_json)
        else:
            data = rooms_json

        if not data.get("success"):
            return (
                f"<p style='color: red;'>❌ {data.get('message', 'Search failed')}</p>"
            )

        rooms = data.get("data", [])

        if not rooms or len(rooms) == 0:
            return "<p>😔 申し訳ございません。指定された条件に合う空室がございません。別の日程または条件をお試しください。</p>"

        # Build HTML for all rooms
        html_parts = [
            f"<div style='margin: 20px 0;'><h3>✨ {len(rooms)}種類のお部屋がご利用可能です</h3></div>"
        ]

        for room in rooms:
            room_html = f"""
<div style='border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px; margin: 15px 0; background-color: #f9f9f9;'>
    <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
        <div style='flex: 0 0 200px;'>
            <img src='{room.get("image_path", "")}'
                 alt='{room.get("room_type_name", "")}'
                 style='width: 100%; border-radius: 8px; object-fit: cover;'/>
        </div>
        <div style='flex: 1; min-width: 250px;'>
            <h4 style='margin: 0 0 10px 0; color: #2c3e50;'>{room.get("room_type_name", "")}</h4>
            <p style='margin: 5px 0; color: #7f8c8d; font-size: 14px;'>{room.get("room_type_name_en", "")}</p>
            <p style='margin: 8px 0; font-size: 14px;'>{room.get("description", "")}</p>
            <div style='margin-top: 10px;'>
                <span style='display: inline-block; margin: 5px 10px 5px 0; padding: 5px 10px; background-color: #e8f4f8; border-radius: 5px; font-size: 13px;'>
                    📐 {room.get("room_size", "")}
                </span>
                <span style='display: inline-block; margin: 5px 10px 5px 0; padding: 5px 10px; background-color: #e8f4f8; border-radius: 5px; font-size: 13px;'>
                    🛏️ {room.get("bed_type", "")}
                </span>
                <span style='display: inline-block; margin: 5px 10px 5px 0; padding: 5px 10px; background-color: #e8f4f8; border-radius: 5px; font-size: 13px;'>
                    👥 最大{room.get("max_occupancy", "")}名
                </span>
                <span style='display: inline-block; margin: 5px 10px 5px 0; padding: 5px 10px; background-color: #e8f4f8; border-radius: 5px; font-size: 13px;'>
                    🏞️ {room.get("view_type", "")}
                </span>
            </div>
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='margin: 5px 0; font-size: 13px; color: #7f8c8d;'>
                            {room.get("nights", 1)}泊 (税込)
                        </p>
                        <p style='margin: 5px 0; font-size: 24px; font-weight: bold; color: #e74c3c;'>
                            ¥{room.get("total_price", 0):,}
                        </p>
                        <p style='margin: 5px 0; font-size: 12px; color: #95a5a6;'>
                            1泊あたり ¥{room.get("price_with_tax", 0):,}
                        </p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='margin: 5px 0; font-size: 14px; color: #27ae60; font-weight: bold;'>
                            残り{room.get("available_rooms", 0)}室
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""
            html_parts.append(room_html)

        # Build booking link with available parameters
        booking_params = []
        if checkin:
            booking_params.append(f"checkin={checkin}")
        if checkout:
            booking_params.append(f"checkout={checkout}")
        if adults > 0:
            booking_params.append(f"adults={adults}")
        if rooms > 0:
            booking_params.append(f"rooms={rooms}")
        if children > 0:
            booking_params.append(f"children={children}")

        booking_url = "/booking-user.html"
        if booking_params:
            booking_url += "?" + "&".join(booking_params)

        # Add a footer with booking link
        html_parts.append(
            f"""
<div style='margin-top: 20px; padding: 15px; background-color: #e8f5e9; border-radius: 8px; border-left: 4px solid #4caf50;'>
    <p style='margin: 0 0 10px 0; font-size: 14px; color: #2e7d32;'>
        💡 ご予約をご希望の場合は、下記のリンクからお手続きください。
    </p>
    <a href='{booking_url}' style='display: inline-block; padding: 10px 20px; background-color: #4caf50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;'>
        📝 ご予約はこちら
    </a>
</div>
"""
        )

        return "".join(html_parts)

    except json.JSONDecodeError as e:
        return f"<p style='color: red;'>❌ データ解析エラー: {str(e)}</p>"
    except Exception as e:
        return f"<p style='color: red;'>❌ フォーマットエラー: {str(e)}</p>"


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
    logger.info(f"[TOOL] create_hotel_booking called: customer_name={customer_name}, check_in={check_in}, check_out={check_out}, room_type_id={room_type_id}")
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
