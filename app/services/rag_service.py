from qdrant_client import models
from app.vector_db.vector_store import get_vector_store
from app.services.llm_services import generate_answer
from app.memory.chat_memory import get_chat_history, save_chat_message

# Minimum similarity score for retrieved chunks.
# We will calibrate this value using actual retrieval tests.

COMPANY_NAME = "Crushaders Tech"

def ensure_text_index():

    from app.vector_db.vector_store import get_qdrant_client, COLLECTION_NAME

    client = get_qdrant_client()

    collection = client.get_collection(COLLECTION_NAME)

    if "page_content" not in collection.payload_schema:

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="page_content",
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=30,
                lowercase=True
            ),
            wait=True
        )

        print("Full-text index created successfully.")

    else:
        print("Full-text index already exists.")


def retrieve_context(question: str):

    from app.vector_db.vector_store import get_qdrant_client, COLLECTION_NAME

    vector_store = get_vector_store()
    client = get_qdrant_client()

    # 1. Semantic search
    semantic_results = vector_store.similarity_search_with_score(
        question,
        k=5
    )

    # 2. Full-text keyword search
    keyword_results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=models.Filter(
            should=[
                models.FieldCondition(
                    key="page_content",
                    match=models.MatchText(text=word)
                )
                for word in question.split()
                if len(word) >= 3
            ]
        ),
        limit=10,
        with_payload=True,
        with_vectors=False
    )

    # 3. Reciprocal Rank Fusion
    rrf_scores = {}
    documents = {}

    for rank, (document, score) in enumerate(semantic_results, 1):

        point_id = document.metadata.get("_id") or document.page_content

        rrf_scores[point_id] = rrf_scores.get(point_id, 0) + 1 / (60 + rank)
        documents[point_id] = document

    for rank, point in enumerate(keyword_results, 1):

        point_id = str(point.id)

        payload = point.payload
        metadata = payload.get("metadata", {})

        from langchain_core.documents import Document

        document = Document(
            page_content=payload.get("page_content", ""),
            metadata=metadata
        )

        rrf_scores[point_id] = rrf_scores.get(point_id, 0) + 1 / (60 + rank)
        documents[point_id] = document

    # 4. Select the best five chunks
    ranked_ids = sorted(
        rrf_scores,
        key=rrf_scores.get,
        reverse=True
    )[:5]

    relevant_chunks = []

    for point_id in ranked_ids:

        document = documents[point_id]

        print("\nRRF score:", rrf_scores[point_id])
        print("Retrieved content:", document.page_content[:500])
        print("Retrieved metadata:", document.metadata)

        source = document.metadata.get("source", "Unknown source")
        title = document.metadata.get("title", "Untitled document")

        relevant_chunks.append(f"""
Source: {title}
Reference: {source}

Content:
{document.page_content}
""")

    return "\n\n".join(relevant_chunks)



def generate_rag_answer(question: str, session_id: str):
    history = get_chat_history(session_id)

    context = retrieve_context(question)

    # Always allow the LLM to generate an answer.
    # It can use company context when available and general
    # knowledge when appropriate.
    answer = generate_answer(
        question,
        context,
        history
    )

    save_chat_message(session_id, question, answer)

    return answer




