// English Gym Article Data
const ARTICLES = [
    {
        link: "post_10.html",
        date: "2026.01.03",
        category: "reading",
        categoryLabel: "Reading",
        icon: "📚",
        title: "Reading Data Log: Toki Soba & Climate Change",
        excerpt: "Project Data Centerより。各スキルの学習データを記録・分析。"
    },
    {
        link: "post_9.html",
        date: "2026.01.01",
        category: "listening",
        categoryLabel: "Listening",
        icon: "🇬🇧",
        title: "Let It Be 聴解チャレンジ",
        excerpt: "歌を聞いて書いて合ってるか確認。ビートルズ「Let It Be」"
    }
];

// Article Renderer
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('article-list-container');
    if (!container) return; // コンテナがないページでは何もしない

    // 現在のページがどのカテゴリか判定（data-category属性またはURLから）
    const pageCategory = container.getAttribute('data-category') || 'all';

    // フィルタリング
    let targetArticles = ARTICLES;
    if (pageCategory !== 'all') {
        targetArticles = ARTICLES.filter(article => article.category === pageCategory);
    }

    // HTML生成
    let html = '';
    if (targetArticles.length === 0) {
        // Empty State
        const catName = pageCategory === 'all' ? '' : pageCategory;
        html = `
            <div style="text-align:center; padding: 40px; color:#94a3b8;">
                <p>現在、${catName}の記事はありません。</p>
            </div>
        `;
    } else {
        targetArticles.forEach(article => {
            html += `
            <article class="article-item">
                <a href="${article.link}">
                    <div class="item-meta-group">
                        <span class="item-meta">${article.date} • <span class="text-${article.category}">${article.categoryLabel}</span></span>
                        <div class="item-logo-row">
                            <span class="item-logo">${article.icon}</span>
                            <span class="item-click-hint text-${article.category}">CLICK READ MORE →</span>
                        </div>
                    </div>
                    <div class="item-title-box">
                        <h3 class="article-title text-${article.category}">${article.title}</h3>
                        <p class="item-excerpt">${article.excerpt}</p>
                    </div>
                </a>
            </article>
            `;
        });
    }

    container.innerHTML = html;
});
