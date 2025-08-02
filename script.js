// Add to the end of your existing script.js

// Breaking News Section
async function fetchBreakingNews() {
  try {
    const news = liveFinancialNews.slice(0, 5);
    const container = document.getElementById('breaking-news-container');
    let html = '';
    news.forEach(item => {
      html += `
        <div class="breaking-news-item">
          <h3>${item.title}</h3>
          <p>${item.source || ''} • <a href="${item.url}" target="_blank">Read Full Article</a></p>
        </div>`;
    });
    container.innerHTML = html || '<div>No breaking news available.</div>';
  } catch (err) {
    console.error('Failed to update breaking news', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  fetchBreakingNews();
  setInterval(fetchBreakingNews, 3 * 60 * 1000);
});
// Breaking News Section
async function fetchBreakingNews() {
  try {
    if (typeof liveFinancialNews !== "undefined" && liveFinancialNews.length > 0) {
      const news = liveFinancialNews.slice(0, 5);
      const container = document.getElementById('breaking-news-container');
      let html = '';
      news.forEach(item => {
        html += `
          <div class="breaking-news-item">
            <h3>${item.title}</h3>
            <p>${item.source || ''} • <a href="${item.url}" target="_blank">Read Full Article</a></p>
          </div>`;
      });
      container.innerHTML = html || '<div>No breaking news available.</div>';
    } else {
      document.getElementById('breaking-news-container').innerHTML = "<div>No breaking news available.</div>";
    }
  } catch (err) {
    document.getElementById('breaking-news-container').innerHTML = "<div>No breaking news available.</div>";
    console.error('Failed to update breaking news', err);
  }
}
document.addEventListener('DOMContentLoaded', () => {
  fetchBreakingNews();
  setInterval(fetchBreakingNews, 3 * 60 * 1000);
});
