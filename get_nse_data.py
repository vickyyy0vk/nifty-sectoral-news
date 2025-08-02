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
    s.headers.update(HEADERS)
    s.get('https://www.nseindia.com', timeout=5)
    time.sleep(1)
    return s

def fetch_sector_data(session: requests.Session) -> List[Dict]:
    results = []
    for name, url in SECTORS.items():
        try:
            r = session.get(url, timeout=5)
            data = r.json().get('data', [])[0]
            pct = float(data.get('pChange', 0))
            results.append({
                'name': name,
                'last_price': float(data.get('last', 0)),
                'percent_change': pct
            })
        except:
            continue
        time.sleep(1)
    return results

# News scrapers
def fetch_business_today_economy() -> List[Dict]:
    url="https://www.businesstoday.in/latest/economy"
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=5)
    soup=BeautifulSoup(r.text,"html.parser")
    arts=[]
    for a in soup.select("ul.listingNews li a"):
        t=a.get_text(strip=True)
        link=a["href"]
        if not link.startswith("http"):
            link="https://www.businesstoday.in"+link
        arts.append({'title':t,'url':link})
    return arts

def fetch_moneycontrol_market_news() -> List[Dict]:
    url="https://www.moneycontrol.com/news/business/markets/"
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=5)
    soup=BeautifulSoup(r.text,"html.parser")
    arts=[]
    for div in soup.select("div.listingnews_block article"):
        a=div.find("a",href=True)
        arts.append({'title':a.get_text(strip=True),'url':a['href']})
    return arts

def fetch_tradingeconomics_india_news() -> List[Dict]:
    url="https://api.tradingeconomics.com/news/country/india?c=guest:guest"
    r=requests.get(url,timeout=5)
    items=r.json()
    return [{'title':i.get('title'),'url':i.get('url'),'source':i.get('source')} for i in items]

def generate_js(sector_data, news_data):
    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    js=f"""// Auto-generated on {now}
const realNSEData = {json.dumps(sector_data,indent=2)};
const liveFinancialNews = {json.dumps(news_data,indent=2)};

// Update sectors
function updateWebsiteWithRealNSEData(){{
  document.querySelectorAll('.sector-card').forEach(card=>{{
    const name=card.querySelector('h3').textContent.trim();
    const sd=realNSEData.find(s=>s.name===name);
    if(sd){{
      const badge=card.querySelector('.performance-badge');
      badge.textContent=(sd.percent_change>=0?'+':'')+sd.percent_change.toFixed(2)+'%';
      badge.className='performance-badge '+(sd.percent_change>0?'positive':sd.percent_change<0?'negative':'neutral');
    }}
  }});
  console.log('NSE sectors updated');
}}

// Update news
function updateNewsWithRealData(){{
  const c=document.getElementById('news-container');
  c.innerHTML = liveFinancialNews.map(n=>`
    <div class="news-item">
      <h3>${{n.title}}</h3>
      <p>Source: ${{n.source||'Unknown'}}</p>
      <a href="${{n.url}}" target="_blank">Read more</a>
    </div>
  `).join('');
  console.log('News updated');
}}

document.addEventListener('DOMContentLoaded',()=>{
  updateWebsiteWithRealNSEData();
  updateNewsWithRealData();
  setInterval(updateWebsiteWithRealNSEData,60000);
  setInterval(updateNewsWithRealData,300000);
});
"""
    with open('nse_data_updater.js','w') as f: f.write(js)

def main():
    sess=create_session()
    sectors=fetch_sector_data(sess)
    news = fetch_business_today_economy()+fetch_moneycontrol_market_news()+fetch_tradingeconomics_india_news()
    generate_js(sectors,news)
    print("✅ Generated nse_data_updater.js with live data")

if __name__=='__main__':
    main()
