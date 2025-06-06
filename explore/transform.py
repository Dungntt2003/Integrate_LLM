import json
import os
import shutil
from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from chromadb.config import Settings # type: ignore

def save_to_chromadb(json_path, collection_name="travel_guide_improved", db_path="./chromaDB"):
    db_path = os.path.abspath(db_path)

    if os.path.exists(db_path):
        print(f"Đang xóa ChromaDB cũ tại: {db_path}")
        shutil.rmtree(db_path)
    
    os.makedirs(db_path, exist_ok=True)
    print(f"Đã tạo ChromaDB mới tại: {db_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("Đang tải model embedding...")
    model = SentenceTransformer("keepitreal/vietnamese-sbert")
    
    texts = []
    ids = []
    metadatas = []
    
    print("Đang chuẩn bị dữ liệu...")
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
    

    print("Đang tạo embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    try:
        try:
            chroma_client.delete_collection(name=collection_name)
            print(f"Đã xóa collection cũ: {collection_name}")
        except:
            pass
        
        collection = chroma_client.create_collection(
            name=collection_name, 
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Đã tạo collection mới: {collection_name}")
        
    except Exception as e:
        print(f"Lỗi khi tạo collection: {e}")
        return

    batch_size = 100
    print(f"Đang lưu {len(texts)} documents vào ChromaDB...")
    
    for i in range(0, len(texts), batch_size):
        end = min(i + batch_size, len(texts))
        try:
            collection.add(
                documents=texts[i:end],
                embeddings=embeddings[i:end],
                metadatas=metadatas[i:end],
                ids=ids[i:end]
            )
            print(f"Đã lưu batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
        except Exception as e:
            print(f"Lỗi khi lưu batch {i//batch_size + 1}: {e}")
            return
    
    print(f"Hoàn thành! Đã lưu {len(texts)} chunks vào ChromaDB")
    print(f"Vị trí database: {db_path}")
    print(f"Collection: {collection_name}")

if __name__ == "__main__":
    json_file = "./merge.json" 
    

    if not os.path.exists(json_file):
        print(f"Không tìm thấy file: {json_file}")
        print("Vui lòng đặt file merge.json trong cùng thư mục với script này")
    else:
        save_to_chromadb(json_file)