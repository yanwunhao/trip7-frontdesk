import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv(override=True)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

model = init_chat_model(model="deepseek-chat", model_provider="deepseek")

question = "鲁迅和周树人是什么关系？"

result = model.invoke(question)
output = result.content

print(output)

model = init_chat_model(model="deepseek-reasoner", model_provider="deepseek")

question = "鲁迅和周树人是什么关系？"

result = model.invoke(question)
output = result.content
kwargs = result.additional_kwargs

print(output)
print(kwargs)
