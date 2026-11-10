import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from app.services.embedding_service import get_embeddings
from langchain_core.documents import Document
from app.services.text_chunking import split_text_into_chunks

def get_vector_store():

    load_dotenv()

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="company_knowledge",
        embedding=get_embeddings()
    )

    return vector_store

def store_document(document: dict):

    chunks = split_text_into_chunks(document["content"])

    documents = []

    for index, chunk in enumerate(chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "source": document.get("url") or document.get("filename"),
                    "title": document.get("title") or document.get("filename"),
                    "source_type": document.get("source_type"),
                    "chunk_index": index
                }
            )
        )

    if not documents:
        return 0

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

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






