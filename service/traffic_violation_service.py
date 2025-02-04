from configs.logging_info import logger
from storage.traffic_violations_storage import TrafficViolationsStorage
from service.openai_service import TrafficLawChain


class TrafficViolationService:
    def __init__(
        self,
        traffic_violation_storage: TrafficViolationsStorage,
        openai_service: TrafficLawChain,
    ):
        self.logger = logger
        self.storage = traffic_violation_storage
        self.openai_service = openai_service

    async def traffic_law_violation(self, input_text: str):
        try:
            result_text = self.storage.get_collection_results(input_text=input_text)
            logger.info(result_text)
            response = self.openai_service.get_open_ai_response(
                input_text=input_text, result_text=result_text
            )
            return {"response": response}
        except Exception as e:
            self.logger.error(f"problem: {e}")
            raise e
