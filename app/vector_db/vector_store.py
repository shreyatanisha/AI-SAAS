# import os
# from dotenv import load_dotenv
# from qdrant_client import QdrantClient
# from langchain_qdrant import QdrantVectorStore
# from app.services.embedding_service import get_embeddings
# from langchain_core.documents import Document
# from app.services.text_chunking import split_text_into_chunks

# def get_vector_store():

#     client = QdrantClient(
#         url=os.getenv("QDRANT_URL"),
#         api_key=os.getenv("QDRANT_API_KEY")
#     )
    
#     vector_store = QdrantVectorStore(
#         client=client,
#         collection_name="company_knowledge",
#         embedding=get_embeddings()
#     )

#     return vector_store

# def store_document(document: dict):

#     chunks = split_text_into_chunks(document["content"])

#     documents = []

#     for index, chunk in enumerate(chunks):
#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "source": document.get("url") or document.get("filename"),
#                     "title": document.get("title") or document.get("filename"),
#                     "source_type": document.get("source_type"),
#                     "chunk_index": index
#                 }
#             )
#         )

#     if not documents:
#         return 0

#     vector_store = get_vector_store()

#     vector_store.add_documents(documents)

#     return len(documents)

# if __name__ == "__main__":

#     sample_document = {
#         "filename": "company_info.txt",
#         "title": "Company Information",
#         "content": (
#             "Our company develops websites and AI chatbots. " * 100
#         ),
#         "source_type": "txt"
#     }

#     total = store_document(sample_document)

#     print("Successfully stored chunks:", total)
    
import os

import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from app.services.embedding_service import get_embeddings
from langchain_core.documents import Document
from app.services.text_chunking import split_text_into_chunks

load_dotenv()

COLLECTION_NAME = "company_knowledge"


def get_qdrant_client():

    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )


def get_vector_store():

    client = get_qdrant_client()

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings()
    )

    return vector_store


def generate_chunk_id(source: str, chunk_index: int):
    unique_value = f"{source}:{chunk_index}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, unique_value))


def store_document(document: dict):

    content = document.get("content", "").strip()

    if not content:
        return 0

    source = (
        document.get("url")
        or document.get("filename")
    )

    if not source:
        raise ValueError("Document source is missing.")

    chunks = split_text_into_chunks(content)

    if not chunks:
        return 0

    client = get_qdrant_client()

    vector_store = get_vector_store()

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.source",
        field_schema=models.PayloadSchemaType.KEYWORD,
        wait=True
    )

    # Delete previously stored chunks belonging to this source.
    client.delete(
    collection_name=COLLECTION_NAME,
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.source",
                    match=models.MatchValue(value=source)
                )
            ]
        )
    ),
    wait=True
)

    documents = []
    ids = []

    for index, chunk in enumerate(chunks):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": source,
                    "title": document.get("title") or document.get("filename"),
                    "source_type": document.get("source_type"),
                    "chunk_index": index
                }
            )
        )

        ids.append(
            generate_chunk_id(source, index)
        )

    vector_store.add_documents(
        documents,
        ids=ids
    )

    return len(documents)


if __name__ == "__main__":

    sample_document = {
        "filename": "company_info.txt",
        "title": "Company Information",
        "content": (
            "Our company develops websites and AI chatbots. " * 100
        ),
        "source_type": "txt"
    }

    total = store_document(sample_document)

    print("Successfully stored chunks:", total)

    
    
    