import os
from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from chromadb.config import Settings # type: ignore


def search_with_hybrid(query, collection_name="travel_guide_improved", n_results=5):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CHROMA_DB_PATH = os.path.join(BASE_DIR, "explore", "chromaDB")

    model = SentenceTransformer("keepitreal/vietnamese-sbert")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_collection(name=collection_name)

    results = {
        "documents": [],
        "metadatas": [],
        "distances": []
    }

    queries = [q.strip() for q in query.split(",")] if "," in query else [query.strip()]

    for q in queries:
        query_embedding = model.encode(q).tolist()
        partial_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        results["documents"].extend(partial_results.get("documents", [])[0])
        results["metadatas"].extend(partial_results.get("metadatas", [])[0])
        results["distances"].extend(partial_results.get("distances", [])[0])

    return results
