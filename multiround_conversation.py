from langchain_ollama import ChatOllama

local_model = ChatOllama(model="qwen3:latest")

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

chatbot_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你叫李鹤，是一位AI助手。"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

basic_qa_chain = chatbot_prompt | local_model | StrOutputParser()

message_list = [AIMessage(content="Hello!")]

question = "你叫什么名字?"

message_list.append(HumanMessage(content=question))

result = basic_qa_chain.invoke({"messages": message_list})

print(result)

import asyncio

async def stream_response():
    async for chunk in basic_qa_chain.astream({"messages": message_list}):
        print(chunk, end="", flush=True)

asyncio.run(stream_response())
