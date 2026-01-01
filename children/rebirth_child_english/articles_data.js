// English Gym Article Data
const ARTICLES = [
    {
        id: 9,
        date: "2025.12.25",
        category: "writing",
        categoryLabel: "ライティング (English)",
        icon: "📝",
        title: "My First English Essay: Why I Code",
        excerpt: "My first attempt at writing a full English essay. Sharing my passion for programming and why I started learning English at 51.",
        link: "post_writing_essay1.html"
    },
    {
        id: 8,
        date: "2025.07.15",
        category: "reading", // reading, listening, writing, speaking
        categoryLabel: "リーディング",
        icon: "📚",
        title: "初心者におすすめの洋書（Graded Readers）レベル別リスト",
        excerpt: "自分のレベルに合わない本を読むのは挫折のもと。語彙制限本を活用して「読めた！」という自信を積み重ねよう。",
        link: "post_8.html"
    },
    {
        id: 3,
        date: "2025.07.01",
        category: "writing",
        categoryLabel: "ライティング",
        icon: "✍️",
        title: "3行日記から始める英語アウトプット。Grammarlyで添削してみた",
        excerpt: "今日あったことを3行だけ。AI添削ツールを使えば、独学でも正しい文法が身につくのか？1週間の検証結果。",
        link: "post_3.html"
    },
    {
        id: 4,
        date: "2025.06.20",
        category: "writing",
        categoryLabel: "ライティング",
        icon: "📝",
        title: "英語でTo-Doリストを書くと実行力が上がる件",
        excerpt: "仕事のタスクを英語で書き出すだけで、なぜか「やる気」が出る現象について。シンプルな箇条書きの魔力。",
        link: "post_4.html"
    },
    {
        id: 7,
        date: "2025.06.10",
        category: "reading",
        categoryLabel: "リーディング",
        icon: "📖",
        title: "多読を開始して1ヶ月。Kindleで洋書を読むメリット3選",
        excerpt: "辞書機能、進捗表示、そして何より「持ち運びの楽さ」。50代からの英語やり直しに電子書籍が最強な理由。",
        link: "post_7.html"
    },
    {
        id: 6,
        date: "2025.06.05",
        category: "listening",
        categoryLabel: "リスニング",
        icon: "🎧",
        title: "ポッドキャスト学習法：通勤時間に聴けるおすすめ番組5選",
        excerpt: "隙間時間を英語漬けに。ニュースからエンタメまで、飽きずに続けられる良質な番組を厳選して紹介。",
        link: "post_6.html"
    },
    {
        id: 5,
        date: "2025.05.25",
        category: "speaking",
        categoryLabel: "スピーキング",
        icon: "🚿",
        title: "独り言英会話のすすめ。お風呂とトイレが留学先になる？",
        excerpt: "誰にも聞かれずにスピーキング練習ができる最強のメソッド。日常の動作を実況中継するだけで英語脳は作れる。",
        link: "post_5.html"
    },
    {
        id: 1,
        date: "2025.05.20",
        category: "listening",
        categoryLabel: "リスニング",
        icon: "🎧",
        title: "CNN 10を毎日聴き続けて3ヶ月。聴こえ方が変わった瞬間。",
        excerpt: "最初は雑音にしか聞こえなかったニュース英語が、単語の塊として認識できるようになったブレイクスルー体験について。",
        link: "post_1.html"
    },
    {
        id: 2,
        date: "2025.05.18",
        category: "speaking",
        categoryLabel: "スピーキング",
        icon: "🗣️",
        title: "オンライン英会話で「沈黙」が怖くなくなる魔法のフレーズ10選",
        excerpt: "Yes/Noで会話を終わらせないための、中年男性向け「切り返し」テクニック。",
        link: "post_2.html"
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

    container.innerHTML = html;
});
