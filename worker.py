import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from job_queue import pop_job

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_job(job: dict):
    file_path = job["file_path"]
    print(f"\n⚙️  Worker processing: {file_path}")

    # 1. LOAD
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()
    print(f"✅ Loaded {len(documents)} page(s)")

    # 2. CHUNK
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")

    # 3. EMBED + STORE
    print("⏳ Embedding and storing...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print(f"✅ Done! {file_path} is now searchable.")

if __name__ == "__main__":
    print("🚀 Worker started. Waiting for jobs...\n")
    while True:
        job = pop_job()
        process_job(job)