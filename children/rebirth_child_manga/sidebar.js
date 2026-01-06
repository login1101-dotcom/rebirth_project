document.addEventListener('DOMContentLoaded', function () {
    const categories = [
    {
        "name": "レビュー",
        "link": "category_review.html",
        "count": 0,
        "className": "text-review"
    },
    {
        "name": "おすすめ本",
        "link": "category_list.html",
        "count": 0,
        "className": "text-list"
    },
    {
        "name": "ニュース",
        "link": "category_news.html",
        "count": 0,
        "className": "text-news"
    }
];

    const currentPath = window.location.pathname.split('/').pop();
    const listContainer = document.getElementById('category-list');

    if (listContainer) {
        const ul = document.createElement('ul');
        ul.style.listStyle = 'none';
        ul.style.lineHeight = '2';

        categories.forEach(cat => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = cat.link;
            a.textContent = `${cat.name} (${cat.count})`;
            if (cat.className) a.className = cat.className;

            if (currentPath === cat.link) {
                a.classList.add('active');
            }

            li.appendChild(a);
            ul.appendChild(li);
        });

        listContainer.appendChild(ul);
    }
});