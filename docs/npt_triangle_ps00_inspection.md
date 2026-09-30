# NPT Triangle concept ps00 - SketchUp inspection

Source: `NPT Triangle concept ps00.skp`

## File observations

- File size: approximately 31 MB.
- SketchUp version metadata: 25.0.660.
- Model units: meter.
- The SketchUp container opens successfully and contains `model.dat`, thumbnails, materials and model metadata.
- Preview shows a low-rise / station-like architectural concept with roof/platform elements.

## Structural-related tags/names detected

The following strings are present in the model and are useful for structural filtering:

- `BEAM`
- `Layer_BEAM`
- `S-FLOOR`
- `FLOOR LEVEL`
- `FLOOR LEVEL II`
- `WALL`
- `Layer_WALL`
- `Roof`
- `Layer_Roof`
- `PLATFORM-ROOF`
- `ROOF POST-PLAN`
- `Structure Gage`
- `ARCHI-BTSStation-Beam2`

Architectural floor/wall/stair tags also exist, including:

- `AR_floor 2`
- `AR_floor 4`
- `AR_stair 9`
- `AR_wall 2`

These should not automatically be treated as structural without review.

## Proposed structural extraction

High-priority structural candidates:
1. Objects/components on BEAM tags.
2. Objects/components on S-FLOOR / structural floor tags.
3. Roof platform/post elements where geometry confirms framing.
4. WALL objects only after structural/non-structural review.

Exclude by default:
- furniture
- sanitary fixtures
- vehicles
- people
- decorative/details
- purely architectural walls/floors/stairs unless confirmed structural

## BOQ target

After geometry parsing, extract:
- concrete volume (m3) by member class
- formwork area (m2), where geometry permits
- slab/roof area (m2)
- beam lengths (m) and volumes (m3)
- column/post counts, lengths and volumes
- structural wall area/volume
- item counts for distinct structural components

No reinforcement quantity should be inferred unless reinforcement geometry or structural drawings are supplied.

## Limitation

This inspection reads SketchUp metadata and embedded strings, but does not yet constitute a verified structural design or final quantity takeoff. Geometry and dimensions must be parsed and checked before BOQ values are issued.
