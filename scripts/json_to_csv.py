#!/usr/bin/env python3
"""Export airlines.json / luggage.json as the CSVs that seed Aly's Google Sheet.

    python3 scripts/json_to_csv.py          # writes docs/sheet-template/*.csv

Import each CSV as a tab (Airlines, Luggage) in a new Google Sheet — that
sheet then becomes the site's control panel via scripts/sheet_to_json.py.
"""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORY_LABELS = {"hardside": "Hard-shell", "softside": "Soft-side", "value": "Value", "luxury": "Luxury"}

AIRLINE_FIELDS = [
    "Airline", "Region", "Height (cm)", "Width (cm)", "Depth (cm)",
    "Weight limit (kg)", "Personal item height (cm)", "Personal item width (cm)",
    "Personal item depth (cm)", "Notes", "Official source", "Last verified",
]
LUGGAGE_FIELDS = ["Bag", "Aly's pick", "Category", "Height (cm)", "Width (cm)", "Depth (cm)", "Weight (kg)", "Notes", "Product link"]


def _fmt(n):
    if n is None:
        return ""
    return str(int(n)) if float(n) == int(n) else str(n)


def airlines_to_csv(data: dict) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=AIRLINE_FIELDS, lineterminator="\n")
    w.writeheader()
    for a in data["airlines"]:
        d = a.get("dimensions", {})
        pi = a.get("personal_item", {})
        w.writerow({
            "Airline": a["name"],
            "Region": a.get("region", ""),
            "Height (cm)": _fmt(d.get("height")),
            "Width (cm)": _fmt(d.get("width")),
            "Depth (cm)": _fmt(d.get("depth")),
            "Weight limit (kg)": _fmt(a.get("weight_limit_kg")),
            "Personal item height (cm)": _fmt(pi.get("height")),
            "Personal item width (cm)": _fmt(pi.get("width")),
            "Personal item depth (cm)": _fmt(pi.get("depth")),
            "Notes": a.get("notes", ""),
            "Official source": a.get("source_url", ""),
            "Last verified": a.get("last_verified", ""),
        })
    return buf.getvalue()


def luggage_to_csv(data: dict) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=LUGGAGE_FIELDS, lineterminator="\n")
    w.writeheader()
    for b in data["luggage"]:
        d = b.get("dimensions", {})
        w.writerow({
            "Bag": b["name"],
            "Aly's pick": "Yes" if b.get("recommended") else "",
            "Category": CATEGORY_LABELS.get(b.get("category"), b.get("category", "")),
            "Height (cm)": _fmt(d.get("height")),
            "Width (cm)": _fmt(d.get("width")),
            "Depth (cm)": _fmt(d.get("depth")),
            "Weight (kg)": _fmt(b.get("weight_kg")),
            "Notes": b.get("notes", ""),
            "Product link": b.get("product_url", ""),
        })
    return buf.getvalue()


def main() -> None:
    out = ROOT / "docs" / "sheet-template"
    out.mkdir(parents=True, exist_ok=True)
    airlines = json.loads((ROOT / "airlines.json").read_text())
    luggage = json.loads((ROOT / "luggage.json").read_text())
    (out / "airlines.csv").write_text(airlines_to_csv(airlines), encoding="utf-8")
    (out / "luggage.csv").write_text(luggage_to_csv(luggage), encoding="utf-8")
    print(f"wrote {out}/airlines.csv and luggage.csv")


if __name__ == "__main__":
    main()
