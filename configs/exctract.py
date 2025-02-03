from PyPDF2 import PdfReader
from configs.logging_info import logging_setup


logger = logging_setup()


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
