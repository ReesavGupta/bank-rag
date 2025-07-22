# Task List for Banking RAG Implementation

## Core RAG Pipeline
- [x] Document loading and chunking (DoclingLoader + UnstructuredElementNodeParser)
- [x] Embedding generation (NomicEmbeddings)
- [x] Vector store setup and ingestion (Pinecone)
- [x] Retrieval chain implementation (RetrievalQA, ConversationalRetrievalChain)
- [x] LLM integration and prompt engineering
- [ ] Memory for conversation context
- [ ] Custom chunking for cross-references and table context
- [ ] Consistency and compliance validation in responses

## Documentation & Analysis
- [ ] Main README with usage, architecture, and setup instructions
- [ ] Architecture diagram (LangChain component usage)
- [ ] Documentation of custom chunking strategy for tables/cross-references
- [ ] Cost-Effective RAG Implementation Guide (cost analysis, trade-offs, recommendations)

## Usability & Testing
- [x] Main orchestration script (CLI, API, or UI)
- [x] Test cases and sample queries
- [x] Example banking documents for testing

## Deployment & Optimization
- [ ] Embedding caching and batch processing logic
- [ ] Tiered LLM strategy (optional, for cost optimization) 