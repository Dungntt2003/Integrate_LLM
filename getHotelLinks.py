import asyncio
import requests
from bs4 import BeautifulSoup
from hotel import extract_data_hotel
def extract_domestic_hotel_links(url):
    headers = {
    "User-Agent": "Mozilla/5.0" 
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    footer_links = soup.select("div.block-link")

    for block in footer_links:
        h3 = block.find("h3")
        if h3 and "Khách sạn trong nước" in h3.text:
            links = block.select("a")
            result = [a["href"] for a in links if a.has_attr("href")]
            full_urls = ["https://bestprice.vn" + link for link in result]
            return full_urls 

    return [] 

def extract_hotel_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    hotel_links = soup.select("h3.mktnd_txt_productname")
    result = []

    for h3 in hotel_links:
        a_tag = h3.find("a")
        if a_tag and a_tag.has_attr("href"):
            result.append(a_tag["href"])

    full_urls = ["https://bestprice.vn" + link for link in result]
    return full_urls

async def main():
    url = "https://www.bestprice.vn/khach-san/da-nang"
    links = extract_hotel_links(url)[:2]
    for link in links:
        await extract_data_hotel(link)

if __name__ == "__main__":
    # links = extract_domestic_hotel_links(url="https://www.bestprice.vn/khach-san/")
    # print("Các link khách sạn trong nước:")
    # for link in links:
    #     print(link)
    asyncio.run(main())
    