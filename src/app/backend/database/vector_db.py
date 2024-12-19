from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from qdrant_client import QdrantClient

client = QdrantClient(url="http://qdrant:6333")


def get_doc_store(collection_name: str) -> QdrantDocumentStore:
    return QdrantDocumentStore(
        url="http://qdrant:6333",
        index=collection_name,
        embedding_dim=384,
        use_sparse_embeddings=False,
    )
