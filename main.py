import fastapi
from configs.logging_info import logger
from storage.knowledge_base import extract_from_pdf, invoke_text_spliter
from route.traffic_violation_router import traffic_violation
from contextlib import asynccontextmanager
from storage.traffic_violations_storage import TrafficViolationsStorage
from configs.chromadb_conn import get_chroma_client
from service.traffic_violation_service import TrafficViolationService
from service.openai_service import TrafficLawChain
from configs.openai_client import get_openai_client
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    logger.info("Starting application")

    db_client = get_chroma_client()
    openai_client = get_openai_client()

    traffic_violation_storage = TrafficViolationsStorage(client=db_client)
    open_ai_service = TrafficLawChain(client_openai=openai_client)
    traffic_violation_service = TrafficViolationService(
        traffic_violation_storage=traffic_violation_storage,
        openai_service=open_ai_service,
    )

    def load_knowlegde_base(storage):
        pdf_content = extract_from_pdf(os.getenv("TRAFFIC_LAW_PDF"))
        text_chunks = invoke_text_spliter(
            separators=["\n\n", "\n", ". ", "? ", "! "],
            chunk_size=2000,
            chunk_overlap=250,
            content=pdf_content,
        )
        storage.add_to_collection(text_chunks=text_chunks)

    load_knowlegde_base(traffic_violation_storage)

    yield {"traffic_violation_service": traffic_violation_service}

    traffic_violation_storage.delete_collection()

    logger.info("shutting down application, collection deleted")


app = fastapi.FastAPI(lifespan=lifespan, title="Infrações de trânsito")

app.include_router(traffic_violation)
