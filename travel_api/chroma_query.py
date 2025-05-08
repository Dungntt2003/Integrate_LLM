from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from chromadb.config import Settings # type: ignore

def search_with_hybrid(query, collection_name="travel_guide_improved", n_results=1):
    model = SentenceTransformer("keepitreal/vietnamese-sbert")
    chroma_client = chromadb.PersistentClient(path="/media/dell/New Volume/chromaDB")
    collection = chroma_client.get_collection(name=collection_name)
    
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results