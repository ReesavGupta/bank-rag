import os
from ingestion import Embeddings, VectorStore, load_and_chunk
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

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
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",  # or another supported model
    temperature=0.2,
    max_tokens=512,
)

# 5. Set up conversation memory with output_key
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# 6. Set up ConversationalRetrievalChain with output_key
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

def main():
    print("Banking RAG Assistant (Groq LLM) with Conversation Memory")
    print("Type your question or 'exit' to quit.")
    chat_history = []
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ("exit", "quit"): break
        result = qa_chain.invoke({"question": query, "chat_history": chat_history})
        print("\nAnswer:", result["answer"])
        print("\n--- Source Documents ---")
        for i, doc in enumerate(result["source_documents"], 1):
            print(f"[{i}] {doc.metadata.get('source', 'N/A')}")
            print(doc.page_content[:500], "...\n")
        chat_history.append((query, result["answer"]))

if __name__ == "__main__":
    main() 