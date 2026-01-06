document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: "リーディング", link: "category_reading.html", count: 0, className: "text-reading" },
        { name: "リスニング", link: "category_listening.html", count: 1, className: "text-listening" },
        { name: "ライティング", link: "category_writing.html", count: 0, className: "text-writing" },
        { name: "スピーキング", link: "category_speaking.html", count: 0, className: "text-speaking" },
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
