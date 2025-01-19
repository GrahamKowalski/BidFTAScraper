from bidfta_scraper import BidFTAScraper, format_results

# Initialize scraper
scraper = BidFTAScraper(location_id="616")  # Default location

# Define search terms
search_terms = ["aquarium", "fish tank", "filter"]

# Get results
results_df = scraper.scrape_search_terms(search_terms)

# Format and save results
format_results(results_df, 'auction_results.csv')