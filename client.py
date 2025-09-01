import os
from langchain_core.messages import AIMessage, HumanMessage

from model import create_frontdesk_chain


def load_hotel_introduction(file_path="hotel_introd.txt"):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


frontdesk_chain = create_frontdesk_chain(
    bot_name="李小鹤",
    hotel_name="Trip7箱根仙石原温泉ホテル",
    hotel_description=load_hotel_introduction(),
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


def generate_response(conversation_history):
    message_list = create_message_list(conversation_history)
    response = frontdesk_chain.invoke(message_list)

    return response
