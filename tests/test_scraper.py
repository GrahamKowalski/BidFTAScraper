"""
Tests for the BidFTA Scraper
"""

import pytest
from bidfta_scraper import BidFTAScraper, BidFTAItem, format_results
import pandas as pd
from unittest.mock import Mock, patch

@pytest.fixture
def mock_response():
    """Create a mock response with test data"""
    return {
        "props": {
            "pageProps": {
                "initialData": {
                    "items": [
                        {
                            "title": "Test Aquarium",
                            "currentBid": 50.00,
                            "imageUrl": "http://example.com/image.jpg",
                            "utcEndDateTime": "2024-01-20T14:19:00Z",
                            "itemTimeRemaining": "3600",
                            "msrp": 100.00,
                            "condition": "As Is",
                            "lotCode": "TEST123",
                            "bidsCount": 5,
                            "auctionId": "12345"
                        }
                    ]
                }
            }
        }
    }

@pytest.fixture
def scraper():
    """Create a BidFTAScraper instance"""
    return BidFTAScraper()

def test_build_url(scraper):
    """Test URL building"""
    url = scraper.build_url("aquarium")
    expected = "https://www.bidfta.com/items?pageId=1&itemSearchKeywords=aquarium&locations=616"
    assert url == expected

def test_bidfta_item_creation():
    """Test BidFTAItem object creation"""
    item_data = {
        "title": "Test Item",
        "currentBid": 10.00,
        "imageUrl": "http://example.com/test.jpg",
        "utcEndDateTime": "2024-01-20T00:00:00Z",
        "itemTimeRemaining": "7200",
        "msrp": 20.00,
        "condition": "New",
        "lotCode": "ABC123",
        "bidsCount": 3,
        "auctionId": "54321"
    }
    
    item = BidFTAItem(item_data, "test")
    
    assert item.title == "Test Item"
    assert item.current_bid == 10.00
    assert item.search_term == "test"

@patch('requests.Session')
def test_scrape_search_term(mock_session, scraper, mock_response):
    """Test scraping a single search term"""
    # Setup mock response
    mock_get = Mock()
    mock_get.text = '<script id="__NEXT_DATA__">' + str(mock_response) + '</script>'
    mock_session.return_value.get.return_value = mock_get
    
    items = scraper.scrape_search_term("aquarium")
    
    assert len(items) == 1
    assert items[0].title == "Test Aquarium"

def test_format_results(capsys):
    """Test results formatting"""
    # Create test DataFrame
    data = {
        'title': ['Test Item'],
        'current_bid': ['$10.00'],
        'hours_remaining': [2.0],
        'search_term': ['test']
    }
    df = pd.DataFrame(data)
    
    # Test without save path
    format_results(df)
    captured = capsys.readouterr()
    assert "Found Items:" in captured.out
    assert "Test Item" in captured.out

def test_format_results_with_save(tmp_path):
    """Test results formatting with file saving"""
    data = {
        'title': ['Test Item'],
        'current_bid': ['$10.00'],
        'hours_remaining': [2.0],
        'search_term': ['test']
    }
    df = pd.DataFrame(data)
    
    # Create temporary file path
    save_path = tmp_path / "test_results.csv"
    
    # Test with save path
    format_results(df, str(save_path))
    
    # Verify file was created and contains correct data
    assert save_path.exists()
    saved_df = pd.read_csv(save_path)
    assert len(saved_df) == 1
    assert saved_df['title'][0] == 'Test Item'

def test_empty_results(capsys):
    """Test handling of empty results"""
    df = pd.DataFrame()
    format_results(df)
    
    captured = capsys.readouterr()
    assert "No items found" in captured.out

def test_scrape_search_terms():
    """Test scraping multiple search terms"""
    scraper = BidFTAScraper()
    
    # Mock the scrape_search_term method
    with patch.object(scraper, 'scrape_search_term') as mock_scrape:
        # Setup mock return values
        mock_item = BidFTAItem({
            "title": "Test Item",
            "currentBid": 10.00,
            "msrp": 20.00,
            "condition": "New",
            "lotCode": "ABC123"
        }, "test")
        mock_scrape.return_value = [mock_item]
        
        # Test with multiple search terms
        results_df = scraper.scrape_search_terms(["term1", "term2"])
        
        # Verify the method was called for each search term
        assert mock_scrape.call_count == 2
        assert len(results_df) == 2  # One result per search term