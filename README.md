# PinZi 拼字 — where sound meets character

**PinYin + HanZi = PinZi.** A free flashcard website for learning every word you need for **TOCFL** (Taiwan, Traditional characters) or **HSK 3.0** (Mainland, Simplified characters), 20 words at a time.

- **Pick** a test and level (TOCFL Pre-A1 → C, HSK 1 → 7–9), or browse by **theme** (People, Time, Food…)
- **Tap** a character to watch its stroke order, or 🔊 to hear it (Taiwan or Mainland accent)
- **Mark** each word ✓ sure / ✗ again until every card is done
- **Stories:** each TOCFL Band A card (Pre-A1 to A2) has a short story that uses all 20 of its words
- **Intro to Chinese:** a starter page covering the language, the history of characters, pinyin and tones, plus a tone game
- Day theme (rice paper and vermilion seal) and night theme (lanterns)

No backend and no AI at runtime: it's a static site of HTML plus JSON.

## Folder structure

```
pinzi/
├── public/                 ← the website (deploy this folder)
│   ├── index.html          ← whole app: UI, voice, stroke order, themes, intro
│   ├── data/               ← word lists: tocfl-*.json, hsk-*.json, themes-*.json
│   └── strokes/            ← stroke-order data, one file per 20 cards
├── content/
│   └── essays.txt          ← the 61 hand-written Band A stories (Chinese | English)
├── scripts/                ← Python build pipeline
│   ├── paths.py            ← all paths, relative to the repo root
│   ├── common.py           ← shared helpers (word forms, story loader)
│   ├── fetch_sources.py    ← downloads word lists + stroke data into sources/
│   ├── step1_band_a_cards.py    ← TOCFL Band A → 61 cards of 20 words
│   ├── step2_band_a_stories.py  ← adds stories + auto pinyin (Taiwan readings)
│   ├── step3_build_decks.py     ← all TOCFL + HSK levels → public/data, public/strokes
│   ├── step4_build_themes.py    ← 18 themes via keyword rules → public/data/themes-*.json
│   └── build_all.py        ← runs everything
├── requirements.txt
└── .gitignore              ← ignores sources/ and build/
```

## Rebuild the data

Needs Python 3.9+, git and npm.

```bash
pip install -r requirements.txt
python scripts/build_all.py --fetch     # first time: downloads sources, then builds
python scripts/build_all.py             # later: rebuild only
```

Builds are deterministic: the same inputs always give the same files.

**Editing a story:** change `content/essays.txt` (one sentence per line: `中文|English`, cards start with `## n`) and rerun. Step 2 checks that each story still uses all 20 of its card's words.

**Editing themes:** change the keyword rules in `scripts/step4_build_themes.py` and rerun.

## Run locally

```bash
python -m http.server -d public 8000
# open http://localhost:8000
```

(Opening `index.html` directly from disk won't work, because the browser blocks loading the JSON files.)

## Deploy (free)

Upload the `public/` folder to **Cloudflare Pages**, **GitHub Pages** or **Vercel**. The whole site is about 62 MB, and the largest file is about 1.7 MB.

## Known limits

- Voice uses the device's built-in text-to-speech, so quality depends on the phone or browser. Planned: pre-recorded neural audio (Breeze2-VITS for the Taiwan accent).
- Stroke data follows Mainland stroke order. It differs from Taiwan's standard for a few characters (e.g. 必). Six rare variant characters have no stroke data: 汙 溼 嚐 証 羣 艶.
- Story pinyin is auto-generated (pypinyin + jieba, with manual fixes for 得 / 還 / 長 / 行 etc.).
- Themes come from keyword rules on English meanings, so a few words may be misplaced.
- Progress is saved per browser (localStorage).

## Data sources and licenses

| What | Source | License |
|---|---|---|
| TOCFL word lists (2023 official, 2018 categories) | [ivankra/tocfl](https://github.com/ivankra/tocfl), from the official SC-TOP lists | see repo |
| English meanings | [CC-CEDICT](https://cc-cedict.org) (via the TOCFL repo) | CC BY-SA 4.0 |
| HSK 3.0 word lists | [drkameleon/complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary) | MIT |
| Stroke-order data | [hanzi-writer-data](https://github.com/chanind/hanzi-writer-data), from Make Me a Hanzi | Arphic Public License |
| Stroke animation | [Hanzi Writer](https://hanziwriter.org) (loaded from CDN) | MIT |
| Hanzi font | [LXGW WenKai TC](https://github.com/lxgw/LxgwWenkaiTC) (Google Fonts) | OFL |

Stories, themes and the app code are original to PinZi.
