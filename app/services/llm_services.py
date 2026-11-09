from dotenv import load_dotenv
from groq import Groq

load_dotenv()  #Load environment variables from .env file
client = Groq()


# while True:
    
#     user_question = input("User: ")
    
#     if user_question.lower() == "exit":
#         print("Exiting the chat. Goodbye!")
#         break

def generate_answer(user_question: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": user_question,
            }
        ],
    )
    answer = response.choices[0].message.content
    return answer
    