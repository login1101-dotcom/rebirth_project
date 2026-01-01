document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: "エッセイ", link: "category_essay.html", count: 2, className: "text-essay" },
        { name: "物語", link: "category_short.html", count: 2, className: "text-short" },
        { name: "その他", link: "category_others.html", count: 2, className: "text-other" },
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
