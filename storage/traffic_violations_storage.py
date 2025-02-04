from configs.logging_info import logger
import uuid
import chromadb
import os
import shutil


class TrafficViolationsStorage:
    def __init__(self, client: chromadb.PersistentClient):
        self.client = client
        self.collection = self._create_collection("leis-transito")
        self.logger = logger

    def _create_collection(self, collection_name: str) -> chromadb.Collection:
        try:
            return self.client.get_or_create_collection(
                name=collection_name, metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            self.logger.error(
                f"Having following issue in create_db_collection file  - {e}"
            )
            return None

    def add_to_collection(self, text_chunks):
        try:
            documents = []
            ids = []

            for idx, text in enumerate(text_chunks):
                random_id = str(uuid.uuid4())
                ids.append(f"chunk_id_{idx}_unique_id_{random_id}")
                documents.append(text.page_content)

            self.collection.add(documents=documents, ids=ids)
            self.logger.info(f"Added {len(documents)} documents to collection.")
        except Exception as e:
            self.logger.error(
                f"Having following issue in add_to_collection method - {e}"
            )
            return None

    def get_collection_results(self, input_text: str):
        try:
            results = self.collection.query(
                query_texts=[input_text],
                n_results=1,
                include=["documents", "metadatas"],
            )

            document_list = results.get("documents", [])

            if document_list and isinstance(document_list[0], list):
                result_text = " ".join(document_list[0])
            else:
                result_text = ""

            return result_text
        except Exception as e:
            self.logger.error(
                f"Having following issue in get_collection_results method - {e}"
            )
            return None

    def delete_collection(self):
        try:
            self.client.delete_collection("leis-transito")
            collection_path = "./mycollection"
            if os.path.exists(collection_path):
                for item in os.listdir(collection_path):
                    shutil.rmtree(
                        os.path.join(collection_path, item), ignore_errors=True
                    )
        except Exception as e:
            self.logger.error(
                f"Having following issue in delete_collection method - {e}"
            )
            return None
