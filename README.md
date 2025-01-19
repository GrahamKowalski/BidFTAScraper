# BidFTA Scraper

A Python package for scraping auction listings from BidFTA.com. Supports both synchronous and asynchronous operations for efficient data collection across multiple search terms.

## Features

- Search for multiple terms simultaneously
- Filter by location
- Extract detailed item information including:
  - Current bid
  - Time remaining
  - MSRP
  - Item condition
  - Image URLs
  - Lot codes
- Export results to CSV
- Configurable request delays to respect server limits
- Comprehensive logging

## Example Return

![Alt text](/reference/example_return.png?raw=true "CSV Data")

## Installation

Install from source:

```bash
git clone https://github.com/GrahamKowalski/BidFTAScraper.git
cd bidfta-scraper
pip install -e .
```

## Quick Start

### Synchronous Usage

```python
from bidfta_scraper import BidFTAScraper, format_results

# Initialize scraper
scraper = BidFTAScraper(location_id="616")  # Default location | Strongsville

# Define search terms
search_terms = ["aquarium", "fish tank", "filter"]

# Get results
results_df = scraper.scrape_search_terms(search_terms)

# Format and save results
format_results(results_df, 'auction_results.csv')
```

### Asynchronous Usage

#### **IMPORTANT**

As of 1-19-25, aiodns requires a SelectorEventLoop, but Python 3.12 uses ProactorEventLoop.
For Windows use be sure to set event loop correctly:

```python
import sys

if sys.platform == 'win32':
    # Force use of selector event loop on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

```python
from bidfta_scraper import AsyncBidFTAScraper, format_async_results
import asyncio

async def main():
    # Initialize async scraper with custom settings
    scraper = AsyncBidFTAScraper(
        location_id="616",
        max_concurrent_requests=5,  # Limit concurrent requests
        request_delay=0.5  # Delay between requests in seconds
    )
    
    # Define search terms
    search_terms = ["aquarium", "fish tank", "filter"]
    
    # Get results asynchronously
    results_df = await scraper.scrape_search_terms(search_terms)
    
    # Format and save results
    format_async_results(results_df, 'async_results.csv')

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Location ID

```python
# Initialize with a different location
scraper = BidFTAScraper(location_id="123", request_delay=3)
```

### Processing Individual Items

```python
# Scrape a single search term
items = scraper.scrape_search_term("aquarium")

# Process individual items
for item in items:
    print(f"Title: {item.title}")
    print(f"Current Bid: {item.current_bid}")
    print(f"Time Remaining: {item.time_remaining}")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/GrahamKowalski/BidFTAScraper.git
cd bidfta-scraper

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Me - Graham Kowalski

Project Link: [https://github.com/GrahamKowalski/BidFTAScraper](https://github.com/GrahamKowalski/BidFTAScraper)
