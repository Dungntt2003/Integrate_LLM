from openai import OpenAI
import os
from dotenv import load_dotenv

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# dotenv_path = os.path.join(parent_dir, ".env")


# load_dotenv(dotenv_path)
# api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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", 
)

def get_ai_response(user_input, context_chunks):
    context = "\n".join(context_chunks)

    prompt = f"""
Bạn là một hướng dẫn viên du lịch thông minh.

Dưới đây là nội dung tham khảo từ cẩm nang du lịch:

{context}

Người dùng đã lên kế hoạch du lịch như sau:

{user_input}

Dựa vào nội dung cẩm nang, hãy mô tả chi tiết hành trình du lịch này và đưa ra những lời khuyên hữu ích, bao gồm cả mẹo di chuyển, gợi ý điểm tham quan/phụ thêm, và lưu ý cho từng khu vực nếu có.
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-prover-v2:free",
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

    try:
        return response.choices[0].message.content
    except Exception as e:
        return f"[Lỗi khi lấy kết quả từ AI]: {str(e)}"
