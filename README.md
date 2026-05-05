AsyncRAG-queue: Distributed Asynchronous RAG Pipeline
AsyncRAG-queue is a scalable Retrieval-Augmented Generation (RAG) system designed to solve the latency issues associated with document ingestion. By decoupling the file upload process from the embedding generation using a Redis-backed Producer-Consumer architecture, the system ensures a non-blocking user experience even when processing large-scale datasets.

🏗 System Architecture
Unlike standard RAG implementations that process documents "in-request," AsyncRAG-queue utilizes a distributed approach:

API Layer (The Producer): A Flask-based REST API that receives document uploads and pushes ingestion metadata to a Redis queue.

Message Broker (Redis): Orchestrates the job flow, ensuring tasks are persisted and distributed efficiently.

Background Worker (The Consumer): A dedicated process that monitors the queue, performs heavy-duty PDF/Text parsing, generates embeddings via HuggingFace, and indexes them into ChromaDB.

Inference Engine (Groq): Powered by Llama-3.3-70B, the system performs semantic retrieval from the vector store to generate context-aware, grounded responses.

🚀 Key Engineering Features
Asynchronous Ingestion: Offloads high-latency tasks (chunking/embedding) to background workers, preventing API timeouts.

Horizontal Scalability: The system is designed to scale; multiple worker instances can be deployed to process the Redis queue in parallel.

Persistent Vector Store: Uses ChromaDB for long-term storage of document embeddings, allowing for lightning-fast similarity searches.

Self-Sleeping Workers: Implements blpop (Blocking Pop) logic, ensuring workers consume zero CPU cycles while waiting for new jobs.

Recursive Character Splitting: Optimizes context retrieval by maintaining semantic coherence across document chunks.

🛠 Tech Stack
Backend: Flask (Python)

Task Queue: Redis

Vector Database: ChromaDB

Embeddings: HuggingFace (all-MiniLM-L6-v2)

LLM Engine: Groq (Llama-3.3-70B-Versatile)

Framework: LangChain

🔧 Installation & Setup
Start the Redis Server:

Bash
# Ensure Redis is running on localhost:6379
redis-server
Clone & Install Dependencies:

Bash
git clone https://github.com/tanmay8506/AsyncRAG-queue.git
cd AsyncRAG-queue
pip install flask redis groq langchain-huggingface langchain-community chromadb pypdf python-dotenv
Configure Environment:
Create a .env file:

Code snippet
GROQ_API_KEY=your_api_key_here
Launch the Pipeline:

Start the Worker: python worker.py

Start the API: python server.py

🎮 Usage
Document Ingestion
POST /upload

Upload a .pdf or .txt file. The server will immediately return a 200 OK with a "queued" status while the worker processes the file in the background.

Semantic Query
POST /ask

JSON
{
  "question": "Explain the relationship between LLMs and RAG based on the document."
}
