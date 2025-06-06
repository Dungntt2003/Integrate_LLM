import asyncio
import json
import os
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler # type: ignore
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig # type: ignore
from openai import OpenAI  # type: ignore

load_dotenv()

async def extract_structured_data(markdown_content, schema):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API_KEY"),  
    )
    
    prompt = f"""
    Dưới đây là nội dung của một trang web về thông tin giá của các mô hình dịch vụ. 
    Bạn cần trích xuất thông tin theo cấu trúc sau:
    {schema}

    Dữ liệu của trang web:
    
    {markdown_content}

    Nhiệm vụ: Hãy trích xuất thông tin chi tiết theo cấu trúc schema đã cho.
    """
    
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://smarttrip.com",  
            "X-Title": "Web Data Extraction Tool",  
        },
        model="google/gemma-3-12b-it:free",
        messages=[
            {"role": "system", "content": "Bạn là một assistant chuyên trích xuất dữ liệu có cấu trúc từ văn bản."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        return response.choices[0].message.content
    except json.JSONDecodeError:
        return {"raw_response": response.choices[0].message.content}

async def crawl_and_extract(url, schema):
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig()
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        
        structured_data = await extract_structured_data(result.markdown, schema)
        
        return structured_data

async def main():
    url = "https://openai.com/api/pricing/" 
    
    schema = {
                "model_name": "string",  
                "input_price": "number", 
                "input_unit": "string", 
                "output_price": "number",
                "output_unit": "string",   
    }

    result = await crawl_and_extract(url, schema)
    parsed_data = json.loads(result.removeprefix("```json").removesuffix("```").strip())
    # with open("ai_price.json", "w", encoding="utf-8") as f:
    #     json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    # print("Save in file successfully")
    print(parsed_data)

if __name__ == "__main__":

    asyncio.run(main())
