import os
from ingestion import Embeddings, VectorStore, load_and_chunk
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

# Set your Groq API key as an environment variable or replace here
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 1. Load embedding model and vector store
embedding_model = Embeddings().get_embedding_model()
vector_store = VectorStore()

# 2. (Optional) Ingest documents if needed
# Example: chunked_docs = load_and_chunk("path/to/your/banking_doc.pdf")
# vector_store.ingest(chunked_docs, embedding_model)

# 3. Load Pinecone index and set up retriever
index = vector_store.create_index()
db = vector_store.get_db(embedding_model, index)
retriever = db.as_retriever()

# 4. Set up Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",  # or another supported model
    temperature=0.2,
    max_tokens=512,
)

# 5. Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
)

def main():
    print("Banking RAG Assistant (Groq LLM)")
    print("Type your question or 'exit' to quit.")
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ("exit", "quit"): break
        result = qa_chain(query)
        print("\nAnswer:", result["result"])
        print("\n--- Source Documents ---")
        for i, doc in enumerate(result["source_documents"], 1):
            print(f"[{i}] {doc.metadata.get('source', 'N/A')}")
            print(doc.page_content[:500], "...\n")

if __name__ == "__main__":
    main() 