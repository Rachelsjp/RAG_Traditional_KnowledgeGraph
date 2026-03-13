
#pip install langchain
#pip install langchain-community
#pip install chromadb
#pip install docx2txt
#pip install python-dotenv

import os
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader

data_path = "data/"

loader = DirectoryLoader(
    data_path,
    glob="**/*.docx",
    loader_cls=Docx2txtLoader
)

documents = loader.load()

print("Total documents loaded:", len(documents))

for doc in documents[:3]:
    print(doc.page_content[:200])