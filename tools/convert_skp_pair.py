#!/usr/bin/env python3
"""Convert one SketchUp model to paired GLB + IFC4 outputs using OpenSKP.

Usage:
    python tools/convert_skp_pair.py "TM50 pd7.skp" --out-dir dist/tm50_pd7

Requirements:
    pip install openskp
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from openskp import SkpFile
from openskp.export import glb, ifc, json_export


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_skp")
    parser.add_argument("--out-dir", default="dist")
    args = parser.parse_args()

    src = Path(args.input_skp).resolve()
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    stem = src.stem.replace(" ", "_")
    glb_path = out / f"{stem}.glb"
    ifc_path = out / f"{stem}.ifc"
    json_path = out / f"{stem}.json"

    skp = SkpFile.open(str(src))
    model = skp.parse()
    scene = skp.build_scene()

    # Both files are generated from the same parsed/resolved scene.
    glb.export(skp, str(glb_path))
    ifc.export(scene, str(ifc_path))
    json_export.export(model, str(json_path), scene=scene)

    result = {
        "source": str(src),
        "glb": str(glb_path),
        "ifc": str(ifc_path),
        "metadata": str(json_path),
        "status": "REFERENCE_MODEL_UNVERIFIED",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
