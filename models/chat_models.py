from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str 


class ChatResponse(BaseModel):
    answer: str
 
 
class WebsiteRequest(BaseModel):
    url: str
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
