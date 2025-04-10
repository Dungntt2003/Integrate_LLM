import asyncio
import json
from utils import crawl_and_extract

async def main(url):
    
    schema = {
    "name": "string",
    "price": "number",
    "images": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "open_time": {
    "type": "integer"
    },
    "close_time": {
        "type": "integer"
    },
    "location": "string",
    "description": "string",
    "url": "string",
    "extra_information": "string",
    "menu_images": {
        "type": "array",
        "items": {
            "type": "string"
        }
    }
    }

    result = await crawl_and_extract(url, schema, des1="thông tin chi tiết của 1 nhà hàng")
    print(result)
    # parsed_data = json.loads(result.removeprefix("```json").removesuffix("```").strip())
    # with open("ai_price.json", "w", encoding="utf-8") as f:
    #     json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    # print("Save in file successfully")

if __name__ == "__main__":
    asyncio.run(main(url="https://pato.com.vn/products/lion-sky-150-truong-chinh"))