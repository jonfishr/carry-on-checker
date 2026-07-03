#!/usr/bin/env python3
"""Regenerate the embedded fallback data in index.html from the JSON files.

The site fetches airlines.json / luggage.json at runtime; the fallback
snapshot between the FALLBACK-DATA markers only serves people who open
index.html straight from disk. Run this after any data change:

    python3 scripts/embed_fallback.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "// FALLBACK-DATA-START"
END = "// FALLBACK-DATA-END"


def main() -> int:
    airlines = json.loads((ROOT / "airlines.json").read_text())
    luggage = json.loads((ROOT / "luggage.json").read_text())

    block = (
        f"{START}\n"
        f"        const FALLBACK_AIRLINES = {json.dumps(airlines, ensure_ascii=False, separators=(',', ': '))};\n"
        f"        const FALLBACK_LUGGAGE = {json.dumps(luggage, ensure_ascii=False, separators=(',', ': '))};\n"
        f"        {END}"
    )

    index = ROOT / "index.html"
    html = index.read_text()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(html):
        print("error: fallback markers not found in index.html", file=sys.stderr)
        return 1
    index.write_text(pattern.sub(lambda _: block, html))
    print(f"embedded {len(airlines['airlines'])} airlines, {len(luggage['luggage'])} bags into index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
