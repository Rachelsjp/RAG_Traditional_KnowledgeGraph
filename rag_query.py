from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from dotenv import load_dotenv

load_dotenv()


# Embedding model
embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# Vector database
vector_db = Chroma(
    persist_directory="vector_db",
    embedding_function=embedding_model
)


# Retriever
retriever = vector_db.as_retriever(search_kwargs={"k": 3})


# OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)


def get_rag_answer(question):

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a data warehouse assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content