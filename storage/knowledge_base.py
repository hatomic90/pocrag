from PyPDF2 import PdfReader
from configs.logging_info import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_from_pdf(file_path):
    logger.info("starting the extract process")
    try:
        with open(file_path, "rb") as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        raise e


def invoke_text_spliter(
    separators: list = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    content: str = None,
):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        text_chunks = text_splitter.create_documents([content])
        return text_chunks
    except Exception as e:
        logger.error(f"Having following issue in invoke_text_splitter method - {e}")
