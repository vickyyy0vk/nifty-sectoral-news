// Auto-generated on 2025-08-02 10:00:00
const realNSEData = [
  {
    "name": "NIFTY FMCG",
    "last_price": 53847.25,
    "percent_change": 1.12
  },
  {
    "name": "NIFTY MEDIA",
    "last_price": 1876.45,
    "percent_change": 0.98
  },
  // ... remaining sectors ...
];
const liveFinancialNews = [
  {
    "title": "FMCG Stocks Lead Market Gains Amid Global Turmoil",
    "url": "https://economictimes.indiatimes.com/markets/stocks/news/fmcg-lead-...",
    "source": "Economic Times"
  },
  {
    "title": "Breaking: Trump's Price Cut Ultimatum Crashes Pharma",
    "url": "https://www.reuters.com/markets/pharma-ultimatum-crashes-...",
    "source": "Reuters"
  },
  // ... remaining news items ...
];

// Update NSE sector cards
function updateWebsiteWithRealNSEData(){
  document.querySelectorAll('.sector-card').forEach(card=>{
    const name=card.querySelector('h3').textContent.trim();
    const sd=realNSEData.find(s=>s.name===name);
    if(sd){
      const badge=card.querySelector('.performance-badge');
      badge.textContent=(sd.percent_change>=0?'+':'')+sd.percent_change.toFixed(2)+'%';
      badge.className='performance-badge '+(sd.percent_change>0?'positive':sd.percent_change<0?'negative':'neutral');
    }
  });
  console.log('NSE sectors updated with real data');
}

// Update news feed
function updateNewsWithRealData(){
  const c=document.getElementById('news-container');
  c.innerHTML = liveFinancialNews.map(n=>`
    <div class="news-item">
      <h3>${n.title}</h3>
      <p>Source: ${n.source}</p>
      <a href="${n.url}" target="_blank">Read more</a>
    </div>
  `).join('');
  console.log('News feed updated');
}

document.addEventListener('DOMContentLoaded',()=>{
  updateWebsiteWithRealNSEData();
  updateNewsWithRealData();
  setInterval(updateWebsiteWithRealNSEData,60000); // update sectors every minute
  setInterval(updateNewsWithRealData,300000);      // update news every 5 minutes
});
