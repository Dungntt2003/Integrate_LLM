import asyncio
import json
from crawl4ai import AsyncWebCrawler # type: ignore
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig # type: ignore
from openai import OpenAI  # type: ignore

async def extract_structured_data(markdown_content, schema, des1):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  
    )
    
    prompt = f"""
    Dưới đây là nội dung của một trang web về {des1}. 
    Bạn cần trích xuất thông tin theo cấu trúc sau:
    {schema}

    Dữ liệu của trang web:
    
    {markdown_content}

    Nhiệm vụ: Hãy trích xuất thông tin {des1}.
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

async def crawl_and_extract(url, schema, des1):
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig()
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        
        structured_data = await extract_structured_data(result.markdown, schema, des1)
        
        return structured_data