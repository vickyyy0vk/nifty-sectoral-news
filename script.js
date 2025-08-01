// Sample news data (you'll replace this with real API calls)
const sampleNews = {
    IT: [
        {
            title: "India's IT Sector Shows Strong Growth in Q3",
            summary: "Major IT companies report robust earnings with cloud services driving growth",
            source: "Economic Times",
            time: "2 hours ago"
        },
        {
            title: "AI Adoption Boosts Indian Software Exports",
            summary: "Artificial intelligence integration increases demand for Indian IT services",
            source: "Business Today",
            time: "4 hours ago"
        }
    ],
    Banking: [
        {
            title: "Banking Sector Credit Growth Accelerates",
            summary: "Private banks lead credit expansion with improved asset quality",
            source: "Financial Express",
            time: "1 hour ago"
        },
        {
            title: "Digital Banking Revolution Continues",
            summary: "UPI transactions reach new highs, boosting fintech partnerships",
            source: "Moneycontrol",
            time: "3 hours ago"
        }
    ],
    Auto: [
        {
            title: "Electric Vehicle Sales Surge in India",
            summary: "EV adoption accelerates with government incentives and charging infrastructure",
            source: "Business Standard",
            time: "30 minutes ago"
        },
        {
            title: "Auto Industry Recovery Gains Momentum",
            summary: "Passenger vehicle sales show strong year-over-year growth",
            source: "Economic Times",
            time: "5 hours ago"
        }
    ],
    Healthcare: [
        {
            title: "Healthcare Sector Investment Rises",
            summary: "Private equity funding in health-tech startups reaches record levels",
            source: "NDTV Profit",
            time: "1.5 hours ago"
        },
        {
            title: "Pharmaceutical Exports Show Strong Growth",
            summary: "Indian pharma companies expand global market presence",
            source: "Business Today",
            time: "6 hours ago"
        }
    ],
    Pharma: [
        {
            title: "New Drug Approvals Boost Pharma Sector",
            summary: "CDSCO approvals for innovative medicines drive sector optimism",
            source: "Financial Express",
            time: "45 minutes ago"
        }
    ]
};

// Function to display all news
function showAllNews() {
    const container = document.getElementById('news-container');
    let allNews = '';
    
    // Remove active class from all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Combine all sector news
    Object.keys(sampleNews).forEach(sector => {
        sampleNews[sector].forEach(news => {
            allNews += createNewsItem(news, sector);
        });
    });
    
    container.innerHTML = allNews || '<div class="loading">No news available</div>';
}

// Function to show sector-specific news
function showSectorNews(sector) {
    const container = document.getElementById('news-container');
    
    // Remove active class from all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    if (sampleNews[sector]) {
        let newsHTML = '';
        sampleNews[sector].forEach(news => {
            newsHTML += createNewsItem(news, sector);
        });
        container.innerHTML = newsHTML;
    } else {
        container.innerHTML = `<div class="loading">No news available for ${sector} sector</div>`;
    }
}

// Function to create news item HTML
function createNewsItem(news, sector) {
    return `
        <div class="news-item">
            <h3>${news.title}</h3>
            <p>${news.summary}</p>
            <div class="news-meta">
                <strong>Source:</strong> ${news.source} | 
                <strong>Sector:</strong> ${sector} | 
                <strong>Time:</strong> ${news.time}
            </div>
        </div>
    `;
}

// Function to fetch real news (placeholder for future API integration)
async function fetchRealNews() {
    // This is where you'll add real news API calls
    // For now, we're using sample data
    console.log('Fetching real news... (placeholder)');
}

// Load news when page loads
document.addEventListener('DOMContentLoaded', function() {
    showAllNews();
    
    // Auto-refresh news every 30 minutes
    setInterval(fetchRealNews, 30 * 60 * 1000);
});

// Add smooth scrolling for better UX
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function() {
        // Add click animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
});
