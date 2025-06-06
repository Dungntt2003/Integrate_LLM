import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from experience import extract_domestic_experience_links
from checkinVn import extract_all_article_links
from datetime import datetime
import json

def clean_string(s):
    return s.replace('\n', '').replace('*', '').replace('\\"', '')

async def quick_parallel_example(funcExtract, base_url, className, file):
    urls = funcExtract(base_url)

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True,  
        target_elements=[className]
    )

    async with AsyncWebCrawler() as crawler:
        results_data = []
        run_conf = run_conf.clone(stream=False)
        results = await crawler.arun_many(urls, config=run_conf)
        for res in results:
            results_data.append({
            "url": res.url,
            "content": clean_string(res.markdown),
            "date": datetime.now().strftime("%Y-%m-%d")
            })
        else:
            print(f"[ERROR] {res.url} => {res.error_message}")
        with open(file, "w", encoding="utf-8") as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(quick_parallel_example(
        funcExtract=extract_domestic_experience_links,
        base_url="https://khamphadisan.com.vn/cam-nang/",
        className="article.post-content",
        file="explore.json"
    ))