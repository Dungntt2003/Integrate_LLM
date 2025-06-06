import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerMonitor, CrawlerRunConfig, CacheMode, DisplayMode, MemoryAdaptiveDispatcher, RateLimiter, SemaphoreDispatcher
from getHotelLinks import extract_hotel_links
from hotel import extract_data_hotel

async def crawl_with_semaphore(urls):
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    dispatcher = SemaphoreDispatcher(
        semaphore_count=5,
        rate_limiter=RateLimiter(
            base_delay=(0.5, 1.0),
            max_delay=10.0
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun_many(
            urls, 
            config=run_config,
            dispatcher=dispatcher
        )
        for res in results:
            if res.success:
                await extract_data_hotel(res.url)
                # print(f"[SUCCESS] {res.url}")
            else:
                print(f"[ERROR] {res.url} => {res.error_message}")
    
if __name__ == "__main__":
    asyncio.run(crawl_with_semaphore(extract_hotel_links(url="https://www.bestprice.vn/khach-san/da-nang")[:2]))