# Architecture Diagram: Banking RAG Assistant

```mermaid
graph TD;
  A[User Query] --> B[ConversationalRetrievalChain]
  B --> C[ConversationBufferMemory]
  B --> D[Retriever (Pinecone VectorStore)]
  D --> E[Nomic Embeddings]
  D --> F[Banking Document Chunks]
  B --> G[Groq LLM]
```

**Component Overview:**
- **ConversationalRetrievalChain:** Orchestrates retrieval and LLM response, maintaining chat context.
- **ConversationBufferMemory:** Stores conversation history for context-aware Q&A.
- **Retriever:** Uses Pinecone vector store to find relevant document chunks.
- **Nomic Embeddings:** Provides semantic search capability for chunk retrieval.
- **Banking Document Chunks:** Preprocessed, table-aware, and cross-reference-preserving document segments.
- **Groq LLM:** Generates answers using retrieved context and conversation history. 