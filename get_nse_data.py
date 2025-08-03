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
    
    sorted_sectors = sorted(sectors, key=lambda x: x['percent_change'], reverse=True)
    
    return {
        'buy': [s['name'] for s in sorted_sectors[:1] if s['percent_change'] > -1.0],
        'sell': [s['name'] for s in sorted_sectors[-2:] if s['percent_change'] < -1.0],
        'hold': [s['name'] for s in sectors if -0.5 <= s['percent_change'] <= 0.5]
    }

def generate_javascript_updater(sectors, news, strategy, next_trading):
    """Generate JavaScript file with all data"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')
    
    js_code = f'''// Nifty Sectoral Updater - Generated: {timestamp}

const sectorData = {json.dumps(sectors, indent=2)};
const liveFinancialNews = {json.dumps(news, indent=2)};
const strategyData = {json.dumps(strategy, indent=2)};
const nextTradingDay = "{next_trading}";
const lastUpdated = "{timestamp}";

function updatePageData() {{
    updateHeaderInfo();
    updateBreakingNews();
    updateSectorPerformance();
    updateGrowthPotential();
    updateTradingStrategy();
}}

function updateHeaderInfo() {{
    document.getElementById('market-status').textContent = "🔔 Markets Closed for Weekend";
    document.getElementById('next-trading-day').textContent = `📅 Next Trading Session: ${{nextTradingDay}} at 9:15 AM IST`;
    document.getElementById('last-updated').textContent = `🕒 Last Updated: ${{lastUpdated}}`;
    document.getElementById('footer-update').textContent = `🕒 Last Updated: ${{lastUpdated}}`;
}}

function updateBreakingNews() {{
    const container = document.getElementById('breaking-news-container');
    let newsHtml = '';
    liveFinancialNews.slice(0, 5).forEach(news => {{
        newsHtml += `
            <div class="breaking-news-item">
                <h3>${{news.title}}</h3>
                <p>${{news.source}} • <a href="${{news.url}}" target="_blank">Read Full Article</a></p>
            </div>
        `;
    }});
    container.innerHTML = newsHtml || '<div>No breaking news available.</div>';
}}

function updateSectorPerformance() {{
    const grid = document.getElementById('performance-grid');
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
    let html = '';
    sectorData.forEach(sector => {{
        const potentialClass = sector.percent_change > 1 ? 'high-potential' :
                              sector.percent_change < -1 ? 'high-risk' : 'medium-potential';
        const sign = sector.percent_change > 0 ? '+' : '';
        const reason = sector.percent_change > 1 ? 'Momentum likely to continue' :
                      sector.percent_change < -1 ? 'Risk of further decline' : 'Mixed outlook';
        
        html += `
            <div class="potential-item ${{potentialClass}}">
                <span class="sector-name">${{sector.name}}</span>
                <span class="potential-change">${{sign}}${{sector.percent_change.toFixed(2)}}%</span>
                <span class="potential-reason">${{reason}}</span>
            </div>
        `;
    }});
    grid.innerHTML = html;
}}

function updateTradingStrategy() {{
    const updates = [
        ['buy-strategy-list', strategyData.buy, 'Strong momentum, potential for further gains'],
        ['sell-strategy-list', strategyData.sell, 'Showing weakness, consider avoiding or booking profits'],
        ['hold-strategy-list', strategyData.hold, 'Range-bound, wait for clear directional signals']
    ];
    
    updates.forEach(([listId, sectors, description]) => {{
        const list = document.getElementById(listId);
        if (list) {{
            let html = '';
            if (sectors.length > 0) {{
                sectors.forEach(sector => {{
                    html += `<li><strong>${{sector}}</strong>: ${{description}}</li>`;
                }});
            }} else {{
                html = '<li>No clear signals in current market conditions</li>';
            }}
            list.innerHTML = html;
        }}
    }});
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
    console.log("🚀 Initializing website...");
    updatePageData();
    
    // Update breaking news every 3 minutes
    setInterval(updateBreakingNews, 180000);
    
    console.log("✅ Website fully loaded!");
}});
'''

    with open('nse_data_updater.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print("✅ Generated nse_data_updater.js with reliable data")

def main():
    print("🚀 Starting Working NSE Data Generator")
    print("=" * 50)
    
    # Get working data
    sectors = get_working_sector_data()
    news = get_working_news()
    next_trading = get_next_trading_day()
    strategy = create_trading_strategy(sectors)
    
    # Generate JS
    generate_working_js(sectors, news, strategy, next_trading)
    
    print("\n" + "=" * 50)
    print("✅ SUCCESS - Your website will now work!")
    print(f"📊 Sectors: {len(sectors)}")
    print(f"📰 News: {len(news)}")
    print(f"📅 Next trading: {next_trading}")
    print("=" * 50)

if __name__ == "__main__":
    main()
