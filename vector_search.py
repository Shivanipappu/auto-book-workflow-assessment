

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer, util
import torch

client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection("book_versions")


embedder = SentenceTransformer('all-MiniLM-L6-v2')

def search_relevant_versions(query: str, chapter_number: int, top_k: int = 3):
    """
    Searches and ranks stored chapter versions based on semantic similarity to the query.

    Args:
        query (str): The user's search query.
        chapter_number (int): The chapter to search within.
        top_k (int): Number of top similar results to return.

    Returns:
        List of tuples: (similarity_score, document_text, metadata, version_id)
    """

   
    result = collection.get(
        where={"chapter": chapter_number},
        include=["documents", "metadatas", "ids"]
    )

    documents = result["documents"]
    metadatas = result["metadatas"]
    ids = result["ids"]

    if not documents:
        return []

    
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    doc_embeddings = embedder.encode(documents, convert_to_tensor=True)

    
    similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]

    
    results = list(zip(similarities, documents, metadatas, ids))
    results.sort(key=lambda x: x[0], reverse=True)

    return results[:top_k]
