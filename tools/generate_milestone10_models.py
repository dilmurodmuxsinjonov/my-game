"""Blender 5.2 Headless Model Generator for Milestone 10:
1. anvil.glb (Tinkers' Blacksmith Dual-Horn Anvil & Quenching Trough)
2. smoke_rack.glb (TerraFirmaCraft Curing & Smokehouse Rack)
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
# 23. Tinkers' Blacksmith Anvil & Quenching Tank
# -------------------------------------------------------------
def build_anvil():
    reset_scene()
    mat_iron = create_material("AnvilIron", (0.16, 0.17, 0.19, 1.0), roughness=0.35, metallic=0.9)
    mat_stump = create_material("AnvilStump", (0.26, 0.16, 0.08, 1.0), roughness=0.8)
    mat_band = create_material("IronBand", (0.12, 0.12, 0.14, 1.0), roughness=0.4, metallic=0.8)
    mat_water = create_material("QuenchWater", (0.15, 0.35, 0.65, 0.8), roughness=0.1)
    mat_wood = create_material("TroughWood", (0.32, 0.20, 0.10, 1.0), roughness=0.7)

    # 1. Sturdy Tree Stump Base (Cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.48, vertices=10, location=(0, 0, 0.24))
    stump = bpy.context.active_object
    stump.data.materials.append(mat_stump)

    # Iron reinforcement bands around stump
    for bz in [0.10, 0.38]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.43, minor_radius=0.02, location=(0, 0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_band)

    # 2. Heavy Cast Iron Anvil Body
    # Anvil Base Foot
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.52))
    base = bpy.context.active_object
    base.scale = (0.58, 0.36, 0.08)
    base.data.materials.append(mat_iron)

    # Anvil Waist / Neck
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.62))
    waist = bpy.context.active_object
    waist.scale = (0.34, 0.22, 0.14)
    waist.data.materials.append(mat_iron)

    # Anvil Face Table
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.04, 0, 0.74))
    face = bpy.context.active_object
    face.scale = (0.50, 0.26, 0.12)
    face.data.materials.append(mat_iron)

    # Rounded Horn (Cone pointing left / -X)
    bpy.ops.mesh.primitive_cone_add(radius1=0.12, radius2=0.02, depth=0.32, vertices=8, location=(-0.34, 0, 0.74), rotation=(0, math.radians(-90), 0))
    horn = bpy.context.active_object
    horn.data.materials.append(mat_iron)

    # Heel / Step on right (+X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.36, 0, 0.70))
    heel = bpy.context.active_object
    heel.scale = (0.16, 0.22, 0.08)
    heel.data.materials.append(mat_iron)

    # 3. Water Quenching Trough next to anvil
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.38, 0.22))
    trough = bpy.context.active_object
    trough.scale = (0.32, 0.44, 0.44)
    trough.data.materials.append(mat_wood)

    # Water inside trough
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.38, 0.38))
    water = bpy.context.active_object
    water.scale = (0.28, 0.40, 0.04)
    water.data.materials.append(mat_water)

    # 4. Blacksmith's Forging Hammer resting on anvil face
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.36, vertices=6, location=(0.06, -0.04, 0.82), rotation=(0, 0, math.radians(25)))
    handle = bpy.context.active_object
    handle.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0.02, 0.82))
    h_head = bpy.context.active_object
    h_head.scale = (0.08, 0.06, 0.06)
    h_head.data.materials.append(mat_iron)

    export_glb("anvil.glb")

# -------------------------------------------------------------
# 24. TerraFirmaCraft Timber Smoke Rack & Embers
# -------------------------------------------------------------
def build_smoke_rack():
    reset_scene()
    mat_timber = create_material("RackTimber", (0.30, 0.18, 0.09, 1.0), roughness=0.75)
    mat_meat = create_material("SmokedMeat", (0.45, 0.15, 0.10, 1.0), roughness=0.6)
    mat_fish = create_material("DriedFish", (0.60, 0.45, 0.30, 1.0), roughness=0.7)
    mat_iron = create_material("PotIron", (0.15, 0.15, 0.16, 1.0), roughness=0.5, metallic=0.85)
    mat_embers = create_material("HotEmbers", (1.0, 0.3, 0.05, 1.0), roughness=0.3)
    bsdf = mat_embers.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.35, 0.05, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0

    # 1. Crossed A-Frame timber legs on Left and Right
    for side in [-0.65, 0.65]:
        # Front leg
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.65, vertices=6, location=(side, -0.32, 0.78), rotation=(math.radians(22), 0, 0))
        leg1 = bpy.context.active_object
        leg1.data.materials.append(mat_timber)

        # Back leg
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.65, vertices=6, location=(side, 0.32, 0.78), rotation=(math.radians(-22), 0, 0))
        leg2 = bpy.context.active_object
        leg2.data.materials.append(mat_timber)

        # Cross tie
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.65, vertices=6, location=(side, 0, 0.52), rotation=(math.radians(90), 0, 0))
        tie = bpy.context.active_object
        tie.data.materials.append(mat_timber)

    # 2. Main Horizontal Suspension Beam at top (Z = 1.48m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=1.55, vertices=8, location=(0, 0, 1.48), rotation=(0, math.radians(90), 0))
    top_beam = bpy.context.active_object
    top_beam.data.materials.append(mat_timber)

    # 3. Hanging Cured Meats & Sausages
    for i, hx in enumerate([-0.42, -0.15, 0.12, 0.38]):
        # Twine string
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.24, vertices=4, location=(hx, 0, 1.34))
        twine = bpy.context.active_object
        twine.data.materials.append(mat_timber)

        # Meat joint or cured sausage
        if i % 2 == 0:
            # Flitch of bacon / ham joint
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, 0, 1.12))
            meat = bpy.context.active_object
            meat.scale = (0.11, 0.16, 0.28)
            meat.data.materials.append(mat_meat)
        else:
            # Hanging cured sausage links
            for sz in [1.18, 1.05]:
                bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.10, vertices=8, location=(hx, 0, sz))
                saus = bpy.context.active_object
                saus.data.materials.append(mat_meat)

    # 4. Brazier Pot with Smoldering Embers below
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.18, vertices=8, location=(0, 0, 0.09))
    pot = bpy.context.active_object
    pot.data.materials.append(mat_iron)

    # Glowing coals
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.06, vertices=8, location=(0, 0, 0.16))
    coals = bpy.context.active_object
    coals.data.materials.append(mat_embers)

    export_glb("smoke_rack.glb")

if __name__ == "__main__":
    print("[BLENDER] Generating Milestone 10 3D assets...")
    build_anvil()
    build_smoke_rack()
    print("[BLENDER] Milestone 10 assets completed successfully!")
