from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


def create_frontdesk_chain():
    local_model = ChatOllama(model="qwen3:latest", reasoning=False)

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="你叫李鹤，是一位AI助手。"),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    frontdesk_chain = chat_prompt | local_model | StrOutputParser()

    return frontdesk_chain
