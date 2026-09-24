"""Blender 5.2 Headless Model Generator for Milestone 12:
1. compost_bin.glb (Farmer's Delight Slatted Organic Compost Bin)
2. cutting_board.glb (Farmer's Delight Butcher Block Cutting Board & Cleaver)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.6, metallic=0.0):
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
# 28. Farmer's Delight Organic Compost Bin (compost_bin.glb)
# -------------------------------------------------------------
def build_compost_bin():
    reset_scene()
    mat_timber = create_material("SlattedTimber", (0.34, 0.22, 0.12, 1.0), roughness=0.75)
    mat_compost = create_material("RichSoilCompost", (0.16, 0.11, 0.07, 1.0), roughness=0.95)
    mat_iron = create_material("CornerIron", (0.15, 0.16, 0.18, 1.0), roughness=0.4, metallic=0.85)
    mat_greens = create_material("PlantMatter", (0.28, 0.48, 0.16, 1.0), roughness=0.8)

    # 1. Four Corner Upright Timber Posts
    post_height = 0.85
    for cx in [-0.42, 0.42]:
        for cy in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, post_height * 0.5))
            post = bpy.context.active_object
            post.scale = (0.10, 0.10, post_height)
            post.data.materials.append(mat_timber)

            # Iron corner cap bracket on top
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, post_height - 0.02))
            cap = bpy.context.active_object
            cap.scale = (0.11, 0.11, 0.06)
            cap.data.materials.append(mat_iron)

    # 2. Slatted Horizontal Wall Planks with aeration gaps
    plank_tiers = [0.12, 0.32, 0.52, 0.72]
    for z in plank_tiers:
        # Front and Back Walls (Y = +/- 0.42)
        for wy in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, wy, z))
            plank = bpy.context.active_object
            plank.scale = (0.84, 0.05, 0.14)
            plank.data.materials.append(mat_timber)

        # Left and Right Walls (X = +/- 0.42)
        for wx in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0, z))
            plank = bpy.context.active_object
            plank.scale = (0.05, 0.74, 0.14)
            plank.data.materials.append(mat_timber)

    # 3. Bottom Timber Floor
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.04))
    floor = bpy.context.active_object
    floor.scale = (0.80, 0.80, 0.06)
    floor.data.materials.append(mat_timber)

    # 4. Rich Steaming Organic Compost Soil inside
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.42))
    soil = bpy.context.active_object
    soil.scale = (0.76, 0.76, 0.68)
    soil.data.materials.append(mat_compost)

    # 5. Scattered decomposing leaves and vegetable trimmings on surface
    for gx, gy in [(-0.15, -0.12), (0.18, 0.10), (-0.10, 0.22), (0.20, -0.18)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(gx, gy, 0.77), rotation=(0, 0, math.radians(25)))
        leaf = bpy.context.active_object
        leaf.scale = (0.12, 0.14, 0.03)
        leaf.data.materials.append(mat_greens)

    export_glb("compost_bin.glb")

# -------------------------------------------------------------
# 29. Farmer's Delight Culinary Cutting Board (cutting_board.glb)
# -------------------------------------------------------------
def build_cutting_board():
    reset_scene()
    mat_board = create_material("ButcherBlock", (0.52, 0.35, 0.20, 1.0), roughness=0.6)
    mat_iron = create_material("CleaverSteel", (0.22, 0.24, 0.26, 1.0), roughness=0.3, metallic=0.92)
    mat_knife_handle = create_material("KnifeHandle", (0.18, 0.12, 0.07, 1.0), roughness=0.7)
    mat_cabbage = create_material("SlicedCabbage", (0.35, 0.65, 0.25, 1.0), roughness=0.5)
    mat_meat_cube = create_material("MincedMeat", (0.60, 0.18, 0.15, 1.0), roughness=0.5)
    mat_onion = create_material("DicedOnion", (0.85, 0.82, 0.72, 1.0), roughness=0.6)

    # 1. Heavy End-Grain Timber Cutting Block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.06))
    board = bpy.context.active_object
    board.scale = (0.68, 0.48, 0.09)
    board.data.materials.append(mat_board)

    # Timber Handle on Left (-X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.41, 0, 0.06))
    handle = bpy.context.active_object
    handle.scale = (0.14, 0.16, 0.06)
    handle.data.materials.append(mat_board)

    # 2. Forged Kitchen Cleaver resting on the right side of the board
    # Cleaver Blade (Rectangular wedge)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.14, -0.05, 0.14), rotation=(0, math.radians(12), math.radians(-15)))
    cleaver = bpy.context.active_object
    cleaver.scale = (0.02, 0.26, 0.10)
    cleaver.data.materials.append(mat_iron)

    # Cleaver Handle Tang
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.18, vertices=8, location=(0.18, -0.22, 0.17), rotation=(math.radians(75), 0, math.radians(-15)))
    k_handle = bpy.context.active_object
    k_handle.data.materials.append(mat_knife_handle)

    # 3. Piles of Sliced Ingredients on Left / Center
    # Sliced Cabbage shreds
    for i in range(4):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.16 + i * 0.03, 0.08, 0.12), rotation=(0, 0, math.radians(i * 15)))
        cab = bpy.context.active_object
        cab.scale = (0.04, 0.12, 0.02)
        cab.data.materials.append(mat_cabbage)

    # Minced Raw Beef Cubes
    for mx, my in [(-0.12, -0.08), (-0.05, -0.10), (-0.08, -0.04)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx, my, 0.12))
        m_cube = bpy.context.active_object
        m_cube.scale = (0.05, 0.05, 0.04)
        m_cube.data.materials.append(mat_meat_cube)

    # Diced Onion Bits
    for ox, oy in [(-0.24, -0.04), (-0.22, 0.04), (-0.26, 0.02)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, 0.12))
        onion = bpy.context.active_object
        onion.scale = (0.03, 0.03, 0.03)
        onion.data.materials.append(mat_onion)

    export_glb("cutting_board.glb")

if __name__ == "__main__":
    print("[BLENDER] Starting Milestone 12 Farmer's Delight Model Generation...")
    build_compost_bin()
    build_cutting_board()
    print("[BLENDER] Milestone 12 Models Generated Successfully!")
