
from pydantic import BaseModel, HttpUrl, Field



class ChatRequest(BaseModel):
    question: str 


class ChatResponse(BaseModel):
    answer: str
 
 
class WebsiteIngestionRequest(BaseModel):
    url: HttpUrl
    max_pages: int = Field(default=10, ge=1, le=100)
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
