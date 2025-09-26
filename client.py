import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from model import (
    create_frontdesk_chain,
    create_booking_confirmation_chain,
    create_json_extraction_chain,
)
from util import load_hotel_introduction
from tools.hotel_api import write_booking_to_database

load_dotenv()

frontdesk_chain = create_frontdesk_chain(
    model_name=os.getenv("FD_MODEL_NAME"),
    bot_name=os.getenv("BOT_NAME"),
    hotel_name=os.getenv("HOTEL_NAME"),
    system_prompt_filepath="./prompts/frontdesk_chatbot_prompt.md",
    hotel_description=load_hotel_introduction("./documents/hotel_introd.txt"),
)

booking_confirmation_model, booking_confirmation_prompt = (
    create_booking_confirmation_chain(
        model_name=os.getenv("VD_MODEL_NAME"),
        system_prompt_filepath="./prompts/user_confirmation_check_prompt.md",
    )
)

json_extraction_model, json_extraction_prompt = create_json_extraction_chain(
    model_name=os.getenv("JSON_EXTRACTION_NAME"),
    system_prompt_filepath="./prompts/booking_json_extraction_prompt.md",
)


def create_message_list(conversation_history):
    message_list = []

    for conversation in conversation_history:
        role = conversation["role"]
        content = conversation["content"]
        if role == "user":
            message_list.append(HumanMessage(content=content))
        elif role == "assistant":
            message_list.append(AIMessage(content=content))
        else:
            pass

    return message_list


def generate_response(conversation_history, lang="jp"):
    message_list = create_message_list(conversation_history)

    lang_instructions = {
        "cn": "[REPLY IN CHINESE] ",
        "jp": "[REPLY IN JAPANESE] ",
        "en": "[REPLY IN ENGLISH] "
    }

    lang_prefix = lang_instructions.get(lang, "[REPLY IN JAPANESE] ")

    if (
        len(conversation_history) >= 2
        and "=== 房间预订信息确认 ===" in conversation_history[-2]["content"]
    ):
        confirmation_result = booking_confirmation_model.invoke(
            [
                {"role": "system", "content": booking_confirmation_prompt},
                {"role": "user", "content": str(message_list)},
            ]
        )
        if confirmation_result.content.strip() == "YES":
            json_result = json_extraction_model.invoke(
                [
                    {"role": "system", "content": json_extraction_prompt},
                    {"role": "user", "content": conversation_history[-2]["content"]},
                ]
            )
            db_result = write_booking_to_database(json_result.content)
            message_list.append(
                SystemMessage(content=f"Booking database result: {db_result}")
            )
        else:
            message_list.append(
                SystemMessage(content="User confirmation failed, not saved to database")
            )

    if message_list and hasattr(message_list[-1], 'content'):
        if message_list[-1].__class__.__name__ == "HumanMessage":
            message_list[-1].content = lang_prefix + message_list[-1].content
        else:
            from langchain_core.messages import HumanMessage
            message_list.append(HumanMessage(content=lang_prefix))

    response = frontdesk_chain.invoke({"messages": message_list})

    return response


