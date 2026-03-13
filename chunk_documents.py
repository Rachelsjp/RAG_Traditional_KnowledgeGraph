from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load documents
data_path = "data/"

loader = DirectoryLoader(
    data_path,
    glob="**/*.docx",
    loader_cls=Docx2txtLoader
)

documents = loader.load()

print("Total documents loaded:", len(documents))


# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))


# Print sample chunks
for chunk in chunks[:3]:
    print("\n--- CHUNK ---")
    print(chunk.page_content[:200])