import requests
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict

# Headers for NSE scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nseindia.com'
}

# NSE Sectoral Indices URLs
SECTORS = {
    'NIFTY FMCG': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FMCG',
    'NIFTY PHARMA': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20PHARMA',
    'NIFTY IT': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20IT',
    'NIFTY BANK': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK',
    'NIFTY AUTO': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20AUTO',
    'NIFTY MEDIA': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MEDIA',
    'NIFTY METAL': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20METAL',
    'NIFTY REALTY': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20REALTY',
    'NIFTY ENERGY': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20ENERGY',
    'NIFTY PSU BANK': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20PSU%20BANK',
    'NIFTY PRIVATE BANK': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20PRIVATE%20BANK',
    'NIFTY FINANCIAL SERVICES': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES',
    'NIFTY HEALTHCARE INDEX': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20HEALTHCARE%20INDEX',
    'NIFTY CONSUMER DURABLES': 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20CONSUMER%20DURABLES'
}

def create_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS
