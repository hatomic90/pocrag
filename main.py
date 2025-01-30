import fastapi
from fastapi import HTTPException
from model import UserInput
from dotenv import load_dotenv
import chromadb
from PyPDF2 import PdfReader
from logging_info import logging_setup
from chuncking_strategy import invoke_text_spliter
from chromadb_function import create_collection, add_to_collection
from invoke_openai import get_open_ai_response
from prompt.RAG_prompt import traffic_violation_prompt

logger = logging_setup()

load_dotenv()

app = fastapi.FastAPI()

client = chromadb.PersistentClient("./mycollection")
collection = create_collection("leis-transito", client)


def extract_from_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        raise HTTPException(status_code=500, detail="Erro ao extrair texto do PDF")


@app.post("/ai")
def llm_response(user_input: UserInput):
    try:
        global collection
        pdf_content = extract_from_pdf("leis-transito.pdf")
        text_chunks = invoke_text_spliter(
            separators=["\n\n", "\n", ". ", "? ", "! "],
            chunk_size=2000,
            chunk_overlap=250,
            content=pdf_content,
        )
        add_to_collection(text_chunks=text_chunks, collection=collection)
        results = collection.query(
            query_texts=[user_input.text],
            n_results=1,
            include=["documents", "metadatas"],
        )
        result_text = "".join(results["documents"][0])
        response = get_open_ai_response(
            prompt=traffic_violation_prompt.format(
                user_question=user_input.text, search_text=result_text
            ),
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"Erro ao processar solicitação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar solicitação")
