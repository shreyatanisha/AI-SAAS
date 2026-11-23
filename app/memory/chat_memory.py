# chat_history = {}


# def get_chat_history(session_id: str):
#     return chat_history.get(session_id, [])


# def save_chat_message(session_id: str, question: str, answer: str):

#     if session_id not in chat_history:
#         chat_history[session_id] = []

#     chat_history[session_id].append({
#         "question": question,
#         "answer": answer
#     })


import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(database_url)

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def initialize_chat_table():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id BIGSERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_history_session
                ON chat_history (session_id, id);
            """)


def get_chat_history(session_id: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT question, answer
                FROM chat_history
                WHERE session_id = %s
                ORDER BY id ASC;
            """, (session_id,))

            rows = cursor.fetchall()

    return [
        {"question": row[0], "answer": row[1]}
        for row in rows
    ]


def save_chat_message(session_id: str, question: str, answer: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chat_history (session_id, question, answer)
                VALUES (%s, %s, %s);
            """, (session_id, question, answer))



