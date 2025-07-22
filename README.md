# Banking RAG Assistant

A Retrieval-Augmented Generation (RAG) system for answering banking questions about loan products, regulatory requirements, and internal policies using LangChain, Groq LLM, and Pinecone vector storage.

---

## Features
- Ingests complex banking documents (PDF, DOCX, etc.)
- Table-aware and cross-reference-preserving chunking
- Semantic search with Nomic embeddings and Pinecone
- Conversational Q&A with Groq LLM (context-aware)
- Modular, cost-optimized, and extensible

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ReesavGupta/bank-rag.git
   cd langsmith-bank-rag
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - `PINECONE_API_KEY` (for Pinecone vector DB)
   - `NOMIC_API_KEY` (for Nomic embeddings)
   - `GROQ_API_KEY` (for Groq LLM)
   - Optionally, use a `.env` file for convenience.

---

## Document Ingestion

1. Place your banking documents (PDF, DOCX, TXT, etc.) in the `sample_docs/` directory.
2. Run the ingestion script:
   ```bash
   python ingest_docs.py
   ```
   This will chunk, embed, and store your documents in Pinecone.

---

## Running the Assistant

Start the conversational RAG assistant:
```bash
python rag_qa.py
```
- Ask banking questions (e.g., "What is the maximum LTV for retail centers?")
- Follow up with context-aware queries (e.g., "What about for first-time buyers?")
- Type `exit` to quit.

---

## Example Queries
- What is the maximum LTV for retail centers?
- What are the reserve requirements for office buildings?
- See Table 3.2: What are the Tier 2 adjustments?
- What was my previous question about?

---

## Architecture Overview

```mermaid
graph TD;
  A[User Query] --> B[ConversationalRetrievalChain]
  B --> C[ConversationBufferMemory]
  B --> D[Retriever (Pinecone VectorStore)]
  D --> E[Nomic Embeddings]
  D --> F[Banking Document Chunks]
  B --> G[Groq LLM]
```
- **Document Loader:** Loads and preprocesses banking documents
- **Chunking:** Table-aware, cross-reference-preserving
- **Embeddings:** Nomic for semantic search
- **Vector Store:** Pinecone for fast retrieval
- **Retriever:** Finds relevant chunks for each query
- **LLM:** Groq for answer generation
- **Memory:** Maintains conversation context

---

## Advanced Features
- Custom chunking for tables and cross-references
- Conversation memory for multi-turn Q&A
- Modular design for cost optimization and future extensions

---

## Next Steps
- Add compliance/consistency validation
- Complete cost analysis documentation
- Optimize for batch processing and embedding caching

---

## License
MIT
