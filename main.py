from bidfta_scraper import AsyncBidFTAScraper
import asyncio

import sys

if sys.platform == 'win32':
    # Force use of selector event loop on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    scraper = AsyncBidFTAScraper(
        max_concurrent_requests=5,  # Maximum concurrent requests
        request_delay=0.5  # Delay between requests in seconds
    )
    
    search_terms = ["aquarium", "fish tank", "filter","monitor","sensor","motor","machine","smart"]
    results_df = await scraper.scrape_search_terms(search_terms)
    
    # Save or process results
    results_df.to_csv('results.csv')

if __name__ == "__main__":
    asyncio.run(main())