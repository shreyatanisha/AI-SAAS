from fastapi import FastAPI, HTTPException


from models.chat_models import ChatRequest, ChatResponse
from services.llm_services import generate_answer

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    
        answer = generate_answer(request.question)
    
        return ChatResponse(answer=answer)
    
