import os
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.messages import SystemMessage


def load_system_prompt_template(file_path="system_prompt.md"):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    return PromptTemplate(
        input_variables=["bot_name", "hotel_name", "hotel_description"],
        template=content,
    )


def create_frontdesk_chain(bot_name, hotel_name, hotel_description):
    local_model = ChatOllama(model="qwen3:latest", reasoning=False)

    # 从文件加载系统提示模板并格式化
    system_template = load_system_prompt_template()
    system_content = system_template.format(
        bot_name=bot_name, hotel_name=hotel_name, hotel_description=hotel_description
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_content),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    frontdesk_chain = chat_prompt | local_model | StrOutputParser()

    return frontdesk_chain
