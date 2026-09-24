"""Generate 3D Low-Poly GLB Assets for Milestone 19:
Outpost Frontier Signpost & Banner, Royal Tax Collector's Strongbox Wagon, and Sanctified Funeral Pyre.
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
# 1. Outpost Banner & Frontier Signpost (outpost_banner.glb)
# -------------------------------------------------------------
def build_outpost_banner(output_path):
    clear_scene()

    mat_wood = create_material("PostWood", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_stone = create_material("StoneBase", (0.45, 0.45, 0.45, 1.0), roughness=0.9)
    mat_banner = create_material("RoyalCloth", (0.12, 0.25, 0.65, 1.0), roughness=0.7)
    mat_gold_trim = create_material("GoldTrim", (0.85, 0.70, 0.20, 1.0), roughness=0.3, metallic=0.8)
    mat_lantern_glow = create_material("LanternFlame", (1.0, 0.75, 0.2, 1.0), roughness=0.2, emission=(1.0, 0.8, 0.25, 1.0), emission_strength=4.0)

    # Cobblestone foundation plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    base = bpy.context.active_object
    base.scale = (0.45, 0.45, 0.15)
    base.data.materials.append(mat_stone)

    # Main vertical timber signpost (height 3.2m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=3.2, location=(0, 0, 1.6))
    post = bpy.context.active_object
    post.data.materials.append(mat_wood)

    # Horizontal banner crossbar
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.2, location=(0, 0, 2.9))
    crossbar = bpy.context.active_object
    crossbar.rotation_euler = (math.radians(90), 0, 0)
    crossbar.data.materials.append(mat_wood)

    # Hanging heraldic banner cloth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.02, 0, 2.1))
    banner = bpy.context.active_object
    banner.scale = (0.015, 0.48, 0.75)
    banner.data.materials.append(mat_banner)

    # Gold crown emblem border
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.04, 0, 2.1))
    emblem = bpy.context.active_object
    emblem.scale = (0.01, 0.20, 0.20)
    emblem.data.materials.append(mat_gold_trim)

    # Outpost direction sign board pointing to Capital
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0, 1.5))
    sign = bpy.context.active_object
    sign.scale = (0.28, 0.08, 0.08)
    sign.data.materials.append(mat_wood)

    # Hanging miner lantern
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.25, 0, 2.7))
    lantern = bpy.context.active_object
    lantern.scale = (0.06, 0.06, 0.10)
    lantern.data.materials.append(mat_lantern_glow)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Tax Collector's Strongbox Wagon (tax_sheriff_cart.glb)
# -------------------------------------------------------------
def build_tax_sheriff_cart(output_path):
    clear_scene()

    mat_dark_wood = create_material("CartWood", (0.28, 0.18, 0.10, 1.0), roughness=0.8)
    mat_iron = create_material("IronReinforce", (0.20, 0.20, 0.22, 1.0), roughness=0.4, metallic=0.9)
    mat_gold_coins = create_material("GoldCoins", (0.92, 0.76, 0.18, 1.0), roughness=0.3, metallic=0.85)
    mat_cloth = create_material("CanopyCloth", (0.55, 0.12, 0.12, 1.0), roughness=0.8) # Royal red

    # Wagon heavy timber chassis (2.6m x 1.4m x 0.15m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.55))
    chassis = bpy.context.active_object
    chassis.scale = (1.3, 0.7, 0.08)
    chassis.data.materials.append(mat_dark_wood)

    # 4 Heavy spiked wagon wheels with iron rims
    wheel_coords = [(-0.9, -0.75), (0.9, -0.75), (-0.9, 0.75), (0.9, 0.75)]
    for wx, wy in wheel_coords:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.10, location=(wx, wy, 0.45))
        wheel = bpy.context.active_object
        wheel.rotation_euler = (math.radians(90), 0, 0)
        wheel.data.materials.append(mat_iron)
        # Hub
        bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.16, location=(wx, wy, 0.45))
        hub = bpy.context.active_object
        hub.rotation_euler = (math.radians(90), 0, 0)
        hub.data.materials.append(mat_dark_wood)

    # Front draft shaft / horse harness poles
    for sy in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.4, location=(1.8, sy, 0.48))
        shaft = bpy.context.active_object
        shaft.rotation_euler = (0, math.radians(90), 0)
        shaft.data.materials.append(mat_dark_wood)

    # Wagon wooden body sidewalls
    for wy in [-0.65, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, wy, 0.95))
        wall = bpy.context.active_object
        wall.scale = (1.2, 0.05, 0.32)
        wall.data.materials.append(mat_dark_wood)

    # Rear tailgate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.2, 0, 0.95))
    back = bpy.context.active_object
    back.scale = (0.05, 0.65, 0.32)
    back.data.materials.append(mat_dark_wood)

    # Large Crown Royal Strongbox in the cargo bed
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.2, 0, 0.88))
    chest = bpy.context.active_object
    chest.scale = (0.60, 0.45, 0.25)
    chest.data.materials.append(mat_dark_wood)

    # Iron chest bands and heavy padlock
    for bx in [-0.6, 0.2]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, 0.88))
        band = bpy.context.active_object
        band.scale = (0.04, 0.47, 0.26)
        band.data.materials.append(mat_iron)

    # Royal Crown Pennant flying from wagon corner
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=1.8, location=(-1.1, 0.6, 1.7))
    flagpole = bpy.context.active_object
    flagpole.data.materials.append(mat_iron)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.95, 0.6, 2.3))
    flag = bpy.context.active_object
    flag.scale = (0.22, 0.01, 0.15)
    flag.data.materials.append(mat_cloth)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Funeral Pyre & Sanctified Crematorium (funeral_pyre.glb)
# -------------------------------------------------------------
def build_funeral_pyre(output_path):
    clear_scene()

    mat_stone = create_material("PyreStone", (0.32, 0.30, 0.28, 1.0), roughness=0.9)
    mat_charred_log = create_material("CharredWood", (0.16, 0.14, 0.12, 1.0), roughness=0.95)
    mat_brazier_iron = create_material("BrazierIron", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.85)
    mat_holy_flame = create_material("HolyFlame", (1.0, 0.45, 0.05, 1.0), roughness=0.2, emission=(1.0, 0.55, 0.10, 1.0), emission_strength=5.0)

    # Octagonal stone ceremonial platform
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.2, depth=0.25, location=(0, 0, 0.12))
    platform = bpy.context.active_object
    platform.data.materials.append(mat_stone)

    # Tiered step
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.95, depth=0.15, location=(0, 0, 0.30))
    step = bpy.context.active_object
    step.data.materials.append(mat_stone)

    # Stacked wooden lattice logs (criss-cross pyre)
    # Layer 1: along X
    for py in [-0.4, 0.0, 0.4]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.3, location=(0, py, 0.45))
        log = bpy.context.active_object
        log.rotation_euler = (0, math.radians(90), 0)
        log.data.materials.append(mat_charred_log)

    # Layer 2: along Y
    for px in [-0.4, 0.0, 0.4]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.3, location=(px, 0, 0.58))
        log = bpy.context.active_object
        log.rotation_euler = (math.radians(90), 0, 0)
        log.data.materials.append(mat_charred_log)

    # Layer 3: along X
    for py in [-0.3, 0.3]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.1, location=(0, py, 0.70))
        log = bpy.context.active_object
        log.rotation_euler = (0, math.radians(90), 0)
        log.data.materials.append(mat_charred_log)

    # Central roaring holy sanctification flame
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.45, radius2=0.05, depth=0.95, location=(0, 0, 1.15))
    flame = bpy.context.active_object
    flame.data.materials.append(mat_holy_flame)

    # 4 Corner ceremonial incense braziers
    brazier_pos = [(-0.8, -0.8), (0.8, -0.8), (-0.8, 0.8), (0.8, 0.8)]
    for bx, by in brazier_pos:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.45, location=(bx, by, 0.35))
        brazier = bpy.context.active_object
        brazier.data.materials.append(mat_brazier_iron)
        # Small flame
        bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.08, depth=0.20, location=(bx, by, 0.65))
        b_flame = bpy.context.active_object
        b_flame.data.materials.append(mat_holy_flame)

    export_glb(output_path)

# -------------------------------------------------------------
# Main Batch Runner
# -------------------------------------------------------------
if __name__ == "__main__":
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(models_dir, exist_ok=True)

    print("=== Generating Milestone 19 Outpost, Crown Tax Cart & Funeral Pyre 3D Models ===")
    build_outpost_banner(os.path.join(models_dir, "outpost_banner.glb"))
    build_tax_sheriff_cart(os.path.join(models_dir, "tax_sheriff_cart.glb"))
    build_funeral_pyre(os.path.join(models_dir, "funeral_pyre.glb"))
    print("=== Milestone 19 3D Asset Generation Complete! ===")
