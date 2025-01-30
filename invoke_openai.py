import os
import logging
from langchain_openai import ChatOpenAI

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_open_ai_response(prompt: str):
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            max_tokens=5000,
            top_p=1,
        )
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente que entende sobre lei de trânsito, se a pergunta não estiver relacionada a lei de transito, educadamente redirecione o usuário para o tema correto.",
            },
            {"role": "user", "content": prompt},
        ]

        response = llm.invoke(messages)
        return response.content

    except Exception as e:
        logger.error(f"Error in get_open_ai_response: {e}")
        return None
