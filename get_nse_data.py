import requests
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict

# Headers for NSE site scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nseindia.com'
}

# List of sectors to scrape (names only)
SECTORS = {
    'NIFTY FMCG': None,
    'NIFTY PHARMA': None,
    'NIFTY IT': None,
    'NIFTY BANK': None,
    'NIFTY AUTO': None,
    'NIFTY MEDIA': None,
    'NIFTY METAL': None,
    'NIFTY REALTY': None,
    'NIFTY ENERGY': None,
    'NIFTY PSU BANK': None,
    'NIFTY PRIVATE BANK': None,
    'NIFTY FINANCIAL SERVICES': None,
    'NIFTY HEALTHCARE INDEX': None,
    'NIFTY CONSUMER DURABLES': None
}

def create_session() -> requests.Session:
    """Initialize NSE session to obtain cookies."""
    session = requests.Session()
    session.headers.update(HEADERS)
    # Hit homepage to establish session cookies
    session.get('https://www.nseindia.com', timeout=5)
    time.sleep(1)
    return session

def fetch_sector_data(session: requests.Session) -> List[Dict]:
    """
    Fetch true NSE sector index percent changes via the allIndices endpoint.
    Returns a list of dicts with name, last_price, percent_change.
    """
    try:
        resp = session.get('https://www.nseindia.com/api/allIndices', timeout=10)
        resp.raise_for_status()
        data = resp.json().get('data', [])
    except Exception as e:
        print(f"❌ Failed to fetch allIndices: {e}")
        return []

    results = []
    for sector_name in SECTORS:
        match = next((item for item in data if item.get('index') == sector_name), None)
        if match:
            last = float(match.get('last', 0))
            pct  = float(match.get('pChange', 0))
            results.append({
                'name': sector_name,
                'last_price': last,
                'percent_change': pct
            })
            print(f"✅ {sector_name}: {pct:+.2f}%")
        else:
            print(f"⚠️ {sector_name} not found in allIndices")
    return results

# Business Today news scraper
def fetch_business_today_economy() -> List[Dict]:
    url = "https://www.businesstoday.in/latest/economy"
    r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = []
    for a in soup.select("ul.listingNews li a"):
        title = a.get_text(strip=True)
        link = a['href']
        if not link.startswith('http'):
            link = "https://www.businesstoday.in" + link
        articles.append({'title': title, 'url': link, 'source': 'Business Today'})
    return articles

# MoneyControl news scraper
def fetch_moneycontrol_market_news() -> List[Dict]:
    url = "https://www.moneycontrol.com/news/business/markets/"
    r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = []
    for div in soup.select("div.listingnews_block article"):
        a = div.find('a', href=True)
        title = a.get_text(strip=True)
        link = a['href']
        articles.append({'title': title, 'url': link, 'source': 'MoneyControl'})
    return articles

# Trading Economics API (free) news
def fetch_tradingeconomics_india_news() -> List[Dict]:
    url = "https://api.tradingeconomics.com/news/country/india?c=guest:guest"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [
        {'title': item.get('title'),
         'url': item.get('url'),
         'source': item.get('source')}
        for item in data
    ]

def generate_js(sectors: List[Dict], news: List[Dict]):
    """Generate nse_data_updater.js with live sector + news data."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    js = f"""// Auto-generated on {timestamp}
const realNSEData = {json.dumps(sectors, indent=2)};
const liveFinancialNews = {json.dumps(news, indent=2)};

// Update sector cards
function updateWebsiteWithRealNSEData() {{
  document.querySelectorAll('.sector-card').forEach(card => {{
    const nameEl = card.querySelector('h3');
    if (!nameEl) return;
    const sector = nameEl.textContent.trim();
    const sd = realNSEData.find(s => s.name === sector);
    if (sd) {{
      const badge = card.querySelector('.performance-badge');
      badge.textContent = (sd.percent_change >= 0 ? '+' : '') + sd.percent_change.toFixed(2) + '%';
      badge.className = 'performance-badge ' + (sd.percent_change > 0 ? 'positive' : sd.percent_change < 0 ? 'negative' : 'neutral');
    }}
  }});
}}

// Update news feed
function updateNewsWithRealData() {{
  const container = document.getElementById('news-container');
  container.innerHTML = liveFinancialNews.map(n => `
    <div class="news-item">
      <h3>${{n.title}}</h3>
      <p><strong>Source:</strong> ${{n.source}}</p>
      <a href="${{n.url}}" target="_blank">Read more</a>
    </div>
  `).join('');
}}

// Auto-run on page load
document.addEventListener('DOMContentLoaded', () => {{
  updateWebsiteWithRealNSEData();
  updateNewsWithRealData();
  setInterval(updateWebsiteWithRealNSEData, 60000);
  setInterval(updateNewsWithRealData, 300000);
}});
"""
    with open('nse_data_updater.js', 'w') as f:
        f.write(js)
    print("💾 Generated nse_data_updater.js")

def main():
    session = create_session()
    sectors = fetch_sector_data(session)
    news = (
        fetch_business_today_economy() +
        fetch_moneycontrol_market_news() +
        fetch_tradingeconomics_india_news()
    )
    generate_js(sectors, news)
    print("✅ Script complete.")

if __name__ == "__main__":
    main()
