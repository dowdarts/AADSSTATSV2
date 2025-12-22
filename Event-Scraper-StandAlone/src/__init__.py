"""
Event Scraper Application - Source Package
"""

__version__ = "1.0.0"
__author__ = "AADS Development Team"
__description__ = "Standalone event scraper for DartConnect tournaments"

from .database_manager import AADSDataManager
from .scraper import DartConnectScraper
from .event_data_manager import EventDataManager

__all__ = [
    'AADSDataManager',
    'DartConnectScraper',
    'EventDataManager'
]
