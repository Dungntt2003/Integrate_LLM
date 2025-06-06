import asyncio
import requests
from bs4 import BeautifulSoup

def gen_url_list(base_url): 
    url_list = []
    for i in range(1, 24): 
        url = f"{base_url}/page/{i}/"
        url_list.append(url)
    return url_list

def extract_article_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all('article')
    href_set = set()  

    for section in sections:
        a_tag = section.find('a')
        href = a_tag.get('href')
        href_set.add(href)
    return list(href_set)


def extract_all_article_links(base_url):
    url_list = gen_url_list(base_url)
    all_links = set()

    for url in url_list:
        article_links = extract_article_links(url)
        all_links.update(article_links)
    return list(all_links)
    
async def main():
    urls = extract_all_article_links(base_url="https://checkintravel.vn/blog")
    for url in urls:
        print(url)

if __name__ == "__main__":
    asyncio.run(main())