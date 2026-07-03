#!/usr/bin/env python3
"""Tests for the sheet -> JSON converter. Run: python3 -m unittest discover scripts"""
import json
import tempfile
import unittest
from pathlib import Path

import sheet_to_json as s2j
import json_to_csv as j2c

AIRLINE_HEADER = (
    "Airline,Region,Height (cm),Width (cm),Depth (cm),Weight limit (kg),"
    "Personal item height (cm),Personal item width (cm),Personal item depth (cm),"
    "Notes,Official source,Last verified"
)
LUGGAGE_HEADER = (
    "Bag,Category,Height (cm),Width (cm),Depth (cm),Weight (kg),Notes"
)


def parse_airlines(rows):
    return s2j.parse_airlines_csv(AIRLINE_HEADER + "\n" + "\n".join(rows) + "\n")


def parse_luggage(rows):
    return s2j.parse_luggage_csv(LUGGAGE_HEADER + "\n" + "\n".join(rows) + "\n")


class AirlineParsing(unittest.TestCase):
    def test_happy_path(self):
        data = parse_airlines([
            'Air Canada,North America,55,40,23,,43,33,16,"Includes wheels and handles.",https://example.com/ac,2026-07-02'
        ])
        a = data["airlines"][0]
        self.assertEqual(a["id"], "air-canada")
        self.assertEqual(a["dimensions"], {"height": 55.0, "width": 40.0, "depth": 23.0, "unit": "cm"})
        self.assertEqual(a["personal_item"], {"height": 43.0, "width": 33.0, "depth": 16.0, "unit": "cm"})
        self.assertEqual(a["source_url"], "https://example.com/ac")
        self.assertEqual(a["last_verified"], "2026-07-02")
        self.assertNotIn("weight_limit_kg", a)

    def test_id_derivation_strips_punctuation(self):
        data = parse_airlines(['Briggs & Riley "Global",Europe,55,40,20,,,,,,,'])
        self.assertEqual(data["airlines"][0]["id"], "briggs-riley-global")

    def test_sorted_by_id_for_stable_output(self):
        data = parse_airlines([
            "Zeta Air,Europe,55,40,20,,,,,,,",
            "Alpha Air,Europe,55,40,20,,,,,,,",
        ])
        self.assertEqual([a["id"] for a in data["airlines"]], ["alpha-air", "zeta-air"])

    def test_missing_dimension_rejected(self):
        with self.assertRaises(s2j.ValidationError) as ctx:
            parse_airlines(["Air Canada,North America,55,,23,,,,,,,"])
        self.assertIn("Air Canada", str(ctx.exception))
        self.assertIn("width", str(ctx.exception).lower())

    def test_out_of_range_height_rejected(self):
        with self.assertRaises(s2j.ValidationError) as ctx:
            parse_airlines(["Tiny Air,Europe,5.5,40,20,,,,,,,"])
        self.assertIn("height", str(ctx.exception).lower())

    def test_duplicate_airline_rejected(self):
        with self.assertRaises(s2j.ValidationError) as ctx:
            parse_airlines([
                "Air Canada,North America,55,40,23,,,,,,,",
                "Air Canada,North America,56,40,23,,,,,,,",
            ])
        self.assertIn("duplicate", str(ctx.exception).lower())

    def test_bad_date_rejected(self):
        with self.assertRaises(s2j.ValidationError) as ctx:
            parse_airlines(["Air Canada,North America,55,40,23,,,,,,https://x.com,07/02/2026"])
        self.assertIn("last verified", str(ctx.exception).lower())

    def test_empty_rows_skipped(self):
        data = parse_airlines(["Air Canada,North America,55,40,23,,,,,,,", ",,,,,,,,,,,"])
        self.assertEqual(len(data["airlines"]), 1)


class LuggageParsing(unittest.TestCase):
    def test_happy_path_with_category_alias(self):
        data = parse_luggage(['Monos Carry-On,Hard-shell,55.88,35.56,22.86,,"I love my monos"'])
        b = data["luggage"][0]
        self.assertEqual(b["id"], "monos-carry-on")
        self.assertEqual(b["category"], "hardside")
        self.assertEqual(b["notes"], "I love my monos")

    def test_unknown_category_rejected(self):
        with self.assertRaises(s2j.ValidationError):
            parse_luggage(["Some Bag,Enormous,55,35,22,,"])

    def test_weight_parsed(self):
        data = parse_luggage(["Cotopaxi Allpa,Soft-side,56,30,25,1.33,"])
        self.assertEqual(data["luggage"][0]["weight_kg"], 1.33)


class RoundTrip(unittest.TestCase):
    def test_repo_json_to_csv_to_json_is_identity(self):
        root = Path(__file__).resolve().parent.parent
        airlines = json.loads((root / "airlines.json").read_text())
        luggage = json.loads((root / "luggage.json").read_text())
        a_csv = j2c.airlines_to_csv(airlines)
        l_csv = j2c.luggage_to_csv(luggage)
        self.assertEqual(s2j.parse_airlines_csv(a_csv), airlines)
        self.assertEqual(s2j.parse_luggage_csv(l_csv), luggage)


if __name__ == "__main__":
    unittest.main()
