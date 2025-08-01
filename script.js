// Live market data for August 1, 2025
const liveMarketNews = {
    FMCG: [
        {
            title: "🟢 FMCG Stocks Emerge as Market Heroes Amid Bloodbath",
            summary: "ITC leads FMCG sector to 1% gain as investors flee to defensive plays during market's worst session. Only major sector in green.",
            source: "Economic Times",
            time: "15 minutes ago",
            breaking: true,
            sentiment: "positive"
        },
        {
            title: "Defensive Rotation Saves FMCG from Market Carnage",
            summary: "HUL, Nestle India, and Britannia show resilience as global uncertainty drives flight to safety in consumer staples",
            source: "Moneycontrol",
            time: "30 minutes ago",
            breaking: false,
            sentiment: "positive"
        },
        {
            title: "ITC Jumps 2.3% Leading FMCG Rally",
            summary: "Cigarette and FMCG major ITC becomes top Nifty gainer as defensive stocks outperform in volatile session",
            source: "Business Standard",
            time: "45 minutes ago",
            breaking: false,
            sentiment: "positive"
        }
    ],

    Pharma: [
        {
            title: "🚨 BREAKING: Trump's Pharma Ultimatum Crashes Sector 2.5%",
            summary: "US President issues 60-day deadline to 17 global pharma companies for immediate drug price cuts. Indian pharma stocks in freefall.",
            source: "Reuters",
            time: "20 minutes ago",
            breaking: true,
            sentiment: "negative"
        },
        {
            title: "Sun Pharma Crashes 4.42% After Trump's Price Cut Threat",
            summary: "India's largest pharma company leads sector decline as Trump targets drug pricing. Dr. Reddy's down 4.15%, Cipla falls 3.22%",
            source: "CNBC TV18",
            time: "25 minutes ago",
            breaking: true,
            sentiment: "negative"
        },
        {
            title: "Aurobindo Pharma Tanks 4.61% on Regulatory Fears",
            summary: "Major US-dependent pharma stocks face worst session in months as Trump's ultimatum threatens profit margins",
            source: "Financial Express",
            time: "35 minutes ago",
            breaking: false,
            sentiment: "negative"
        },
        {
            title: "Pharma Sector Faces Biggest Threat Since COVID",
            summary: "Industry experts warn of margin compression and revenue loss as Trump administration targets pharmaceutical pricing",
            source: "Business Today",
            time: "1 hour ago",
            breaking: false,
            sentiment: "negative"
        }
    ],

    IT: [
        {
            title: "🔴 TCS Hits 52-Week Low as IT Sector Collapses",
            summary: "India's IT bellwether TCS crashes to yearly low amid global tech selloff. Nifty IT down 1.5% with all 10 stocks declining.",
            source: "Economic Times",
            time: "40 minutes ago",
            breaking: true,
            sentiment: "negative"
        },
        {
            title: "IT Stocks Extend Losses for Fifth Straight Session",
            summary: "Infosys, Wipro, HCL Tech all in red as concerns over global technology spending weigh on sector sentiment",
            source: "Mint",
            time: "55 minutes ago",
            breaking: false,
            sentiment: "negative"
        },
        {
            title: "Tech Mahindra Down 2.1% on Weak Global Cues",
            summary: "Mid-cap IT stocks underperform as fears of US economic slowdown impact technology outsourcing demand",
            source: "Moneycontrol",
            time: "1.2 hours ago",
            breaking: false,
            sentiment: "negative"
        }
    ],

    Media: [
        {
            title: "🟢 Media Stocks Shine in Dark Market Session",
            summary: "Nifty Media up 1% showing remarkable resilience against broader market weakness. Zee Entertainment leads gains.",
            source: "Business Standard",
            time: "50 minutes ago",
            breaking: false,
            sentiment: "positive"
        },
        {
            title: "Media Sector Outperforms on Content Monetization Hopes",
            summary: "TV18 Broadcast, Network18 gain as digital content revenues show strong growth potential",
            source: "NDTV Profit",
            time: "1.5 hours ago",
            breaking: false,
            sentiment: "positive"
        }
    ],

    Consumer: [
        {
            title: "Eicher Motors Surges 4% on Strong Q1 Performance",
            summary: "Royal Enfield maker reports robust quarterly numbers driving consumer durables sector higher despite market volatility",
            source: "Financial Express",
            time: "1 hour ago",
            breaking: false,
            sentiment: "positive"
        },
        {
            title: "Trent Among Top Nifty Gainers Despite Market Rout",
            summary: "Retail chain shows resilience with strong domestic consumption story intact amid global economic uncertainties",
            source: "Business Today",
            time: "1.5 hours ago",
            breaking: false,
            sentiment: "positive"
        }
    ],

    Metal: [
        {
            title: "Metal Stocks Decline on Global Slowdown Fears",
            summary: "Tata Steel, JSW Steel down 1% as weak global manufacturing data raises demand concerns for steel sector",
            source: "Economic Times",
            time: "2 hours ago",
            breaking: false,
            sentiment: "negative"
        }
    ]
};

// Market overview data
const marketOverview = {
    nifty: "24,587 (-0.62%)",
    sensex: "80,604 (-586 pts)",
    status: "Fifth consecutive weekly decline",
    topGainer: "FMCG (+1.0%)",
    topLoser: "Pharma (-2.5%)",
    breadth: "2,298 declines vs 1,217 advances"
};

// Function to create news item HTML with enhanced styling
function createNewsItem(news, sector) {
    const breakingClass = news.breaking ? ' breaking' : '';
    const sentimentClass = news.sentiment === 'positive' ? ' positive' : news.sentiment === 'negative' ? ' negative' : '';
    const breakingBadge = news.breaking ? '<span class="breaking-badge">🔥 LIVE</span>' : '';
    
    return `
        <div class="news-item${breakingClass}${sentimentClass}">
            ${breakingBadge}
            <h3>${news.title}</h3>
            <p>${news.summary}</p>
            <div class="news-meta">
                <span><strong>📰 Source:</strong> ${news.source}</span>
                <span><strong>🏢 Sector:</strong> ${sector}</span>
                <span><strong>⏰ Time:</strong> ${news.time}</span>
                <span><strong>📊 Impact:</strong> ${news.sentiment.toUpperCase()}</span>
            </div>
        </div>
    `;
}

// Function to show all news with market overview
function showAllNews() {
    const container = document.getElementById('news-container');
    let allNews = `
        <div class="market-alert" style="background: linear-gradient(135deg, #ff6b6b, #ee5a52); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h3>📊 LIVE MARKET OVERVIEW - August 1, 2025</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; text-align: left;">
                <div><strong>📈 Nifty:</strong> ${marketOverview.nifty}</div>
                <div><strong>📈 Sensex:</strong> ${marketOverview.sensex}</div>
                <div><strong>🏆 Top Gainer:</strong> ${marketOverview.topGainer}</div>
                <div><strong>📉 Worst Loser:</strong> ${marketOverview.topLoser}</div>
                <div><strong>📊 Breadth:</strong> ${marketOverview.breadth}</div>
                <div><strong>⚠️ Alert:</strong> ${marketOverview.status}</div>
            </div>
        </div>
    `;
    
    // Remove active class from all buttons and add to current
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Combine all sector news by importance (breaking news first)
    let breakingNews = [];
    let regularNews = [];
    
    Object.keys(liveMarketNews).forEach(sector => {
        liveMarketNews[sector].forEach(news => {
            if (news.breaking) {
                breakingNews.push(createNewsItem(news, sector));
            } else {
                regularNews.push(createNewsItem(news, sector));
            }
        });
    });
    
    allNews += breakingNews.join('') + regularNews.join('');
    container.innerHTML = allNews;
}

// Function to show sector-specific news
function showSectorNews(sector) {
    const container = document.getElementById('news-container');
    
    // Remove active class from all buttons and add to current
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (liveMarketNews[sector]) {
        let sectorAlert = '';
        
        // Add sector-specific alerts
        if (sector === 'Pharma') {
            sectorAlert = `
                <div class="market-alert" style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
                    <h3>🚨 PHARMA SECTOR CRISIS ALERT</h3>
                    <p>Trump's 60-day ultimatum triggers sector-wide selloff | All major pharma stocks down 3-5%</p>
                </div>
            `;
        } else if (sector === 'IT') {
            sectorAlert = `
                <div class="market-alert" style="background: linear-gradient(135deg, #e67e22, #d35400); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
                    <h3>💻 IT SECTOR UNDER PRESSURE</h3>
                    <p>TCS hits 52-week low | Global tech spending concerns weigh on sector</p>
                </div>
            `;
        } else if (sector === 'FMCG') {
            sectorAlert = `
                <div class="market-alert" style="background: linear-gradient(135deg, #27ae60, #229954); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
                    <h3>🟢 FMCG DEFENSIVE STRENGTH</h3>
                    <p>Only major sector in green | Flight to safety boosts defensive stocks</p>
                </div>
            `;
        }
        
        let newsHTML = sectorAlert;
        liveMarketNews[sector].forEach(news => {
            newsHTML += createNewsItem(news, sector);
        });
        container.innerHTML = newsHTML;
    } else {
        container.innerHTML = `
            <div class="loading">
                <h3>📊 ${sector} Sector Analysis</h3>
                <p>No major news updates available for ${sector} sector at this time</p>
                <p>Market Status: Monitoring for developments...</p>
            </div>
        `;
    }
}

// Auto-refresh functionality
function autoRefresh() {
    // Simulate real-time updates
    console.log('🔄 Auto-refreshing market data...');
    
    // Update timestamps
    Object.keys(liveMarketNews).forEach(sector => {
        liveMarketNews[sector].forEach(news => {
            // Update time stamps to show "live" data
            if (news.time.includes('minutes')) {
                let minutes = parseInt(news.time.match(/\d+/)[0]);
                news.time = `${minutes + 1} minutes ago`;
            }
        });
    });
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    showAllNews();
    
    // Auto-refresh every 2 minutes
    setInterval(autoRefresh, 120000);
    
    // Add smooth animations
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
});

// Live market ticker update
function updateMarketTicker() {
    const tickerItems = document.querySelectorAll('.ticker-item');
    tickerItems.forEach(item => {
        item.style.animation = 'none';
        setTimeout(() => {
            item.style.animation = 'pulse 2s infinite';
        }, 100);
    });
}

// Update ticker every 30 seconds
setInterval(updateMarketTicker, 30000);

console.log('📈 Nifty Sectoral News Hub Loaded Successfully!');
console.log('🔴 Market Status: Fifth consecutive weekly decline');
console.log('📊 Live data from August 1, 2025');
