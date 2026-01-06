document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: "食事", link: "category_diet.html", count: 6, className: "text-diet" },
        { name: "筋トレ", link: "category_muscle.html", count: 3, className: "text-muscle" },
        { name: "睡眠", link: "category_sleep.html", count: 2, className: "text-sleep" },
        { name: "その他", link: "category_others.html", count: 1, className: "text-others" },
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
