from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Step 1 — Embedding model (MUST match vector_store.py)
# -----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -----------------------------
# Step 2 — Load Vector DB
# -----------------------------
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

print("✅ Vector DB loaded successfully")

# -----------------------------
# Step 3 — Retriever
# -----------------------------
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# -----------------------------
# Step 4 — LLM
# -----------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# -----------------------------
# Step 5 — RAG Function
# -----------------------------
def get_rag_answer(question):

    # 🔍 Retrieve relevant chunks
    docs = retriever.invoke(question)

    # -----------------------------
    # DEBUG (IMPORTANT)
    # -----------------------------

    print(f"📄 Retrieved docs count: {len(docs)}")

    if not docs:
        return "⚠️ No relevant documents found."

    # -----------------------------
    # Build context
    # -----------------------------
    context = "\n\n".join([doc.page_content for doc in docs])

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are a data warehouse assistant.

Answer the question using ONLY the provided context.

Provide a clear explanation with relevant details from the context.
Do not summarize into a single sentence.

Context:
{context}

Question:
{question}
"""

    # -----------------------------
    # LLM Response
    # -----------------------------
    response = llm.invoke(prompt)

    return response.content