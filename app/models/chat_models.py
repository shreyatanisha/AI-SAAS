
from pydantic import BaseModel, HttpUrl, Field



class ChatRequest(BaseModel):
    question: str 
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    session_id: str
 
 
class WebsiteIngestionRequest(BaseModel):
    url: HttpUrl
    max_pages: int | None = None


class AdminLoginRequest(BaseModel):
    password: str
