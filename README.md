# Agentic ESG Compliance Copilot

NLP-driven RAG + agentic orchestration for clause-level ESG compliance across frameworks (BRSR, GRI, SASB, TCFD).

## Repo layout
- backend/ — FastAPI app, FAISS vector store, embeddings, ingestion and search APIs
- frontend/ — Next.js (app router) UI scaffold
- .env.example — backend config template
- .gitignore — excludes venv, node_modules, build artifacts, data/indexes

## Prerequisites
- Python 3.11 (recommended for spaCy wheels)
- Node.js 18+ and Yarn 1.x
- Git

## Clone
```powershell
git clone https://github.com/Kabeeraa27/AgenticESG.git
cd AgenticESG
```

## Backend setup (FastAPI)
```powershell
# from repo root
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt

# configure env (copy template and adjust)
Copy-Item backend\.env.example backend\.env
# optional: use SQLite for local dev
$env:DATABASE_URL="sqlite:///./data/app.db"

# create tables
python -m app.db.init_db

# run API
uvicorn app.main:app --reload --app-dir backend
```

### Backend endpoints (current)
- `GET /api/health` — health check
- `POST /api/ingest` — chunk + embed + store
	- body: `{ "title": "Doc", "source_type": "company_doc"|"framework", "framework": "TCFD", "text": "..." }`
- `POST /api/search` — semantic search over chunks
	- body: `{ "query": "climate risk", "k": 5 }`

### Quick smoke (PowerShell)
```powershell
$ingest = @{title="Test"; source_type="company_doc"; framework="TCFD"; text="Line one. More text for chunking."}
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/ingest -ContentType "application/json" -Body ($ingest | ConvertTo-Json)

$search = @{query="climate"; k=5}
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/search -ContentType "application/json" -Body ($search | ConvertTo-Json)
```

## Frontend setup (Next.js)
```powershell
cd frontend
yarn install

# API base for frontend -> backend
"NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000" | Out-File -Encoding utf8 -FilePath .env.local

yarn dev
# open http://localhost:3000
```

## Notes
- Default embeddings: sentence-transformers/all-MiniLM-L6-v2; FAISS index at `./data/vector_store/faiss.index` (configurable).
- To switch to Postgres, set `DATABASE_URL=postgresql+psycopg://user:pass@host:port/db` and rerun `python -m app.db.init_db`.
- Keep `.venv/`, `node_modules/`, `.next/`, and data/index files out of git (handled by .gitignore).

## Next build steps
- Add filters/rerank and hybrid matching to search
- Introduce agentic orchestration (LangGraph/AutoGen) for reasoning and critique
- Implement audit trail and human review UI
