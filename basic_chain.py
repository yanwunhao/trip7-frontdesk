# from langchain_ollama import ChatOllama

# model = ChatOllama(model="qwen3")

import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv(override=True)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(model="deepseek-chat", model_provider="deepseek")

from langchain_core.output_parsers import StrOutputParser

basic_qa_chain = model | StrOutputParser()

question = "自己紹介してください。"
result = basic_qa_chain.invoke(question)

print(result)

from langchain.output_parsers.boolean import BooleanOutputParser
from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个数学家。"),
        ("user", "这是用户的问题: {topic}, 请用yes或者no回答"),
    ]
)

bool_qa_chain = prompt_template | model | BooleanOutputParser()

question = "请问1+1是否大于2？"
result = bool_qa_chain.invoke(question)

print(result)

from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

schemas = [
    ResponseSchema(name="name", description="用户的名字"),
    ResponseSchema(name="age", description="用户的年龄"),
]
parser = StructuredOutputParser.from_response_schemas(schemas)

prompt = PromptTemplate.from_template(
    "请根据以下内容提取用户信息，并返回JSON格式: \n{input}\n\n{format_instructions}"
)

chain = (
    prompt.partial(format_instructions=parser.get_format_instructions())
    | model
    | parser
)

result = chain.invoke({"input": "我叫李雷，今年25岁，是一名工程师。"})
print(result)
