from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Step 1 — Load Documents
data_path = "data/"

loader = DirectoryLoader(
    data_path,
    glob="**/*.docx",
    loader_cls=Docx2txtLoader
)

documents = loader.load()

print("Total documents loaded:", len(documents))


# Step 2 — Split Documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))


# Step 3 — Create Embeddings Model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

print("Embedding model loaded")


# Step 4 — Create Vector Store
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

vector_db.persist()

print("Vector database created successfully!")