import os
import asyncio
import logging
import time
from typing import Optional
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_model = None
_deepseek_chain = None
_semaphore = asyncio.Semaphore(5)


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


def get_deepseek_chain():
    global _model, _deepseek_chain
    
    if _deepseek_chain is None:
        logger.info("Initializing DeepSeek model and chain...")
        _model = init_chat_model(model="deepseek-chat", model_provider="deepseek")
        _deepseek_chain = _model | StrOutputParser()
        logger.info("DeepSeek model initialized successfully")
    
    return _deepseek_chain


async def deepseek_response_proxy(conversation_history, timeout: int = 30):
    start_time = time.time()
    request_id = f"{int(start_time * 1000) % 100000}"
    
    logger.info(f"[{request_id}] Starting DeepSeek request, waiting for semaphore...")
    
    async with _semaphore:
        wait_time = time.time() - start_time
        logger.info(f"[{request_id}] Acquired semaphore after {wait_time:.2f}s, processing request...")
        
        try:
            system_prompt = load_system_prompt()
            deepseek_chain = get_deepseek_chain()

            message_list = create_message_list_with_system_prompt(
                system_prompt, conversation_history
            )

            response = await asyncio.wait_for(
                asyncio.to_thread(deepseek_chain.invoke, message_list),
                timeout=timeout
            )

            total_time = time.time() - start_time
            logger.info(f"[{request_id}] Request completed successfully in {total_time:.2f}s")
            
            return response
            
        except asyncio.TimeoutError:
            total_time = time.time() - start_time
            error_msg = f"DeepSeek API request timeout after {timeout} seconds (total: {total_time:.2f}s)"
            logger.error(f"[{request_id}] {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            total_time = time.time() - start_time
            error_msg = f"DeepSeek API error after {total_time:.2f}s: {str(e)}"
            logger.error(f"[{request_id}] {error_msg}")
            raise Exception(error_msg)


def deepseek_response_proxy_sync(conversation_history):
    system_prompt = load_system_prompt()
    deepseek_chain = get_deepseek_chain()

    message_list = create_message_list_with_system_prompt(
        system_prompt, conversation_history
    )

    try:
        response = deepseek_chain.invoke(message_list)
        return response
    except Exception as e:
        raise Exception(f"DeepSeek API error: {str(e)}")
