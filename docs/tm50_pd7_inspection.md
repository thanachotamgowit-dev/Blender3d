# TM50 pd7 SketchUp inspection

Source: `TM50 pd7.skp`

## File observations

- SketchUp file size: approximately 207 MB.
- The file is a ZIP-based SketchUp container with `model.dat`, thumbnails, materials, styles, and an IFC 2x3 classification resource.
- Metadata identifies SketchUp 25.0.660 / SketchUp Client (Windows) 25.0.660.
- Model units are meters.
- The embedded preview shows a tall building/tower mass with adjacent lower volumes and site/context geometry.

## Structural/BIM evidence found in model metadata

The model already contains IFC/BIM-like classification strings. This is useful because structural elements can be mapped using more than geometry alone.

### Columns

Detected column families/types include:

- C1 — 800 x 800 mm
- C2 — 600 x 800 mm
- C3 — 250 x 800 mm
- C4 — 250 x 1200 mm
- C5 — 250 x 1000 mm

Examples are classified with `IfcColumn` / `IfcColumnType` metadata.

### Beams

Detected:

- Concrete rectangular beam — 300 x 600 mm

The model includes `IfcBeam`, `IfcBeamType`, `Pset_BeamCommon`, and Structural Framing metadata.

### Slabs / floors

Detected:

- `Floor:F1`
- `Floor:Insitu Concrete 225mm`
- Multiple `IfcSlab` records
- Multiple stair landing slabs represented as `IfcSlab - Precast Stair ... Landing`

### Walls

The file contains many wall objects/types, including:

- `Basic Wall:W1`
- `Basic Wall:Partition 1`
- `Basic Wall:Interior Wall`
- `IfcWallStandardCase`
- `IfcWallType`

Walls must be reviewed before being classified as structural because the model contains both architectural and partition walls.

## Proposed reconstruction strategy

1. Import/convert the SketchUp model into Blender while preserving names and hierarchy where possible.
2. Read names, component definitions, layers/tags, and IFC classification strings.
3. Build a structural-only collection from:
   - IfcColumn / known rectangular column families
   - IfcBeam / Structural Framing
   - IfcSlab / concrete floors
   - verified structural walls only
4. Exclude furniture, vehicles, decorative components, finishes, landscape, and non-structural partitions.
5. Normalize structural geometry into clean analytical/BIM-friendly solids.
6. Export IFC using Bonsai / IfcOpenShell.
7. Generate an element schedule and BOQ.
8. Produce a QA list for ambiguous elements.

## Engineering caution

This inspection confirms that the SketchUp file contains useful BIM/IFC metadata, but it does **not** verify structural adequacy. Member dimensions found in the model should be treated as model data only until checked against structural drawings/calculations. Reinforcement, loads, load combinations, supports, material strengths, and code compliance are not established by this inspection.
