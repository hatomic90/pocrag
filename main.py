import fastapi
import chromadb
import asyncio
import os
import shutil
from configs.logging_info import logging_setup
from configs.chromadb_function import create_collection, add_to_collection
from configs.chuncking_strategy import invoke_text_spliter
from configs.exctract import extract_from_pdf
from route.ai_router import router
from contextlib import asynccontextmanager

logger = logging_setup()


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    logger.info("Starting application")
    client = chromadb.PersistentClient("./mycollection")
    collection = create_collection("leis-transito", client)
    pdf_content = extract_from_pdf("leis-transito.pdf")
    text_chunks = invoke_text_spliter(
        separators=["\n\n", "\n", ". ", "? ", "! "],
        chunk_size=2000,
        chunk_overlap=250,
        content=pdf_content,
    )
    add_to_collection(text_chunks=text_chunks, collection=collection)

    yield {"client": client, "collection": collection}

    await asyncio.sleep(1)
    client.delete_collection("leis-transito")

    collection_path = "./mycollection"
    if os.path.exists(collection_path):
        for item in os.listdir(collection_path):
            shutil.rmtree(os.path.join(collection_path, item), ignore_errors=True)

    logger.info("shutting down application, collection deleted")


app = fastapi.FastAPI(lifespan=lifespan, title="Infrações de trânsito")

app.include_router(router)
