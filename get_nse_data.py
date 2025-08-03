import requests
import json
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Fallback data when NSE scraping is blocked
def get_working_sector_data():
    return [
        {'name': 'NIFTY FMCG', 'percent_change': 0.69, 'status': 'Defensive Strength'},
        {'name': 'NIFTY PHARMA', 'percent_change': -3.33, 'status': 'Trump Pricing Pressure'},
        {'name': 'NIFTY IT', 'percent_change': -1.53, 'status': 'Global Tech Slowdown'},
        {'name': 'NIFTY BANK', 'percent_change': -0.62, 'status': 'RBI Speech Awaited'},
        {'name': 'NIFTY AUTO', 'percent_change': -0.85, 'status': 'EV Policy Ahead'},
        {'name': 'NIFTY METAL', 'percent_change': -1.12, 'status': 'Commodity Weakness'},
        {'name': 'NIFTY REALTY', 'percent_change': -1.98, 'status': 'Interest Rate Pressure'},
        {'name': 'NIFTY ENERGY', 'percent_change': -1.18, 'status': 'Oil Demand Concerns'},
        {'name': 'NIFTY PSU BANK', 'percent_change': -1.45, 'status': 'Government Bank Stress'},
        {'name': 'NIFTY PRIVATE BANK', 'percent_change': -0.78, 'status': 'Credit Growth Slow'},
        {'name': 'NIFTY MEDIA', 'percent_change': 0.98, 'status': 'Content Monetization'},
        {'name': 'NIFTY CONSUMER DURABLES', 'percent_change': 0.47, 'status': 'Mixed Demand'},
        {'name': 'NIFTY FINANCIAL SERVICES', 'percent_change': -0.05, 'status': 'Flat Performance'},
        {'name': 'NIFTY HEALTHCARE INDEX', 'percent_change': 0.23, 'status': 'Stable Demand'}
    ]

def get_working_news():
    return [
        {'title': 'FMCG Leads Market Rally Amid Volatility', 'url': 'https://economictimes.indiatimes.com/markets', 'source': 'Economic Times'},
        {'title': 'Pharma Stocks Slide on US Policy Fears', 'url': 'https://www.businesstoday.in/markets', 'source': 'Business Today'},
        {'title': 'IT Stocks Weigh on Index as Global Tech Falters', 'url': 'https://www.moneycontrol.com/news', 'source': 'MoneyControl'},
        {'title': 'Banks Recover Slightly After RBI Comment', 'url': 'https://economictimes.indiatimes.com/banking', 'source': 'Economic Times'},
        {'title': 'Auto Sector Eyes EV Incentives for Growth', 'url': 'https://www.moneycontrol.com/auto', 'source': 'MoneyControl'},
        {'title': 'Metal Stocks Await China Demand Recovery', 'url': 'https://www.businesstoday.in/markets', 'source': 'Business Today'},
        {'title': 'Realty Faces Funding Headwinds Amid Rate Hikes', 'url': 'https://economictimes.indiatimes.com/realty', 'source': 'Economic Times'},
        {'title': 'Media Stocks Bounce on Advertising Uptick', 'url': 'https://www.moneycontrol.com/media', 'source': 'MoneyControl'}
    ]

def get_next_trading_day():
    now = datetime.now()
    w = now.weekday()
    days = 3 if w == 4 else 2 if w == 5 else 1
    nxt = now + timedelta(days=days)
    return nxt.strftime("%A, %B %d, %Y")

def create_trading_strategy(sectors):
    sorted_secs = sorted(sectors, key=lambda x: x['percent_change'], reverse=True)
    buy = [s['name'] for s in sorted_secs[:2] if s['percent_change'] > -1.0]
    sell = [s['name'] for s in sorted_secs[-2:] if s['percent_change'] < -1.0]
    hold = [s['name'] for s in sectors if -0.5 <= s['percent_change'] <= 0.5]
    return {'buy': buy, 'sell': sell, 'hold': hold}

def generate_js_updater(sectors, news, strategy, next_day):
    timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    js = f"""// Auto-generated at {timestamp}
const sectorData = {json.dumps(sectors, indent=2)};
const liveFinancialNews = {json.dumps(news, indent=2)};
const strategyData = {json.dumps(strategy, indent=2)};
const nextTradingDay = "{next_day}";
const lastUpdated = "{timestamp}";

function updatePage() {{
  // Header
  document.getElementById('market-status').textContent = "🔔 Markets Closed for Weekend";
  document.getElementById('next-trading-day').textContent = `📅 Next Trading Session: ${{nextTradingDay}} at 9:15 AM IST`;
  document.getElementById('last-updated').textContent = `🕒 Last Updated: ${{lastUpdated}}`;
  document.getElementById('footer-update').textContent = `🕒 Last Updated: ${{lastUpdated}}`;

  // Breaking News
  const bn = document.getElementById('breaking-news-container');
  bn.innerHTML = sectorData && liveFinancialNews.length
    ? liveFinancialNews.slice(0,5).map(n=>`
      <div class="breaking-news-item">
        <h3>${{n.title}}</h3>
        <p>${{n.source}} • <a href="${{n.url}}" target="_blank">Read Full Article</a></p>
      </div>`).join('')
    : '<div class="loading">No breaking news available.</div>';

  // Performance
  const pg = document.getElementById('performance-grid');
  pg.innerHTML = sectorData.length
    ? sectorData.map(s=>`
      <div class="sector-performance-item ${s.percent_change>0.2?'gainer':s.percent_change<-0.2?'decliner':'neutral'}">
        <span class="sector-name">${s.name}</span>
        <span class="today-change ${s.percent_change>0?'positive':s.percent_change<0?'negative':'neutral'}">
          ${s.percent_change>0?'+':''}${s.percent_change.toFixed(2)}%
        </span>
        <span class="sector-status">${s.status}</span>
      </div>`).join('')
    : '<div class="loading">Unable to load performance data.</div>';

  // Growth Potential
  const pot = document.getElementById('potential-grid');
  pot.innerHTML = sectorData.length
    ? sectorData.map(s=>`
      <div class="potential-item ${s.percent_change>1?'high-potential':s.percent_change<-1?'high-risk':'medium-potential'}">
        <span class="sector-name">${s.name}</span>
        <span class="potential-change">${s.percent_change>0?'+':''}${s.percent_change.toFixed(2)}%</span>
        <span class="potential-reason">${
          s.percent_change>1?'Momentum likely to continue':
          s.percent_change<-1?'Risk of further decline':'Mixed signals'}
        </span>
      </div>`).join('')
    : '<div class="loading">Unable to analyze growth potential.</div>';

  // Strategy
  const [buyEl, sellEl, holdEl] = [
    'buy-strategy-list','sell-strategy-list','hold-strategy-list'
  ].map(id=>document.getElementById(id));
  if(strategyData.buy.length){
    buyEl.innerHTML = strategyData.buy.map(s=>`<li><strong>${s}</strong>: Strong momentum</li>`).join('');
  } else { buyEl.innerHTML = '<li>No buy signals.</li>'; }
  if(strategyData.sell.length){
    sellEl.innerHTML = strategyData.sell.map(s=>`<li><strong>${s}</strong>: Consider avoiding</li>`).join('');
  } else { sellEl.innerHTML = '<li>No sell signals.</li>'; }
  if(strategyData.hold.length){
    holdEl.innerHTML = strategyData.hold.map(s=>`<li><strong>${s}</strong>: Hold and monitor</li>`).join('');
  } else { holdEl.innerHTML = '<li>No hold signals.</li>'; }
}}

document.addEventListener('DOMContentLoaded', ()=>{ updatePage(); setInterval(updatePage,180000); });
"""
    with open('nse_data_updater.js','w',encoding='utf-8') as f: f.write(js)
    print("✅ nse_data_updater.js generated")

def main():
    # Assemble data
    sectors = get_working_sector_data()
    news = get_working_news()
    next_day = get_next_trading_day()
    strategy = create_trading_strategy(sectors)
    # Generate JS
    generate_js_updater(sectors, news, strategy, next_day)

if __name__=="__main__":
    main()
