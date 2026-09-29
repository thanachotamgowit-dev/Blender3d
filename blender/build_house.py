"""Build a simple editable 10x10 m Modern Box House in Blender.

Run:
  blender --background --python blender/build_house.py -- \
    --spec spec/house_10x10.json --output-dir dist
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import bpy

def cli():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("dist"))
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return p.parse_args(argv)

def material(name, color, metallic=0.0, roughness=0.6, transmission=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = transmission
    bsdf.inputs["Alpha"].default_value = alpha
    if alpha < 1:
        m.surface_render_method = "DITHERED"
    return m

def box(name, loc, dims, mat, collection, props=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    for k, v in (props or {}).items():
        o[k] = v
    for c in list(o.users_collection):
        c.objects.unlink(o)
    collection.objects.link(o)
    return o

def new_collection(name, parent):
    c = bpy.data.collections.new(name)
    parent.children.link(c)
    return c

def main():
    a = cli()
    s = json.loads(a.spec.read_text(encoding="utf-8"))

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene["project_name"] = s["name"]
    scene["design_status"] = s["design_status"]

    w = float(s["footprint"]["width_m"])
    d = float(s["footprint"]["depth_m"])
    h = float(s["floor_height_m"])
    slab = float(s["slab_thickness_m"])
    wt = float(s["wall_thickness_m"])
    st = s["structure"]
    col = float(st["column_size_m"])
    bw = float(st["beam_width_m"])
    bd = float(st["beam_depth_m"])
    fw = float(st["footing_width_m"])
    fd = float(st["footing_depth_m"])
    ft = float(st["footing_thickness_m"])

    concrete = material("Concrete", (0.58, 0.58, 0.56), roughness=0.8)
    wall = material("White plaster", (0.92, 0.92, 0.89), roughness=0.9)
    timber = material("Timber accent", (0.42, 0.20, 0.08), roughness=0.55)
    dark = material("Dark aluminium", (0.03, 0.04, 0.05), metallic=0.7, roughness=0.3)
    glass = material("Glass", (0.14, 0.30, 0.36), roughness=0.12, transmission=0.5, alpha=0.45)

    building = new_collection("Building", scene.collection)
    c_foot = new_collection("01_Footings", building)
    c_beam = new_collection("02_Foundation_Beams", building)
    c_col = new_collection("03_Columns", building)
    c_slab = new_collection("04_Slabs", building)
    c_wall = new_collection("05_Walls", building)
    c_open = new_collection("06_Doors_Windows", building)
    c_roof = new_collection("07_Roof", building)

    grid = [(-w/2+0.5, -d/2+0.5), (0, -d/2+0.5), (w/2-0.5, -d/2+0.5),
            (-w/2+0.5, 0), (w/2-0.5, 0),
            (-w/2+0.5, d/2-0.5), (0, d/2-0.5), (w/2-0.5, d/2-0.5)]

    footing_z = -ft/2
    for i, (x, y) in enumerate(grid, 1):
        box(f"F{i:02d}", (x, y, footing_z), (fw, fd, ft), concrete, c_foot,
            {"ifc_class":"IfcFooting","boq_category":"Footing"})

    z_beam = 0.10
    for name, loc, dims in [
        ("GB_N", (0, d/2-0.5, z_beam), (w-1, bw, bd)),
        ("GB_S", (0, -d/2+0.5, z_beam), (w-1, bw, bd)),
        ("GB_E", (w/2-0.5, 0, z_beam), (bw, d-1, bd)),
        ("GB_W", (-w/2+0.5, 0, z_beam), (bw, d-1, bd)),
        ("GB_CX", (0, 0, z_beam), (w-1, bw, bd)),
        ("GB_CY", (0, 0, z_beam), (bw, d-1, bd))
    ]:
        box(name, loc, dims, concrete, c_beam, {"ifc_class":"IfcBeam","boq_category":"Foundation beam"})

    for i, (x, y) in enumerate(grid, 1):
        box(f"C{i:02d}", (x, y, slab + h/2), (col, col, h), concrete, c_col,
            {"ifc_class":"IfcColumn","boq_category":"Column"})

    box("Ground_Slab", (0, 0, slab/2), (w, d, slab), concrete, c_slab,
        {"ifc_class":"IfcSlab","boq_category":"Ground slab"})

    z_wall = slab + h/2
    box("Wall_Left", (-w/2+wt/2, 0, z_wall), (wt, d, h), wall, c_wall, {"ifc_class":"IfcWall"})
    box("Wall_Right", (w/2-wt/2, 0, z_wall), (wt, d, h), wall, c_wall, {"ifc_class":"IfcWall"})
    box("Wall_Rear", (0, d/2-wt/2, z_wall), (w, wt, h), wall, c_wall, {"ifc_class":"IfcWall"})

    front_y = -d/2 + wt/2
    box("Wall_Front_L", (-4.15, front_y, z_wall), (1.7, wt, h), wall, c_wall, {"ifc_class":"IfcWall"})
    box("Wall_Front_R", (4.15, front_y, z_wall), (1.7, wt, h), wall, c_wall, {"ifc_class":"IfcWall"})

    box("Partition_A", (-1.6, 2.5, z_wall), (wt, 5.0, h), wall, c_wall, {"ifc_class":"IfcWall"})
    box("Partition_B", (1.6, 2.5, z_wall), (wt, 5.0, h), wall, c_wall, {"ifc_class":"IfcWall"})
    box("Partition_C", (0, 1.1, z_wall), (6.4, wt, h), wall, c_wall, {"ifc_class":"IfcWall"})

    box("Front_Glazing", (0, -d/2+0.03, slab+1.35), (5.8, 0.06, 2.4), glass, c_open,
        {"ifc_class":"IfcWindow","boq_category":"Glazing"})
    for x in (-2.9, -1.45, 0, 1.45, 2.9):
        box("Frame", (x, -d/2, slab+1.35), (0.06, 0.10, 2.45), dark, c_open)

    box("Timber_Left", (-3.15, -d/2+0.10, slab+1.35), (0.35, 0.22, 2.7), timber, c_open)
    box("Timber_Right", (3.15, -d/2+0.10, slab+1.35), (0.35, 0.22, 2.7), timber, c_open)

    roof_z = slab + h + slab/2
    box("Roof_Slab", (0, 0, roof_z), (w, d, slab), concrete, c_roof,
        {"ifc_class":"IfcRoof","boq_category":"Roof slab"})
    ph = float(s["parapet_height_m"])
    pz = slab + h + slab + ph/2
    box("Parapet_N", (0, d/2-wt/2, pz), (w, wt, ph), wall, c_roof)
    box("Parapet_S", (0, -d/2+wt/2, pz), (w, wt, ph), wall, c_roof)
    box("Parapet_E", (w/2-wt/2, 0, pz), (wt, d, ph), wall, c_roof)
    box("Parapet_W", (-w/2+wt/2, 0, pz), (wt, d, ph), wall, c_roof)

    a.output_dir.mkdir(parents=True, exist_ok=True)
    blend = (a.output_dir / "house_10x10.blend").resolve()
    glb = (a.output_dir / "house_10x10.glb").resolve()
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.export_scene.gltf(filepath=str(glb), export_format="GLB")
    print(json.dumps({"blend": str(blend), "glb": str(glb), "status": s["design_status"]}))

if __name__ == "__main__":
    main()
