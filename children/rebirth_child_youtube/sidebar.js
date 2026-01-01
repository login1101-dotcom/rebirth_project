document.addEventListener('DOMContentLoaded', function () {
    const categories = [
        { name: "撮影編集過程記録", link: "category_process.html", count: 2, className: "text-process" },
        { name: "使用ツール", link: "category_tools.html", count: 2, className: "text-tools" },
        { name: "完成作品", link: "category_works.html", count: 2, className: "text-works" },
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
