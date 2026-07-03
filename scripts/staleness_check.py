#!/usr/bin/env python3
"""Best-effort watch for airline policy-page changes.

Fetches each airline's source_url, reduces the page to normalized text, and
compares a fingerprint against the last run (stored in
.github/staleness-hashes.json). Prints a markdown report of airlines whose
pages changed — a human then re-checks the numbers; nothing is ever edited
automatically. Airlines whose pages can't be fetched (bot walls are common)
are listed as skipped, not changed.

Exit code: 0 always (best-effort); the workflow decides what to do with the
report via the CHANGED count on stdout line 1.
"""
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HASHES = ROOT / ".github" / "staleness-hashes.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def page_fingerprint(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as resp:
            html = resp.read(2_000_000).decode("utf-8", errors="replace")
    except Exception:
        return None
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    if len(text) < 200:  # bot-wall / empty shell — don't treat as content
        return None
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    airlines = json.loads((ROOT / "airlines.json").read_text())["airlines"]
    old = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    new, changed, skipped, first_seen = dict(old), [], [], []

    for a in airlines:
        url = a.get("source_url")
        if not url:
            continue
        fp = page_fingerprint(url)
        if fp is None:
            skipped.append(a["name"])
            continue
        if a["id"] not in old:
            first_seen.append(a["name"])
        elif old[a["id"]] != fp:
            changed.append((a["name"], url))
        new[a["id"]] = fp

    HASHES.parent.mkdir(exist_ok=True)
    HASHES.write_text(json.dumps(new, indent=2, sort_keys=True) + "\n")

    print(f"CHANGED={len(changed)}")
    if changed:
        print("\nThese airlines' baggage pages changed since the last check. "
              "That usually just means a website tweak — but please re-check "
              "the carry-on numbers and update the Sheet if needed:\n")
        for name, url in changed:
            print(f"- **{name}** — {url}")
    if first_seen:
        print(f"\n_First snapshot recorded for {len(first_seen)} airline(s)._")
    if skipped:
        print(f"\n_Skipped (page wouldn't load for a robot — normal for some airlines): "
              f"{', '.join(skipped)}_")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
