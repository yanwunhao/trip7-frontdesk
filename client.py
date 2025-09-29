import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from model import create_frontdesk_chain
from util import load_hotel_introduction
from tools.database_tools import create_hotel_booking

load_dotenv()

frontdesk_chain = create_frontdesk_chain(
    model_name=os.getenv("FD_MODEL_NAME"),
    bot_name=os.getenv("BOT_NAME"),
    hotel_name=os.getenv("HOTEL_NAME"),
    system_prompt_filepath="./prompts/frontdesk_chatbot_prompt.md",
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
        "en": "[REPLY IN ENGLISH] "
    }

    lang_prefix = lang_instructions.get(lang, "[REPLY IN JAPANESE] ")

    if message_list and hasattr(message_list[-1], 'content'):
        if message_list[-1].__class__.__name__ == "HumanMessage":
            message_list[-1].content = lang_prefix + message_list[-1].content
        else:
            from langchain_core.messages import HumanMessage
            message_list.append(HumanMessage(content=lang_prefix))

    response = frontdesk_chain.invoke({"messages": message_list})

    # Handle tool calls if the response contains them
    if hasattr(response, 'tool_calls') and response.tool_calls:
        # Execute tool calls
        message_list.append(response)

        for tool_call in response.tool_calls:
            if tool_call['name'] == 'create_hotel_booking':
                tool_result = create_hotel_booking.invoke(tool_call['args'])
                message_list.append(ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call['id']
                ))

        # Get final response after tool execution
        final_response = frontdesk_chain.invoke({"messages": message_list})
        return final_response

    return response


