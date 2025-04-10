import asyncio
import json
from utils import crawl_and_extract

async def extract_data_hotel(url):
    # url = "https://www.bestprice.vn/khach-san/sapa-charm-1406.html" 
    
    schema = {
    "name": "string",
    "price": "number",
    "rating": "number",
    "facilities": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "images": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "attractions": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "location": "string",
    "description": "string",
    "url": "string",
    "rooms": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "roomName": "string",
                "roomDescription": "string",
                "roomImage": "string",
                "roomPrice": "number"
                }
            }
        }
    }

    result = await crawl_and_extract(url, schema, des1="thông tin chi tiết của 1 khách sạn")
    print(result)
    # parsed_data = json.loads(result.removeprefix("```json").removesuffix("```").strip())
    # with open("ai_price.json", "w", encoding="utf-8") as f:
    #     json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    # print("Save in file successfully")

if __name__ == "__main__":
    asyncio.run(extract_data_hotel(url="https://bestprice.vn/khach-san/chicland-hotel-da-nang-1681.html"))