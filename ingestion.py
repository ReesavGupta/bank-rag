import os
from langchain_pinecone import PineconeVectorStore
from langchain_nomic import NomicEmbeddings
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")

class Embeddings:
    def __init__(self):
        self.model = NomicEmbeddings(
            model="nomic-embed-text-v1.5",
            nomic_api_key=NOMIC_API_KEY
        )

    def get_embedding_model(self):
        return self.model

class VectorStore:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = "bank-index"
        self.dimension = 768  # Update this if your embedding dimension changes
        self.index = None

    def create_index(self):
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self.index = self.pc.Index(self.index_name)
        return self.index

    def get_db(self, embedding, index):
        return PineconeVectorStore(index=index, embedding=embedding)

    def ingest(self, documents, embedding_model):
        """
        Ingests documents into Pinecone index using the provided embedding_model.
        :param documents: List of LangChain Document objects
        :param embedding_model: Embedding model instance (e.g. from Embeddings().get_embedding_model())
        """
        index = self.create_index()
        vector_store = self.get_db(embedding_model, index)
        vector_store.add_documents(documents)
        return vector_store
