# tools/generate_milestone29_models.py
# Voxel Lord: Feudal Realm - Milestone 29: Road Paving, Street Lamp & Logistics Wayposts
# Generates 3D models for Paved Road Tile, Street Lamp, and Road Signpost via Blender 5.2.1 LTS

import bpy
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.8, metallic=0.0, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission_color and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def create_paved_road_tile():
    clear_scene()

    mat_mortar = create_material("RoadMortar", (0.42, 0.40, 0.38, 1.0), roughness=0.92)
    mat_stone_a = create_material("PaverStoneA", (0.48, 0.46, 0.44, 1.0), roughness=0.82)
    mat_stone_b = create_material("PaverStoneB", (0.36, 0.35, 0.34, 1.0), roughness=0.85)
    mat_curb = create_material("RoadCurb", (0.32, 0.31, 0.30, 1.0), roughness=0.78)

    # 1. Base mortar bed (2.0m x 2.0m x 0.1m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.05))
    base = bpy.context.active_object
    base.scale = (2.0, 2.0, 0.1)
    base.data.materials.append(mat_mortar)

    # 2. Left and right raised curb borders
    for x in [-0.95, 0.95]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.12))
        curb = bpy.context.active_object
        curb.scale = (0.16, 2.0, 0.14)
        curb.data.materials.append(mat_curb)

    # 3. Individual cobblestone paving blocks laid in a staggered grid
    pavers = [
        (-0.55, -0.65, 0.45, 0.55), (0.0, -0.65, 0.48, 0.52), (0.55, -0.65, 0.44, 0.56),
        (-0.35, 0.0, 0.58, 0.50), (0.35, 0.0, 0.56, 0.52),
        (-0.55, 0.65, 0.46, 0.54), (0.0, 0.65, 0.47, 0.55), (0.55, 0.65, 0.45, 0.53)
    ]
    for i, (px, py, pw, pl) in enumerate(pavers):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, py, 0.13))
        p = bpy.context.active_object
        p.scale = (pw, pl, 0.08)
        p.data.materials.append(mat_stone_a if i % 2 == 0 else mat_stone_b)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "paved_road_tile.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_street_lamp():
    clear_scene()

    mat_stone = create_material("LampStoneBase", (0.44, 0.43, 0.41, 1.0), roughness=0.85)
    mat_iron = create_material("LampForgedIron", (0.16, 0.16, 0.17, 1.0), roughness=0.45, metallic=0.75)
    mat_glass = create_material("LampGlass", (0.85, 0.88, 0.90, 0.6), roughness=0.15)
    mat_lantern_glow = create_material("LampLanternGlow", (1.0, 0.68, 0.18, 1.0), roughness=0.1,
                                       emission_color=(1.0, 0.65, 0.15, 1.0), emission_strength=5.0)

    # 1. Carved stone pedestal plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.2))
    plinth = bpy.context.active_object
    plinth.scale = (0.55, 0.55, 0.4)
    plinth.data.materials.append(mat_stone)

    # 2. Iron base collar
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=0.18, location=(0, 0, 0.48))
    collar = bpy.context.active_object
    collar.data.materials.append(mat_iron)

    # 3. Slender vertical iron lamppost shaft
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.065, depth=2.4, location=(0, 0, 1.7))
    shaft = bpy.context.active_object
    shaft.data.materials.append(mat_iron)

    # Decorative mid-shaft collar ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.11, depth=0.08, location=(0, 0, 2.1))
    mid_ring = bpy.context.active_object
    mid_ring.data.materials.append(mat_iron)

    # 4. Ornate curved bracket arms supporting lantern cage
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        bx = math.cos(rad) * 0.16
        by = math.sin(rad) * 0.16
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, 2.82))
        arm = bpy.context.active_object
        arm.scale = (0.05, 0.05, 0.22)
        arm.rotation_euler = (math.radians(25) * math.sin(rad), math.radians(25) * math.cos(rad), 0)
        arm.data.materials.append(mat_iron)

    # 5. Lantern cage bottom base
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.25, depth=0.08, location=(0, 0, 2.95))
    cage_base = bpy.context.active_object
    cage_base.data.materials.append(mat_iron)

    # 6. Glowing lantern interior (core oil flame)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.10, depth=0.28, location=(0, 0, 3.16))
    glow_core = bpy.context.active_object
    glow_core.data.materials.append(mat_lantern_glow)

    # 7. Faceted glass pane cage walls
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.22, depth=0.38, location=(0, 0, 3.16))
    glass = bpy.context.active_object
    glass.data.materials.append(mat_glass)

    # 8. Peaked iron lantern roof cap with finial
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.28, radius2=0.02, depth=0.25, location=(0, 0, 3.48))
    roof = bpy.context.active_object
    roof.data.materials.append(mat_iron)

    # Top finial ball
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(0, 0, 3.65))
    finial = bpy.context.active_object
    finial.data.materials.append(mat_iron)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "street_lamp.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_road_signpost():
    clear_scene()

    mat_wood = create_material("SignpostWood", (0.34, 0.22, 0.12, 1.0), roughness=0.85)
    mat_board = create_material("SignBoardWood", (0.42, 0.28, 0.16, 1.0), roughness=0.80)
    mat_iron = create_material("SignIronBands", (0.18, 0.18, 0.19, 1.0), roughness=0.45, metallic=0.7)

    # 1. Main timber post planted in ground
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.09, depth=2.4, location=(0, 0, 1.2))
    post = bpy.context.active_object
    post.data.materials.append(mat_wood)

    # Protective iron cap on top of post
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.11, radius2=0.01, depth=0.14, location=(0, 0, 2.45))
    post_cap = bpy.context.active_object
    post_cap.data.materials.append(mat_iron)

    # 2. Directional Fingerboard #1 (pointing towards +X / Market)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.42, 0, 2.05))
    b1 = bpy.context.active_object
    b1.scale = (0.75, 0.05, 0.18)
    b1.data.materials.append(mat_board)

    # Chevron pointer tip for Board #1
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.12, radius2=0.01, depth=0.18, location=(0.85, 0, 2.05))
    tip1 = bpy.context.active_object
    tip1.rotation_euler = (0, math.radians(-90), 0)
    tip1.scale = (1.0, 0.4, 1.0)
    tip1.data.materials.append(mat_board)

    # 3. Directional Fingerboard #2 (pointing towards -Y / Castle Keep)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.38, 1.82))
    b2 = bpy.context.active_object
    b2.scale = (0.05, 0.68, 0.18)
    b2.data.materials.append(mat_board)

    # Chevron pointer tip for Board #2
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.12, radius2=0.01, depth=0.18, location=(0, -0.78, 1.82))
    tip2 = bpy.context.active_object
    tip2.rotation_euler = (math.radians(90), 0, 0)
    tip2.scale = (0.4, 1.0, 1.0)
    tip2.data.materials.append(mat_board)

    # 4. Directional Fingerboard #3 (pointing towards -X / Mountain Mine)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.38, 0, 1.58))
    b3 = bpy.context.active_object
    b3.scale = (0.68, 0.05, 0.18)
    b3.data.materials.append(mat_board)

    # Chevron pointer tip for Board #3
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.12, radius2=0.01, depth=0.18, location=(-0.78, 0, 1.58))
    tip3 = bpy.context.active_object
    tip3.rotation_euler = (0, math.radians(90), 0)
    tip3.scale = (1.0, 0.4, 1.0)
    tip3.data.materials.append(mat_board)

    # 5. Iron mounting collar bands around post
    for bz in [1.58, 1.82, 2.05]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.10, depth=0.04, location=(0, 0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_iron)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "road_signpost.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_paved_road_tile()
    create_street_lamp()
    create_road_signpost()
    print("Milestone 29 3D models generated successfully!")
