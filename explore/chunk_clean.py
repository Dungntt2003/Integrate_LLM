import json
from datetime import datetime
import re
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("keepitreal/vietnamese-sbert")

def count_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))

def split_content_semantic(text, max_tokens=1000):
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if re.match(r'^#+\s+', para) or (len(para) < 50 and "**" in para):
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
            continue
            
        # Kiểm tra độ dài token
        para_tokens = count_tokens(para)
        current_tokens = count_tokens(current_chunk)
        
        if current_tokens + para_tokens <= max_tokens:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Nếu đoạn quá dài, chia nhỏ hơn nữa
            if para_tokens > max_tokens:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                temp_chunk = ""
                for sentence in sentences:
                    if count_tokens(temp_chunk + sentence) <= max_tokens:
                        temp_chunk += sentence + " "
                    else:
                        chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + " "
                if temp_chunk:
                    current_chunk = temp_chunk
            else:
                current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def is_noise(text):
    if len(text.strip()) < 30:
        return True
        
    noise_patterns = [
        r"nguồn:", r"xem thêm", r"click", r"theo dõi", r"đừng quên",
        r"wpcd_coupon", r"\d+/\d+ - \(\d+ bình chọn\)", r"https?://",
        r"wp-content"
    ]
    
    for pattern in noise_patterns:
        if re.search(pattern, text.lower()):
            return True
            
    return False

def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold text
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Images
    return text

def process_json_improved(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chunks = []
    for item in data:
        url = item["url"]
        date = item.get("date", datetime.now().strftime("%Y-%m-%d"))
        text = item["content"]
        
        if not text:
            continue
            
        title = ""
        title_match = re.search(r'\*\*(.*?)\*\*', text)
        if title_match:
            title = title_match.group(1)
        
        locations = re.findall(r'##\s+\*\*([^*]+)\*\*', text)
        
        split_parts = split_content_semantic(text)
        for i, part in enumerate(split_parts):
            if part.strip():
                clean_part = clean_markdown(part).strip()
                chunks.append({
                    "url": url,
                    "date": date,
                    "content": clean_part,
                    "title": title,
                    "locations": locations,
                    "chunk_id": i
                })
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_json_improved("/home/dell/Crawl/explore/explore.json", "/home/dell/Crawl/explore/explore_chunk.json")
