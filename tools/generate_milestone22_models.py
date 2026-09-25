"""Generate 3D Low-Poly GLB Assets for Milestone 22:
Woven Straw Beehive Skep, Mead Fermentation Barrel, and Beeswax Candelabra.
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
# 1. Woven Straw Beehive Skep (beehive_skep.glb)
# -------------------------------------------------------------
def build_beehive_skep(output_path):
    clear_scene()

    mat_wood = create_material("StandTimber", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_straw = create_material("SkepStraw", (0.78, 0.64, 0.26, 1.0), roughness=0.92)
    mat_honey = create_material("GoldenHoney", (0.95, 0.72, 0.12, 1.0), roughness=0.25, emission=(0.95, 0.70, 0.10, 1.0), emission_strength=0.6)
    mat_dark = create_material("HiveOpening", (0.08, 0.06, 0.04, 1.0), roughness=0.95)

    # 4 Wooden Stand Legs
    for lx in [-0.35, 0.35]:
        for ly in [-0.35, 0.35]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.22))
            leg = bpy.context.active_object
            leg.scale = (0.08, 0.08, 0.44)
            leg.data.materials.append(mat_wood)

    # Wooden Hive Base Platform + Landing Board
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.05, 0.46))
    base = bpy.context.active_object
    base.scale = (0.90, 1.00, 0.06)
    base.data.materials.append(mat_wood)

    # Stacked Woven Coils of Straw Skep Dome
    coils = [
        (0.55, 0.38, 0.08),
        (0.68, 0.37, 0.08),
        (0.81, 0.34, 0.08),
        (0.94, 0.30, 0.08),
        (1.06, 0.24, 0.07),
        (1.17, 0.16, 0.07)
    ]
    for z_pos, maj_r, min_r in coils:
        bpy.ops.mesh.primitive_torus_add(major_radius=maj_r, minor_radius=min_r, location=(0, 0, z_pos))
        ring = bpy.context.active_object
        ring.data.materials.append(mat_straw)

    # Top Cap Finial
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(0, 0, 1.25))
    cap = bpy.context.active_object
    cap.scale = (1.0, 1.0, 0.7)
    cap.data.materials.append(mat_straw)

    # Dark Bee Entrance Arch
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.42, 0.53))
    hole = bpy.context.active_object
    hole.scale = (0.16, 0.06, 0.09)
    hole.data.materials.append(mat_dark)

    # Golden Honeycomb Glaze on Landing Board
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.03, location=(0.22, -0.44, 0.50))
    comb = bpy.context.active_object
    comb.data.materials.append(mat_honey)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Mead Fermentation Barrel (mead_fermenter.glb)
# -------------------------------------------------------------
def build_mead_fermenter(output_path):
    clear_scene()

    mat_oak = create_material("BarrelOak", (0.38, 0.23, 0.12, 1.0), roughness=0.75)
    mat_iron = create_material("BarrelHoops", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.9)
    mat_brass = create_material("BrassSpigot", (0.85, 0.68, 0.20, 1.0), roughness=0.3, metallic=0.88)
    mat_glass = create_material("AirlockGlass", (0.80, 0.92, 0.95, 1.0), roughness=0.15)

    # Timber Cradle Trestles (Front and Back)
    for ty in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, ty, 0.22))
        trestle = bpy.context.active_object
        trestle.scale = (0.85, 0.12, 0.44)
        trestle.data.materials.append(mat_oak)

    # Horizontal Oak Barrel Body
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=1.15, location=(0, 0, 0.65))
    barrel = bpy.context.active_object
    barrel.rotation_euler = (1.57, 0, 0)
    barrel.data.materials.append(mat_oak)

    # 4 Wrought Iron Hoops
    for hy in [-0.46, -0.18, 0.18, 0.46]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.02, location=(0, hy, 0.65))
        hoop = bpy.context.active_object
        hoop.rotation_euler = (1.57, 0, 0)
        hoop.data.materials.append(mat_iron)

    # Brass Tap Spigot at Front
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.16, location=(0, -0.62, 0.55))
    spigot = bpy.context.active_object
    spigot.rotation_euler = (1.57, 0, 0)
    spigot.data.materials.append(mat_brass)

    # Top Fermentation Airlock Bubbler
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.22, location=(0, 0, 1.15))
    airlock = bpy.context.active_object
    airlock.data.materials.append(mat_glass)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Beeswax Standing Candelabra (candle_candelabra.glb)
# -------------------------------------------------------------
def build_candle_candelabra(output_path):
    clear_scene()

    mat_iron = create_material("WroughtStand", (0.16, 0.16, 0.18, 1.0), roughness=0.45, metallic=0.9)
    mat_wax = create_material("BeeswaxCream", (0.94, 0.86, 0.55, 1.0), roughness=0.55)
    mat_flame = create_material("WarmFlame", (1.0, 0.78, 0.22, 1.0), roughness=0.1, emission=(1.0, 0.80, 0.25, 1.0), emission_strength=4.5)

    # Circular Iron Foot Base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.06, location=(0, 0, 0.03))
    base = bpy.context.active_object
    base.data.materials.append(mat_iron)

    # Central Wrought-Iron Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=1.35, location=(0, 0, 0.70))
    shaft = bpy.context.active_object
    shaft.data.materials.append(mat_iron)

    # Horizontal 3-Branch Crossbar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.35))
    bar = bpy.context.active_object
    bar.scale = (0.72, 0.05, 0.04)
    bar.data.materials.append(mat_iron)

    # 3 Beeswax Candles & Glowing Flames
    for cx in [-0.30, 0.0, 0.30]:
        # Drip Tray
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.02, location=(cx, 0, 1.38))
        tray = bpy.context.active_object
        tray.data.materials.append(mat_iron)

        # Beeswax Pillar
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.26, location=(cx, 0, 1.52))
        candle = bpy.context.active_object
        candle.data.materials.append(mat_wax)

        # Flame Teardrop
        bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.003, depth=0.09, location=(cx, 0, 1.69))
        flame = bpy.context.active_object
        flame.data.materials.append(mat_flame)

    export_glb(output_path)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(base_dir, exist_ok=True)

    build_beehive_skep(os.path.join(base_dir, "beehive_skep.glb"))
    build_mead_fermenter(os.path.join(base_dir, "mead_fermenter.glb"))
    build_candle_candelabra(os.path.join(base_dir, "candle_candelabra.glb"))
    print("\n>>> All Milestone 22 models generated successfully! <<<")
