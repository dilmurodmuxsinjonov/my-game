# tools/generate_milestone24_models.py
# Voxel Lord: Feudal Realm - Milestone 24: Animal Husbandry & Wool Textiles
# Generates 3D models for Pasture Barn, Sheep Pen, and Feeding Trough via Blender 5.2.1 LTS

import bpy
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.8, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def create_pasture_barn():
    clear_scene()
    
    # Materials
    mat_wood = create_material("BarnWood", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_dark_wood = create_material("DarkBeams", (0.22, 0.14, 0.08, 1.0), roughness=0.9)
    mat_roof = create_material("ThatchedShingle", (0.45, 0.35, 0.20, 1.0), roughness=0.9)
    mat_straw = create_material("GoldenHay", (0.85, 0.70, 0.25, 1.0), roughness=0.95)
    mat_iron = create_material("IronFittings", (0.15, 0.15, 0.18, 1.0), roughness=0.4, metallic=0.9)
    mat_stone = create_material("StoneBase", (0.42, 0.42, 0.40, 1.0), roughness=0.8)

    # 1. Stone foundation slab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    base = bpy.context.active_object
    base.scale = (4.4, 3.2, 0.3)
    base.data.materials.append(mat_stone)

    # 2. Main timber barn body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.3))
    body = bpy.context.active_object
    body.scale = (4.0, 2.8, 2.0)
    body.data.materials.append(mat_wood)

    # 3. Corner vertical timber columns (4 corners)
    corners = [(-2.0, -1.4), (2.0, -1.4), (-2.0, 1.4), (2.0, 1.4)]
    for cx, cy in corners:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=2.4, location=(cx, cy, 1.3))
        col = bpy.context.active_object
        col.data.materials.append(mat_dark_wood)

    # 4. Pitched roof (gabled prism)
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.8, depth=4.6, location=(0, 0, 2.8))
    roof = bpy.context.active_object
    roof.rotation_euler = (0, math.radians(90), 0)
    roof.scale = (1.3, 1.15, 1.0)
    roof.data.materials.append(mat_roof)

    # 5. Front Dutch double barn doors (recessed)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.42, 0.9))
    door = bpy.context.active_object
    door.scale = (1.4, 0.08, 1.5)
    door.data.materials.append(mat_dark_wood)

    # Iron door hinges and latch
    for hy in [0.4, 1.4]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.5, -1.46, hy))
        hinge_l = bpy.context.active_object
        hinge_l.scale = (0.35, 0.04, 0.08)
        hinge_l.data.materials.append(mat_iron)
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.5, -1.46, hy))
        hinge_r = bpy.context.active_object
        hinge_r.scale = (0.35, 0.04, 0.08)
        hinge_r.data.materials.append(mat_iron)

    # 6. Upper hay loft opening with straw spilling out
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.42, 2.3))
    loft_door = bpy.context.active_object
    loft_door.scale = (0.9, 0.06, 0.8)
    loft_door.data.materials.append(mat_dark_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.48, 2.0))
    hay_tuft = bpy.context.active_object
    hay_tuft.scale = (0.7, 0.25, 0.15)
    hay_tuft.data.materials.append(mat_straw)

    # 7. Exterior log hitching post with rail for oxen
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.1, location=(-1.5, -2.1, 0.55))
    hp1 = bpy.context.active_object
    hp1.data.materials.append(mat_dark_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.1, location=(1.5, -2.1, 0.55))
    hp2 = bpy.context.active_object
    hp2.data.materials.append(mat_dark_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=3.2, location=(0, -2.1, 0.95))
    h_rail = bpy.context.active_object
    h_rail.rotation_euler = (0, math.radians(90), 0)
    h_rail.data.materials.append(mat_dark_wood)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "pasture_barn.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated pasture_barn.glb -> {output_path}")

def create_sheep_pen():
    clear_scene()

    mat_wattle = create_material("WattleFence", (0.42, 0.30, 0.16, 1.0), roughness=0.9)
    mat_post = create_material("FencePost", (0.28, 0.18, 0.10, 1.0), roughness=0.85)
    mat_thatch = create_material("ThatchRoof", (0.50, 0.40, 0.22, 1.0), roughness=0.9)
    mat_wool = create_material("FluffyWool", (0.92, 0.90, 0.85, 1.0), roughness=0.98)
    mat_wicker = create_material("WickerBasket", (0.55, 0.38, 0.20, 1.0), roughness=0.85)
    mat_iron = create_material("ShearsIron", (0.20, 0.20, 0.22, 1.0), roughness=0.3, metallic=0.9)

    # 1. Enclosed wattle fence perimeter (Square enclosure 3.6m x 3.6m)
    # Posts at corners and midpoints
    fence_posts = [
        (-1.8, -1.8), (0.0, -1.8), (1.8, -1.8),
        (-1.8, 1.8), (0.0, 1.8), (1.8, 1.8),
        (-1.8, 0.0), (1.8, 0.0)
    ]
    for px, py in fence_posts:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.1, location=(px, py, 0.55))
        post = bpy.context.active_object
        post.data.materials.append(mat_post)

    # Horizontal wattle fence rails (Back, Left, Right, and partial Front for gate opening)
    rails = [
        # Back wall (Y = 1.8)
        ((0, 1.8, 0.4), (3.6, 0.06, 0.1)),
        ((0, 1.8, 0.8), (3.6, 0.06, 0.1)),
        # Left wall (X = -1.8)
        ((-1.8, 0, 0.4), (0.06, 3.6, 0.1)),
        ((-1.8, 0, 0.8), (0.06, 3.6, 0.1)),
        # Right wall (X = 1.8)
        ((1.8, 0, 0.4), (0.06, 3.6, 0.1)),
        ((1.8, 0, 0.8), (0.06, 3.6, 0.1)),
        # Front wall left section (X = -1.0, Y = -1.8)
        ((-1.0, -1.8, 0.4), (1.6, 0.06, 0.1)),
        ((-1.0, -1.8, 0.8), (1.6, 0.06, 0.1)),
        # Front wall right section (X = 1.2, Y = -1.8)
        ((1.2, -1.8, 0.4), (1.2, 0.06, 0.1)),
        ((1.2, -1.8, 0.8), (1.2, 0.06, 0.1)),
    ]
    for r_loc, r_scale in rails:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=r_loc)
        rail = bpy.context.active_object
        rail.scale = r_scale
        rail.data.materials.append(mat_wattle)

    # 2. Rustic lean-to shelter in back-left corner
    # Shelter posts
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.6, location=(-0.5, 0.6, 0.8))
    sp1 = bpy.context.active_object
    sp1.data.materials.append(mat_post)

    # Thatched canopy
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.1, 1.1, 1.6))
    canopy = bpy.context.active_object
    canopy.scale = (1.5, 1.5, 0.12)
    canopy.rotation_euler = (math.radians(-15), math.radians(10), 0)
    canopy.data.materials.append(mat_thatch)

    # 3. Wool shearing stool & iron shears
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.45, location=(0.8, -0.6, 0.225))
    stool = bpy.context.active_object
    stool.data.materials.append(mat_post)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.8, -0.6, 0.47))
    shears = bpy.context.active_object
    shears.scale = (0.22, 0.08, 0.02)
    shears.data.materials.append(mat_iron)

    # 4. Wicker baskets filled with freshly shorn wool
    basket_locs = [(0.7, 0.2), (1.2, -0.1)]
    for bx, by in basket_locs:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.4, location=(bx, by, 0.2))
        basket = bpy.context.active_object
        basket.data.materials.append(mat_wicker)

        # Fluffy fleece mound on top
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(bx, by, 0.42))
        fleece = bpy.context.active_object
        fleece.scale = (1.0, 1.0, 0.6)
        fleece.data.materials.append(mat_wool)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "sheep_pen.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated sheep_pen.glb -> {output_path}")

def create_feeding_trough():
    clear_scene()

    mat_dark_wood = create_material("TroughTimber", (0.30, 0.18, 0.10, 1.0), roughness=0.85)
    mat_hay = create_material("SilageHay", (0.80, 0.65, 0.22, 1.0), roughness=0.95)
    mat_iron = create_material("TroughIronBand", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.85)

    # 1. Main hollowed timber trough container (Length 2.2m, Width 0.8m, Height 0.6m)
    # Bottom slab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.25))
    bottom = bpy.context.active_object
    bottom.scale = (2.2, 0.8, 0.12)
    bottom.data.materials.append(mat_dark_wood)

    # Side walls (Front & Back)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.38, 0.5))
    w_front = bpy.context.active_object
    w_front.scale = (2.2, 0.08, 0.5)
    w_front.data.materials.append(mat_dark_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.38, 0.5))
    w_back = bpy.context.active_object
    w_back.scale = (2.2, 0.08, 0.5)
    w_back.data.materials.append(mat_dark_wood)

    # End caps (Left & Right)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.06, 0, 0.5))
    w_left = bpy.context.active_object
    w_left.scale = (0.08, 0.84, 0.5)
    w_left.data.materials.append(mat_dark_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.06, 0, 0.5))
    w_right = bpy.context.active_object
    w_right.scale = (0.08, 0.84, 0.5)
    w_right.data.materials.append(mat_dark_wood)

    # 2. Four sturdy splayed wooden support legs
    legs = [(-0.9, -0.35), (0.9, -0.35), (-0.9, 0.35), (0.9, 0.35)]
    for lx, ly in legs:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.45, location=(lx, ly, 0.15))
        leg = bpy.context.active_object
        leg.data.materials.append(mat_dark_wood)

    # 3. Reinforced iron banding straps
    for bx in [-0.6, 0.0, 0.6]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, 0.45))
        band = bpy.context.active_object
        band.scale = (0.06, 0.88, 0.52)
        band.data.materials.append(mat_iron)

    # 4. Lush mound of golden hay & winter silage filling the trough
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.55))
    hay = bpy.context.active_object
    hay.scale = (2.0, 0.66, 0.3)
    hay.data.materials.append(mat_hay)

    # Scattered stray stalks draping over edge
    for hx, hy in [(-0.4, -0.42), (0.3, 0.42), (0.7, -0.42)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, hy, 0.65))
        stalk = bpy.context.active_object
        stalk.scale = (0.25, 0.06, 0.08)
        stalk.rotation_euler = (math.radians(15), math.radians(20), math.radians(5))
        stalk.data.materials.append(mat_hay)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "feeding_trough.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated feeding_trough.glb -> {output_path}")

if __name__ == "__main__":
    create_pasture_barn()
    create_sheep_pen()
    create_feeding_trough()
    print("[ALL DONE] Milestone 24 models generated successfully!")
