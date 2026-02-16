# Servicenow Documentation Assistant 🛠️

A Retrieval‑Augmented Generation (RAG) assistant for ServiceNow developer documentation. This project crawls ServiceNow docs, indexes them into a vector store, and exposes a conversational UI (Streamlit) and a lightweight REST API (FastAPI) backed by a LangChain agent + OpenAI models.

---

## Highlights ✅

- Ingests and chunks ServiceNow docs using TavilyCrawl and LangChain text splitters
- Embeds content with OpenAI embeddings and stores vectors in Pinecone (primary) and Chroma (local dev)
- RAG agent built with LangChain that retrieves context before answering
- Web UI: `streamlit run main.py`
- API: `uvicorn api:app --reload` (POST `/ask`)

---

## Quickstart — run locally (recommended)

Prerequisites

- Python 3.11+
- OpenAI account + API key
- Pinecone account + API key (optional but recommended for production)

1) Create & activate virtual env

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2) Install dependencies (example)

Create a `requirements.txt` with the packages your environment needs. Example packages used in this project:

```text
streamlit
fastapi
uvicorn[standard]
python-dotenv
certifi
langchain
openai
pinecone-client
chromadb
```

Then:

```bash
pip install -r requirements.txt
```

3) Add environment variables

Create a `.env` file in the project root with at least:

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=us-west1-gcp
# Optional
PINECONE_INDEX=servicenow-chat-agent
```

4) Ingest docs (build vector index)

```bash
python ingestion.py
```

This crawls the ServiceNow developer site, splits pages into chunks, computes embeddings and indexes them into the vector store.

5) Run the Streamlit UI

```bash
streamlit run main.py
```

6) (Optional) Run the API

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Example request:

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query":"How do I create a business rule in ServiceNow?"}'
```

Response:

```json
{ "answer": "...generated answer..." }
```

---

## How it works (overview) 🔍

1. ingestion.py
   - Crawls ServiceNow docs via `TavilyCrawl`
   - Splits pages using `RecursiveCharacterTextSplitter`
   - Embeds and indexes chunks into the vector store (Pinecone; Chroma is available locally)

2. core.py
   - Defines a LangChain agent with a `retrieve_context` tool
   - Agent retrieves top relevant documents, then generates an answer with citations

3. main.py (Streamlit)
   - Conversational UI that sends queries (and optional chat history) to `run_llm`

4. api.py (FastAPI)
   - Minimal REST wrapper exposing `/ask` endpoint for programmatic use

---

## Files & responsibilities 📂

- `ingestion.py` — crawler, splitter, embeddings, indexing
- `core.py` — RAG agent + retrieval tool + inference
- `main.py` — Streamlit UI (chat + memory)
- `api.py` — FastAPI wrapper for programmatic access
- `logger.py` — colored logging helpers
- `consts.py` — shared constants (index name)

---

## Configuration & env vars ⚙️

- OPENAI_API_KEY — required for embeddings & model
- PINECONE_API_KEY — required when using PineconeVectorStore
- PINECONE_ENV — Pinecone environment/region

Security: do NOT commit `.env` or any secrets.

---

## Development notes & tips 💡

- Local dev: if you don't want to use Pinecone, you can adapt the vectorstore to use Chroma only (see `ingestion.py`).
- Increase `chunk_size`/`chunk_overlap` in `ingestion.py` to tune retrieval granularity.
- The project uses `gpt-4o-mini` (model configured in `core.py`) — swap for another provider/model in `init_chat_model` if needed.

---

## Common commands

- Ingest docs: `python ingestion.py`
- Run UI: `streamlit run main.py`
- Run API: `uvicorn api:app --reload`
- Clear local Chroma DB: remove `chroma_db/` directory

---

## Troubleshooting ⚠️

- "No API key" errors: confirm `.env` contains `OPENAI_API_KEY` and you restarted the process
- Pinecone auth failures: verify `PINECONE_API_KEY` and `PINECONE_ENV`
- SSL / cert errors on Windows: the project sets `certifi` in `ingestion.py`; ensure `certifi` is installed


---

# Servicenow Documentation Assistant 🛠️

A Retrieval‑Augmented Generation (RAG) assistant for ServiceNow developer documentation. This project crawls ServiceNow docs, indexes them into a vector store, and exposes a conversational UI (Streamlit) and a lightweight REST API (FastAPI) backed by a LangChain agent + OpenAI models.

---

## Highlights ✅

- Ingests and chunks ServiceNow docs using TavilyCrawl and LangChain text splitters
- Embeds content with OpenAI embeddings and stores vectors in Pinecone (primary) and Chroma (local dev)
- RAG agent built with LangChain that retrieves context before answering
- Web UI: `streamlit run main.py`
- API: `uvicorn api:app --reload` (POST `/ask`)

---

## Quickstart — run locally (recommended)

Prerequisites

- Python 3.11+
- OpenAI account + API key
- Pinecone account + API key (optional but recommended for production)

1) Create & activate virtual env

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2) Install dependencies (example)

Create a `requirements.txt` with the packages your environment needs. Example packages used in this project:

```text
streamlit
fastapi
uvicorn[standard]
python-dotenv
certifi
langchain
openai
pinecone-client
chromadb
```

Then:

```bash
pip install -r requirements.txt
```

3) Add environment variables

Create a `.env` file in the project root with at least:

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENV=us-west1-gcp
# Optional
PINECONE_INDEX=servicenow-chat-agent
```

4) Ingest docs (build vector index)

```bash
python ingestion.py
```

This crawls the ServiceNow developer site, splits pages into chunks, computes embeddings and indexes them into the vector store.

5) Run the Streamlit UI

```bash
streamlit run main.py
```

6) (Optional) Run the API

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Example request:

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query":"How do I create a business rule in ServiceNow?"}'
```

Response:

```json
{ "answer": "...generated answer..." }
```

---

## How it works (overview) 🔍

1. ingestion.py
   - Crawls ServiceNow docs via `TavilyCrawl`
   - Splits pages using `RecursiveCharacterTextSplitter`
   - Embeds and indexes chunks into the vector store (Pinecone; Chroma is available locally)

2. core.py
   - Defines a LangChain agent with a `retrieve_context` tool
   - Agent retrieves top relevant documents, then generates an answer with citations

3. main.py (Streamlit)
   - Conversational UI that sends queries (and optional chat history) to `run_llm`

4. api.py (FastAPI)
   - Minimal REST wrapper exposing `/ask` endpoint for programmatic use

---

## Files & responsibilities 📂

- `ingestion.py` — crawler, splitter, embeddings, indexing
- `core.py` — RAG agent + retrieval tool + inference
- `main.py` — Streamlit UI (chat + memory)
- `api.py` — FastAPI wrapper for programmatic access
- `logger.py` — colored logging helpers
- `consts.py` — shared constants (index name)

---

## Configuration & env vars ⚙️

- OPENAI_API_KEY — required for embeddings & model
- PINECONE_API_KEY — required when using PineconeVectorStore
- PINECONE_ENV — Pinecone environment/region

Security: do NOT commit `.env` or any secrets.

---

## Development notes & tips 💡

- Local dev: if you don't want to use Pinecone, you can adapt the vectorstore to use Chroma only (see `ingestion.py`).
- Increase `chunk_size`/`chunk_overlap` in `ingestion.py` to tune retrieval granularity.
- The project uses `gpt-4o-mini` (model configured in `core.py`) — swap for another provider/model in `init_chat_model` if needed.

---

## Common commands

- Ingest docs: `python ingestion.py`
- Run UI: `streamlit run main.py`
- Run API: `uvicorn api:app --reload`
- Clear local Chroma DB: remove `chroma_db/` directory

---

## Troubleshooting ⚠️

- "No API key" errors: confirm `.env` contains `OPENAI_API_KEY` and you restarted the process
- Pinecone auth failures: verify `PINECONE_API_KEY` and `PINECONE_ENV`
- SSL / cert errors on Windows: the project sets `certifi` in `ingestion.py`; ensure `certifi` is installed


---

