from configs.logging_info import logger
from prompt.RAG_prompt import traffic_violation_prompt, SYSTEM_PROMPT
from langchain_core.output_parsers import StrOutputParser
from configs.openai_client import get_openai_client


class TrafficLawChain:
    def __init__(self, client_openai: get_openai_client):
        self.llm = client_openai
        self.chain = self._create_chain()

    def _create_chain(self):
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
        chain = self.llm | StrOutputParser()
        return lambda prompt: chain.invoke(
            messages + [{"role": "user", "content": prompt}]
        )

    def get_open_ai_response(self, input_text: str, result_text):
        try:
            prompt = traffic_violation_prompt.format(
                user_question=input_text, search_text=result_text
            )
            response = self.chain(prompt)  # Agora self.chain é uma função válida
            return response if response else None

        except Exception as e:
            logger.error(f"Error in get_open_ai_response: {e}")
            return None
