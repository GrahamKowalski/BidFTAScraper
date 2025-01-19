"""
BidFTAScraper: A module for scraping auction data from BidFTA.com
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BidFTAItem:
    """Class to represent a single BidFTA auction item"""
    def __init__(self, item_data: Dict, search_term: str):
        self.title = item_data.get('title', '')
        self.current_bid = item_data.get('currentBid', 0)
        self.image_url = item_data.get('imageUrl', '')
        self.end_datetime = item_data.get('utcEndDateTime', '')
        self.time_remaining = item_data.get('itemTimeRemaining', '')
        self.msrp = item_data.get('msrp', 0)
        self.condition = item_data.get('condition', '')
        self.lot_code = item_data.get('lotCode', '')
        self.search_term = search_term
        self.bids_count = item_data.get('bidsCount', 0)
        self.auction_id = item_data.get('auctionId', '')

    def to_dict(self) -> Dict:
        """Convert item to dictionary format"""
        return {
            'title': self.title,
            'current_bid': self.current_bid,
            'image_url': self.image_url,
            'end_datetime': self.end_datetime,
            'time_remaining': self.time_remaining,
            'msrp': self.msrp,
            'condition': self.condition,
            'lot_code': self.lot_code,
            'search_term': self.search_term,
            'bids_count': self.bids_count,
            'auction_id': self.auction_id
        }

class BidFTAScraper:
    """Main scraper class for BidFTA.com"""
    
    def __init__(self, location_id: str = "616", request_delay: int = 2):
        """
        Initialize the BidFTA scraper
        
        Args:
            location_id: The location ID to filter results (default: "616")
            request_delay: Delay between requests in seconds (default: 2)
        """
        self.base_url = "https://www.bidfta.com/items"
        self.location_id = location_id
        self.request_delay = request_delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def build_url(self, search_term: str) -> str:
        """
        Build the URL for the search query
        
        Args:
            search_term: Term to search for
            
        Returns:
            Complete URL for the search
        """
        return f"{self.base_url}?pageId=1&itemSearchKeywords={search_term}&locations={self.location_id}"
    
    def extract_items_from_json(self, json_data: Dict, search_term: str) -> List[BidFTAItem]:
        """
        Extract item information from JSON data
        
        Args:
            json_data: JSON data from the webpage
            search_term: The search term used to find these items
            
        Returns:
            List of BidFTAItem objects
        """
        items = []
        try:
            raw_items = json_data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('items', [])
            for item_data in raw_items:
                items.append(BidFTAItem(item_data, search_term))
        except Exception as e:
            logger.error(f"Error extracting items: {str(e)}")
        
        return items

    def scrape_search_term(self, search_term: str) -> List[BidFTAItem]:
        """
        Scrape data for a single search term
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of BidFTAItem objects
        """
        url = self.build_url(search_term)
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            
            if script_tag:
                json_data = json.loads(script_tag.string)
                return self.extract_items_from_json(json_data, search_term)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for term '{search_term}': {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for term '{search_term}': {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error for term '{search_term}': {str(e)}")
        
        return []

    def scrape_search_terms(self, search_terms: List[str]) -> pd.DataFrame:
        """
        Scrape data for multiple search terms and return as a DataFrame
        
        Args:
            search_terms: List of terms to search for
            
        Returns:
            DataFrame containing all found items
        """
        all_items = []
        
        for term in search_terms:
            logger.info(f"Scraping term: {term}")
            items = self.scrape_search_term(term)
            all_items.extend([item.to_dict() for item in items])
            time.sleep(self.request_delay)
        
        df = pd.DataFrame(all_items)
        if not df.empty:
            # Process DataFrame
            df['end_datetime'] = pd.to_datetime(df['end_datetime'])
            df['hours_remaining'] = df['time_remaining'].astype(float) / 3600
            df['current_bid'] = df['current_bid'].apply(lambda x: f"${x:,.2f}")
            df['msrp'] = df['msrp'].apply(lambda x: f"${x:,.2f}")
        
        return df

def format_results(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Format and optionally save the results
    
    Args:
        df: DataFrame containing the results
        save_path: Optional path to save CSV file
    """
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

if __name__ == "__main__":
    # Example usage
    scraper = BidFTAScraper()
    search_terms = ["aquarium", "fish tank", "filter"]
    results_df = scraper.scrape_search_terms(search_terms)
    format_results(results_df, 'bidfta_results.csv')