document.addEventListener("DOMContentLoaded", async () => {
    // 1. カウンター要素の取得
    const counterEls = document.querySelectorAll("#visit-counter");
    if (!counterEls.length) return;

    // 2. ページごとのユニークキー生成
    const pathParts = location.pathname.split('/').filter(p => p.length > 0);
    const fileName = pathParts.pop() || 'index.html';
    const dirName = pathParts.pop() || 'unknown_site';
    const cleanFileName = fileName.replace('.html', '').replace(/\./g, '_');
    const appKey = `${dirName}_${cleanFileName}`;

    // 3. 管理者モード（自分を除外）のチェック
    const IS_ADMIN_KEY = 'admin_ignore_count';
    let isAdmin = localStorage.getItem(IS_ADMIN_KEY) === 'true';

    // ============================================
    // クリックイベントの設定（隠しコマンド）
    // ============================================
    let clickCount = 0;
    counterEls.forEach(el => {
        // カーソルをpointerにして「押せそう」にするかどうかはお好みですが、
        // 完全に隠すなら default のままが良いでしょう。
        // 今回はわかりやすさのため、クリック可能範囲だけ設定します。
        el.style.userSelect = "none";

        el.addEventListener('click', () => {
            clickCount++;
            if (clickCount >= 5) {
                // トグル切り替え
                isAdmin = !isAdmin;
                localStorage.setItem(IS_ADMIN_KEY, isAdmin);
                clickCount = 0;

                if (isAdmin) {
                    alert("【管理者モード】このブラウザからのアクセスはカウントされなくなりました。（数字の後ろに * がつきます）");
                    updateCounterDisplay(el, currentCountValue, true);
                } else {
                    alert("【通常モード】カウント除外を解除しました。");
                    updateCounterDisplay(el, currentCountValue, false);
                }
            }
        });
    });

    let currentCountValue = null;

    // 表示更新用関数
    function updateCounterDisplay(element, count, admin) {
        if (!element) return;

        let text = "";
        if (count === null || !Number.isFinite(count)) {
            text = "訪問数：--";
        } else {
            text = `訪問数：${count}`;
        }

        // 管理者なら目印をつける
        if (admin) {
            text += " *";
            element.style.color = "#aaa"; // 少し薄くする等の視覚フィードバック
        } else {
            element.style.color = ""; // 元に戻す
        }

        element.textContent = text;
    }


    // 4. ローカル環境（localhost）の場合
    if (location.origin.startsWith("http://localhost")) {
        const storageKey = `visitCount_${appKey}`;
        let count = Number(localStorage.getItem(storageKey)) || 0;

        if (!isAdmin) {
            count++;
            localStorage.setItem(storageKey, count);
        }
        currentCountValue = count;

        counterEls.forEach(el => {
            updateCounterDisplay(el, count, isAdmin);
            if (!isAdmin) el.textContent += " (Loc)";
        });
        return;
    }

    // 5. 本番環境（Cloudflare Workers）
    try {
        // 管理者の場合はカウントアップしないパラメータ（例: &ignore=true）を送る手もあるが、
        // シンプルに「GETだけして、カウントアップしないAPI」が今のWorkerにあるか不明。
        // もし今のWorkerが「アクセス＝即カウント」なら、fetch自体を止めるしかない。
        // しかし数字は見たいはず。
        // よって、今回は「カウントしてしまうが、自分が見たときは無視」はできない（Workerの仕様による）。
        // Worker側が「?readonly=true」などに対応していない限り、fetchした時点でカウントされる可能性が高い。

        // 今回の既存Worker（counter-app...）は「GETするとインクリメントして値を返す」単純なものと想定される。
        // なので、「数字は見たいがカウントはしたくない」を実現するには、Worker側の対応か、
        // あるいは「管理者は数字を見ない（fetchしない）」という仕様にするしかない。

        // ★ユーザー要望：「数字を知りたい」＆「カウントされたくない」
        // 解決策：今のWorker仕様を変えられないなら、「fetchしない」＝「数字も見れない」になってしまう。
        // それだと意味がないので、現状は「fetchはする（カウントされちゃう）」を受け入れるか、
        // 「自分が見たときはfetchしない（数字も見れない）」の2択になる。

        // もし「fetchして結果だけ見る（インクリメントしない）」APIがない場合、
        // ここでは暫定的に「管理者モードならfetchしない（数字は -- のまま）」とするのが安全です。
        // 「数字は見たい」場合は、Workerを改造する必要があります。

        // とりあえず今回は「管理者モードならfetchをスキップする」実装にします。
        // これで「アクセスがカウントされてしまう」は防げます（その代わり、自分の画面で数字は見れません）。

        if (isAdmin) {
            // fetchしない
            counterEls.forEach(el => {
                updateCounterDisplay(el, null, true);
                // Adminだとわかるようにテキスト変更
                el.textContent = "訪問数：(管理者)";
            });
            return;
        }

        // 通常ユーザー
        const res = await fetch(
            `https://counter-app.english-phonics.workers.dev/?app=${appKey}`,
            { cache: "no-store" }
        );

        const data = await res.json();
        const count = Number(data.count);
        currentCountValue = count;

        counterEls.forEach(el => {
            updateCounterDisplay(el, count, isAdmin);
        });

    } catch (e) {
        console.error(e);
        counterEls.forEach(el => {
            el.textContent = `訪問数：--`;
        });
    }
});
