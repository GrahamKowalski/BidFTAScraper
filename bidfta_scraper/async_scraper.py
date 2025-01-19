"""
Async implementation of the BidFTA Scraper
"""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
import logging
from .scraper import BidFTAItem

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AsyncBidFTAScraper:
    """Asynchronous scraper class for BidFTA.com"""
    
    def __init__(self, 
                 location_id: str = "616", 
                 request_delay: float = 0.5,
                 max_concurrent_requests: int = 5):
        """
        Initialize the async BidFTA scraper
        
        Args:
            location_id: The location ID to filter results (default: "616")
            request_delay: Delay between requests in seconds (default: 0.5)
            max_concurrent_requests: Maximum number of concurrent requests (default: 5)
        """
        self.base_url = "https://www.bidfta.com/items"
        self.location_id = location_id
        self.request_delay = request_delay
        self.max_concurrent_requests = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        
    def build_url(self, search_term: str) -> str:
        """Build the URL for the search query"""
        return f"{self.base_url}?pageId=1&itemSearchKeywords={search_term}&locations={self.location_id}"
    
    async def extract_items_from_json(self, json_data: Dict, search_term: str) -> List[BidFTAItem]:
        """Extract item information from JSON data"""
        items = []
        try:
            raw_items = json_data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('items', [])
            for item_data in raw_items:
                items.append(BidFTAItem(item_data, search_term))
        except Exception as e:
            logger.error(f"Error extracting items: {str(e)}")
        
        return items

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a page with rate limiting"""
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    await asyncio.sleep(self.request_delay)
                    return await response.text()
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                return None

    async def scrape_search_term(self, 
                               session: aiohttp.ClientSession, 
                               search_term: str) -> List[BidFTAItem]:
        """Scrape data for a single search term"""
        url = self.build_url(search_term)
        items = []
        
        try:
            html_content = await self.fetch_page(session, url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                
                if script_tag:
                    json_data = json.loads(script_tag.string)
                    items = await self.extract_items_from_json(json_data, search_term)
                    logger.info(f"Found {len(items)} items for search term: {search_term}")
                else:
                    logger.warning(f"No data found for search term: {search_term}")
        except Exception as e:
            logger.error(f"Error processing search term '{search_term}': {str(e)}")
        
        return items

    async def scrape_search_terms(self, search_terms: List[str]) -> pd.DataFrame:
        """
        Scrape data for multiple search terms asynchronously
        
        Args:
            search_terms: List of terms to search for
            
        Returns:
            DataFrame containing all found items
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_search_term(session, term) for term in search_terms]
            results = await asyncio.gather(*tasks)
            
        # Flatten results and convert to list of dictionaries
        all_items = []
        for items in results:
            all_items.extend([item.to_dict() for item in items])
        
        # Convert to DataFrame
        df = pd.DataFrame(all_items)
        if not df.empty:
            # Process DataFrame
            df['end_datetime'] = pd.to_datetime(df['end_datetime'])
            df['hours_remaining'] = df['time_remaining'].astype(float) / 3600
            df['current_bid'] = df['current_bid'].apply(lambda x: f"${x:,.2f}")
            df['msrp'] = df['msrp'].apply(lambda x: f"${x:,.2f}")
        
        return df

def format_async_results(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """Format and optionally save the results"""
    if df.empty:
        logger.info("No items found")
        return
    
    # Display results
    print("\nFound Items:")
    display_columns = ['title', 'current_bid', 'hours_remaining', 'search_term']
    print(df[display_columns].to_string())
    
    # Save to CSV if path provided
    if save_path:
        df.to_csv(save_path, index=False)
        logger.info(f"Results saved to '{save_path}'")

async def main():
    """Example usage of the async scraper"""
    scraper = AsyncBidFTAScraper()
    search_terms = ["aquarium", "fish tank", "filter"]
    results_df = await scraper.scrape_search_terms(search_terms)
    format_async_results(results_df, 'async_results.csv')

if __name__ == "__main__":
    asyncio.run(main())