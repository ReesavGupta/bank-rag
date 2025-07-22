import os
from llama_index.core.node_parser import UnstructuredElementNodeParser 
from llama_index.core.schema import MetadataMode 
from llama_index.core import Document as LlamaDocument
from langchain.schema import Document
from langchain_pinecone import PineconeVectorStore
from langchain_nomic import NomicEmbeddings
from langchain_docling.loader import DoclingLoader
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")

def sanitize_metadata(metadata):
    """
    Recursively ensure all metadata values are strings, numbers, booleans, or lists of strings.
    Dicts are converted to JSON strings. Lists are processed recursively.
    """
    if isinstance(metadata, dict):
        sanitized = {}
        for k, v in metadata.items():
            if isinstance(v, (str, int, float, bool)):
                sanitized[k] = v
            elif isinstance(v, dict):
                sanitized[k] = json.dumps(v)
            elif isinstance(v, list):
                sanitized[k] = [str(item) if not isinstance(item, (str, int, float, bool)) else item for item in v]
            else:
                sanitized[k] = str(v)
        return sanitized
    return metadata

def load_and_chunk(filepath: str):
    loader = DoclingLoader(file_path=filepath)
    docs = loader.load()  # list of raw LangChain Documents
    
    # Convert LangChain Documents to LlamaIndex Documents
    llama_docs = [
        LlamaDocument(text=doc.page_content, metadata=doc.metadata or {})
        for doc in docs
    ]

    node_parser = UnstructuredElementNodeParser()
    # get structured nodes (table-aware, hierarchical)
    nodes = node_parser.get_nodes_from_documents(documents=llama_docs)
    
    # Convert nodes to LangChain Documents suitable for Pinecone ingestion
    chunked_docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    for node in nodes:
        content = node.get_content(metadata_mode=MetadataMode.ALL)
        metadata = sanitize_metadata(node.metadata or {})
        # Split content into <=512 token chunks (approx 2000 chars)
        splits = splitter.split_text(content)
        for split in splits:
            chunked_docs.append(Document(page_content=split, metadata=metadata))
    
    print(f"Loaded and chunked into {len(chunked_docs)} structured documents.")
    return chunked_docs

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
        self.dimension = 768 
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
