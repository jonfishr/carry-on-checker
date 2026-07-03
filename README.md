# 🧳 Carry-On Checker — Will Your Bag Fit?

**Check any carry-on against airlines' published size rules — with real-world
"close call" guidance from [Aly Smalls](https://likewhereyouregoing.com), who
tests bags in actual airline sizers.**

👉 **[Try it live](https://jonfishr.github.io/carry-on-checker/)**

Built from Aly's *Carry-On Compliance Checker* spreadsheet as a thank-you for
years of genuinely useful travel content. Data and methodology are hers;
the site just makes them instant.

---

## ✨ What it does

- Checks your bag's dimensions against **73 airlines** in real time, in cm or inches
- Three-tier verdicts using Aly's methodology:
  **✅ Fits** · **⚠️ Close call** (≤ 2.5 cm / 1 in over — usually fine in real
  sizers) · **❌ Too big** — with exactly which dimension is over, and by how much
- Explains the **height → width → depth** hierarchy (why an over-depth bag
  beats an over-height bag)
- **Recommended bags** library — Aly's tested hard-shell / soft-side / value
  picks, one tap to check any of them
- Per-airline **official source links** and **last-verified dates**
- 100% static: no backend, no build step, loads instantly, costs $0 to host

## 🗂 How data flows

```
Google Sheet (Aly edits)          airlines.json / luggage.json
  Airlines tab  ──┐   daily         (source of truth, fetched
  Luggage tab   ──┴──► GitHub ────► by index.html at runtime)
                      Action              │
                                          └─► embedded fallback snapshot
                                              (for opening the file offline)
```

- **Normal updates:** edit the Google Sheet — the *Update data from Google
  Sheet* workflow syncs it daily (or run it manually from the Actions tab).
  Invalid rows never reach the site; the workflow opens an issue explaining
  the problem instead.
- **Direct updates (developers):** edit the JSON files, then run
  `python3 scripts/embed_fallback.py && python3 scripts/json_to_csv.py`
  and commit. CI enforces that everything stays in sync.
- **Freshness:** a monthly workflow diffs each airline's official baggage
  page and opens an issue when a page changes, so a human can re-check the
  numbers. Data is never edited automatically.

Owner documentation:
- **[docs/GUIDE-FOR-ALY.md](docs/GUIDE-FOR-ALY.md)** — plain-English owner's
  guide (how it works, how to update, what to do when something breaks)
- **[MAINTENANCE.md](MAINTENANCE.md)** — one-time sheet setup, local dev,
  transfer/custom-domain instructions

## 📁 Repository layout

```
index.html                     the whole site (data fetched from the JSON files)
airlines.json / luggage.json   the data
scripts/                       sheet↔JSON converters, fallback embedder, tests
docs/sheet-template/           CSV mirrors of the data — import to (re)create the Sheet
docs/GUIDE-FOR-ALY.md          non-technical owner's guide
docs/drafts/                   early design docs kept for reference
.github/workflows/             daily sheet sync · CI validation · policy-page watch
```

## 📊 Data format

```jsonc
// airlines.json — dimensions in cm, height = longest side, incl. wheels/handles
{
  "id": "air-canada",              // derived from name; kebab-case
  "name": "Air Canada",
  "region": "North America",
  "dimensions": { "height": 55.0, "width": 40.0, "depth": 23.0, "unit": "cm" },
  "weight_limit_kg": 10,           // optional
  "personal_item": { "height": 43, "width": 33, "depth": 16, "unit": "cm" }, // optional
  "notes": "…",                    // optional, shown on the airline card
  "source_url": "https://…",       // optional, official baggage page
  "last_verified": "2026-07-02"    // optional, ISO date
}

// luggage.json
{
  "id": "monos-carry-on",
  "name": "Monos Carry-On",
  "category": "hardside",          // hardside | softside | value
  "dimensions": { "height": 55.88, "width": 35.56, "depth": 22.86, "unit": "cm" },
  "weight_kg": 1.9,                // optional
  "notes": "…"                     // optional, Aly's take, shown verbatim
}
```

## 🧪 Development

```bash
python3 -m http.server 8765           # run locally → http://localhost:8765
python3 -m unittest discover scripts  # test suite
```

## 🤝 Contributing

Spotted an outdated limit or a bag worth adding? Open an issue or PR with
the airline/bag name, a link to the **official** source, and the date you
checked it.

## 🙏 Credits & license

- **Data & methodology:** [Aly Smalls](https://likewhereyouregoing.com) —
  [YouTube @alysmalls](https://www.youtube.com/@alysmalls) — from her
  *Carry-On Compliance Checker* spreadsheet
- **License:** [MIT](LICENSE)

*Airlines can change their rules, and enforcement can vary. This tool is
here to help you plan with confidence — not add stress. When in doubt,
double-check before you fly.* ✈️
