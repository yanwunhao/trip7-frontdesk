import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from model import create_frontdesk_chain
from util import load_hotel_introduction
from tools.database_tools import (
    create_hotel_booking,
    search_available_rooms,
    format_rooms_html,
)

load_dotenv()

frontdesk_chain = create_frontdesk_chain(
    model_name=os.getenv("FD_MODEL_NAME"),
    bot_name=os.getenv("BOT_NAME"),
    hotel_name=os.getenv("HOTEL_NAME"),
    system_prompt_filepath="./prompts/frontdesk_chatbot_prompt_v2.md",
    hotel_description=load_hotel_introduction("./documents/hotel_introd.txt"),
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
        "en": "[REPLY IN ENGLISH] ",
    }

    lang_prefix = lang_instructions.get(lang, "[REPLY IN JAPANESE] ")

    if message_list and hasattr(message_list[-1], "content"):
        if message_list[-1].__class__.__name__ == "HumanMessage":
            message_list[-1].content = lang_prefix + message_list[-1].content
        else:
            from langchain_core.messages import HumanMessage

            message_list.append(HumanMessage(content=lang_prefix))

    # DEBUG: Print the full message list sent to LLM
    print("\n" + "=" * 60)
    print("DEBUG: Message list sent to LLM:")
    for i, msg in enumerate(message_list):
        msg_type = msg.__class__.__name__
        content_preview = msg.content[:200] if len(msg.content) > 200 else msg.content
        print(f"  [{i}] {msg_type}: {content_preview}")
    print("=" * 60 + "\n")

    response = frontdesk_chain.invoke({"messages": message_list})

    # Tool mapping
    tools = {
        "create_hotel_booking": create_hotel_booking,
        "search_available_rooms": search_available_rooms,
        "format_rooms_html": format_rooms_html,
    }

    # Handle tool calls if the response contains them
    while hasattr(response, "tool_calls") and response.tool_calls:
        message_list.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            if tool_name in tools:
                tool_result = tools[tool_name].invoke(tool_call["args"])

                # 如果是搜索房间，自动调用格式化并直接返回HTML
                if tool_name == "search_available_rooms":
                    html_result = format_rooms_html.invoke({"rooms_json": tool_result})
                    return html_result

                message_list.append(
                    ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
                )

        # Get next response after tool execution
        response = frontdesk_chain.invoke({"messages": message_list})

    return response
