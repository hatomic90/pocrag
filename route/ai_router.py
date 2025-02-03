from fastapi import APIRouter, HTTPException, status, Request, Depends
from model.model import UserInput
from service.ai_service import IaService
from configs.logging_info import logging_setup
from typing import Annotated

logger = logging_setup()
router = APIRouter()


def get_collection(request: Request):
    return request.state.collection


def get_ia_service(collection=Depends(get_collection)):
    return IaService(collection=collection)


@router.post("/ai")
async def llm_response(
    user_input: UserInput, service: Annotated[IaService, Depends(get_ia_service)]
):
    logger.info("bateu na rota")
    try:
        return await service.ia(user_input.text)
    except ValueError:
        logger.error("router error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    # por enquanto vou deixar um bad request mesmo, depois faço uma tratativa mais apurada
    # eu vou mexer aqui ainda, mas como uma base muito base vai ficar assim
    # pelo menos pra eu estruturar a linha de racicionio
