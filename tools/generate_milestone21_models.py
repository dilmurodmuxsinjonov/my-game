"""Generate 3D Low-Poly GLB Assets for Milestone 21:
Apothecary Herbalist Bench, Infirmary Recovery Bed, and Medicine Chest.
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
# 1. Apothecary Herbalist & Alchemist Bench (apothecary_bench.glb)
# -------------------------------------------------------------
def build_apothecary_bench(output_path):
    clear_scene()

    mat_wood = create_material("ApothecaryOak", (0.34, 0.21, 0.12, 1.0), roughness=0.8)
    mat_stone = create_material("MortarGranite", (0.48, 0.48, 0.50, 1.0), roughness=0.85)
    mat_herb = create_material("CrushedHerbs", (0.20, 0.55, 0.22, 1.0), roughness=0.9)
    mat_elixir = create_material("HealingElixir", (0.15, 0.85, 0.55, 1.0), roughness=0.15, emission=(0.15, 0.9, 0.55, 1.0), emission_strength=2.5)
    mat_ceramic = create_material("CeramicJar", (0.85, 0.80, 0.72, 1.0), roughness=0.4)
    mat_copper = create_material("AlembicCopper", (0.78, 0.45, 0.25, 1.0), roughness=0.35, metallic=0.85)

    # 4 Table Legs
    for lx in [-0.75, 0.75]:
        for ly in [-0.35, 0.35]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.42))
            leg = bpy.context.active_object
            leg.scale = (0.10, 0.10, 0.84)
            leg.data.materials.append(mat_wood)

    # Tabletop (1.7m x 0.85m x 0.08m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.86))
    top = bpy.context.active_object
    top.scale = (1.7, 0.85, 0.08)
    top.data.materials.append(mat_wood)

    # Lower Shelf
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.25))
    shelf = bpy.context.active_object
    shelf.scale = (1.5, 0.70, 0.05)
    shelf.data.materials.append(mat_wood)

    # Back Herb Rack Uprights & Top Rail
    for rx in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, 0.35, 1.35))
        post = bpy.context.active_object
        post.scale = (0.07, 0.07, 0.95)
        post.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.35, 1.80))
    rail = bpy.context.active_object
    rail.scale = (1.6, 0.12, 0.06)
    rail.data.materials.append(mat_wood)

    # Hanging Dried Herb Bundles (3 bundles from top rail)
    for hx in [-0.45, 0.0, 0.45]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.09, radius2=0.02, depth=0.32, location=(hx, 0.32, 1.58))
        bundle = bpy.context.active_object
        bundle.data.materials.append(mat_herb)

    # Stone Mortar & Pestle on right side of tabletop
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.14, location=(0.45, -0.05, 0.97))
    mortar = bpy.context.active_object
    mortar.data.materials.append(mat_stone)

    # Crushed green herb paste inside mortar
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.04, location=(0.45, -0.05, 1.03))
    paste = bpy.context.active_object
    paste.data.materials.append(mat_herb)

    # Stone Pestle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.24, location=(0.48, -0.05, 1.10))
    pestle = bpy.context.active_object
    pestle.rotation_euler = (0.35, -0.25, 0)
    pestle.data.materials.append(mat_stone)

    # Glowing Glass Distillation Flask & Copper Stand on left side
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.03, location=(-0.45, -0.05, 0.92))
    stand = bpy.context.active_object
    stand.data.materials.append(mat_copper)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(-0.45, -0.05, 1.05))
    flask = bpy.context.active_object
    flask.data.materials.append(mat_elixir)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.16, location=(-0.45, -0.05, 1.20))
    neck = bpy.context.active_object
    neck.data.materials.append(mat_elixir)

    # Apothecary Ceramic Medicine Jars in center
    for jx in [-0.12, 0.12]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.18, location=(jx, 0.08, 0.99))
        jar = bpy.context.active_object
        jar.data.materials.append(mat_ceramic)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Infirmary Recovery Bed (infirmary_bed.glb)
# -------------------------------------------------------------
def build_infirmary_bed(output_path):
    clear_scene()

    mat_frame = create_material("BedTimber", (0.36, 0.23, 0.13, 1.0), roughness=0.8)
    mat_linen = create_material("CleanLinen", (0.92, 0.90, 0.86, 1.0), roughness=0.75)
    mat_blanket = create_material("MedicBlanket", (0.72, 0.18, 0.18, 1.0), roughness=0.85)
    mat_cross = create_material("EmblemWhite", (0.96, 0.96, 0.96, 1.0), roughness=0.6)

    # 4 Corner Bedposts (Footprint: 2.1m length x 1.1m width)
    for bx, bz_h in [(-0.98, 0.95), (0.98, 0.70)]:
        for by in [-0.48, 0.48]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz_h / 2.0))
            post = bpy.context.active_object
            post.scale = (0.10, 0.10, bz_h)
            post.data.materials.append(mat_frame)

    # Wooden Bed Platform Frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.35))
    frame = bpy.context.active_object
    frame.scale = (2.0, 1.0, 0.12)
    frame.data.materials.append(mat_frame)

    # Headboard Panel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.98, 0, 0.68))
    headboard = bpy.context.active_object
    headboard.scale = (0.06, 0.96, 0.48)
    headboard.data.materials.append(mat_frame)

    # Clean White Linen Mattress
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.02, 0, 0.48))
    mattress = bpy.context.active_object
    mattress.scale = (1.88, 0.92, 0.16)
    mattress.data.materials.append(mat_linen)

    # Elevated Bolster Pillow
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.82, location=(-0.72, 0, 0.60))
    pillow = bpy.context.active_object
    pillow.rotation_euler = (1.57, 0, 0)
    pillow.scale = (1.0, 0.65, 1.0)
    pillow.data.materials.append(mat_linen)

    # Red Infirmary Blanket over lower two-thirds
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, 0, 0.50))
    blanket = bpy.context.active_object
    blanket.scale = (1.32, 0.95, 0.17)
    blanket.data.materials.append(mat_blanket)

    # White Healing Cross Emblem on Blanket
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, 0, 0.59))
    c1 = bpy.context.active_object
    c1.scale = (0.36, 0.12, 0.02)
    c1.data.materials.append(mat_cross)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, 0, 0.59))
    c2 = bpy.context.active_object
    c2.scale = (0.12, 0.36, 0.02)
    c2.data.materials.append(mat_cross)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Apothecary Medicine Chest (medicine_chest.glb)
# -------------------------------------------------------------
def build_medicine_chest(output_path):
    clear_scene()

    mat_wood = create_material("ChestWood", (0.30, 0.18, 0.10, 1.0), roughness=0.75)
    mat_iron = create_material("IronBands", (0.20, 0.20, 0.22, 1.0), roughness=0.45, metallic=0.9)
    mat_brass = create_material("BrassClasp", (0.85, 0.68, 0.22, 1.0), roughness=0.3, metallic=0.85)
    mat_bandage = create_material("BandageRoll", (0.94, 0.93, 0.89, 1.0), roughness=0.8)
    mat_poultice = create_material("PoulticeGreen", (0.22, 0.65, 0.30, 1.0), roughness=0.5)

    # Main Chest Box (0.9m x 0.55m x 0.45m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.23))
    box = bpy.context.active_object
    box.scale = (0.90, 0.55, 0.45)
    box.data.materials.append(mat_wood)

    # Iron Straps
    for sx in [-0.32, 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 0, 0.24))
        strap = bpy.context.active_object
        strap.scale = (0.06, 0.58, 0.47)
        strap.data.materials.append(mat_iron)

    # Brass Front Lockplate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.28, 0.35))
    lock = bpy.context.active_object
    lock.scale = (0.14, 0.03, 0.14)
    lock.data.materials.append(mat_brass)

    # Slightly Open Hinged Lid revealing supplies inside
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.18, 0.58))
    lid = bpy.context.active_object
    lid.rotation_euler = (-0.65, 0, 0)
    lid.scale = (0.92, 0.56, 0.10)
    lid.data.materials.append(mat_wood)

    # Rolled Sterile Bandages visible inside chest
    for bx in [-0.25, -0.08, 0.08]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.14, location=(bx, -0.05, 0.46))
        roll = bpy.context.active_object
        roll.data.materials.append(mat_bandage)

    # Herbal Poultice Jars inside chest
    for px in [0.22, 0.34]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.15, location=(px, 0.02, 0.47))
        jar = bpy.context.active_object
        jar.data.materials.append(mat_poultice)

    export_glb(output_path)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(base_dir, exist_ok=True)

    build_apothecary_bench(os.path.join(base_dir, "apothecary_bench.glb"))
    build_infirmary_bed(os.path.join(base_dir, "infirmary_bed.glb"))
    build_medicine_chest(os.path.join(base_dir, "medicine_chest.glb"))
    print("\n>>> All Milestone 21 models generated successfully! <<<")
