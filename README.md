# BidFTA Scraper

A Python package for scraping auction listings from BidFTA.com. This tool allows you to monitor multiple search terms and track auction items across different locations.

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

## Installation

Install from source:

```bash
git clone https://github.com/GrahamKowalski/BidFTAScraper.git
cd bidfta-scraper
pip install -e .
```

## Quick Start

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

## Advanced Usage

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
