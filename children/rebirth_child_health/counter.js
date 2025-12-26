document.addEventListener("DOMContentLoaded", async () => {
    const counterEls = document.querySelectorAll("#visit-counter");
    if (!counterEls.length) return;

    if (location.origin.startsWith("http://localhost")) {
        let count = localStorage.getItem("visitCount_health");
        if (!count) count = 0;
        count++;
        localStorage.setItem("visitCount_health", count);

        counterEls.forEach(el => {
            el.textContent = `訪問数：${count}`;
        });
        return;
    }

    try {
        const res = await fetch(
            "https://counter-app.english-phonics.workers.dev/?app=rebirth_child_health",
            { cache: "no-store" }
        );

        const data = await res.json();
        const count = Number(data.count);

        counterEls.forEach(el => {
            el.textContent = Number.isFinite(count)
                ? `訪問数：${count}`
                : `訪問数：--`;
        });

    } catch (e) {
        console.error(e);
        counterEls.forEach(el => {
            el.textContent = `訪問数：--`;
        });
    }
});
