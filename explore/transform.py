import json
from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from chromadb.config import Settings # type: ignore

def save_to_chromadb(json_path, collection_name="travel_guide_improved"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    model = SentenceTransformer("keepitreal/vietnamese-sbert")
    
    texts = []
    ids = []
    metadatas = []
    
    for i, item in enumerate(data):
        content = item["content"]

        if item.get("title"):
            content = f"{item['title']}\n\n{content}"
        
        texts.append(content)
        ids.append(f"doc_{i}")
        
        metadata = {
            "url": item["url"],
            "date": item["date"],
            "locations": ", ".join(item.get("locations", [])),
            "title": item.get("title", ""),
            "chunk_id": item.get("chunk_id", 0)
        }
        metadatas.append(metadata)
    
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    

    chroma_client = chromadb.PersistentClient(path="/media/dell/New Volume/chromaDB")
    collection = chroma_client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

    batch_size = 100
    # collection.delete(where={}) 
    for i in range(0, len(texts), batch_size):
        end = min(i + batch_size, len(texts))
        collection.add(
            documents=texts[i:end],
            embeddings=embeddings[i:end],
            metadatas=metadatas[i:end],
            ids=ids[i:end]
        )
    
    print(f"✅ Đã lưu {len(texts)} chunks vào ChromaDB trong collection '{collection_name}'")

if __name__ == "__main__":
    save_to_chromadb("/home/dell/Crawl/explore/merge.json")
