# aqui vai ficar a lógica da criação da collection, e a parte de apagar todo o processo

import chromadb
import os
from dotenv import load_dotenv

load_dotenv()


def get_chroma_client():
    return chromadb.PersistentClient(os.getenv("TRAFFIC_VIOLATION_COLLECTION"))
