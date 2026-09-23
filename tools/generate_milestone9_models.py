"""Blender 5.2 Headless Model Generator for Milestone 9:
1. wheelbarrow.glb (Delivery Courier Hauler Wheelbarrow)
2. architect_desk.glb (Architect's Drafting Table & Blueprint Station)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def export_glb(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORT] Generated: {filepath} ({os.path.getsize(filepath)} bytes)")

# -------------------------------------------------------------
# 21. Hauler Wheelbarrow (Logistical Transport Hand-Cart)
# -------------------------------------------------------------
def build_wheelbarrow():
    reset_scene()
    mat_wood = create_material("BarrowWood", (0.35, 0.22, 0.12, 1.0), roughness=0.7)
    mat_plank = create_material("BarrowPlank", (0.28, 0.17, 0.09, 1.0), roughness=0.8)
    mat_iron = create_material("BarrowIron", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.85)
    mat_cargo = create_material("BarrowCargo", (0.75, 0.68, 0.42, 1.0), roughness=0.9)

    # 1. Two main wooden handle shafts running from back to front wheel hub
    for side in [-0.28, 0.28]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.7, 0.05, 0.32), rotation=(math.radians(8), 0, 0))
        shaft = bpy.context.active_object
        shaft.scale = (0.07, 1.45, 0.07)
        shaft.data.materials.append(mat_wood)

    # Handle grips at rear
    for side in [-0.28, 0.28]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.18, vertices=8, location=(side * 0.95, -0.68, 0.45), rotation=(0, math.radians(90), 0))
        grip = bpy.context.active_object
        grip.data.materials.append(mat_wood)

    # 2. Front Wheel (Single central iron-rimmed wooden wheel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.07, vertices=12, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    wheel = bpy.context.active_object
    wheel.data.materials.append(mat_wood)

    # Iron Tire Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.24, minor_radius=0.02, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    tire = bpy.context.active_object
    tire.data.materials.append(mat_iron)

    # Wheel Axle rod
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.46, vertices=8, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    axle = bpy.context.active_object
    axle.data.materials.append(mat_iron)

    # 3. Cargo Tub Bed (slanted box container)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.12, 0.38))
    bed = bpy.context.active_object
    bed.scale = (0.64, 0.78, 0.05)
    bed.data.materials.append(mat_plank)

    # Front bulkhead
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.50, 0.52), rotation=(math.radians(-22), 0, 0))
    f_wall = bpy.context.active_object
    f_wall.scale = (0.64, 0.05, 0.32)
    f_wall.data.materials.append(mat_plank)

    # Left & Right sideboards
    for side in [-0.32, 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, 0.12, 0.50), rotation=(0, math.radians(side * -35), 0))
        sideboard = bpy.context.active_object
        sideboard.scale = (0.05, 0.76, 0.28)
        sideboard.data.materials.append(mat_plank)

    # 4. Two vertical support legs at rear
    for side in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, -0.28, 0.16))
        leg = bpy.context.active_object
        leg.scale = (0.06, 0.06, 0.32)
        leg.data.materials.append(mat_wood)

    # 5. Low-poly Cargo Mound inside tub
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.12, 0.46))
    cargo = bpy.context.active_object
    cargo.scale = (0.52, 0.62, 0.18)
    cargo.data.materials.append(mat_cargo)

    export_glb("wheelbarrow.glb")

# -------------------------------------------------------------
# 22. Architect's Drafting Desk (Colony Blueprint Station)
# -------------------------------------------------------------
def build_architect_desk():
    reset_scene()
    mat_wood = create_material("DeskOak", (0.28, 0.18, 0.10, 1.0), roughness=0.65)
    mat_tabletop = create_material("DeskTop", (0.34, 0.22, 0.13, 1.0), roughness=0.6)
    mat_parchment = create_material("BlueprintParchment", (0.86, 0.82, 0.72, 1.0), roughness=0.9)
    mat_ink = create_material("BlueprintInk", (0.12, 0.55, 0.85, 1.0), roughness=0.5)
    mat_brass = create_material("DeskBrass", (0.85, 0.72, 0.25, 1.0), roughness=0.3, metallic=0.85)
    mat_stone = create_material("InkpotStone", (0.15, 0.15, 0.17, 1.0), roughness=0.7)
    mat_feather = create_material("QuillFeather", (0.95, 0.95, 0.92, 1.0), roughness=0.8)

    # 1. 4 Sturdy Legs
    for x, y in [(-0.65, -0.45), (0.65, -0.45), (-0.65, 0.45), (0.65, 0.45)]:
        # Front legs slightly shorter to slope the table
        lz = 0.36 if y < 0 else 0.42
        lheight = 0.72 if y < 0 else 0.84
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, lz))
        leg = bpy.context.active_object
        leg.scale = (0.11, 0.11, lheight)
        leg.data.materials.append(mat_wood)

    # Cross bracing beams
    for y in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, 0.22))
        brace = bpy.context.active_object
        brace.scale = (1.20, 0.06, 0.08)
        brace.data.materials.append(mat_wood)

    # 2. Slanted Drafting Tabletop (15 degree incline)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.84), rotation=(math.radians(10), 0, 0))
    top = bpy.context.active_object
    top.scale = (1.55, 1.12, 0.09)
    top.data.materials.append(mat_tabletop)

    # Bottom retainer lip to prevent plans sliding off
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.54, 0.79), rotation=(math.radians(10), 0, 0))
    lip = bpy.context.active_object
    lip.scale = (1.55, 0.06, 0.06)
    lip.data.materials.append(mat_wood)

    # 3. Unrolled Feudal Blueprint Parchment
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0.02, 0.895), rotation=(math.radians(10), 0, 0))
    parchment = bpy.context.active_object
    parchment.scale = (1.05, 0.78, 0.015)
    parchment.data.materials.append(mat_parchment)

    # Ink Blueprint lines / castle layout on parchment
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0.02, 0.905), rotation=(math.radians(10), 0, 0))
    plan_lines = bpy.context.active_object
    plan_lines.scale = (0.85, 0.58, 0.01)
    plan_lines.data.materials.append(mat_ink)

    # 4. Rolled Scrolls on top corner
    for roffset in [0.0, 0.07]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.72, vertices=10, location=(0.58, 0.22 + roffset, 0.94), rotation=(0, math.radians(90), math.radians(15)))
        scroll = bpy.context.active_object
        scroll.data.materials.append(mat_parchment)

    # 5. Brass Drafting Compass / Divider
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.28, vertices=6, location=(0.34, -0.15, 0.89), rotation=(math.radians(10), math.radians(25), 0))
    leg1 = bpy.context.active_object
    leg1.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.28, vertices=6, location=(0.42, -0.18, 0.89), rotation=(math.radians(10), math.radians(-25), 0))
    leg2 = bpy.context.active_object
    leg2.data.materials.append(mat_brass)

    # 6. Stone Inkpot & Feather Quill
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.09, vertices=8, location=(0.58, -0.32, 0.86), rotation=(math.radians(10), 0, 0))
    inkpot = bpy.context.active_object
    inkpot.data.materials.append(mat_stone)

    # Angled Quill
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.35, vertices=6, location=(0.60, -0.36, 0.98), rotation=(math.radians(-35), math.radians(20), 0))
    quill = bpy.context.active_object
    quill.data.materials.append(mat_feather)

    export_glb("architect_desk.glb")

if __name__ == "__main__":
    print("[BLENDER] Generating Milestone 9 3D assets...")
    build_wheelbarrow()
    build_architect_desk()
    print("[BLENDER] Milestone 9 assets completed successfully!")
