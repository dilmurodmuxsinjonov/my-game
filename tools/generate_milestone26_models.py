# tools/generate_milestone26_models.py
# Voxel Lord: Feudal Realm - Milestone 26: Hunting Lodge, Leather Tannery & Fur Curing
# Generates 3D models for Hunting Lodge, Tannery Vat, and Fur Drying Rack via Blender 5.2.1 LTS

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

def create_hunting_lodge():
    clear_scene()

    mat_logs = create_material("LodgeLogs", (0.32, 0.20, 0.11, 1.0), roughness=0.85)
    mat_roof = create_material("WoodShingles", (0.22, 0.15, 0.09, 1.0), roughness=0.80)
    mat_stone = create_material("ChimneyStone", (0.42, 0.40, 0.38, 1.0), roughness=0.90)
    mat_antlers = create_material("DeerAntlers", (0.82, 0.78, 0.70, 1.0), roughness=0.60)
    mat_door = create_material("TimberDoor", (0.26, 0.16, 0.08, 1.0), roughness=0.75)
    mat_iron = create_material("LodgeIron", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.7)

    # 1. Main log cabin body (2.6m wide, 3.2m deep, 1.8m wall height)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.9))
    cabin = bpy.context.active_object
    cabin.scale = (2.6, 3.2, 1.8)
    cabin.data.materials.append(mat_logs)

    # 2. Sloped gable roof
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.7, depth=3.6, location=(0, 0, 2.35))
    roof = bpy.context.active_object
    roof.rotation_euler = (0, math.radians(90), 0)
    roof.scale = (0.75, 1.0, 1.0)
    roof.data.materials.append(mat_roof)

    # 3. Fieldstone chimney on right wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.45, 0.4, 1.5))
    chimney = bpy.context.active_object
    chimney.scale = (0.55, 0.7, 2.4)
    chimney.data.materials.append(mat_stone)

    # 4. Front porch roof overhang and support posts
    for x in [-1.15, 1.15]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.8, location=(x, -1.9, 0.9))
        post = bpy.context.active_object
        post.data.materials.append(mat_logs)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.75, 1.75))
    porch_roof = bpy.context.active_object
    porch_roof.scale = (2.6, 0.8, 0.12)
    porch_roof.rotation_euler = (math.radians(12), 0, 0)
    porch_roof.data.materials.append(mat_roof)

    # 5. Heavy timber door
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.61, 0.75))
    door = bpy.context.active_object
    door.scale = (0.8, 0.08, 1.45)
    door.data.materials.append(mat_door)

    # 6. Mounted stag deer antlers above entrance
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.8, location=(-0.25, -1.65, 1.6))
    antler_l = bpy.context.active_object
    antler_l.rotation_euler = (math.radians(-30), math.radians(-40), 0)
    antler_l.data.materials.append(mat_antlers)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.8, location=(0.25, -1.65, 1.6))
    antler_r = bpy.context.active_object
    antler_r.rotation_euler = (math.radians(-30), math.radians(40), 0)
    antler_r.data.materials.append(mat_antlers)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "hunting_lodge.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_tannery_vat():
    clear_scene()

    mat_staves = create_material("VatWood", (0.36, 0.24, 0.14, 1.0), roughness=0.80)
    mat_tannin = create_material("TanninBroth", (0.28, 0.16, 0.06, 1.0), roughness=0.25)
    mat_iron = create_material("VatHoops", (0.16, 0.16, 0.18, 1.0), roughness=0.45, metallic=0.7)
    mat_beam = create_material("ScrapingBeam", (0.45, 0.35, 0.22, 1.0), roughness=0.70)
    mat_steel = create_material("ScraperKnife", (0.65, 0.68, 0.72, 1.0), roughness=0.35, metallic=0.85)

    # 1. Main round soaking tub (diameter 1.8m, height 1.1m)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.9, depth=1.05, location=(0, 0, 0.53))
    vat = bpy.context.active_object
    vat.data.materials.append(mat_staves)

    # 2. Dark brown tannin soaking liquid
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.85, depth=0.1, location=(0, 0, 0.95))
    liquid = bpy.context.active_object
    liquid.data.materials.append(mat_tannin)

    # 3. Two iron reinforcing hoops around vat
    for z in [0.25, 0.82]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.91, minor_radius=0.03, location=(0, 0, z))
        hoop = bpy.context.active_object
        hoop.data.materials.append(mat_iron)

    # 4. Angled wooden scraping beam (beam horse) on side
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=1.7, location=(1.35, 0, 0.55))
    beam = bpy.context.active_object
    beam.rotation_euler = (math.radians(35), 0, math.radians(20))
    beam.data.materials.append(mat_beam)

    # Scraping beam support legs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(1.75, 0.45, 0.38))
    leg_a = bpy.context.active_object
    leg_a.rotation_euler = (math.radians(-25), 0, 0)
    leg_a.data.materials.append(mat_staves)

    # 5. Curved two-handed steel scraper knife resting on beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.25, -0.05, 0.78))
    knife = bpy.context.active_object
    knife.scale = (0.04, 0.65, 0.08)
    knife.rotation_euler = (math.radians(35), 0, math.radians(20))
    knife.data.materials.append(mat_steel)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "tannery_vat.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_fur_drying_rack():
    clear_scene()

    mat_frame = create_material("RackTimber", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_pelt_brown = create_material("DeerSkin", (0.48, 0.30, 0.16, 1.0), roughness=0.92)
    mat_pelt_white = create_material("HarePelt", (0.78, 0.75, 0.70, 1.0), roughness=0.95)
    mat_cords = create_material("Lashings", (0.60, 0.52, 0.40, 1.0), roughness=0.80)

    # 1. Main A-frame vertical posts (left & right)
    for x in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.1, location=(x, 0, 1.05))
        pole = bpy.context.active_object
        pole.data.materials.append(mat_frame)

    # 2. Horizontal support crossbars
    for z in [0.45, 1.15, 1.85]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.85, location=(0, 0, z))
        bar = bpy.context.active_object
        bar.rotation_euler = (0, math.radians(90), 0)
        bar.data.materials.append(mat_frame)

    # 3. Ground support diagonal struts
    for x in [-0.85, 0.85]:
        for rot, y in [(30, -0.4), (-30, 0.4)]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=1.0, location=(x, y, 0.45))
            strut = bpy.context.active_object
            strut.rotation_euler = (math.radians(rot), 0, 0)
            strut.data.materials.append(mat_frame)

    # 4. Large stretched deer hide on upper section
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.25, 0, 1.48))
    deer_pelt = bpy.context.active_object
    deer_pelt.scale = (0.75, 0.04, 0.55)
    deer_pelt.data.materials.append(mat_pelt_brown)

    # 5. Small hare/fox pelt on lower section
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.35, 0, 0.80))
    hare_pelt = bpy.context.active_object
    hare_pelt.scale = (0.50, 0.03, 0.45)
    hare_pelt.data.materials.append(mat_pelt_white)

    # 6. Tension tie lashings
    for x in [-0.62, 0.12]:
        for z in [1.22, 1.74]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.25, location=(x, 0, z))
            cord = bpy.context.active_object
            cord.rotation_euler = (0, math.radians(45), 0)
            cord.data.materials.append(mat_cords)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "fur_drying_rack.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_hunting_lodge()
    create_tannery_vat()
    create_fur_drying_rack()
