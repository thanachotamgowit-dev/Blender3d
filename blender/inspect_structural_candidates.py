"""Inspect Blender objects and flag likely structural candidates.

Run:
    blender model.blend --background --python blender/inspect_structural_candidates.py

This script does not perform structural design. It only classifies candidate objects
using object names and basic dimensions so that a human can review the mapping.
"""

import bpy
import csv
import os

KEYWORDS = {
    "Footing": ["footing", "foundation pad", "ฐานราก"],
    "FoundationBeam": ["foundation beam", "ground beam", "คานคอดิน"],
    "Column": ["column", "เสา"],
    "Beam": ["beam", "คาน"],
    "Slab": ["slab", "floor", "พื้น"],
    "StructuralWall": ["structural wall", "shear wall", "ผนังโครงสร้าง"],
}

def classify(name):
    n = name.lower()
    for cls, words in KEYWORDS.items():
        if any(w.lower() in n for w in words):
            return cls
    return "Unmapped"

rows = []
for obj in bpy.context.scene.objects:
    if obj.type != "MESH":
        continue
    dims = obj.dimensions
    rows.append({
        "object_name": obj.name,
        "candidate_class": classify(obj.name),
        "dim_x": round(dims.x, 4),
        "dim_y": round(dims.y, 4),
        "dim_z": round(dims.z, 4),
        "status": "REVIEW_REQUIRED",
    })

out_dir = bpy.path.abspath("//dist")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "structural_candidates.csv")

with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [
        "object_name", "candidate_class", "dim_x", "dim_y", "dim_z", "status"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} candidate objects to {out_path}")
