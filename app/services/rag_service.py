from app.vector_db.vector_store import get_vector_store
from app.services.llm_services import generate_answer
from app.memory.chat_memory import get_chat_history, save_chat_message


def retrieve_context(question: str):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        question,
        k=4
    )

    return "\n\n".join(
        document.page_content
        for document in results
    )


def generate_rag_answer(question: str, session_id: str):

    history = get_chat_history(session_id)

    context = retrieve_context(question)

    answer = generate_answer(
        question,
        context,
        history
    )

    save_chat_message(
        session_id,
        question,
        answer
    )

    return answer






