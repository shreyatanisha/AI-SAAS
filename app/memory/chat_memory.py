chat_history = {}


def get_chat_history(session_id: str):
    return chat_history.get(session_id, [])


def save_chat_message(session_id: str, question: str, answer: str):

    if session_id not in chat_history:
        chat_history[session_id] = []

    chat_history[session_id].append({
        "question": question,
        "answer": answer
    })



