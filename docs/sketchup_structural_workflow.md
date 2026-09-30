# SketchUp to Structural BIM Workflow

This workflow converts a SketchUp architectural/reference model into a reviewable structural BIM model using open-source tools.

## Recommended stack

- Blender — geometry cleanup, object classification, scripting, GLB export.
- Bonsai — native IFC authoring inside Blender.
- IfcOpenShell — IFC creation, validation, quantity extraction, and automation with Python.
- GitHub — version control for scripts, JSON mappings, documentation, and lightweight outputs.

## Proposed pipeline

1. Import or convert the SketchUp model to a Blender-readable format.
2. Verify units, coordinates, storeys, and model orientation.
3. Separate candidate structural elements:
   - Footings
   - Foundation beams
   - Columns
   - Beams
   - Slabs
   - Structural walls
   - Stairs, if structural
4. Map architectural/reference geometry to structural object classes.
5. Rebuild or regularize structural geometry rather than blindly accepting mesh geometry.
6. Assign structural metadata such as member type, section dimensions, material, storey, and element ID.
7. Export IFC through Bonsai / IfcOpenShell.
8. Generate BOQ / quantity schedules from the validated structural model.
9. Run geometry and metadata checks before engineering use.

## Important engineering limitation

Geometry extracted from SketchUp is a reference model, not a verified structural design. Member sizes, reinforcement, material properties, load paths, supports, design loads, combinations, and code compliance must be checked against drawings/calculations and reviewed by a qualified structural engineer before construction, tender, or analysis use.

## Inputs preferred for model reconstruction

- Original .skp model
- Structural drawings, if available
- Architectural plans/sections
- Grid and level information
- Material assumptions
- Known member sizes
- Design standard/code to be used

## Outputs

- Blender model (.blend)
- IFC structural BIM model (.ifc)
- Web/model exchange file (.glb)
- Element mapping JSON/CSV
- BOQ quantities
- QA report listing uncertain or unmapped elements
