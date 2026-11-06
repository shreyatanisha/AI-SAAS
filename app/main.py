from fastapi import FastAPI, HTTPException, UploadFile, File
from app.services.document_ingestion import extract_document_text
import requests
from app.models.chat_models import ChatRequest, ChatResponse, WebsiteIngestionRequest
from app.services.llm_services import generate_answer
from app.services.website_ingestion import crawl_website

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    
        answer = generate_answer(request.question)
    
        return ChatResponse(answer=answer)
    
@app.post("/ingest-website")
def ingest_website(request: WebsiteIngestionRequest):

    try:

        pages_content = crawl_website(
            str(request.url),
            request.max_pages
        )

        return {
            "message": "Website ingestion completed successfully!",
            "total_pages": len(pages_content),
            "pages": pages_content
        }

    except requests.RequestException as error:

        raise HTTPException(
            status_code=502,
            detail=f"Unable to fetch website: {str(error)}"
        )
        
@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    try:
        file_content = await file.read()

        document = extract_document_text(
            file.filename or "",
            file_content
        )

        if not document["content"].strip():
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in the uploaded file."
            )

        return {
            "message": "Document uploaded and text extracted successfully!",
            "document": document
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        await file.close()
    
