from langchain_ollama import ChatOllama

local_model = ChatOllama(model="qwen3")

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

news_gen_prompt = PromptTemplate.from_template(
    "请根据以下新闻标题编写一段简短的新闻内容（200字以内）：\n\n{title}"
)

news_chain = news_gen_prompt | local_model | StrOutputParser()

fakenews_check_prompt = PromptTemplate.from_template(
    "请根据你的知识和常识，检测以下新闻内容的真实与否（用yes或no回答）：\n{content}"
)

from langchain.output_parsers.boolean import BooleanOutputParser

fakenews_check_chain = fakenews_check_prompt | local_model | BooleanOutputParser()

from langchain_core.runnables import RunnableLambda


def debug_print(x):
    print(x)
    return x


debug_node = RunnableLambda(debug_print)

full_chain = news_chain | debug_node | fakenews_check_chain

result = full_chain.invoke({"title": "巴黎预计于2024年举办奥运会"})

print(result)
