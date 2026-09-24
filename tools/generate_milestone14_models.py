"""Blender 5.2 Headless Model Generator for Milestone 14:
1. gem_cutting_table.glb (Apotheosis Jeweler's Lapidary Gem Cutting Table)
2. boss_trophy.glb (Warlord's Golden Horned Conquest Trophy Plinth)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
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
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
                bsdf.inputs["Emission Strength"].default_value = emission_strength
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission
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
# 33. Apotheosis Gem Cutting Table (gem_cutting_table.glb)
# -------------------------------------------------------------
def build_gem_cutting_table():
    reset_scene()
    mat_wood = create_material("TableMahogany", (0.28, 0.15, 0.08, 1.0), roughness=0.7)
    mat_brass = create_material("JewelerBrass", (0.85, 0.68, 0.22, 1.0), roughness=0.25, metallic=0.9)
    mat_stone = create_material("GrindstoneCarborundum", (0.35, 0.35, 0.38, 1.0), roughness=0.9)
    mat_ruby = create_material("CutRubyGlow", (0.95, 0.12, 0.18, 1.0), roughness=0.1,
                               emission=(0.95, 0.12, 0.18, 1.0), emission_strength=2.5)
    mat_sapphire = create_material("CutSapphireGlow", (0.15, 0.35, 0.95, 1.0), roughness=0.1,
                                   emission=(0.15, 0.35, 0.95, 1.0), emission_strength=2.5)

    # 1. Main Workbench Desk Top
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.75))
    top = bpy.context.active_object
    top.scale = (1.30, 0.85, 0.08)
    top.data.materials.append(mat_wood)

    # 2. Four Sturdy Turned Legs
    for lx in [-0.55, 0.55]:
        for ly in [-0.34, 0.34]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.36))
            leg = bpy.context.active_object
            leg.scale = (0.10, 0.10, 0.72)
            leg.data.materials.append(mat_wood)

    # Footrest stretcher beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    stretcher = bpy.context.active_object
    stretcher.scale = (1.10, 0.08, 0.06)
    stretcher.data.materials.append(mat_wood)

    # 3. Rotating Diamond Lapidary Grinding Wheel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.04, vertices=20, location=(-0.25, 0.05, 0.82))
    grind_wheel = bpy.context.active_object
    grind_wheel.data.materials.append(mat_stone)

    # Grinding wheel center spindle brass arbor
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.10, vertices=12, location=(-0.25, 0.05, 0.84))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_brass)

    # 4. Articulated Brass Magnifier Inspection Arm & Lens
    # Base mount
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.06, vertices=10, location=(-0.45, -0.25, 0.82))
    arm_base = bpy.context.active_object
    arm_base.data.materials.append(mat_brass)

    # Vertical post
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.25, vertices=8, location=(-0.45, -0.25, 0.95))
    arm_post = bpy.context.active_object
    arm_post.data.materials.append(mat_brass)

    # Horizontal cantilever
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.22, vertices=8, location=(-0.36, -0.15, 1.07))
    arm_horiz = bpy.context.active_object
    arm_horiz.rotation_euler = (math.radians(35), math.radians(45), 0)
    arm_horiz.data.materials.append(mat_brass)

    # Magnifier brass bezel ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.012, location=(-0.25, 0.0, 1.05))
    lens_bezel = bpy.context.active_object
    lens_bezel.data.materials.append(mat_brass)

    # 5. Lapidary Gem Dop Stick / Vise Clamp
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.05, 0.08, 0.84))
    dop_stick = bpy.context.active_object
    dop_stick.scale = (0.16, 0.03, 0.03)
    dop_stick.data.materials.append(mat_brass)

    # 6. Gem Sorting Trays with cut sparkling gems on right
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.35, 0.0, 0.81))
    tray = bpy.context.active_object
    tray.scale = (0.35, 0.50, 0.04)
    tray.data.materials.append(mat_wood)

    # Cut Ruby gemstone in tray
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.05, vertices=8, location=(0.28, 0.10, 0.85))
    ruby = bpy.context.active_object
    ruby.rotation_euler = (math.radians(180), 0, 0)
    ruby.data.materials.append(mat_ruby)

    # Cut Sapphire gemstone in tray
    bpy.ops.mesh.primitive_cone_add(radius1=0.045, depth=0.06, vertices=6, location=(0.40, -0.08, 0.85))
    sapphire = bpy.context.active_object
    sapphire.rotation_euler = (math.radians(180), 0, 0)
    sapphire.data.materials.append(mat_sapphire)

    export_glb("gem_cutting_table.glb")

# -------------------------------------------------------------
# 34. Warlord's Golden Trophy Pedestal (boss_trophy.glb)
# -------------------------------------------------------------
def build_boss_trophy():
    reset_scene()
    mat_stone = create_material("MarblePedestal", (0.82, 0.80, 0.78, 1.0), roughness=0.4)
    mat_gold = create_material("TrophyGold", (0.92, 0.78, 0.18, 1.0), roughness=0.2, metallic=0.95)
    mat_horn = create_material("BeastHornIvory", (0.22, 0.18, 0.14, 1.0), roughness=0.6)
    mat_steel = create_material("ConqueredAxe", (0.24, 0.25, 0.28, 1.0), roughness=0.35, metallic=0.9)
    mat_ruby_crest = create_material("CrestRuby", (0.90, 0.10, 0.15, 1.0), roughness=0.1,
                                     emission=(0.90, 0.10, 0.15, 1.0), emission_strength=3.0)

    # 1. Tiered Marble Pedestal Base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.10))
    tier1 = bpy.context.active_object
    tier1.scale = (0.75, 0.75, 0.20)
    tier1.data.materials.append(mat_stone)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.30))
    tier2 = bpy.context.active_object
    tier2.scale = (0.60, 0.60, 0.20)
    tier2.data.materials.append(mat_stone)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.58))
    tier3 = bpy.context.active_object
    tier3.scale = (0.48, 0.48, 0.36)
    tier3.data.materials.append(mat_stone)

    # 2. Golden Commemorative Inscribed Plaque on front
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.25, 0.58))
    plaque = bpy.context.active_object
    plaque.scale = (0.34, 0.02, 0.20)
    plaque.data.materials.append(mat_gold)

    # 3. Golden Pedestal Crown Cap
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.78))
    cap = bpy.context.active_object
    cap.scale = (0.54, 0.54, 0.06)
    cap.data.materials.append(mat_gold)

    # 4. Conquered Warlord Battleaxe mounted across trophy
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.85, vertices=10, location=(0, 0, 1.05))
    axe_shaft = bpy.context.active_object
    axe_shaft.rotation_euler = (0, math.radians(45), 0)
    axe_shaft.data.materials.append(mat_steel)

    # Axe double crescent blade
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.22, 0, 1.25))
    axe_blade = bpy.context.active_object
    axe_blade.scale = (0.16, 0.03, 0.24)
    axe_blade.rotation_euler = (0, math.radians(45), 0)
    axe_blade.data.materials.append(mat_steel)

    # 5. Two Curving Warlord Horns mounted on trophy
    for sign in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.06, depth=0.45, vertices=10, location=(sign * 0.18, 0, 0.98))
        horn = bpy.context.active_object
        horn.rotation_euler = (math.radians(-15), math.radians(sign * 45), math.radians(sign * 20))
        horn.data.materials.append(mat_horn)

    # 6. Radiant Crown of Conquest on center crest
    bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.02, location=(0, 0, 0.88))
    crown_ring = bpy.context.active_object
    crown_ring.data.materials.append(mat_gold)

    for i in range(5):
        ang = math.radians(i * 72)
        cx = 0.12 * math.cos(ang)
        cy = 0.12 * math.sin(ang)
        bpy.ops.mesh.primitive_cone_add(radius1=0.025, depth=0.08, vertices=6, location=(cx, cy, 0.94))
        crown_spire = bpy.context.active_object
        crown_spire.data.materials.append(mat_gold)

    # Center glowing ruby jewel in trophy crown
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.06, vertices=8, location=(0, 0, 0.92))
    crest_gem = bpy.context.active_object
    crest_gem.rotation_euler = (math.radians(180), 0, 0)
    crest_gem.data.materials.append(mat_ruby_crest)

    export_glb("boss_trophy.glb")

if __name__ == "__main__":
    print("--- Generating Milestone 14 Models ---")
    build_gem_cutting_table()
    build_boss_trophy()
    print("--- Milestone 14 Generation Complete ---")
