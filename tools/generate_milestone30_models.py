# tools/generate_milestone30_models.py
# Voxel Lord: Feudal Realm - Milestone 30: Stone Windmill, Flour Silo & Bakery Oven
# Generates 3D models for Stone Windmill, Flour Silo, and Baker Oven via Blender 5.2.1 LTS

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

def create_stone_windmill():
    clear_scene()

    mat_stone = create_material("WindmillStone", (0.46, 0.44, 0.42, 1.0), roughness=0.88)
    mat_wood = create_material("WindmillWood", (0.32, 0.22, 0.14, 1.0), roughness=0.82)
    mat_canvas = create_material("SailCanvas", (0.88, 0.85, 0.78, 1.0), roughness=0.90)
    mat_door = create_material("WindmillDoor", (0.22, 0.15, 0.09, 1.0), roughness=0.80)

    # 1. Main tapered stone masonry tower
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=1.4, radius2=1.05, depth=3.6, location=(0, 0, 1.8))
    tower = bpy.context.active_object
    tower.data.materials.append(mat_stone)

    # Arched entrance door at base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.35, 0.65))
    door = bpy.context.active_object
    door.scale = (0.55, 0.2, 1.1)
    door.data.materials.append(mat_door)

    # 2. Conical timber shingle rotating roof cap
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=1.25, radius2=0.05, depth=1.4, location=(0, 0, 4.3))
    roof = bpy.context.active_object
    roof.data.materials.append(mat_wood)

    # 3. Horizontal timber windshaft axle protruding forward
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.12, depth=0.85, location=(0, -1.0, 3.9))
    axle = bpy.context.active_object
    axle.rotation_euler = (math.radians(90), 0, 0)
    axle.data.materials.append(mat_wood)

    # 4. Central wooden rotor hub
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.28, depth=0.18, location=(0, -1.45, 3.9))
    hub = bpy.context.active_object
    hub.rotation_euler = (math.radians(90), 0, 0)
    hub.data.materials.append(mat_wood)

    # 5. Four cross-timber lattice sail arms with canvas cloth
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        # Lattice beam
        bx = math.sin(rad) * 1.1
        bz = 3.9 + math.cos(rad) * 1.1
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, -1.48, bz))
        beam = bpy.context.active_object
        beam.scale = (0.06, 0.05, 2.2)
        beam.rotation_euler = (0, -rad, 0)
        beam.data.materials.append(mat_wood)

        # Canvas sail blade
        cx = math.sin(rad) * 1.15 + math.cos(rad) * 0.18
        cz = 3.9 + math.cos(rad) * 1.15 - math.sin(rad) * 0.18
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, -1.50, cz))
        sail = bpy.context.active_object
        sail.scale = (0.35, 0.02, 1.8)
        sail.rotation_euler = (0, -rad, math.radians(12)) # Slight pitch angle
        sail.data.materials.append(mat_canvas)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "stone_windmill.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_flour_silo():
    clear_scene()

    mat_wood = create_material("SiloTimber", (0.38, 0.26, 0.16, 1.0), roughness=0.82)
    mat_iron = create_material("SiloIron", (0.18, 0.18, 0.19, 1.0), roughness=0.45, metallic=0.75)
    mat_slate = create_material("SiloSlate", (0.30, 0.32, 0.34, 1.0), roughness=0.85)

    # 1. Four heavy timber support stilts
    for sx in [-0.75, 0.75]:
        for sy in [-0.75, 0.75]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, sy, 0.6))
            leg = bpy.context.active_object
            leg.scale = (0.16, 0.16, 1.2)
            leg.data.materials.append(mat_wood)

    # 2. Bottom inverted cone discharge funnel
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.95, radius2=0.22, depth=0.65, location=(0, 0, 1.45))
    funnel = bpy.context.active_object
    funnel.rotation_euler = (math.radians(180), 0, 0)
    funnel.data.materials.append(mat_iron)

    # Bottom slide gate valve
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.05))
    valve = bpy.context.active_object
    valve.scale = (0.35, 0.35, 0.15)
    valve.data.materials.append(mat_iron)

    # 3. Main cylindrical timber stave silo body
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.05, depth=2.4, location=(0, 0, 2.95))
    body = bpy.context.active_object
    body.data.materials.append(mat_wood)

    # 4. Iron reinforcement bands around body
    for bz in [1.95, 2.7, 3.45, 4.1]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.09, depth=0.06, location=(0, 0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_iron)

    # 5. Conical slate roof cap
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=1.25, radius2=0.05, depth=0.95, location=(0, 0, 4.6))
    roof = bpy.context.active_object
    roof.data.materials.append(mat_slate)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "flour_silo.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_baker_oven():
    clear_scene()

    mat_stone = create_material("OvenStoneBase", (0.42, 0.40, 0.38, 1.0), roughness=0.88)
    mat_brick = create_material("OvenRedBrick", (0.55, 0.28, 0.20, 1.0), roughness=0.85)
    mat_iron = create_material("OvenIronDoor", (0.16, 0.16, 0.17, 1.0), roughness=0.5, metallic=0.7)
    mat_wood = create_material("PeelWood", (0.48, 0.34, 0.20, 1.0), roughness=0.75)
    mat_embers = create_material("OvenEmbers", (1.0, 0.52, 0.08, 1.0), roughness=0.2,
                                 emission_color=(1.0, 0.48, 0.05, 1.0), emission_strength=4.5)

    # 1. Heavy stone hearth foundation base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.4))
    base = bpy.context.active_object
    base.scale = (1.5, 1.5, 0.8)
    base.data.materials.append(mat_stone)

    # 2. Vaulted brick masonry oven dome
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, location=(0, 0.05, 0.95))
    dome = bpy.context.active_object
    dome.scale = (1.0, 1.1, 0.85)
    dome.data.materials.append(mat_brick)

    # 3. Arched front entrance mouth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.65, 0.95))
    arch = bpy.context.active_object
    arch.scale = (0.65, 0.35, 0.5)
    arch.data.materials.append(mat_brick)

    # Glowing red ember bed inside oven opening
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.25, depth=0.1, location=(0, -0.45, 0.82))
    embers = bpy.context.active_object
    embers.data.materials.append(mat_embers)

    # Iron oven door (partially swung ajar)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.35, -0.82, 0.95))
    door = bpy.context.active_object
    door.scale = (0.45, 0.04, 0.45)
    door.rotation_euler = (0, 0, math.radians(-35))
    door.data.materials.append(mat_iron)

    # 4. Brick exhaust chimney
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.45, 1.65))
    chimney = bpy.context.active_object
    chimney.scale = (0.35, 0.35, 0.8)
    chimney.data.materials.append(mat_brick)

    # 5. Baker's wooden peel shovel propped against the side
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(0.82, -0.2, 0.85))
    peel_shaft = bpy.context.active_object
    peel_shaft.rotation_euler = (math.radians(18), math.radians(-15), 0)
    peel_shaft.data.materials.append(mat_wood)

    # Baker's peel shovel paddle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.95, -0.48, 0.22))
    paddle = bpy.context.active_object
    paddle.scale = (0.28, 0.38, 0.03)
    paddle.rotation_euler = (math.radians(18), math.radians(-15), 0)
    paddle.data.materials.append(mat_wood)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "baker_oven.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_stone_windmill()
    create_flour_silo()
    create_baker_oven()
    print("Milestone 30 3D models generated successfully!")
