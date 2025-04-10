import asyncio
import requests
from bs4 import BeautifulSoup
def extract_domestic_experience_links(url):
    headers = {
    "User-Agent": "Mozilla/5.0" 
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', class_='items-cam-nang')

    all_urls = []

    for a in links:
        href = a.get('href')
        if href:
            href = href.strip()
            if not href.startswith("http"):
                href = "https://khamphadisan.com.vn" + href
            sub_links = extract_links(href)
            all_urls.extend(sub_links)

    return list(set(all_urls))

def extract_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.find_all('section')
    href_set = set()  

    for section in sections:
        a_tags = section.find_all('a')
        for a in a_tags:
            href = a.get('href')
            if href:
                href = href.strip()
                if any(x in href for x in ["/tour", "/review", "/am-thuc-viet", "/le-hoi-viet-nam","/khach-san", "/diem-den-hap-dan", "/di-san-the-gioi-o-viet-nam"]):
                    continue
                if href.startswith("/"):
                    href = "https://khamphadisan.com.vn" + href
                href_set.add(href)


    return list(href_set)

def extract_content(url):
    headers = {
    "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    post_content = soup.find("article", class_="post-content")

    if post_content:
        text = post_content.get_text(separator="\n", strip=True)  
        print(text)
    else:
        print("Not found content in article.post-content")

# async def main():
#     url = "https://khamphadisan.com.vn/cam-nang/"
#     print(extract_domestic_experience_links(url=url))

# if __name__ == "__main__":
#     asyncio.run(main())