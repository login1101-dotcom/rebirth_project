document.addEventListener('DOMContentLoaded', function () {
    const categories = [
    {
        "name": "善の研究",
        "link": "category_nishida.html",
        "count": 5,
        "className": "text-nishida"
    },
    {
        "name": "生命とは何か",
        "link": "category_schrodinger.html",
        "count": 2,
        "className": "text-schrodinger"
    },
    {
        "name": "日本はなぜ",
        "link": "category_yamamoto.html",
        "count": 2,
        "className": "text-yamamoto"
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