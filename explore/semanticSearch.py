from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from chromadb.config import Settings # type: ignore

def search_with_hybrid(query, collection_name="travel_guide_improved", n_results=5):
    model = SentenceTransformer("keepitreal/vietnamese-sbert")
    chroma_client = chromadb.PersistentClient(path="/media/dell/New Volume/chromaDB")
    collection = chroma_client.get_collection(name=collection_name)
    
    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    print(f"Kết quả '{query}':")
    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"\n--- Kết quả #{i+1} (distance: {distance:.2f}) ---")
        print(f"Tiêu đề: {metadata.get('title', 'Không có tiêu đề')}")
        print(f"Đoạn trích: {doc[:200]}...")
    
    return results

if __name__ == "__main__":
    search_with_hybrid("Huế, Đà Nẵng")
