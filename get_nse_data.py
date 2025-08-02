import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Headers to mimic real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nseindia.com'
}

# NSE Sector indices to track
SECTORS = [
    'NIFTY FMCG', 'NIFTY PHARMA', 'NIFTY IT', 'NIFTY BANK', 'NIFTY AUTO',
    'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY REALTY', 'NIFTY ENERGY', 'NIFTY PSU BANK',
    'NIFTY PRIVATE BANK', 'NIFTY FINANCIAL SERVICES', 'NIFTY HEALTHCARE INDEX', 'NIFTY CONSUMER DURABLES'
]

def create_session():
    """Create NSE session with proper cookies"""
    session = requests.Session()
    session.headers.update(HEADERS)
    try:
        # Get cookies from NSE homepage
        session.get('https://www.nseindia.com', timeout=10)
        time.sleep(2)
        return session
    except:
        print("Warning: NSE session creation failed, using basic session")
        return session

def fetch_sector_data(session):
    """Fetch real NSE sector index data"""
    try:
        response = session.get('https://www.nseindia.com/api/allIndices', timeout=15)
        data = response.json().get('data', [])
        
        results = []
        for sector in SECTORS:
            sector_data = next((item for item in data if item.get('index') == sector), None)
            if sector_data:
                results.append({
                    'name': sector,
                    'last_price': float(sector_data.get('last', 0)),
                    'percent_change': float(sector_data.get('pChange', 0)),
                    'change': float(sector_data.get('change', 0)),
                    'day_high': float(sector_data.get('dayHigh', 0)),
                    'day_low': float(sector_data.get('dayLow', 0))
                })
                print(f"✅ {sector}: {sector_data.get('pChange', 0):.2f}%")
        
        return results
        
    except Exception as e:
        print(f"❌ Error fetching sector data: {e}")
        return []

def fetch_business_today_news():
    """Scrape Business Today economy news"""
    try:
        url = "https://www.businesstoday.in/latest/economy"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for link in soup.select("ul.listingNews li a")[:5]:
            title = link.get_text(strip=True)
            url_path = link.get('href', '')
            if url_path and not url_path.startswith('http'):
                url_path = "https://www.businesstoday.in" + url_path
            
            articles.append({
                'title': title,
                'url': url_path,
                'source': 'Business Today'
            })
        
        print(f"✅ Business Today: {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"❌ Business Today fetch error: {e}")
        return []

def fetch_moneycontrol_news():
    """Scrape MoneyControl market news"""
    try:
        url = "https://www.moneycontrol.com/news/business/markets/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        for article in soup.select("div.listingnews_block article")[:5]:
            link = article.find('a', href=True)
            if link:
                title = link.get_text(strip=True)
                url_path = link.get('href', '')
                
                articles.append({
                    'title': title,
                    'url': url_path,
                    'source': 'MoneyControl'
                })
        
        print(f"✅ MoneyControl: {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"❌ MoneyControl fetch error: {e}")
        return []

def fetch_trading_economics_news():
    """Fetch Trading Economics India news"""
    try:
        url = "https://api.tradingeconomics.com/news/country/india?c=guest:guest"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        articles = []
        for item in data[:5]:
            articles.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'source': item.get('source', 'Trading Economics')
            })
        
        print(f"✅ Trading Economics: {len(articles)} articles")
        return articles
        
    except Exception as e:
        print(f"❌ Trading Economics fetch error: {e}")
        return []

def get_next_trading_day():
    """Calculate next trading day"""
    now = datetime.now()
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    
    if weekday == 4:  # Friday
        days_to_add = 3  # Next Monday
    elif weekday == 5:  # Saturday
        days_to_add = 2  # Next Monday
    elif weekday == 6:  # Sunday
        days_to_add = 1  # Next Monday
    else:  # Monday-Thursday
        days_to_add = 1  # Next day
    
    next_day = now + timedelta(days=days_to_add)
    return next_day.strftime("%A, %B %d, %Y")

def create_trading_strategy(sectors):
    """Generate trading strategy based on sector performance"""
    if not sectors:
        return {'buy': [], 'sell': [], 'hold': []}
    
    # Sort by performance
    sorted_sectors = sorted(sectors, key=lambda x: x['percent_change'], reverse=True)
    
    # Top performer (potential buy)
    buy_candidates = [s['name'] for s in sorted_sectors[:1] if s['percent_change'] > -1.0]
    
    # Worst performers (avoid/sell)
    sell_candidates = [s['name'] for s in sorted_sectors[-2:] if s['percent_change'] < -1.0]
    
    # Neutral performers (hold)
    hold_candidates = [s['name'] for s in sectors if -0.5 <= s['percent_change'] <= 0.5]
    
    return {
        'buy': buy_candidates,
        'sell': sell_candidates,
        'hold': hold_candidates
    }

def generate_javascript_updater(sectors, news, strategy, next_trading_day_str):
    """Generate JavaScript file with all data"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')
    
    js_code = f'''// Auto-generated NSE Data Updater
// Generated on: {timestamp}
// Data updates every 5 minutes via GitHub Actions

const sectorData = {json.dumps(sectors, indent=2)};
const liveFinancialNews = {json.dumps(news, indent=2)};
const strategyData = {json.dumps(strategy, indent=2)};
const nextTradingDay = "{next_trading_day_str}";
const lastUpdated = "{timestamp}";

// Update page elements with real data
function updatePageData() {{
    // Update header information
    document.getElementById('market-status').textContent = "🔔 Markets Closed for Weekend";
    document.getElementById('next-trading-day').textContent = `📅 Next Trading Session: ${{nextTradingDay}} at 9:15 AM IST`;
    document.getElementById('last-updated').textContent = `🕒 Last Updated: ${{lastUpdated}}`;
    document.getElementById('footer-update').textContent = `🕒 Last Updated: ${{lastUpdated}}`;
    
    // Update breaking news
    updateBreakingNews();
    
    // Update sector performance
    updateSectorPerformance();
    
    // Update growth potential
    updateGrowthPotential();
    
    // Update trading strategy
    updateTradingStrategy();
}}

function updateBreakingNews() {{
    const container = document.getElementById('breaking-news-container');
    if (!liveFinancialNews || liveFinancialNews.length === 0) {{
        container.innerHTML = '<div class="loading">No breaking news available at this time.</div>';
        return;
    }}
    
    let newsHtml = '';
    liveFinancialNews.slice(0, 5).forEach(news => {{
        newsHtml += `
            <div class="breaking-news-item">
                <h3>${{news.title}}</h3>
                <p>${{news.source}} • <a href="${{news.url}}" target="_blank">Read Full Article</a></p>
            </div>
        `;
    }});
    
    container.innerHTML = newsHtml;
}}

function updateSectorPerformance() {{
    const grid = document.getElementById('performance-grid');
    if (!sectorData || sectorData.length === 0) {{
        grid.innerHTML = '<div class="loading">Unable to load sector performance data.</div>';
        return;
    }}
    
    let html = '';
    sectorData.forEach(sector => {{
        const changeClass = sector.percent_change > 0.2 ? 'gainer' : 
                           sector.percent_change < -0.2 ? 'decliner' : 'neutral';
        const signClass = sector.percent_change > 0 ? 'positive' :
                         sector.percent_change < 0 ? 'negative' : 'neutral';
        const sign = sector.percent_change > 0 ? '+' : '';
        
        html += `
            <div class="sector-performance-item ${{changeClass}}">
                <span class="sector-name">${{sector.name}}</span>
                <span class="today-change ${{signClass}}">${{sign}}${{sector.percent_change.toFixed(2)}}%</span>
                <span class="sector-status">${{getStatusText(sector.percent_change)}}</span>
            </div>
        `;
    }});
    
    grid.innerHTML = html;
}}

function updateGrowthPotential() {{
    const grid = document.getElementById('potential-grid');
    if (!sectorData || sectorData.length === 0) {{
        grid.innerHTML = '<div class="loading">Unable to analyze growth potential.</div>';
        return;
    }}
    
    let html = '';
    sectorData.forEach(sector => {{
        const potentialClass = sector.percent_change > 1 ? 'high-potential' :
                              sector.percent_change < -1 ? 'high-risk' : 'medium-potential';
        const sign = sector.percent_change > 0 ? '+' : '';
        
        html += `
            <div class="potential-item ${{potentialClass}}">
                <span class="sector-name">${{sector.name}}</span>
                <span class="potential-change">${{sign}}${{sector.percent_change.toFixed(2)}}%</span>
                <span class="potential-reason">${{getPotentialReason(sector.percent_change)}}</span>
            </div>
        `;
    }});
    
    grid.innerHTML = html;
}}

function updateTradingStrategy() {{
    // Buy opportunities
    const buyList = document.getElementById('buy-strategy-list');
    let buyHtml = '';
    if (strategyData.buy.length > 0) {{
        strategyData.buy.forEach(sector => {{
            buyHtml += `<li><strong>${{sector}}</strong>: Showing relative strength, potential for momentum continuation</li>`;
        }});
    }} else {{
        buyHtml = '<li>No clear buy opportunities in current market conditions</li>';
    }}
    buyList.innerHTML = buyHtml;
    
    // Sell/Avoid
    const sellList = document.getElementById('sell-strategy-list');
    let sellHtml = '';
    if (strategyData.sell.length > 0) {{
        strategyData.sell.forEach(sector => {{
            sellHtml += `<li><strong>${{sector}}</strong>: Showing weakness, consider avoiding or profit booking</li>`;
        }});
    }} else {{
        sellHtml = '<li>No major sell signals in current market conditions</li>';
    }}
    sellList.innerHTML = sellHtml;
    
    // Hold/Monitor
    const holdList = document.getElementById('hold-strategy-list');
    let holdHtml = '';
    if (strategyData.hold.length > 0) {{
        strategyData.hold.forEach(sector => {{
            holdHtml += `<li><strong>${{sector}}</strong>: Range-bound, wait for clear direction</li>`;
        }});
    }} else {{
        holdHtml = '<li>Most sectors showing clear directional moves</li>';
    }}
    holdList.innerHTML = holdHtml;
}}

function getStatusText(change) {{
    if (change > 2) return "Strong Rally";
    if (change > 1) return "Good Gains";
    if (change > 0.5) return "Positive";
    if (change >= -0.1 && change <= 0.1) return "Flat";
    if (change > -1) return "Weak";
    if (change > -2) return "Under Pressure";
    return "Sharp Decline";
}}

function getPotentialReason(change) {{
    if (change > 1) return "Momentum likely to continue";
    if (change < -1) return "Risk of further decline";
    return "Mixed signals, watch closely";
}}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {{
    updatePageData();
    
    // Update breaking news every 3 minutes
    setInterval(updateBreakingNews, 180000);
    
    console.log('✅ Nifty Sectoral News Hub loaded successfully');
    console.log(`📊 Loaded ${{sectorData.length}} sectors`);
    console.log(`📰 Loaded ${{liveFinancialNews.length}} news articles`);
}});
'''
    
    # Write the JavaScript file
    with open('nse_data_updater.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print("✅ Generated nse_data_updater.js successfully")

def main():
    print("🚀 Starting NSE Sectoral Data Scraper...")
    print("=" * 60)
    
    # Create session
    session = create_session()
    
    # Fetch all data
    print("\n📊 Fetching sector data...")
    sectors = fetch_sector_data(session)
    
    print("\n📰 Fetching news...")
    news = []
    news.extend(fetch_business_today_news())
    news.extend(fetch_moneycontrol_news())
    news.extend(fetch_trading_economics_news())
    
    # Get next trading day
    next_trading = get_next_trading_day()
    
    # Create trading strategy
    strategy = create_trading_strategy(sectors)
    
    # Generate JavaScript updater
    print("\n🔧 Generating website updater...")
    generate_javascript_updater(sectors, news, strategy, next_trading)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📈 SCRAPING SUMMARY")
    print("=" * 60)
    print(f"✅ Sectors loaded: {len(sectors)}")
    print(f"✅ News articles: {len(news)}")
    print(f"✅ Next trading day: {next_trading}")
    print(f"✅ Buy signals: {len(strategy['buy'])}")
    print(f"✅ Sell signals: {len(strategy['sell'])}")
    print(f"✅ Hold signals: {len(strategy['hold'])}")
    
    if sectors:
        sorted_sectors = sorted(sectors, key=lambda x: x['percent_change'], reverse=True)
        print(f"\n🏆 Top Performer: {sorted_sectors[0]['name']} ({sorted_sectors[0]['percent_change']:+.2f}%)")
        print(f"📉 Worst Performer: {sorted_sectors[-1]['name']} ({sorted_sectors[-1]['percent_change']:+.2f}%)")
    
    print(f"\n🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("✅ Website will auto-update with this fresh data!")

if __name__ == "__main__":
    main()
