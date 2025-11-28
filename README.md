# 📘 **My first RAG app**

## 🔍 Project Overview

This project is a fully local **Retrieval-Augmented Generation (RAG)** system built with:

* **FastAPI** as the backend
* **FAISS** for vector search
* **Ollama** for local LLMs (LLaMA 3, Mistral, Phi-3, etc.)
* **nomic-embed-text** for embeddings

It allows you to:

* Index your own documents
* Perform semantic search
* Ask grounded questions based on document content
* Run everything **offline**, without API keys or cloud services

Ideal for building private assistants, knowledge base bots, or experimenting with RAG architectures.

## ⚙️ Installation

### Install Python dependencies

```bash
pip install fastapi uvicorn faiss-cpu pypdf ollama
```

### Install Ollama

Download from:
[https://ollama.com/download](https://ollama.com/download)

### Pull required models

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### Start the API

```bash
uvicorn main:app --reload
```

Your server will be available at:

```
http://127.0.0.1:8000
```