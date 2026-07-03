#!/usr/bin/env python3
"""Convert Aly's published Google Sheet (CSV export) into the site's JSON files.

Usage:
    python3 scripts/sheet_to_json.py --airlines-csv URL_OR_PATH --luggage-csv URL_OR_PATH

URLs are fetched (use the sheet's "Publish to web" CSV link or the
gviz export: https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=<TAB>).
Paths are read from disk, which is how the tests and dry-runs work.

On success, writes airlines.json and luggage.json in the repo root (stable,
alphabetical order so unchanged data produces no git diff). On any invalid
row it exits 1 with a plain-English report of every problem found — the
update workflow turns that report into a GitHub issue instead of committing.
"""
import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Sanity ranges (cm) — generous enough for every real carry-on rule
# (Qatar 50cm height ... Sun Country 61cm height) but tight enough to
# catch a value typed into the wrong column or unit.
RANGES = {"height": (40, 70), "width": (25, 50), "depth": (14, 35)}
PERSONAL_RANGES = {"height": (20, 60), "width": (15, 50), "depth": (5, 35)}

REGIONS = {
    "North America", "Latin America & Caribbean", "Europe",
    "Asia-Pacific", "Middle East & Africa",
}

CATEGORY_ALIASES = {
    "hardside": "hardside", "hard-shell": "hardside", "hard shell": "hardside", "hardshell": "hardside",
    "softside": "softside", "soft-side": "softside", "soft side": "softside", "soft": "softside",
    "value": "value", "value pick": "value", "value picks": "value",
}


class ValidationError(Exception):
    """Raised with a human-readable, multi-line problem report."""


def clean_id(raw: str) -> str:
    s = raw.lower().replace("&", " ").replace('"', "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _num(row_name, field, value, errors, required=True, ranges=None):
    value = (value or "").strip()
    if not value:
        if required:
            errors.append(f"{row_name}: missing {field}")
        return None
    try:
        n = float(value)
    except ValueError:
        errors.append(f"{row_name}: {field} isn't a number ({value!r})")
        return None
    if ranges and field in ranges:
        lo, hi = ranges[field]
        if not lo <= n <= hi:
            errors.append(
                f"{row_name}: {field} {n} cm looks wrong (expected {lo}-{hi} cm — "
                "was it typed in the right column and in centimeters?)"
            )
            return None
    return round(n, 2)


def _rows(text):
    reader = csv.DictReader(io.StringIO(text))
    for i, row in enumerate(reader, start=2):
        stripped = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
        if any(stripped.values()):
            yield i, stripped


def parse_airlines_csv(text: str) -> dict:
    airlines, errors, seen = [], [], {}
    for line_no, row in _rows(text):
        name = row.get("Airline", "")
        label = name or f"row {line_no}"
        if not name:
            errors.append(f"row {line_no}: missing airline name")
            continue
        aid = clean_id(name)
        if aid in seen:
            errors.append(f"{name}: duplicate of row {seen[aid]} — each airline should appear once")
            continue
        seen[aid] = line_no

        entry = {"id": aid, "name": name}
        region = row.get("Region", "")
        if region:
            if region not in REGIONS:
                errors.append(f"{name}: unknown region {region!r} (expected one of: {', '.join(sorted(REGIONS))})")
            else:
                entry["region"] = region

        dims = {}
        for field in ("height", "width", "depth"):
            n = _num(label, field, row.get(f"{field.capitalize()} (cm)"), errors, ranges=RANGES)
            if n is not None:
                dims[field] = n
        if len(dims) == 3:
            entry["dimensions"] = {**dims, "unit": "cm"}

        w = _num(label, "weight limit", row.get("Weight limit (kg)"), errors, required=False)
        if w is not None:
            entry["weight_limit_kg"] = w

        pi = {}
        for field in ("height", "width", "depth"):
            n = _num(label, f"personal item {field}", row.get(f"Personal item {field} (cm)"),
                     errors, required=False, ranges=None)
            if n is not None:
                pi[field] = n
        if len(pi) == 3:
            entry["personal_item"] = {**pi, "unit": "cm"}
        elif pi:
            errors.append(f"{name}: personal item needs all three of height/width/depth (or none)")

        notes = row.get("Notes", "")
        if notes:
            entry["notes"] = notes
        url = row.get("Official source", "")
        if url:
            if not url.startswith("http"):
                errors.append(f"{name}: official source should be a link, got {url!r}")
            else:
                entry["source_url"] = url
        verified = row.get("Last verified", "")
        if verified:
            try:
                date.fromisoformat(verified)
                entry["last_verified"] = verified
            except ValueError:
                errors.append(f"{name}: last verified should look like 2026-07-02, got {verified!r}")

        airlines.append(entry)

    if errors:
        raise ValidationError("\n".join(errors))
    airlines.sort(key=lambda a: a["id"])
    return {"airlines": airlines}


def parse_luggage_csv(text: str) -> dict:
    luggage, errors, seen = [], [], {}
    for line_no, row in _rows(text):
        name = row.get("Bag", "")
        label = name or f"row {line_no}"
        if not name:
            errors.append(f"row {line_no}: missing bag name")
            continue
        bid = clean_id(name)
        if bid in seen:
            errors.append(f"{name}: duplicate of row {seen[bid]}")
            continue
        seen[bid] = line_no

        entry = {"id": bid, "name": name}
        cat_raw = row.get("Category", "").lower().replace("🧳", "").replace("🎒", "").replace("💸", "").strip()
        cat = CATEGORY_ALIASES.get(cat_raw)
        if not cat:
            errors.append(f"{name}: category {row.get('Category')!r} not recognized "
                          "(use Hard-shell, Soft-side, or Value)")
        else:
            entry["category"] = cat

        dims = {}
        for field in ("height", "width", "depth"):
            n = _num(label, field, row.get(f"{field.capitalize()} (cm)"), errors, ranges=RANGES)
            if n is not None:
                dims[field] = n
        if len(dims) == 3:
            entry["dimensions"] = {**dims, "unit": "cm"}

        w = _num(label, "weight", row.get("Weight (kg)"), errors, required=False)
        if w is not None:
            entry["weight_kg"] = w
        notes = row.get("Notes", "")
        if notes:
            entry["notes"] = notes
        luggage.append(entry)

    if errors:
        raise ValidationError("\n".join(errors))
    luggage.sort(key=lambda b: b["id"])
    return {"luggage": luggage}


def _load(src: str) -> str:
    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=60) as resp:
            return resp.read().decode("utf-8-sig")
    return Path(src).read_text(encoding="utf-8-sig")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--airlines-csv", required=True, help="URL or path of the Airlines tab CSV")
    ap.add_argument("--luggage-csv", required=True, help="URL or path of the Luggage tab CSV")
    ap.add_argument("--out-dir", default=str(ROOT), help="where to write the JSON files")
    args = ap.parse_args()

    problems = []
    airlines = luggage = None
    try:
        airlines = parse_airlines_csv(_load(args.airlines_csv))
    except ValidationError as e:
        problems.append(f"Airlines tab:\n{e}")
    try:
        luggage = parse_luggage_csv(_load(args.luggage_csv))
    except ValidationError as e:
        problems.append(f"Luggage tab:\n{e}")

    if problems:
        print("\n\n".join(problems), file=sys.stderr)
        return 1

    out = Path(args.out_dir)
    (out / "airlines.json").write_text(
        json.dumps(airlines, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "luggage.json").write_text(
        json.dumps(luggage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(airlines['airlines'])} airlines and {len(luggage['luggage'])} bags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
