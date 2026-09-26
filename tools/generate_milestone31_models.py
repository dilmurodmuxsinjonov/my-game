# tools/generate_milestone31_models.py
# Voxel Lord: Feudal Realm - Milestone 31: Environmental Realism & Structural Support Fixtures
# Generates 3D models for Weather Vane, Barometer Station, and Masonry Buttress via Blender 5.2.1 LTS

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

def create_weather_vane():
    clear_scene()

    mat_copper = create_material("WeatherCopper", (0.75, 0.42, 0.26, 1.0), roughness=0.35, metallic=0.85)
    mat_iron = create_material("WeatherIron", (0.16, 0.16, 0.18, 1.0), roughness=0.5, metallic=0.75)
    mat_gold = create_material("WeatherGold", (0.90, 0.72, 0.20, 1.0), roughness=0.25, metallic=0.9)

    # 1. Roof mounting bracket base (pyramidal roof saddle)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.25, radius2=0.04, depth=0.2, location=(0, 0, 0.1))
    saddle = bpy.context.active_object
    saddle.data.materials.append(mat_iron)

    # 2. Vertical spindle rod
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.025, depth=1.4, location=(0, 0, 0.75))
    rod = bpy.context.active_object
    rod.data.materials.append(mat_iron)

    # 3. Cardinal cross-arms (N-S and E-W)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.018, depth=0.8, location=(0, 0, 0.95))
    arm_ns = bpy.context.active_object
    arm_ns.rotation_euler = (math.radians(90), 0, 0)
    arm_ns.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.018, depth=0.8, location=(0, 0, 0.95))
    arm_ew = bpy.context.active_object
    arm_ew.rotation_euler = (0, math.radians(90), 0)
    arm_ew.data.materials.append(mat_iron)

    # Cardinal letter finials
    for pos, rot in [((0, 0.42, 0.95), (math.radians(90), 0, 0)), ((0, -0.42, 0.95), (math.radians(90), 0, 0)),
                     ((0.42, 0, 0.95), (0, math.radians(90), 0)), ((-0.42, 0, 0.95), (0, math.radians(90), 0))]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=pos)
        fin = bpy.context.active_object
        fin.scale = (0.06, 0.06, 0.06)
        fin.data.materials.append(mat_gold)

    # 4. Spinning arrow pointer shaft
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.9, location=(0, 0, 1.25))
    arrow_shaft = bpy.context.active_object
    arrow_shaft.rotation_euler = (0, math.radians(90), 0)
    arrow_shaft.data.materials.append(mat_copper)

    # Arrow point head
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.08, radius2=0.01, depth=0.18, location=(0.48, 0, 1.25))
    head = bpy.context.active_object
    head.rotation_euler = (0, math.radians(-90), 0)
    head.data.materials.append(mat_copper)

    # 5. Ornamental Rooster silhouette above arrow
    # Rooster body
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(-0.05, 0, 1.42))
    body = bpy.context.active_object
    body.scale = (1.4, 0.35, 1.0)
    body.data.materials.append(mat_copper)

    # Rooster tail feathers
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.18, radius2=0.02, depth=0.35, location=(-0.25, 0, 1.52))
    tail = bpy.context.active_object
    tail.rotation_euler = (0, math.radians(45), 0)
    tail.scale = (0.3, 1.0, 1.0)
    tail.data.materials.append(mat_copper)

    # Rooster head & comb
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.06, radius2=0.01, depth=0.14, location=(0.14, 0, 1.55))
    head_comb = bpy.context.active_object
    head_comb.rotation_euler = (0, math.radians(-30), 0)
    head_comb.data.materials.append(mat_gold)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "weather_vane.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_barometer_station():
    clear_scene()

    mat_oak = create_material("BarometerOak", (0.36, 0.24, 0.14, 1.0), roughness=0.80)
    mat_brass = create_material("BarometerBrass", (0.85, 0.70, 0.22, 1.0), roughness=0.30, metallic=0.9)
    mat_glass = create_material("BarometerGlass", (0.85, 0.90, 0.95, 0.7), roughness=0.15)
    mat_mercury = create_material("BarometerMercury", (0.75, 0.76, 0.78, 1.0), roughness=0.1, metallic=0.95)

    # 1. Carved oak backboard
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.05, 0.85))
    board = bpy.context.active_object
    board.scale = (0.55, 0.08, 1.6)
    board.data.materials.append(mat_oak)

    # Pediment crown molding
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.06, 1.7))
    crown = bpy.context.active_object
    crown.scale = (0.62, 0.12, 0.12)
    crown.data.materials.append(mat_oak)

    # 2. Main circular brass aneroid dial housing
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.20, depth=0.08, location=(0, -0.01, 1.25))
    dial_case = bpy.context.active_object
    dial_case.rotation_euler = (math.radians(90), 0, 0)
    dial_case.data.materials.append(mat_brass)

    # Dial face
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.17, depth=0.01, location=(0, -0.055, 1.25))
    dial_face = bpy.context.active_object
    dial_face.rotation_euler = (math.radians(90), 0, 0)
    dial_face.data.materials.append(mat_glass)

    # Pointer needle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.04, -0.062, 1.28))
    needle = bpy.context.active_object
    needle.scale = (0.12, 0.008, 0.015)
    needle.rotation_euler = (0, math.radians(40), 0)
    needle.data.materials.append(mat_brass)

    # 3. Vertical mercury tube in lower half
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.025, depth=0.65, location=(0, -0.02, 0.52))
    tube = bpy.context.active_object
    tube.data.materials.append(mat_glass)

    # Mercury liquid column inside tube
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.018, depth=0.42, location=(0, -0.02, 0.42))
    mercury = bpy.context.active_object
    mercury.data.materials.append(mat_mercury)

    # Brass measurement ruler scale plates
    for rx in [-0.08, 0.08]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, -0.01, 0.52))
        scale_plate = bpy.context.active_object
        scale_plate.scale = (0.05, 0.02, 0.6)
        scale_plate.data.materials.append(mat_brass)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "barometer_station.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_masonry_buttress():
    clear_scene()

    mat_stone = create_material("ButtressStone", (0.45, 0.43, 0.41, 1.0), roughness=0.88)
    mat_coping = create_material("ButtressCoping", (0.36, 0.35, 0.33, 1.0), roughness=0.82)

    # 1. Heavy stone foundation pier footing
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.35))
    footing = bpy.context.active_object
    footing.scale = (1.1, 1.6, 0.7)
    footing.data.materials.append(mat_stone)

    # 2. Main lower vertical support pillar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.1, 1.4))
    pillar = bpy.context.active_object
    pillar.scale = (0.9, 1.3, 1.4)
    pillar.data.materials.append(mat_stone)

    # First stone coping step
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.3, 2.15))
    step1 = bpy.context.active_object
    step1.scale = (0.94, 0.55, 0.18)
    step1.rotation_euler = (math.radians(-35), 0, 0)
    step1.data.materials.append(mat_coping)

    # 3. Slanted diagonal buttress arm rising towards wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.45, 2.65))
    arm = bpy.context.active_object
    arm.scale = (0.75, 1.1, 1.5)
    arm.rotation_euler = (math.radians(-25), 0, 0)
    arm.data.materials.append(mat_stone)

    # Top weather coping slope
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.42, 3.42))
    step2 = bpy.context.active_object
    step2.scale = (0.8, 0.85, 0.2)
    step2.rotation_euler = (math.radians(-40), 0, 0)
    step2.data.materials.append(mat_coping)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "masonry_buttress.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_weather_vane()
    create_barometer_station()
    create_masonry_buttress()
    print("Milestone 31 3D models generated successfully!")
