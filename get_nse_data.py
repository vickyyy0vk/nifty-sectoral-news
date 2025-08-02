import requests, json, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

HEADERS = {'User-Agent':'Mozilla/5.0'}
SECTORS = [
    'NIFTY FMCG','NIFTY PHARMA','NIFTY IT','NIFTY BANK','NIFTY AUTO',
    'NIFTY MEDIA','NIFTY METAL','NIFTY REALTY','NIFTY ENERGY','NIFTY PSU BANK',
    'NIFTY PRIVATE BANK','NIFTY FINANCIAL SERVICES','NIFTY HEALTHCARE INDEX','NIFTY CONSUMER DURABLES'
]

def create_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get('https://www.nseindia.com', timeout=5)
    time.sleep(1)
    return s

def fetch_sectors(s):
    data = s.get('https://www.nseindia.com/api/allIndices',timeout=10).json()['data']
    return [dict(name=x['index'],last_price=float(x['last']),percent_change=float(x['pChange'])) for x in data if x['index'] in SECTORS]

def fetch_news():
    soup = BeautifulSoup(requests.get("https://www.businesstoday.in/latest/economy",headers=HEADERS).text,"html.parser")
    bt = [{'title':a.get_text(strip=True),'url':"https://www.businesstoday.in"+a['href'],'source':'Business Today'} for a in soup.select("ul.listingNews li a")]
    soup2 = BeautifulSoup(requests.get("https://www.moneycontrol.com/news/business/markets/",headers=HEADERS).text,"html.parser")
    mc = [{'title':a.get_text(strip=True),'url':a['href'],'source':'MoneyControl'} for div in soup2.select("div.listingnews_block article") if (a:=div.find("a", href=True))]
    te = requests.get("https://api.tradingeconomics.com/news/country/india?c=guest:guest",timeout=6).json()
    te = [{'title':i.get('title'),'url':i.get('url'),'source':i.get('source')} for i in te][:10]
    return bt+mc+te

def next_trading_day():
    now=datetime.now()
    w=now.weekday()
    days = 3 if w==4 else 2 if w==5 else 1
    nxt=now+timedelta(days=days)
    return nxt.strftime("%A, %B %d, %Y")

def make_strategy(sectors):
    sorted_secs = sorted(sectors,key=lambda x:x['percent_change'],reverse=True)
    buy    = [sorted_secs[0]['name']]
    avoid  = [sorted_secs[-1]['name']]
    hold   = [s['name'] for s in sectors if -0.5<s['percent_change']<0.5]
    return {'buy':buy,'sell':avoid,'hold':hold}

def make_js(sectors,news,strategy,nextstr,last_updated):
    js = f"""\
// Auto-generated at {last_updated}
const sectorData = {json.dumps(sectors)};
const liveFinancialNews = {json.dumps(news)};
const strategyData = {json.dumps(strategy)};
const nextStr = "{nextstr}";
const lastUpdated = "{last_updated}";

function updateTodayPerformance() {{
  let grid = '';
  sectorData.forEach(s => {{
    grid += `<div class="sector-performance-item ${(s.percent_change>0.2?'gainer':s.percent_change<-0.2?'decliner':'neutral')}">
      <span class="sector-name">${{s.name}}</span>
      <span class="today-change ${(s.percent_change>0.2?'positive':s.percent_change<-0.2?'negative':'neutral')}">${{s.percent_change>0?'+':''}}${{s.percent_change.toFixed(2)}}%</span>
    </div>`;
  }});
  document.querySelector('.performance-grid').innerHTML = grid;
}}
function fetchBreakingNews() {{
  const news = liveFinancialNews.slice(0, 5);
  const container = document.getElementById('breaking-news-container');
  let html = '';
  news.forEach(item => {{
    html += `<div class="breaking-news-item">
      <h3>${{item.title}}</h3>
      <p>${{item.source||''}} &bull; <a href='${{item.url}}' target='_blank'>Read Full Article</a></p>
    </div>`;
  }});
  container.innerHTML = html || '<div>No breaking news available.</div>';
}}
function updatePotential() {{
  let grid = '';
  sectorData.slice(0,2).forEach(s => {{
    grid += `<div class="potential-item high-potential">
      <span class="sector-name">${{s.name}}</span>
      <span class="potential-change">${{s.percent_change>0?'+':''}}${{s.percent_change.toFixed(2)}}%</span>
      <span class="potential-reason">Momentum likely to continue</span>
    </div>`;
  }});
  sectorData.slice(-2).forEach(s=>{
    grid += `<div class="potential-item high-risk">
      <span class="sector-name">${{s.name}}</span>
      <span class="potential-change">${{s.percent_change>0?'+':''}}${{s.percent_change.toFixed(2)}}%</span>
      <span class="potential-reason">Caution: Downside risk</span>
    </div>`;
  });
  document.querySelector('.potential-grid').innerHTML = grid;
}}
function updateStrategy() {{
  document.querySelector('.strategy-card.buy-strategy ul').innerHTML =
    strategyData.buy.map(s=>`<li><strong>${{s}}</strong>: Fresh buy signal</li>`).join('');
  document.querySelector('.strategy-card.sell-strategy ul').innerHTML =
    strategyData.sell.map(s=>`<li><strong>${{s}}</strong>: Caution zone</li>`).join('');
  document.querySelector('.strategy-card.hold-strategy ul').innerHTML =
    strategyData.hold.map(s=>`<li><strong>${{s}}</strong>: Rangebound</li>`).join('');
}}
document.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('market-status').textContent = "🔔 Markets Closed for Weekend";
  document.getElementById('next-trading-day').textContent = `Next Trading Session: ${nextStr} at 9:15 AM IST`;
  document.getElementById('last-updated').textContent = "🕒 Last Updated: " + lastUpdated;
  document.getElementById('footer-update').textContent = "🕒 Last Updated: " + lastUpdated;
  updateTodayPerformance();
  updatePotential();
  updateStrategy();
  fetchBreakingNews();
  setInterval(fetchBreakingNews, 180000);
}});
"""
    with open('nse_data_updater.js','w') as f: f.write(js)
    print("🟢 JS updated")

def main():
    s = create_session()
    secs = fetch_sectors(s)
    news = fetch_news()
    ntstr = next_trading_day()
    last_updated = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
    strat = make_strategy(secs)
    make_js(secs, news, strat, ntstr, last_updated)

if __name__=="__main__":
    main()
