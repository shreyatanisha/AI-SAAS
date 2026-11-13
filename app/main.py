import logging

from fastapi import FastAPI, HTTPException, UploadFile, File
from app.services.document_ingestion import extract_document_text
import requests
from app.models.chat_models import ChatRequest, ChatResponse, WebsiteIngestionRequest
from app.services.rag_service import generate_rag_answer
from app.services.website_ingestion import crawl_website
from app.vector_db.vector_store import store_document
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-saas-eta-dusky.vercel.app"
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def read_root():
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = generate_rag_answer(request.question, request.session_id)
        return ChatResponse(answer=answer, session_id=request.session_id)
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a chat response. Please try again.",
        ) from error
    
@app.post("/api/ingest-website")
def ingest_website(request: WebsiteIngestionRequest):
    try:
        pages_content = crawl_website(
            str(request.url),
            request.max_pages
        )

        total_chunks = 0

        for page in pages_content:
            total_chunks += store_document(page)

        
        return {
            "message": "Website ingestion completed successfully!",
            "total_pages": len(pages_content),
            "total_chunks_stored": total_chunks,
            "pages": pages_content
        }


    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to fetch website: {str(error)}"
        )
        
@app.post("/api/upload-document")
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

        total_chunks = store_document(document)

        return {
    "message": "Document uploaded and stored successfully!",
    "filename": document["filename"],
    "total_chunks_stored": total_chunks,
    "document": {
        "filename": document["filename"],
        "content": document["content"],
        "source_type": document.get("source_type", "document")
    }
}

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        await file.close()
