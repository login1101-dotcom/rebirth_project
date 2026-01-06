document.addEventListener('DOMContentLoaded', function () {
    const categories = [
    {
        "name": "動画",
        "link": "category_movie.html",
        "count": 0,
        "className": "text-movie"
    },
    {
        "name": "機材",
        "link": "category_tools.html",
        "count": 0,
        "className": "text-tools"
    },
    {
        "name": "分析",
        "link": "category_analysis.html",
        "count": 0,
        "className": "text-analysis"
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