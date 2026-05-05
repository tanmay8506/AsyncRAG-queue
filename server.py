import os
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from job_queue import push_job

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ── Upload a document → pushes to queue ─────────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    os.makedirs("./docs", exist_ok=True)
    file_path = f"./docs/{file.filename}"
    file.save(file_path)

    # Push job to queue — worker will handle ingestion
    push_job({"file_path": file_path})

    return jsonify({
        "message": f"✅ File '{file.filename}' uploaded and queued for processing.",
        "status": "queued"
    })

# ── Ask a question → searches vector DB ─────────────────────────────────────
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
    except Exception:
        return jsonify({"error": "No documents ingested yet. Upload a file first."}), 400

    # Retrieve relevant chunks
    results = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know based on the provided document."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer, "chunks_used": len(results)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)