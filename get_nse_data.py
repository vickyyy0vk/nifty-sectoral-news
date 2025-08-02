import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nseindia.com'
}

SECTORS = [
    'NIFTY FMCG', 'NIFTY PHARMA', 'NIFTY IT', 'NIFTY BANK', 'NIFTY AUTO',
    'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY REALTY', 'NIFTY ENERGY', 'NIFTY PSU BANK',
    'NIFTY PRIVATE BANK', 'NIFTY FINANCIAL SERVICES', 'NIFTY HEALTHCARE INDEX', 'NIFTY CONSUMER DURABLES'
]

def create_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.get('https://www.nseindia.com', timeout=5)
    time.sleep(1)
    return session

def fetch_sector_data(session):
    resp = session.get('https://www.nseindia.com/api/allIndices', timeout=10)
    data = resp.json().get('data', [])
    results = []
    for sector in SECTORS:
        found = next((item for item in data if item['index'] == sector), None)
        if found:
            results.append({
                'name': sector,
                'last_price': float(found.get('last', 0)),
                'percent_change': float(found.get('pChange', 0))
            })
    return results

def fetch_bt():
    url = "https://www.businesstoday.in/latest/economy"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [{
        'title': a.get_text(strip=True), 'url': ("https://www.businesstoday.in" + a["href"]), 'source': 'Business Today'
    } for a in soup.select("ul.listingNews li a")]

def fetch_mc():
    url = "https://www.moneycontrol.com/news/business/markets/"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, "html.parser")
    return [{
        'title': a.get_text(strip=True), 'url': a['href'], 'source': 'MoneyControl'
    } for div in soup.select("div.listingnews_block article") if (a:=div.find("a", href=True))]

def fetch_te():
    url = "https://api.tradingeconomics.com/news/country/india?c=guest:guest"
    data = requests.get(url, timeout=6).json()
    return [{
        'title': item.get('title'), 'url': item.get('url'), 'source': item.get('source')
    } for item in data][:10]

def next_trading_day():
    now = datetime.now()
    w = now.weekday()
    if w==4: days=3 # Friday
    elif w==5: days=2 # Saturday
    else: days=1
    nxt = now + timedelta(days=days)
    return nxt.strftime("%A, %B %d, %Y"), nxt.strftime("%b %d, %Y")

def make_strategy(sectors):
    # Simple dynamic signals (can be improved with more logic)
    top = max(sectors, key=lambda x: x['percent_change'])
    worst = min(sectors, key=lambda x: x['percent_change'])
    buy = [top['name']]
    avoid = [worst['name']]
    return {
        'buy': buy, 'sell': avoid, 'hold': [s['name'] for s in sectors if abs(s['percent_change'])<0.5]
    }

def make_js(sectors, news, strategy, today_str, next_str, today_date, next_date):
    js = f"""\
// Auto-generated JS at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// AUTO-SCRAPES EVERY 3 MIN

const sectorData = {json.dumps(sectors)};
const liveFinancialNews = {json.dumps(news)};
const strategyData = {json.dumps(strategy)};
const todayDate = "{today_date}";
const nextDate = "{next_date}";
const todayStr = "{today_str}";
const nextStr = "{next_str}";

// --- Sector performance ---
function updateTodayPerformance() {{
  let grid = '';
  sectorData.forEach(s => {{
    grid += `
      <div class="sector-performance-item ${(s.percent_change>0.2?'gainer':s.percent_change<-0.2?'decliner':'neutral')}">
        <span class="sector-name">{s['name']}</span>
        <span class="today-change ${(s.percent_change>0.2?'positive':s.percent_change<-0.2?'negative':'neutral')}">${{s.percent_change>0?'+':''}}${{s.percent_change.toFixed(2)}}%</span>
      </div>`;
  }});
  document.querySelector('.performance-grid').innerHTML = grid;
}}

// --- Breaking news ---
function fetchBreakingNews() {{
  const news = liveFinancialNews.slice(0, 5);
  const container = document.getElementById('breaking-news-container');
  let html = '';
  news.forEach(item => {{
    html += `
      <div class="breaking-news-item">
        <h3>${{item.title}}</h3>
        <p>${{item.source || ''}} &bull; <a href="${{item.url}}" target="_blank">Read Full Article</a></p>
      </div>`;
  }});
  container.innerHTML = html || '<div>No breaking news available.</div>';
}}

// --- Strategy/Next Day Update ---
function updateNextTradingStrategy() {{
  document.querySelector('.strategy-card.buy-strategy ul').innerHTML =
    strategyData.buy.map(s => `<li><strong>${{s}}:</strong> Fresh momentum or signal</li>`).join('');
  document.querySelector('.strategy-card.sell-strategy ul').innerHTML =
    strategyData.sell.map(s => `<li><strong>${{s}}:</strong> Caution advised</li>`).join('');
  document.querySelector('.strategy-card.hold-strategy ul').innerHTML =
    strategyData.hold.map(s => `<li><strong>${{s}}:</strong> Hold or wait and watch</li>`).join('');
}}

document.addEventListener('DOMContentLoaded', () => {{
  updateTodayPerformance();
  fetchBreakingNews();
  updateNextTradingStrategy();
  setInterval(fetchBreakingNews, 180000);
}});
"""
    with open('nse_data_updater.js', 'w') as f:
        f.write(js)
    print("🟢 Updated nse_data_updater.js")

def main():
    session = create_session()
    sectors = fetch_sector_data(session)
    news = fetch_bt() + fetch_mc() + fetch_te()
    today_str, today_date = datetime.now().strftime("%A, %b %d, %Y"), datetime.now().strftime("%b %d, %Y")
    next_str, next_date = next_trading_day()
    strategy = make_strategy(sectors)
    make_js(sectors, news, strategy, today_str, next_str, today_date, next_date)

if __name__ == "__main__":
    main()
