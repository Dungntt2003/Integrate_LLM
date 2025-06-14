import os
from flask import Flask, request, jsonify # type: ignore
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def get_ai_response(user_input, context_chunks):
    context = "\n".join(context_chunks) if isinstance(context_chunks, list) else str(context_chunks)
    
    prompt = f"""
Bạn là một hướng dẫn viên du lịch thông minh.

Dưới đây là nội dung tham khảo từ cẩm nang du lịch:

{context}

Người dùng đã lên kế hoạch du lịch như sau:

{user_input}

Dựa vào nội dung cẩm nang, hãy mô tả chi tiết hành trình du lịch này và đưa ra những lời khuyên hữu ích, bao gồm cả mẹo di chuyển, gợi ý điểm tham quan/phụ thêm, và lưu ý cho từng khu vực nếu có.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            extra_headers={
                "HTTP-Referer": "https://smarttrip.com",
                "X-Title": "Trip Planner AI Assistant",
            },
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI chuyên đưa ra gợi ý và mô tả hành trình du lịch dựa trên nội dung cẩm nang."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Lỗi khi lấy kết quả từ AI]: {str(e)}"

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running", "message": "Travel API v2"})

@app.route("/api/generate-description", methods=["POST"])
def generate_description():
    try:
        data = request.get_json()
        user_input = data.get("itinerary", "").strip()
        destination = data.get("destination", "").strip()
        
        if not user_input:
            return jsonify({"error": "No itinerary provided"}), 400
                
        if not destination:
            return jsonify({"error": "No destination provided"}), 400
        
        ai_response = get_ai_response(user_input, "")
        return jsonify({"description": ai_response})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)