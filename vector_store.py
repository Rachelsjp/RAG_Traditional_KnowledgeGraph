import os
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------
# Step 0 — Config
# -----------------------------
data_path = "./data/"
persist_dir = "chroma_db"

# -----------------------------
# Step 1 — Check if DB exists
# -----------------------------
if os.path.exists(persist_dir):
    print(f"⚠️ Chroma DB already exists at '{persist_dir}'")
    print("👉 Delete the folder if you want to recreate embeddings")
else:
    print("🚀 Creating new vector database...")

    # -----------------------------
    # Step 2 — Load Documents
    # -----------------------------
    loader = DirectoryLoader(
        data_path,
        glob="**/*.docx",
        loader_cls=Docx2txtLoader
    )

    documents = loader.load()
    print("Total documents loaded:", len(documents))

    # -----------------------------
    # Step 3 — Split Documents
    # -----------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)
    print("Total chunks created:", len(chunks))

    # -----------------------------
    # Step 4 — Create Embeddings
    # -----------------------------
    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    print("Embedding model loaded")

    # -----------------------------
    # Step 5 — Create Vector Store
    # -----------------------------
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )

    vector_db.persist()

    print("✅ Vector database created successfully!")
    print(f"📁 Chroma DB stored at: {persist_dir}/")