# Maintainer Notes

Day-to-day ownership is covered in **[docs/GUIDE-FOR-ALY.md](docs/GUIDE-FOR-ALY.md)**
(plain-English, no technical background assumed). This file covers the
one-time setup and developer tasks.

## One-time setup: connect the Google Sheet

1. Create a new Google Sheet. Import `docs/sheet-template/airlines.csv` as a
   tab named **Airlines** (File → Import → Upload → *Insert new sheet(s)*),
   and `docs/sheet-template/luggage.csv` as a tab named **Luggage**. These
   CSVs always mirror the current site data, so the sheet starts in sync.
2. Publish each tab as CSV: File → Share → **Publish to web** → choose the
   tab → *Comma-separated values (.csv)* → Publish. Copy both links.
   (Alternative if the sheet is link-visible: use
   `https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=Airlines`.)
3. In the GitHub repo: Settings → Secrets and variables → Actions →
   **Variables** → add `AIRLINES_CSV_URL` and `LUGGAGE_CSV_URL` with those
   links.
4. Test it: Actions tab → *Update data from Google Sheet* → Run workflow.
   A no-change run should end green with "No data changes today."
5. Hand the sheet to Aly (share or transfer ownership in Google Sheets).
   The repo variables don't need to change unless the sheet is re-published
   under a new link.

Until the variables are set, the daily workflow no-ops harmlessly and data
is maintained by editing the JSON files directly.

## How the pieces fit

- `airlines.json` / `luggage.json` — source of truth the site fetches.
- `index.html` — the whole site; contains an auto-generated fallback copy
  of the data between `FALLBACK-DATA-START/END` markers for file:// use.
- `scripts/sheet_to_json.py` — sheet CSV → JSON, with validation. Bad data
  never reaches the site; the workflow files an issue instead.
- `scripts/json_to_csv.py` — JSON → `docs/sheet-template/*.csv` (kept in
  sync by CI so the sheet can always be rebuilt from the repo).
- `scripts/embed_fallback.py` — refreshes the fallback block in index.html.
- `.github/workflows/update-data.yml` — daily sheet sync (+ manual run).
- `.github/workflows/validate.yml` — push/PR validation: unit tests,
  JSON↔CSV round-trip, fallback/template freshness.
- `.github/workflows/staleness-watch.yml` — monthly diff of each airline's
  official baggage page; opens an issue when pages change. Never edits data.

## Local development

```bash
python3 -m http.server 8765          # serve the site locally
python3 -m unittest discover scripts # run the test suite
python3 scripts/embed_fallback.py    # after editing the JSON by hand
python3 scripts/json_to_csv.py       # after editing the JSON by hand
```

After any manual JSON edit, run both scripts above and commit everything
together, or CI will flag the fallback/templates as stale.

## Transferring the project to Aly

1. GitHub: Settings → General → Danger Zone → **Transfer ownership** (or
   fork to her account). GitHub Pages re-enables under the new owner:
   Settings → Pages → Deploy from branch → `main` → root.
2. Update the `og:url` meta tag in `index.html` and the live links in
   README/GUIDE to the new address.
3. Optional custom domain (e.g. `carryon.likewhereyouregoing.com`): add the
   domain in Settings → Pages, then a CNAME record at the DNS host pointing
   to `<owner>.github.io`. Enable *Enforce HTTPS*.
4. Re-check that the repo variables (`AIRLINES_CSV_URL`, `LUGGAGE_CSV_URL`)
   survived the transfer; re-add if not.
