# Knowledge Assistant – Frontend (React + Vite)

## Run
1. Start the backend: `uvicorn app.main:app --reload` (port 8000)
2. In this folder:
   ```
   npm install
   npm run dev
   ```
3. Open http://localhost:5173

## How it connects
- `vite.config.js` proxies `/api/*` to `http://localhost:8000`, so no CORS is needed in development.
- For production, set `VITE_API_URL` and add CORS to FastAPI:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://your-frontend.com"],
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

## Structure
- `src/api.js` – all fetch calls (health, chat, ingest-website, upload-document)
- `src/App.jsx` – header, status badge, tabs
- `src/components/ChatPanel.jsx` – chat UI
- `src/components/WebsitePanel.jsx` – URL + max pages, crawled page cards
- `src/components/DocumentPanel.jsx` – drag & drop PDF/TXT upload, text preview
