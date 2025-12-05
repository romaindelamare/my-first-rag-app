# 📘 **My First RAG App (Local AI Chat + Document Intelligence)**

A fully local **Retrieval-Augmented Generation (RAG)** application featuring:

* ⚡ **FastAPI** backend
* 📄 **Document ingestion & chunking**
* 🔍 **FAISS** vector store
* 🤖 **Ollama** for local LLM inference
* 🧠 **Local embeddings** with `nomic-embed-text`
* 💬 **ChatGPT-style Frontend** with conversation history
* 📚 **Document viewer & chunk inspector**
* 📊 **FAISS index inspector**

Everything runs **offline** — no API keys, no cloud, fully private.

---

# 🧱 Architecture Overview

```
+-----------------------+        +-----------------------+
|       Frontend        |        |        Backend        |
|  React + Vite + TS    | <----> |      FastAPI          |
|                       |        |  RAG pipeline:         |
| - Chat UI             |        |   - Chunking           |
| - Sidebar sessions    |        |   - Embeddings         |
| - Sources drawer      |        |   - FAISS search       |
| - Documents page      |        |   - Reranking          |
| - FAISS inspector     |        |   - Guardrails         |
+-----------+-----------+        |   - LLM (Ollama)       |
            |                    +-----------+------------+
            |                                |
            |                                |
            v                                v
   +-----------------+              +-----------------------+
   | Local Browser   |              |       Ollama          |
   |  Storage        |              |  LLaMA / Phi / Gemma  |
   | (session data)  |              |  nomic-embed-text     |
   +-----------------+              +-----------------------+
```

---

# 🚀 Features

### 💬 **Chat interface**

* ChatGPT-style UI
* Conversation history
* LocalStorage session management
* Source citations drawer
* Clean Tailwind v4 styling

### 📄 **Document Management**

* Upload PDF / TXT / DOCX
* Chunk viewer (Perplexity-style)
* Delete & reindex documents
* Automatic metadata management

### 🔍 **FAISS Index Inspector**

* Vector count
* Embedding dimension
* Disk size
* Index health

### 🧩 **RAG Pipeline**

* Text chunking
* Embedding generation
* Hybrid search (vector + keyword scoring)
* Reranking
* Rewrite & guardrail layers

### 🔐 **Fully Offline**

* No cloud
* No OpenAI key
* No telemetry
* All models run locally

---

# ⚙️ Backend Installation

### 1. Install Python dependencies

```bash
pip install fastapi python-multipart uvicorn faiss-cpu pypdf python-docx ollama
```

### 2. Install Ollama

Download the desktop app:

➡️ [https://ollama.com/download](https://ollama.com/download)

### 3. Pull required models

```bash
ollama pull phi3:mini
ollama pull llama3.2:3b
ollama pull gemma:2b
ollama pull nomic-embed-text
```

### 4. Run the backend

```bash
uvicorn app.main:app --reload --port 8000
```

Your API runs at:

👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

# 🎨 Frontend Installation

### 1. Go to the frontend folder

```bash
cd rag-frontend
```

### 2. Install dependencies

```bash
npm install
npm install tailwindcss @tailwindcss/vite
npm install marked highlight.js shiki
npm install dompurify
npm install @types/dompurify --save-dev
```

### 3. Start development mode

```bash
npm run dev
```

Frontend is available at:

👉 [http://localhost:5173](http://localhost:5173)