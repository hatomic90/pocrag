from langchain.text_splitter import RecursiveCharacterTextSplitter
from logging_info import logging_setup

logger = logging_setup()


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
