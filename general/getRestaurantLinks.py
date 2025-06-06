import asyncio
import json
from utils import crawl_and_extract

async def main(url):
    
    schema = {
        "link": "string",
    }

    result = await crawl_and_extract(url, schema, des1="tất cả các đường link về nhà hàng, trong đường link có chứa từ khóa products")
    print(result)
    # parsed_data = json.loads(result.removeprefix("```json").removesuffix("```").strip())
    # with open("ai_price.json", "w", encoding="utf-8") as f:
    #     json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    # print("Save in file successfully")

if __name__ == "__main__":
    asyncio.run(main(url="https://pato.com.vn/"))