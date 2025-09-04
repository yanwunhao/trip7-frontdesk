from langchain_core.messages import AIMessage, HumanMessage


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


def generate_response(model, conversation_history):
    message_list = create_message_list(conversation_history)
    response = model.invoke(message_list)

    return response
