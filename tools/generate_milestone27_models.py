# tools/generate_milestone27_models.py
# Voxel Lord: Feudal Realm - Milestone 27: Water Logistics & Aqueduct Irrigation
# Generates 3D models for Water Well, Aqueduct Pipe, and Water Cask via Blender 5.2.1 LTS

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

def create_water_well():
    clear_scene()

    mat_stone = create_material("WellStone", (0.42, 0.40, 0.38, 1.0), roughness=0.88)
    mat_water = create_material("WellWater", (0.15, 0.42, 0.72, 1.0), roughness=0.15)
    mat_wood = create_material("WellPillars", (0.34, 0.22, 0.12, 1.0), roughness=0.80)
    mat_roof = create_material("WellRoof", (0.24, 0.16, 0.10, 1.0), roughness=0.85)
    mat_iron = create_material("WellIron", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.7)
    mat_rope = create_material("WellRope", (0.65, 0.55, 0.42, 1.0), roughness=0.90)

    # 1. Circular cobblestone well wall (cylinder with hollow top)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.8, depth=0.85, location=(0, 0, 0.425))
    well_wall = bpy.context.active_object
    well_wall.data.materials.append(mat_stone)

    # 2. Water surface inside well
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.68, depth=0.1, location=(0, 0, 0.55))
    water = bpy.context.active_object
    water.data.materials.append(mat_water)

    # 3. Two vertical timber posts
    for x in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.85, location=(x, 0, 1.15))
        post = bpy.context.active_object
        post.data.materials.append(mat_wood)

    # 4. Winch axle beam across posts
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.65, location=(0, 0, 1.35))
    axle = bpy.context.active_object
    axle.rotation_euler = (0, math.radians(90), 0)
    axle.data.materials.append(mat_rope)

    # Iron crank handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, location=(0.85, 0.12, 1.35))
    crank = bpy.context.active_object
    crank.rotation_euler = (math.radians(90), 0, 0)
    crank.data.materials.append(mat_iron)

    # Suspended wooden bucket
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.14, depth=0.28, location=(0.15, 0, 0.85))
    bucket = bpy.context.active_object
    bucket.data.materials.append(mat_wood)

    # 5. Pitched timber shingle roof canopy
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.05, depth=1.75, location=(0, 0, 2.25))
    canopy = bpy.context.active_object
    canopy.rotation_euler = (0, math.radians(90), 0)
    canopy.scale = (0.7, 1.0, 1.0)
    canopy.data.materials.append(mat_roof)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "water_well.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_aqueduct_pipe():
    clear_scene()

    mat_stone = create_material("AqueductStone", (0.46, 0.44, 0.42, 1.0), roughness=0.85)
    mat_coping = create_material("StoneCoping", (0.38, 0.36, 0.34, 1.0), roughness=0.80)
    mat_water = create_material("AqueductWater", (0.18, 0.48, 0.78, 1.0), roughness=0.15)

    # 1. Main stone support pier pillar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.85))
    pier = bpy.context.active_object
    pier.scale = (0.7, 0.9, 1.7)
    pier.data.materials.append(mat_stone)

    # 2. Semi-circular Roman masonry arch under conduit
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.45, depth=0.92, location=(0, 0, 1.25))
    arch = bpy.context.active_object
    arch.rotation_euler = (math.radians(90), 0, 0)
    arch.data.materials.append(mat_coping)

    # 3. Elevated water flume channel (bed)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.85))
    channel_bed = bpy.context.active_object
    channel_bed.scale = (0.8, 2.4, 0.2)
    channel_bed.data.materials.append(mat_coping)

    # Side walls of flume channel
    for x in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 2.05))
        wall = bpy.context.active_object
        wall.scale = (0.1, 2.4, 0.3)
        wall.data.materials.append(mat_stone)

    # 4. Flowing water inside flume
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2.0))
    water_flow = bpy.context.active_object
    water_flow.scale = (0.6, 2.4, 0.12)
    water_flow.data.materials.append(mat_water)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "aqueduct_pipe.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_water_cask():
    clear_scene()

    mat_oak = create_material("CaskOak", (0.38, 0.25, 0.14, 1.0), roughness=0.75)
    mat_hoops = create_material("CaskHoops", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.7)
    mat_brass = create_material("BrassSpigot", (0.75, 0.62, 0.24, 1.0), roughness=0.35, metallic=0.85)
    mat_stand = create_material("StandTimber", (0.28, 0.18, 0.10, 1.0), roughness=0.85)

    # 1. Main barrel body lying horizontally
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.55, depth=1.3, location=(0, 0, 0.72))
    barrel = bpy.context.active_object
    barrel.rotation_euler = (math.radians(90), 0, 0)
    barrel.data.materials.append(mat_oak)

    # 2. Iron hoops around barrel
    for y in [-0.45, -0.18, 0.18, 0.45]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.025, location=(0, y, 0.72))
        hoop = bpy.context.active_object
        hoop.rotation_euler = (math.radians(90), 0, 0)
        hoop.data.materials.append(mat_hoops)

    # 3. Brass spigot tap on front face
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.22, location=(0, -0.72, 0.52))
    tap = bpy.context.active_object
    tap.rotation_euler = (math.radians(90), 0, 0)
    tap.data.materials.append(mat_brass)

    # 4. Timber trestle cradle stand
    for y in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, 0.22))
        cradle = bpy.context.active_object
        cradle.scale = (0.75, 0.12, 0.44)
        cradle.data.materials.append(mat_stand)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "water_cask.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_water_well()
    create_aqueduct_pipe()
    create_water_cask()
