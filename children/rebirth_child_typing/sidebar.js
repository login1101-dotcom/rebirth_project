document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: "練習", link: "category_daily.html", count: 3, className: "text-daily" },
        { name: "分析", link: "category_analysis.html", count: 3, className: "text-analysis" },
        { name: "使用サイト・ツール", link: "category_tools.html", count: 3, className: "text-tools" },
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

            // Simple active check
            if (currentPath === cat.link) {
                a.classList.add('active');
            }

            li.appendChild(a);
            ul.appendChild(li);
        });

        listContainer.appendChild(ul);
    }
});
