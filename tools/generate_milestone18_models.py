"""Generate 3D Low-Poly GLB Assets for Milestone 18:
Tinkers' Construct Smeltery Multiblock Controller, Casting Basin, and Casting Table.
Using Blender 5.2.1 LTS Headless Python API.
"""

import bpy
import os
import math

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.6, metallic=0.0, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission:
            bsdf.inputs["Emission Color"].default_value = emission
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def export_glb(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORT] Successfully saved {filepath} ({os.path.getsize(filepath)} bytes)")

# -------------------------------------------------------------
# 1. Smeltery Controller (smeltery_controller.glb)
# -------------------------------------------------------------
def build_smeltery_controller(output_path):
    clear_scene()
    
    mat_seared_brick = create_material("SearedBrick", (0.24, 0.22, 0.21, 1.0), roughness=0.85, metallic=0.1)
    mat_seared_dark = create_material("SearedDark", (0.16, 0.14, 0.14, 1.0), roughness=0.9, metallic=0.1)
    mat_brass = create_material("BrassFaucet", (0.83, 0.68, 0.22, 1.0), roughness=0.3, metallic=0.85)
    mat_molten_lava = create_material("MoltenLava", (0.95, 0.35, 0.05, 1.0), roughness=0.2, emission=(1.0, 0.45, 0.08, 1.0), emission_strength=4.5)
    mat_glass = create_material("RefractoryGlass", (0.15, 0.18, 0.20, 0.8), roughness=0.1, metallic=0.1)

    # Main seared brick block body (0.9 x 0.9 x 0.9)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.45))
    body = bpy.context.active_object
    body.scale = (0.45, 0.45, 0.45)
    body.data.materials.append(mat_seared_brick)

    # Top reinforced rim
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.92))
    rim = bpy.context.active_object
    rim.scale = (0.48, 0.48, 0.05)
    rim.data.materials.append(mat_seared_dark)

    # Bottom foundation plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.04))
    base = bpy.context.active_object
    base.scale = (0.48, 0.48, 0.04)
    base.data.materials.append(mat_seared_dark)

    # Front viewing window frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.46, 0.0, 0.55))
    win_frame = bpy.context.active_object
    win_frame.scale = (0.02, 0.22, 0.22)
    win_frame.data.materials.append(mat_seared_dark)

    # Glowing molten glass aperture
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.47, 0.0, 0.55))
    molten_core = bpy.context.active_object
    molten_core.scale = (0.01, 0.18, 0.18)
    molten_core.data.materials.append(mat_molten_lava)

    # Protective iron grates on window
    for gz in [-0.08, 0.0, 0.08]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.38, location=(0.48, 0.0, 0.55 + gz))
        grate = bpy.context.active_object
        grate.rotation_euler = (0, math.radians(90), 0)
        grate.data.materials.append(mat_seared_dark)

    # Brass pouring spigot / faucet on side/front
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.18, location=(0.45, 0.25, 0.25))
    pipe = bpy.context.active_object
    pipe.rotation_euler = (0, math.radians(90), 0)
    pipe.data.materials.append(mat_brass)

    # Downward faucet spout
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.10, location=(0.52, 0.25, 0.18))
    spout = bpy.context.active_object
    spout.data.materials.append(mat_brass)

    # Brass faucet turn-wheel / valve
    bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.012, location=(0.45, 0.25, 0.33))
    valve = bpy.context.active_object
    valve.rotation_euler = (math.radians(90), 0, 0)
    valve.data.materials.append(mat_brass)

    # Top central exhaust vent
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.12, location=(0, 0, 0.98))
    vent = bpy.context.active_object
    vent.data.materials.append(mat_seared_dark)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Casting Basin (casting_basin.glb)
# -------------------------------------------------------------
def build_casting_basin(output_path):
    clear_scene()

    mat_seared = create_material("SearedBasin", (0.22, 0.20, 0.19, 1.0), roughness=0.8, metallic=0.15)
    mat_dark = create_material("BasinTrim", (0.14, 0.13, 0.12, 1.0), roughness=0.9, metallic=0.2)
    mat_bronze_glow = create_material("SolidifyingBronze", (0.85, 0.45, 0.12, 1.0), roughness=0.3, metallic=0.7, emission=(0.8, 0.35, 0.08, 1.0), emission_strength=2.2)
    mat_brass = create_material("BasinDrain", (0.80, 0.65, 0.20, 1.0), roughness=0.35, metallic=0.8)

    # 4 Heavy seared stone legs
    leg_coords = [(-0.35, -0.35), (0.35, -0.35), (-0.35, 0.35), (0.35, 0.35)]
    for lx, ly in leg_coords:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.22))
        leg = bpy.context.active_object
        leg.scale = (0.10, 0.10, 0.22)
        leg.data.materials.append(mat_dark)

    # Basin bottom slab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.46))
    floor_slab = bpy.context.active_object
    floor_slab.scale = (0.42, 0.42, 0.04)
    floor_slab.data.materials.append(mat_seared)

    # 4 Thick outer basin walls
    # North & South
    for sy in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, sy, 0.62))
        wall = bpy.context.active_object
        wall.scale = (0.42, 0.06, 0.14)
        wall.data.materials.append(mat_seared)
    # East & West
    for sx in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 0, 0.62))
        wall = bpy.context.active_object
        wall.scale = (0.06, 0.42, 0.14)
        wall.data.materials.append(mat_seared)

    # Basin top trim ring
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.77))
    trim = bpy.context.active_object
    trim.scale = (0.44, 0.44, 0.02)
    trim.data.materials.append(mat_dark)

    # Molten metal block solidifying inside the basin cavity
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.58))
    ingot_block = bpy.context.active_object
    ingot_block.scale = (0.31, 0.31, 0.08)
    ingot_block.data.materials.append(mat_bronze_glow)

    # Side brass drainage plug / faucet connection
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.14, location=(0.42, 0.0, 0.54))
    drain = bpy.context.active_object
    drain.rotation_euler = (0, math.radians(90), 0)
    drain.data.materials.append(mat_brass)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Casting Table (casting_table.glb)
# -------------------------------------------------------------
def build_casting_table(output_path):
    clear_scene()

    mat_seared = create_material("TableSeared", (0.25, 0.23, 0.22, 1.0), roughness=0.75, metallic=0.1)
    mat_dark = create_material("TableDark", (0.15, 0.14, 0.13, 1.0), roughness=0.85, metallic=0.2)
    mat_gold_mold = create_material("ClayMold", (0.76, 0.60, 0.32, 1.0), roughness=0.45, metallic=0.5)
    mat_cast_liquid = create_material("MoltenToolBlade", (0.92, 0.40, 0.08, 1.0), roughness=0.25, emission=(0.95, 0.42, 0.10, 1.0), emission_strength=3.0)
    mat_brass = create_material("TableClamps", (0.82, 0.68, 0.24, 1.0), roughness=0.3, metallic=0.85)

    # 4 Sturdy carved pillar legs
    leg_pos = [(-0.38, -0.38), (0.38, -0.38), (-0.38, 0.38), (0.38, 0.38)]
    for lx, ly in leg_pos:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.32))
        leg = bpy.context.active_object
        leg.scale = (0.08, 0.08, 0.32)
        leg.data.materials.append(mat_dark)

    # Lower structural cross braces
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.18))
    brace = bpy.context.active_object
    brace.scale = (0.36, 0.36, 0.03)
    brace.data.materials.append(mat_dark)

    # Table stone tabletop slab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.66))
    table_top = bpy.context.active_object
    table_top.scale = (0.44, 0.44, 0.05)
    table_top.data.materials.append(mat_seared)

    # Raised perimeter rim for drainage
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.72))
    rim = bpy.context.active_object
    rim.scale = (0.45, 0.45, 0.02)
    rim.data.materials.append(mat_dark)

    # Interchangeable refractory clay/gold mold bed in the center
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.73))
    mold = bpy.context.active_object
    mold.scale = (0.30, 0.30, 0.015)
    mold.data.materials.append(mat_gold_mold)

    # Molten sword blade / pickaxe head impression being cast
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.745))
    tool_cast = bpy.context.active_object
    tool_cast.scale = (0.22, 0.06, 0.008)
    tool_cast.data.materials.append(mat_cast_liquid)

    # Crossguard cast impression
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.08, 0, 0.745))
    cross_cast = bpy.context.active_object
    cross_cast.scale = (0.03, 0.14, 0.008)
    cross_cast.data.materials.append(mat_cast_liquid)

    # Brass locking clamps holding the mold in place
    for cx in [-0.33, 0.33]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0, 0.735))
        clamp = bpy.context.active_object
        clamp.scale = (0.025, 0.12, 0.02)
        clamp.data.materials.append(mat_brass)

    # Side mold lever handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.18, location=(0.47, 0.22, 0.70))
    lever = bpy.context.active_object
    lever.rotation_euler = (math.radians(35), 0, 0)
    lever.data.materials.append(mat_brass)

    export_glb(output_path)

# -------------------------------------------------------------
# Main Batch Runner
# -------------------------------------------------------------
if __name__ == "__main__":
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(models_dir, exist_ok=True)

    print("=== Generating Milestone 18 Tinkers' Construct Smeltery & Casting 3D Models ===")
    build_smeltery_controller(os.path.join(models_dir, "smeltery_controller.glb"))
    build_casting_basin(os.path.join(models_dir, "casting_basin.glb"))
    build_casting_table(os.path.join(models_dir, "casting_table.glb"))
    print("=== Milestone 18 3D Asset Generation Complete! ===")
