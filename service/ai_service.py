from configs.logging_info import logging_setup
from configs.invoke_openai import get_open_ai_response
from prompt.RAG_prompt import traffic_violation_prompt


class IaService:
    def __init__(self, collection):
        self.logger = logging_setup()
        self.collection = collection
        self.logger.info(collection)

    async def ia(self, input_text: str):
        try:
            # meu vscode tá todo desconfigurado, ossada kkkk
            # talvez a criação de chunck também não faça sentido estar aqui
            # pq provavelmente a criação no banco vetorial
            #  vai ficar na hora de subir o app

            # se pá só  a partir do results vai ficar na service, o resto vai ser feito antes

            # Encapsular logica de retriever em uma classe
            results = self.collection.query(
                query_texts=[input_text],
                n_results=1,
                include=["documents", "metadatas"],
            )
            result_text = "".join(results["documents"][0])

            # Encapsular logica de chamada da llm em uma classe
            response = get_open_ai_response(
                prompt=traffic_violation_prompt.format(
                    user_question=input_text, search_text=result_text
                ),
            )
            
            return {"response": response}
        except Exception as e:
            self.logger.error(f"problem: {e}")
            raise e
