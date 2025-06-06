import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

async def main():
    config = CrawlerRunConfig(
        # Target article body and sidebar, but not other content
        target_elements=["article.post-content"]
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://khamphadisan.com.vn/dia-diem-checkin-bac-giang/", 
            config=config
        )
        print("Markdown focused on target elements")
        print("Markdown: ", result.markdown)

if __name__ == "__main__":
    asyncio.run(main())