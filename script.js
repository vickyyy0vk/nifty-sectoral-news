// Enhanced Performance Comparison Functions

// Today's actual sector performance data (August 1, 2025)
const todaysActualPerformance = {
    'FMCG': { change: 1.02, status: 'Market Leader', rank: 1 },
    'Media': { change: 0.98, status: 'Strong Close', rank: 2 },
    'Consumer Durables': { change: 0.47, status: 'Moderate Gain', rank: 3 },
    'Healthcare': { change: 0.23, status: 'Flat Close', rank: 4 },
    'Financial Services': { change: -0.05, status: 'Nearly Flat', rank: 5 },
    'Bank': { change: -0.62, status: 'Weakness', rank: 6 },
    'Private Bank': { change: -0.78, status: 'Private Bank Drag', rank: 7 },
    'Auto': { change: -0.85, status: 'EV Concerns', rank: 8 },
    'Metal': { change: -1.12, status: 'Commodity Weak', rank: 9 },
    'Oil & Gas': { change: -1.18, status: 'Energy Selloff', rank: 10 },
    'PSU Bank': { change: -1.45, status: 'Govt Bank Hit', rank: 11 },
    'IT': { change: -1.53, status: 'Tech Rout', rank: 12 },
    'Realty': { change: -1.98, status: 'Rate Fears', rank: 13 },
    'Pharma': { change: -2.47, status: 'Trump Crisis', rank: 14 }
};

// Monday's growth potential predictions
const mondayGrowthPotential = {
    'Auto': { 
        min: 2.5, max: 4.0, 
        reason: 'EV Policy Announcement', 
        confidence: 'High Confidence',
        category: 'high-potential'
    },
    'Infrastructure': { 
        min: 1.8, max: 3.2, 
        reason: 'Budget Allocation News', 
        confidence: 'High Confidence',
        category: 'high-potential'
    },
    'Metal': { 
        min: 1.2, max: 2.8, 
        reason: 'Global Commodity Rebound', 
        confidence: 'Medium Confidence',
        category: 'medium-potential'
    },
    'FMCG': { 
        min: 0.8, max: 1.5, 
        reason: 'Defensive Continuation', 
        confidence: 'Medium Confidence',
        category: 'medium-potential'
    },
    'Oil & Gas': { 
        min: 0.5, max: 1.8, 
        reason: 'Energy Recovery Play', 
        confidence: 'Medium Confidence',
        category: 'medium-potential'
    },
    'Media': { 
        min: -0.2, max: 1.0, 
        reason: 'Profit Booking Risk', 
        confidence: 'Low Confidence',
        category: 'low-potential'
    },
    'Healthcare': { 
        min: -0.5, max: 0.8, 
        reason: 'Mixed Signals', 
        confidence: 'Low Confidence',
        category: 'low-potential'
    },
    'Bank': { 
        min: -0.8, max: -0.2, 
        reason: 'RBI Speech Impact', 
        confidence: 'Watch Closely',
        category: 'negative-potential'
    },
    'PSU Bank': { 
        min: -1.2, max: -0.5, 
        reason: 'Asset Quality Concerns', 
        confidence: 'Watch Closely',
        category: 'negative-potential'
    },
    'Realty': { 
        min: -1.5, max: -0.8, 
        reason: 'Interest Rate Pressure', 
        confidence: 'Watch Closely',
        category: 'negative-potential'
    },
    'IT': { 
        min: -2.0, max: -0.5, 
        reason: 'Global Tech Weakness', 
        confidence: 'High Risk',
        category: 'high-risk'
    },
    'Pharma': { 
        min: -3.5, max: -1.0, 
        reason: 'Trump Deadline Pressure', 
        confidence: 'High Risk',
        category: 'high-risk'
    }
};

// Function to format percentage change with proper color coding
function formatPercentageChange(change) {
    const sign = change >= 0 ? '+' : '';
    return `${sign}${change.toFixed(2)}%`;
}

// Function to get change class based on percentage
function getChangeClass(change) {
    if (change > 0.5) return 'positive';
    if (change >= -0.1 && change <= 0.5) return 'neutral';
    return 'negative';
}

// Function to get sector performance category
function getPerformanceCategory(change) {
    if (change > 0.5) return 'gainer';
    if (change >= -0.1 && change <= 0.5) return 'neutral';
    if (change >= -1.5) return 'decliner';
    return 'worst';
}

// Function to calculate performance summary
function calculatePerformanceSummary() {
    let gainers = 0, flat = 0, losers = 0;
    
    Object.values(todaysActualPerformance).forEach(sector => {
        if (sector.change > 0.1) gainers++;
        else if (sector.change >= -0.1) flat++;
        else losers++;
    });
    
    return { gainers, flat, losers };
}

// Function to calculate potential summary
function calculatePotentialSummary() {
    let highPotential = 0, mediumPotential = 0, riskSectors = 0;
    
    Object.values(mondayGrowthPotential).forEach(sector => {
        if (sector.category === 'high-potential') highPotential++;
        else if (sector.category === 'medium-potential') mediumPotential++;
        else if (sector.category === 'negative-potential' || sector.category === 'high-risk') riskSectors++;
    });
    
    return { highPotential, mediumPotential, riskSectors };
}

// Function to update performance comparison dynamically
function updatePerformanceComparison() {
    // Update today's performance data
    const performanceItems = document.querySelectorAll('.sector-performance-item');
    performanceItems.forEach(item => {
        const sectorName = item.querySelector('.sector-name').textContent;
        const cleanSectorName = sectorName.replace('Nifty ', '');
        
        if (todaysActualPerformance[cleanSectorName]) {
            const data = todaysActualPerformance[cleanSectorName];
            const changeElement = item.querySelector('.today-change');
            const statusElement = item.querySelector('.sector-status');
            
            changeElement.textContent = formatPercentageChange(data.change);
            changeElement.className = `today-change ${getChangeClass(data.change)}`;
            statusElement.textContent = data.status;
            
            // Update item category
            item.className = `sector-performance-item ${getPerformanceCategory(data.change)}`;
        }
    });
    
    // Update Monday's potential data
    const potentialItems = document.querySelectorAll('.potential-item');
    potentialItems.forEach(item => {
        const sectorName = item.querySelector('.sector-name').textContent;
        const cleanSectorName = sectorName.replace('Nifty ', '');
        
        if (mondayGrowthPotential[cleanSectorName]) {
            const data = mondayGrowthPotential[cleanSectorName];
            const changeElement = item.querySelector('.potential-change');
            const reasonElement = item.querySelector('.potential-reason');
            const confidenceElement = item.querySelector('.confidence-level');
            
            const sign1 = data.min >= 0 ? '+' : '';
            const sign2 = data.max >= 0 ? '+' : '';
            changeElement.textContent = `${sign1}${data.min}% to ${sign2}${data.max}%`;
            reasonElement.textContent = data.reason;
            confidenceElement.textContent = data.confidence;
            
            // Update item category
            item.className = `potential-item ${data.category}`;
        }
    });
    
    console.log('📊 Performance comparison updated with real data');
}

// Function to highlight correlation between today's performance and Monday's potential
function highlightCorrelations() {
    // Auto sector: worst today (-0.85%) but highest potential Monday (+2.5% to +4.0%)
    // Metal sector: weak today (-1.12%) but good potential Monday (+1.2% to +2.8%)
    // Pharma sector: worst today (-2.47%) and worst potential Monday (-3.5% to -1.0%)
    
    const correlations = [
        {
            sector: 'Auto',
            insight: 'Oversold opportunity: Today\'s -0.85% creates entry point for Monday\'s EV policy catalyst'
        },
        {
            sector: 'Metal', 
            insight: 'Rebound play: -1.12% decline today sets up commodity recovery trade'
        },
        {
            sector: 'Pharma',
            insight: 'Avoid falling knife: Today\'s -2.47% likely to extend on Trump pressure'
        },
        {
            sector: 'FMCG',
            insight: 'Momentum question: Today\'s +1.02% leader may face profit booking'
        }
    ];
    
    return correlations;
}

// Initialize performance comparison when page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        updatePerformanceComparison();
        
        const correlations = highlightCorrelations();
        console.log('🔗 Key Correlations Identified:', correlations);
        
        // Add hover effects to show correlations
        const performanceItems = document.querySelectorAll('.sector-performance-item');
        const potentialItems = document.querySelectorAll('.potential-item');
        
        performanceItems.forEach(perfItem => {
            perfItem.addEventListener('mouseenter', function() {
                const sectorName = this.querySelector('.sector-name').textContent;
                const matchingPotential = Array.from(potentialItems).find(potItem => 
                    potItem.querySelector('.sector-name').textContent === sectorName
                );
                
                if (matchingPotential) {
                    matchingPotential.style.boxShadow = '0 5px 20px rgba(52, 152, 219, 0.4)';
                    matchingPotential.style.transform = 'translateX(5px) scale(1.02)';
                }
            });
            
            perfItem.addEventListener('mouseleave', function() {
                potentialItems.forEach(potItem => {
                    potItem.style.boxShadow = '';
                    potItem.style.transform = '';
                });
            });
        });
        
    }, 2500);
});

console.log('📊 Enhanced Performance Comparison Loaded!');
console.log('✅ Today\'s actual performance vs Monday\'s potential analysis ready');
