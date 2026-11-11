from dotenv import load_dotenv
from groq import Groq

load_dotenv()  #Load environment variables from .env file
client = Groq()
# while True:
    
#     user_question = input("User: ")
    
#     if user_question.lower() == "exit":
#         print("Exiting the chat. Goodbye!")
#         break

def generate_answer(
    user_question: str,
    context: str = "",
    chat_history: list = []
):

    history = []

    for message in chat_history:
        history.append({
            "role": "user",
            "content": message["question"]
        })

        history.append({
            "role": "assistant",
            "content": message["answer"]
        })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a helpful company AI assistant.

                Use the following company information
                to answer the user's questions:

                {context}

                Use previous conversation messages to
                understand follow-up questions.

                If the answer is unavailable in the
                company information, say so.
                """
            },
            *history,
            {
                "role": "user",
                "content": user_question
            }
        ],
    )

    return response.choices[0].message.content
    