# Deployment Guide — Production RAG System

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│  User Browser │────▶│  Vercel (React)  │────▶│  HF Spaces  │
│  (Any device) │     │  Frontend         │     │  FastAPI     │
└──────────────┘     └──────────────────┘     └──────┬──────┘
                                                     │
                          ┌──────────────────────────┼──────────┐
                          │            │             │          │
                     ┌────┴────┐ ┌────┴────┐  ┌─────┴─────┐
                     │ Qdrant  │ │  Groq   │  │    BGE    │
                     │ Cloud   │ │  LLM    │  │ Embeddings│
                     │ (Vector)│ │ (2 keys)│  │  (ONNX)   │
                     └─────────┘ └─────────┘  └───────────┘
```

## URLs

| Component | URL |
|-----------|-----|
| **Frontend** | `https://frontend-olive-one-a95hrma84g.vercel.app` |
| **Backend API** | `https://haris-83-rag-backend.hf.space` |
| **Health Check** | `https://haris-83-rag-backend.hf.space/api/health` |
| **Docker Image** | `ghcr.io/haris-ahmed83/production-rag-system` |
| **GitHub** | `https://github.com/Haris-Ahmed83/production-rag-system` |

---

## Backend — Hugging Face Spaces

### Auto-Deploy
- Push to `main` branch on GitHub triggers rebuild
- Or upload files via HF API

### Required Secrets

Set these in **HF Space Settings → Repository Secrets**:

| Secret | Value |
|--------|-------|
| `QDRANT_HOST` | `https://cccfed4d-b54a-45f3-8f66-b37829b804fa.us-east-2-0.aws.cloud.qdrant.io` |
| `QDRANT_API_KEY` | *(from Qdrant Cloud dashboard)* |
| `GROQ_API_KEY` | *(primary Groq API key)* |
| `GROQ_FALLBACK_API_KEY` | *(secondary, for rate-limit failover)* |

### Configuration (backend/.env)

```env
# Vector DB
QDRANT_HOST=:memory:              # :memory: for local, cloud URL for prod
QDRANT_PORT=6333
QDRANT_COLLECTION=documents

# Embeddings
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
EMBEDDING_DIMENSION=768

# Chunking
CHUNK_SIZE=350
CHUNK_OVERLAP=50

# Retrieval
RETRIEVAL_TOP_K=30
RERANKER_TOP_K=5
FINAL_TOP_K=6

# LLM
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1024
```

### Dockerfile (HF Space)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
ENV PYTHONPATH=/app
EXPOSE 7860
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## Frontend — Vercel

### Rewrites (vercel.json)

Requests to `/api/*` proxy to the HF Space backend:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://haris-83-rag-backend.hf.space/api/$1" }
  ]
}
```

### Deploy
```bash
cd frontend
npx vercel --prod
```

---

## Qdrant Cloud

### Setup
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Sign up (free tier: 1GB storage)
3. Create a new cluster
4. Copy the **Cluster URL** and **API Key**
5. Set as HF Space secrets

### Connection Modes

| Mode | Condition | Client Init |
|------|-----------|-------------|
| **In-memory** | `QDRANT_HOST=:memory:` | `QdrantClient(location=":memory:")` |
| **Cloud** | `QDRANT_API_KEY` is set | `QdrantClient(url=host, api_key=key)` |
| **Local** | host:port without API key | `QdrantClient(host=host, port=port)` |

---

## GitHub Packages

Docker images are auto-published to GHCR on every push to `main`:

```
ghcr.io/haris-ahmed83/production-rag-system:latest
ghcr.io/haris-ahmed83/production-rag-system:<commit-sha>
```

### Usage
```bash
docker pull ghcr.io/haris-ahmed83/production-rag-system:latest
docker run -p 8000:8000 ghcr.io/haris-ahmed83/production-rag-system
```

---

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+

### Backend
```bash
git clone https://github.com/Haris-Ahmed83/production-rag-system.git
cd production-rag-system/backend
pip install -r requirements.txt
echo "QDRANT_HOST=:memory:" > .env
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend
```bash
cd ../frontend
npm install
npm run dev
```

---

## Stress Testing

```bash
python C:\Users\haris\AppData\Local\Temp\complex_test.py
```

Tests 22 queries across 13 complex documents. Expected accuracy: **95%+**.

---

## Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Hobby | Free |
| HF Spaces | Free (cpu-basic, 2GB RAM) | Free |
| Qdrant Cloud | Free (1GB) | Free |
| Groq API | Free (2 keys, 12k TPM combined) | Free |
| GitHub Actions | Free (2,000 min/mo) | Free |
| GitHub Packages | Free (500 MB) | Free |
| **Total** | | **$0/month** |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 500 on `/api/query/chat` | Check `HnswConfigDiff` / `SearchParams` in qdrant-client v1.18 |
| Empty Qdrant Cloud | Verify `QDRANT_HOST` and `QDRANT_API_KEY` secrets are set |
| Groq 429 rate limit | System auto-fails to fallback key + retries |
| HF Space in-memory reset | Migrate to Qdrant Cloud for persistence |
| Reranker OOM | Runs on free tier; upgrades to `cpu-upgrade` for full performance |
