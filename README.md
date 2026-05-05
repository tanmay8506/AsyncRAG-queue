AsyncRAG-Queue: Distributed Document Ingestion & Retrieval
AsyncRAG-Queue is a production-ready RAG (Retrieval-Augmented Generation) pipeline designed to handle document processing asynchronously. Instead of making users wait for high-latency embedding tasks, the system uses a Redis-backed job queue to manage document ingestion in the background.

🏗 System Architecture
The project implements a Producer-Consumer pattern:

The Producer (API): A Flask server that handles file uploads and user queries. When a file is uploaded, it pushes a job metadata to Redis.

The Broker (Redis): Acts as the orchestration layer, holding jobs in a queue until a worker is free.

The Consumer (Worker): A background script that watches the Redis queue, loads files (PDF/TXT), chunks them, generates embeddings, and updates the ChromaDB vector store.

The LLM (Groq): Provides high-speed inference using Llama 3.3-70B for final answer generation based on retrieved context.

🚀 Key Features
Asynchronous Ingestion: Upload large PDFs without blocking the API or timing out.

Persistent Vector Storage: Uses ChromaDB to store and persist embeddings for long-term retrieval.

Blocking-Pop Logic: Efficient worker resource management—workers sleep until a job is pushed to the queue.

Flexible Loaders: Supports both .pdf and .txt formats with intelligent recursive character splitting.

Contextual Accuracy: Strict prompting ensures the LLM only answers based on the provided document context.

🛠 Tech Stack
Orchestration: Redis

Backend: Flask

Vector DB: ChromaDB

Embeddings: HuggingFace (all-MiniLM-L6-v2)

LLM: Llama-3.3-70B (via Groq)

RAG Framework: LangChain

🔧 Installation & Setup
Install & Start Redis:

Bash
# Ensure Redis is running on localhost:6379
redis-server
Clone & Install Dependencies:

Bash
git clone https://github.com/tanmay8506/AsyncRAG-Stream.git
cd AsyncRAG-Stream
pip install flask redis groq langchain-huggingface langchain-community chromadb pypdf python-dotenv
Run the System (Two Terminals Required):

Terminal 1 (The Worker): python worker.py

Terminal 2 (The API): python main.py

🎮 API Usage
1. Upload a Document
POST /upload with a file attached. This triggers the background worker.

2. Ask a Question
POST /ask

JSON
{
  "question": "What is RAG?"
}
