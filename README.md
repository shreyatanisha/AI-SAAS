# AI Chatbot Development – Phase-wise Technical Roadmap

**Project:** Company AI Chatbot  
**Development Approach:** Step-by-Step Implementation  
**Backend:** Python + FastAPI  
**LLM:** Groq API  
**Vector Database:** Qdrant Cloud  
**Architecture:** RAG (Retrieval-Augmented Generation)

---

## 1. Project Objective

The objective is to develop an AI-powered chatbot that can understand company-specific information and answer user questions using company website content and uploaded documents.

Development will be divided into two major stages:

**Stage 1 – Single-Company RAG Chatbot**

First, develop a complete and functional RAG chatbot using Python FastAPI, Groq and Qdrant.

**Stage 2 – Multi-Tenant SaaS Platform**

After successfully completing and testing the RAG chatbot, extend the existing architecture to support multiple companies and their individual knowledge bases.

**Important:** Multi-tenancy will not be implemented during the initial RAG development.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| LangChain | RAG pipeline integration |
| Groq API | LLM and answer generation |
| Qdrant Cloud | Vector database |
| Sentence Transformers | Embedding generation |
| PostgreSQL | Application data and chat history (when required) |
| Postman | API testing |
| GitHub | Version control |

**Initial embedding model:** `all-MiniLM-L6-v2` (384 dimensions).

## 3. Stage 1 – Single-Company RAG Chatbot

### Step 1: Project Setup

**Tasks:**
- Create GitHub repository.
- Set up Python virtual environment.
- Install required dependencies.
- Configure FastAPI.
- Create project folder structure.
- Configure environment variables.
- Create a health-check endpoint.

**Expected Outcome:** A working FastAPI backend with a health-check API.

### Step 2: Groq LLM Integration

**Tasks:**
- Create a Groq API account.
- Generate and configure the API key.
- Connect Groq with FastAPI.
- Configure the selected LLM model.
- Create a basic question-answer API.
- Test responses through Postman.

**Expected Outcome:** The API accepts a user question and returns an AI-generated response through Groq.

### Step 3: Website Data Ingestion

**Tasks:**
- Accept company website URLs.
- Crawl website pages.
- Extract website content.
- Remove unnecessary HTML elements.
- Clean and structure extracted text.
- Store source URLs and document metadata.

**Expected Outcome:** The system can extract and prepare company website content for RAG processing.

### Step 4: Document Upload

**Tasks:**
- Implement PDF upload.
- Implement TXT upload.
- Extract text from uploaded documents.
- Store document names and metadata.
- Handle invalid files and extraction errors.

**Expected Outcome:** The system can process website content and uploaded documents.

### Step 5: Text Chunking

**Tasks:**
- Divide extracted content into smaller chunks.
- Configure chunk size and overlap.
- Preserve document IDs.
- Maintain source URLs and metadata.
- Test the quality of generated chunks.

**Expected Outcome:** Large documents are converted into meaningful, searchable text chunks.

### Step 6: Embedding Generation

**Tasks:**
- Integrate Sentence Transformers.
- Configure `all-MiniLM-L6-v2`.
- Generate embeddings for each text chunk.
- Verify vector dimensions.
- Handle embedding generation errors.

**Expected Outcome:** Every text chunk is converted into a 384-dimensional numerical vector.

### Step 7: Qdrant Integration

**Tasks:**
- Create Qdrant Cloud account.
- Create a vector collection.
- Configure the vector dimensions.
- Connect FastAPI with Qdrant.
- Store embeddings and associated metadata.
- Implement similarity search.
- Test vector retrieval.

**Expected Outcome:** Document embeddings are stored and can be retrieved using semantic search.

### Step 8: RAG Pipeline Integration

**Tasks:**
- Accept user questions.
- Generate question embeddings.
- Retrieve relevant chunks from Qdrant.
- Prepare context using retrieved information.
- Send context and user questions to Groq.
- Generate context-based responses.
- Return source URLs.
- Handle questions with no relevant information.

**Expected Outcome:** A functional RAG chatbot that answers questions using actual company information.

### Step 9: Chat API and Conversation History

**Tasks:**
- Create chat API endpoints.
- Generate session IDs.
- Maintain conversation history.
- Implement structured JSON responses.
- Add API error handling.
- Store chat history when required.

**Expected Outcome:** A chatbot backend that supports conversations and maintains session context.

### Step 10: Testing and Optimization

**Tasks:**
- Test using actual company website information.
- Prepare 30–50 test questions.
- Verify retrieval accuracy.
- Check response correctness.
- Test unknown questions.
- Check hallucinations.
- Verify source references.
- Measure response time.
- Fix bugs and optimize prompts.

**Expected Outcome:** A stable and tested single-company RAG chatbot ready for multi-tenant development.

---

## 4. Stage 2 – Multi-Tenant SaaS Development

This stage will begin only after successful completion and approval of Stage 1.

| Phase | Module | Objective |
|---|---|---|
| Phase 2 | Multi-Tenancy | Support multiple companies and isolated knowledge bases |
| Phase 3 | Company Authentication | Company registration, login and access control |
| Phase 4 | Website Widget | Develop an embeddable JavaScript chatbot |
| Phase 5 | SaaS Dashboard | Company dashboard and chatbot management |
| Phase 6 | Lead Management | Capture enquiries and integrate email/WhatsApp |
| Phase 7 | Analytics | Usage tracking, reports and billing limits |

Each company must have access only to its own documents, conversations and chatbot configuration.

## 5. Development and Approval Workflow

The project will follow a controlled development process.

1. Assign one development step to the developer.
2. Developer implements the assigned functionality.
3. Developer pushes the completed code to GitHub.
4. Developer shares API endpoints and testing results.
5. Technical Lead reviews the implementation.
6. Testing and approval are completed.
7. The next development step is assigned.

**No new step should begin until the previous step has been reviewed and approved.**

## 6. Initial Development Milestones

| Milestone | Expected Deliverable |
|---|---|
| Milestone 1 | FastAPI project setup |
| Milestone 2 | Working Groq integration |
| Milestone 3 | Website and document ingestion |
| Milestone 4 | Text chunking and embeddings |
| Milestone 5 | Qdrant storage and retrieval |
| Milestone 6 | Complete RAG pipeline |
| Milestone 7 | Chat API and conversation history |
| Milestone 8 | Testing and final approval |

## 7. Important Development Guidelines

- Follow a modular and reusable project structure.
- Keep API keys and credentials in environment variables.
- Maintain proper error handling.
- Document all API endpoints.
- Use GitHub for version control.
- Test every module before integration.
- Preserve document metadata and source references.
- Keep RAG processing separate from application business logic.
- Design the initial architecture so multi-tenancy can be added later without rewriting the entire RAG engine.

## 8. First Development Assignment

**Immediate Priority: Complete Step 1 and Step 2.**

The developer must demonstrate:

1. A successfully running FastAPI application.
2. A working health-check endpoint.
3. A successful connection with Groq.
4. An API that accepts a question and returns an AI-generated response.
5. Successful Postman testing.

**Final Acceptance Criteria:** The Technical Lead must verify the working APIs and approve the initial setup before proceeding to website ingestion.

---

**Project Development Principle**

Build a reliable single-company RAG chatbot first. Test and optimize it using real company data. Once the core architecture is stable, extend it into a scalable multi-tenant AI chatbot SaaS platform.
