import os
from configs.logging_info import logger
from langchain_openai import ChatOpenAI


def get_openai_client():
    try:
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=5000,
            top_p=1,
        )
    except ValueError as e:
        logger.info("Was ocurred an error with open ai client: %s", e)
        raise e
