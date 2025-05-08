from openai import OpenAI
import os

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
