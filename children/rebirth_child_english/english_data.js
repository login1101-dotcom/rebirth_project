// English Gym Data Management
// 3つのモード：多読(Extensive), 精読(Intensive), 只管朗読(Shikan)

const ENGLISH_DATA = {
    // 1. 多読 (Extensive Reading)
    // 目的：量(語数)、スピード(WPM)、推測力
    extensive: [
        {
            id: 1,
            date: "2025-12-20",
            title: "Enjoy Simple English - Rakugo 'Toki Soba'",
            category: "Comedy",
            wordCount: 450,
            timeSec: 240, // 4分
            wpm: 112, // 自動計算: 450 / (240/60) = 112.5
            summary: "お蕎麦屋さんで時間を誤魔化す男の話。最後は失敗するのが面白い。",
            guessCount: 2, // 推測チャレンジ回数
            svClear: true, // SVを見失わずに読めたか
            rating: 5, // 面白さ
            status: "done"
        },
        {
            id: 2,
            date: "2025-12-25",
            title: "News Article - Climate Change",
            category: "News",
            wordCount: 800,
            timeSec: 600, // 10分
            wpm: 80,
            summary: "気候変動の影響で北極の氷が溶けている話。専門用語が多くて難しかった。",
            guessCount: 5,
            svClear: false, // 難しくてSV見失った（精読候補）
            rating: 3,
            status: "done"
        }
    ],

    // 2. 精読 (Intensive Reading)
    // 目的：100%理解、弱点解剖、DB化
    intensive: [
        {
            id: 101,
            date: "2025-12-26",
            source: "News Article - Climate Change",
            full_sentence: "Rarely have I seen such a rapid decline in ice sheet thickness.",
            // 解剖データ
            analysis: [
                {
                    type: "Grammar",
                    item: "倒置 (Inversion)",
                    memo: "否定語 'Rarely' が文頭に来ているため、have I (VS) の順になっている。",
                    tags: ["倒置", "否定語"]
                },
                {
                    type: "Vocabulary",
                    item: "decline",
                    memo: "減少、低下。動詞だけでなく名詞としても使う。",
                    tags: ["名詞利用"]
                }
            ],
            translation: "これほど急速な氷床の厚さの減少を見たことはめったにない。",
            pronunciation_mem: "RarelyのRの発音に注意。declineのiは二重母音。",
            status: "learning", // learning, stocked
            review_history: [false] // 理解度チェック履歴
        },
        {
            id: 102,
            date: "2025-12-28",
            source: "Enjoy Simple English",
            full_sentence: "It cost me an arm and a leg to fix my car.",
            analysis: [
                {
                    type: "Idiom",
                    item: "cost (someone) an arm and a leg",
                    memo: "「莫大なお金がかかる」という意味の慣用句。手足を失うくらい高い代償。",
                    tags: ["慣用句", "比喩"]
                }
            ],
            translation: "車の修理にものすごいお金がかかった。",
            pronunciation_mem: "arm and a leg は繋げて読む。",
            status: "stocked",
            review_history: [true, true, true] // 3回連続OKで殿堂入り
        }
    ],

    // 3. 只管朗読 (Shikan / Reading Aloud)
    // 目的：身体化、500回反復
    shikan: [
        {
            id: 201,
            title: "Toki Soba (Intro Paragraph)",
            ref_source: "Enjoy Simple English",
            target_count: 500,
            current_count: 52,
            best_time: 35, // 秒
            // 発音・意識ポイントメモ
            notes: "Sobaのイントネーションは平坦に。Edikkoの感じを出す。",
            pronunciation_marks: "What time is it? (T消える)",
            logs: [
                { date: "2025-12-29", count: 10, time: 45 },
                { date: "2025-12-30", count: 20, time: 40 }
            ],
            status: "active" // active, hall_of_fame
        }
    ],

    // 4. リスニング (Listening)
    // カテゴリ: Song(歌), Tech(AI/IT), Motivation(モチベ)
    listening: [
        {
            id: 301,
            date: "2025-12-28",
            category: "Song",
            title: "The Beatles - Let It Be",
            timeMin: 5,
            memo: "歌詞の意味を噛み締めながらシャドーイング。",
            tags: ["Classic", "British"],
            youtube_id: "",
            // 歌詞学習用データ (抜粋引用 + 解説)
            phrase_study: {
                quote: "When I find myself in times of trouble, Mother Mary comes to me",
                translation: "私が苦難の時にあると気づくとき、聖母マリアが私の元へやってくる",
                points: [
                    { item: "find myself", memo: "気づくと〜にいる、ふと我に返る" },
                    { item: "times of trouble", memo: "困難な時期、苦しい時" }
                ],
                sound_points: [
                    "Let it be は繋げて 'レリビー' に聞こえる (Flapping)",
                    "Mother Mary の th はしっかり舌を噛む",
                    "Trouble の tr は 'チュ' に近い音になる"
                ],
                external_lyrics_url: "https://genius.com/The-beatles-let-it-be-lyrics"
            }
        },
        {
            id: 302,
            date: "2025-12-29",
            category: "Tech",
            title: "Elon Musk Interview on AI Safety",
            timeMin: 15,
            memo: "早口で聞き取るのが大変だったが、AIの未来についての話は興味深い。",
            tags: ["Interview", "AI"],
            youtube_id: ""
        },
        {
            id: 303,
            date: "2025-12-29",
            category: "Motivation",
            title: "Arnold Schwarzenegger - Work Like Hell",
            timeMin: 10,
            memo: "朝の気合い入れに視聴。パワーをもらった。",
            tags: ["Speech", "Mindset"],
            youtube_id: ""
        }
    ],

    // 5. スピーキング (Speaking)
    // カテゴリ: AI(AI会話), Lesson(英会話), Singing(歌 - Listeningから自動連携)
    speaking: [
        {
            id: 401,
            date: "2025-12-28",
            category: "AI",
            title: "Talk with Gemini about Coding",
            timeMin: 15,
            memo: "技術的な話題を英語で説明する練習。関係代名詞につまる。",
            tags: ["Tech", "Output"]
        },
        {
            id: 402,
            date: "2025-12-29",
            category: "Lesson",
            title: "DMM Eikaiwa (Teacher: Sarah)",
            timeMin: 25,
            memo: "昨日のニュースについて議論。Climate Changeの単語を使って話せた。",
            tags: ["Discussion", "Correction"]
        }
    ],

    // 6. ライティング (Writing)
    // データ: 英語で書いた記事のみ (日本語の記事はカテゴリーには入るがここには含まない)
    writing: [
        {
            id: 501,
            date: "2025-12-25",
            title: "My First English Essay: Why I Code",
            wordCount: 215,
            memo: "First try. Expressing passion for coding.",
            tags: ["Essay", "Personal"],
            url: "post_writing_essay1.html"
        }
    ]
};
