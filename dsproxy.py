import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


def load_system_prompt():
    with open("prompts/deepseek_system_prompt.md", "r", encoding="utf-8") as f:
        return f.read()


def create_message_list_with_system_prompt(system_prompt, conversation_history):
    message_list = [SystemMessage(content=system_prompt)]

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


def deepseek_response_proxy(conversation_history):
    system_prompt = load_system_prompt()

    model = init_chat_model(model="deepseek-chat", model_provider="deepseek")
    deepseek_chain = model | StrOutputParser()

    message_list = create_message_list_with_system_prompt(
        system_prompt, conversation_history
    )

    response = deepseek_chain.invoke(message_list)

    return response
