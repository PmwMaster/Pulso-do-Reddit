document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const contentArea = document.getElementById('content-area');
    let redditData = null;

    // Load Data
    async function loadData() {
        try {
            // Fetching from parent directory path - in real server this might need adjustment
            // For local file opening, we might need the user to run a server or use the file directly.
            // Assuming relative path for now.
            const response = await fetch('./reddit_report.json');
            if (!response.ok) throw new Error('Failed to load data');
            redditData = await response.json();
            renderCategory('n8n'); // Default
        } catch (error) {
            console.error(error);
            contentArea.innerHTML = `<div style="text-align:center; color: #ff6b6b;">
                <h3>Error loading data</h3>
                <p>Please ensure reddit_report.json exists in the parent directory.</p>
                <p>${error.message}</p>
            </div>`;
        }
    }

    // Render Cards
    function renderCategory(category) {
        if (!redditData || !redditData[category]) return;

        contentArea.innerHTML = '';
        const posts = redditData[category];
        const accentColor = category === 'n8n' ? '#ff6b6b' : '#4facfe';

        posts.forEach((post, index) => {
            const card = document.createElement('a');
            card.href = post.permalink;
            card.target = "_blank";
            card.className = 'post-card fade-in';
            card.style.animationDelay = `${index * 0.1}s`;

            // Highlight border on hover based on category
            card.addEventListener('mouseenter', () => {
                card.style.borderColor = accentColor;
            });
            card.addEventListener('mouseleave', () => {
                card.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            });

            card.innerHTML = `
                <div class="card-header">
                    <div class="score-badge">
                        <i data-lucide="trending-up" width="16"></i> ${post.score} Score
                    </div>
                    <span style="color: var(--text-secondary); font-size: 0.8rem;">${post.created_utc}</span>
                </div>
                <h3 class="post-title">${post.title}</h3>
                <div class="card-footer">
                    <div class="stat">
                        <i data-lucide="arrow-big-up" width="18"></i> ${post.ups}
                    </div>
                    <div class="stat">
                        <i data-lucide="message-square" width="18"></i> ${post.comments} Comments
                    </div>
                </div>
            `;

            contentArea.appendChild(card);
        });

        lucide.createIcons();
    }

    // Tab Switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderCategory(tab.dataset.target);

            // Adjust Globe Colors
            const globe1 = document.querySelector('.globe-1');
            if (tab.dataset.target === 'n8n') {
                globe1.style.background = 'var(--accent-n8n)';
            } else {
                globe1.style.background = 'var(--accent-auto)';
            }
        });
    });

    loadData();
});
