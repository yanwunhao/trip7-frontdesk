import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.messages import SystemMessage
from tools.database_tools import (
    create_hotel_booking,
    search_available_rooms,
    format_rooms_html,
)


def load_system_prompt_template(file_path):
    current_dir = os.path.dirname(__file__)
    full_path = os.path.join(current_dir, file_path)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    return PromptTemplate(
        input_variables=["bot_name", "hotel_name", "hotel_description"],
        template=content,
    )


def create_frontdesk_chain(
    model_name, system_prompt_filepath, bot_name, hotel_name, hotel_description
):
    local_model = ChatOllama(model=model_name, reasoning=False)

    # Bind all tools to the model for functional calling
    local_model_with_tools = local_model.bind_tools([
        search_available_rooms,
        format_rooms_html,
        create_hotel_booking,
    ])

    system_template = load_system_prompt_template(system_prompt_filepath)
    system_content = system_template.format(
        bot_name=bot_name, hotel_name=hotel_name, hotel_description=hotel_description
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_content),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    frontdesk_chain = chat_prompt | local_model_with_tools

    return frontdesk_chain
