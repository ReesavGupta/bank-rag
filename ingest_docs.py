import os
import glob
from ingestion import load_and_chunk, Embeddings, VectorStore

# Directory containing your sample banking documents
DOCS_DIR = "sample_docs"

embedding_model = Embeddings().get_embedding_model()
vector_store = VectorStore()

def ingest_all_documents():
    filepaths = glob.glob(os.path.join(DOCS_DIR, "*"))
    if not filepaths:
        print(f"No documents found in {DOCS_DIR}/. Please add sample banking documents.")
        return
    for filepath in filepaths:
        print(f"Processing: {filepath}")
        docs = load_and_chunk(filepath)
        vector_store.ingest(docs, embedding_model)
        print(f"Ingested: {filepath}")
    print("\nAll documents ingested successfully.")

if __name__ == "__main__":
    ingest_all_documents() 