document.addEventListener("DOMContentLoaded", async () => {
    // 1. カウンター表示要素を取得
    const counterEls = document.querySelectorAll("#visit-counter");
    if (!counterEls.length) return;

    // 2. 現在のページに応じたユニークなキー（appパラメータ）を生成
    // 例: .../rebirth_child_health/index.html -> rebirth_child_health_index
    // 例: .../rebirth_child_novel/post_1.html -> rebirth_child_novel_post_1
    const pathParts = location.pathname.split('/').filter(p => p.length > 0);
    const fileName = pathParts.pop() || 'index.html';
    const dirName = pathParts.pop() || 'unknown_site';

    // 拡張子(.html)を除去し、ドットなどをアンダースコアに置換してキーにする
    const cleanFileName = fileName.replace('.html', '').replace(/\./g, '_');
    const appKey = `${dirName}_${cleanFileName}`;

    // 3. ローカル環境（localhost）の場合の処理
    if (location.origin.startsWith("http://localhost")) {
        const storageKey = `visitCount_${appKey}`;
        let count = localStorage.getItem(storageKey);
        if (!count) count = 0;
        // ローカルではリロードごとにインクリメントして動作確認用とする（本番はサーバー側で制御）
        count++;
        localStorage.setItem(storageKey, count);

        counterEls.forEach(el => {
            el.textContent = `訪問数：${count} (Local)`;
            el.title = `Key: ${appKey}`; // デバッグ用にキーをツールチップ表示
        });
        return;
    }

    // 4. 本番環境（Cloudflare Workers）へのリクエスト
    try {
        const res = await fetch(
            `https://counter-app.english-phonics.workers.dev/?app=${appKey}`,
            { cache: "no-store" }
        );

        const data = await res.json();
        const count = Number(data.count);

        counterEls.forEach(el => {
            if (Number.isFinite(count)) {
                el.textContent = `訪問数：${count}`;
            } else {
                el.textContent = `訪問数：--`;
            }
            // 分析用にコンソールにキーを出力
            console.log(`Counter Key: ${appKey}, Count: ${count}`);
        });

    } catch (e) {
        console.error(e);
        counterEls.forEach(el => {
            el.textContent = `訪問数：--`;
        });
    }
});
