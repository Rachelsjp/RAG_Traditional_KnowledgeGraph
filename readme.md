🚀 AI Data Pipeline Impact Analyzer

Traditional RAG vs Graphical RAG Comparison

This project demonstrates the difference between Traditional Retrieval-Augmented Generation (RAG) and Graph-based RAG (Knowledge Graph RAG) using a simplified data warehouse pipeline example.
The application allows users to ask questions about systems, tables, and dashboards, and compares how document-based retrieval and graph-based reasoning answer the same question.
A Streamlit interface displays answers side-by-side to highlight the differences.
________________________________________
Project Goal
Data teams often need to answer questions like:
•	Which dashboards use fact_orders?
•	What tables does fact_orders depend on?
•	Which source system feeds dim_customer?
This project demonstrates two AI approaches:
Traditional RAG
Uses documents + embeddings + LLM reasoning
Graphical RAG
Uses a knowledge graph to query structured relationships
________________________________________
## Architecture Overview

```
                  ┌───────────────────────┐
                  │      User Question    │
                  └─────────┬─────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
  ┌─────────▼─────────┐           ┌─────────▼─────────┐
  │ Traditional RAG   │           │ Knowledge Graph RAG │
  └─────────┬─────────┘           └─────────┬─────────┘
            │                               │
   ┌────────▼─────────┐           ┌────────▼─────────┐
   │ Question → Embedding │       │ Graph Query       │
   └────────┬─────────┘           └────────┬─────────┘
            │                               │
   ┌────────▼─────────┐           ┌────────▼─────────┐
   │ Vector Database   │           │ Neo4j Graph DB   │
   └────────┬─────────┘           └────────┬─────────┘
            │                               │
   ┌────────▼─────────┐           ┌────────▼─────────┐
   │ Top-K Documents   │           │ Graph Traversal  │
   └────────┬─────────┘           └────────┬─────────┘
            │                               │
            └──────────┐    ┌───────────────┘
                       ▼    ▼
                ┌───────────────┐
                │ LLM generates │
                │ final answer  │
                └──────┬────────┘
                       │
                ┌──────▼──────┐
                │ User sees   │
                │ answer      │
                └─────────────┘
```
________________________________________
Technologies Used
Component	Technology
UI	Streamlit
RAG Framework	LangChain
Embeddings	HuggingFace Sentence Transformers
Vector Database	ChromaDB
LLM	OpenAI GPT-3.5
Graph Database	Neo4j
Graph Query Language	Cypher
Document Loader	LangChain Community
________________________________________
Project Structure
project_folder
│
├── data/
│   └── pipeline_docs.docx
│
├── document_loader.py
├── chunk_documents.py
├── vector_store.py
├── rag_query.py
│
├── graph_loader.py
├── graph_query.py
│
├── rag_comparison_app.py
│
├── .env
└── README.md
________________________________________
How Traditional RAG Works in This Project
1️⃣ Load pipeline documentation
2️⃣ Split documents into chunks
3️⃣ Convert chunks into vector embeddings
Model used:
all-MiniLM-L6-v2
4️⃣ Store embeddings in ChromaDB
5️⃣ When a user asks a question:
•	Query is embedded
•	Vector DB retrieves top-k similar chunks
•	Context is sent to OpenAI GPT-3.5
•	LLM generates the answer
________________________________________
How Graphical RAG Works in This Project
Instead of documents, we store structured relationships in Neo4j.
Graph nodes include:
•	Systems
•	Tables
•	Dashboards
Relationships include:
System → FEEDS → Table
Table → DEPENDS_ON → Table
Table → USED_IN → Dashboard
When a question is asked:
1️⃣ Identify table mentioned in question
2️⃣ Run Cypher query
Example:
MATCH (t:Table {name:'fact_orders'})-[:USED_IN]->(d:Dashboard)
RETURN d.name
3️⃣ Return exact results from graph traversal
________________________________________
Example Questions
Which dashboards use fact_orders?

What tables does fact_orders depend on?

Which system feeds dim_customer?
________________________________________
Setup Instructions
Install Dependencies
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install chromadb
pip install sentence-transformers
pip install docx2txt
pip install python-dotenv
pip install streamlit
pip install neo4j
________________________________________
Add OpenAI API Key
Create .env file
________________________________________
Create Vector Database
Run:
python vector_store.py
This generates the Chroma vector database.
________________________________________
Load Graph Data
Run:
python graph_loader.py
This loads nodes and relationships into Neo4j.
________________________________________
Start the Application
streamlit run rag_comparison_app.py
Open browser:
http://localhost:8501
________________________________________
Traditional RAG vs Graph RAG
Feature	Traditional RAG	Graph RAG
Data source	Documents	Knowledge Graph
Retrieval	Semantic search	Graph traversal
Uses LLM	Yes	Optional
Accuracy for relationships	Medium	High
Best for	Unstructured knowledge	Data lineage
________________________________________
Visual Comparison
Traditional RAG

User Question
      │
      ▼
Embedding Model
      │
      ▼
Vector Database
      │
      ▼
Retriever
      │
      ▼
LLM
      │
      ▼
Answer


Graph RAG

User Question
      │
      ▼
Cypher Query
      │
      ▼
Neo4j Graph Database
      │
      ▼
Graph Traversal
      │
      ▼
Answer
________________________________________
Key Learning
This project shows that:
•	Traditional RAG is ideal for document understanding
•	Graph RAG is better for structured relationships like data pipelines
•	Combining both approaches can create powerful AI data assistants
________________________________________
Knowledge Graph Visualization (Neo4j)

The Graph RAG implementation stores the data pipeline structure in a Neo4j knowledge graph.

Nodes represent:

- Source Systems
- Data Warehouse Tables
- BI Dashboards

Relationships represent:

- System → FEEDS → Table
- Table → DEPENDS_ON → Table
- Table → USED_IN → Dashboard

Below is the visualization of the graph in Neo4j Browser.

![Neo4j Graph](images/neo4j_graph.png)
________________________________________
Architecture Diagram

![RAG Architecture](images/rag_architecture.png)
________________________________________
Application Demo

Below is the Streamlit application comparing Traditional RAG and Graph RAG.

![App Screenshot](images/app_demo.png)
________________________________________
Future Improvements
•	Automatic question classification
•	LLM-generated Cypher queries
•	LangChain GraphRAG integration
•	Graph visualization inside UI
•	Support for large enterprise data pipelines
________________________________________
Author
Rachel Purnima Johnpeter


