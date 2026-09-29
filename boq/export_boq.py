"""Export concept quantities from spec/house_10x10.json to CSV.

This is a teaching/concept estimate, not a tender BOQ.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("dist/boq.csv"))
    a = p.parse_args()

    s = json.loads(a.spec.read_text(encoding="utf-8"))
    w = float(s["footprint"]["width_m"])
    d = float(s["footprint"]["depth_m"])
    h = float(s["floor_height_m"])
    slab_t = float(s["slab_thickness_m"])
    wt = float(s["wall_thickness_m"])
    st = s["structure"]

    footing_count = 8
    footing_vol = footing_count * float(st["footing_width_m"]) * float(st["footing_depth_m"]) * float(st["footing_thickness_m"])
    slab_area = w * d
    slab_vol = slab_area * slab_t
    ext_wall_gross = 2 * (w + d) * h
    ext_wall_vol = ext_wall_gross * wt

    beam_total_len = 2*(w-1) + 2*(d-1) + (w-1) + (d-1)
    beam_vol = beam_total_len * float(st["beam_width_m"]) * float(st["beam_depth_m"])
    column_vol = footing_count * float(st["column_size_m"])**2 * h

    rows = [
        ("RC isolated footings", "m3", footing_vol, "8 pads from concept grid"),
        ("RC foundation beams", "m3", beam_vol, "Perimeter plus two center beams"),
        ("RC columns", "m3", column_vol, "8 columns"),
        ("Ground floor slab", "m2", slab_area, "10 x 10 m footprint"),
        ("Ground floor concrete", "m3", slab_vol, "Footprint x slab thickness"),
        ("Roof slab", "m2", slab_area, "Concept flat roof area"),
        ("External wall gross area", "m2", ext_wall_gross, "Before door/window deductions"),
        ("External wall gross volume", "m3", ext_wall_vol, "Gross wall area x wall thickness"),
    ]

    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open("w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["Work Category", "Unit", "Quantity", "Basis", "Status"])
        for name, unit, qty, basis in rows:
            wr.writerow([name, unit, round(qty, 3), basis, "Concept / teaching only"])
    print(a.output)

if __name__ == "__main__":
    main()
