
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection("book_versions")

def save_version(text: str, version_type: str, chapter_number: int, version_id: str):
    """
    Saves a text version of a chapter into ChromaDB with metadata.

    Args:
        text (str): The content to save.
        version_type (str): One of ['original', 'ai_rewritten', 'ai_review', 'human_final'].
        chapter_number (int): The chapter index.
        version_id (str): A unique ID for this version (e.g., "chapter1_v1").
    """
    collection.add(
        documents=[text],
        metadatas=[{
            "stage": version_type,
            "chapter": chapter_number
        }],
        ids=[version_id]
    )
    print(f"✅ Stored version '{version_type}' for chapter {chapter_number} with ID {version_id}")

def get_versions_by_chapter(chapter_number: int):
    """
    Retrieves all versions of a given chapter.
    """
    return collection.query(
        query_texts=[" "],
        where={"chapter": chapter_number},
        include=["documents", "metadatas"]
    )
