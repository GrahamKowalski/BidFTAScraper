"""
BidFTA Scraper
~~~~~~~~~~~~~

A Python package for scraping auction listings from BidFTA.com.
"""

from .scraper import BidFTAScraper, BidFTAItem, format_results

__version__ = "0.1.0"
__author__ = "Graham Kowalski"

__all__ = ["BidFTAScraper", "BidFTAItem", "format_results"]