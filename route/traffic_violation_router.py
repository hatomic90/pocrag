from fastapi import APIRouter, HTTPException, status, Request, Depends
from model.traffic_violation_input_schema import UserInputSchema
from service.traffic_violation_service import TrafficViolationService
from configs.logging_info import logger
from typing import Annotated


traffic_violation = APIRouter()


def get_traffic_law_service(request: Request):
    return request.state.traffic_violation_service


@traffic_violation.post("/ai")
async def llm_response(
    user_input: UserInputSchema,
    service: Annotated[TrafficViolationService, Depends(get_traffic_law_service)],
):
    try:
        return await service.traffic_law_violation(user_input.text)
    except ValueError:
        logger.error("router error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
