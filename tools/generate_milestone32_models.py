# tools/generate_milestone32_models.py
# Voxel Lord: Feudal Realm - Milestone 32: Kinetic Transmission & Mechanical Grid Systems
# Generates 3D models for Drive Shaft, Bevel Gearbox, and Mechanical Clutch via Blender 5.2.1 LTS

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

def create_drive_shaft():
    clear_scene()

    mat_steel = create_material("ShaftSteel", (0.28, 0.29, 0.32, 1.0), roughness=0.35, metallic=0.85)
    mat_wood = create_material("BearingOak", (0.38, 0.24, 0.14, 1.0), roughness=0.85, metallic=0.0)
    mat_iron = create_material("ClampIron", (0.16, 0.16, 0.18, 1.0), roughness=0.55, metallic=0.75)
    mat_brass = create_material("BushBrass", (0.78, 0.62, 0.24, 1.0), roughness=0.30, metallic=0.90)

    # 1. Main rotating cylindrical shaft (1 meter long along X axis)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.05, depth=1.0, location=(0, 0, 0))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (0, math.radians(90), 0)
    shaft.data.materials.append(mat_steel)

    # 2. Left and Right end coupling flanges (teeth cogs for interlocking)
    for x_pos in [-0.48, 0.48]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.085, depth=0.04, location=(x_pos, 0, 0))
        flange = bpy.context.active_object
        flange.rotation_euler = (0, math.radians(90), 0)
        flange.data.materials.append(mat_iron)

        # Spline teeth around flange
        for i in range(4):
            angle = i * (math.pi / 2.0)
            y_off = math.cos(angle) * 0.08
            z_off = math.sin(angle) * 0.08
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, y_off, z_off))
            spline = bpy.context.active_object
            spline.scale = (0.04, 0.02, 0.02)
            spline.data.materials.append(mat_steel)

    # 3. Central Pillow Block Bearing Bracket (Oak wood base mounting)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.12))
    base = bpy.context.active_object
    base.scale = (0.22, 0.28, 0.12)
    base.data.materials.append(mat_wood)

    # Mounting base plate lugs with bolt holes
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.17))
    foot = bpy.context.active_object
    foot.scale = (0.26, 0.36, 0.03)
    foot.data.materials.append(mat_iron)

    # 4. Central Brass Bearing Bushing Ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.068, depth=0.14, location=(0, 0, 0))
    bush = bpy.context.active_object
    bush.rotation_euler = (0, math.radians(90), 0)
    bush.data.materials.append(mat_brass)

    # 5. Top Iron Retaining Strap / Bearing Cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.09, depth=0.18, location=(0, 0, 0))
    cap = bpy.context.active_object
    cap.rotation_euler = (0, math.radians(90), 0)
    cap.scale = (1.0, 1.0, 0.5)
    cap.location.z = 0.03
    cap.data.materials.append(mat_iron)

    # Clamping bolts
    for y_b in [-0.10, 0.10]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.015, depth=0.12, location=(0, y_b, 0.04))
        bolt = bpy.context.active_object
        bolt.data.materials.append(mat_steel)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "drive_shaft.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def create_bevel_gearbox():
    clear_scene()

    mat_iron = create_material("GearboxIron", (0.18, 0.18, 0.20, 1.0), roughness=0.50, metallic=0.80)
    mat_bronze = create_material("BevelBronze", (0.78, 0.52, 0.22, 1.0), roughness=0.30, metallic=0.85)
    mat_steel = create_material("ShaftSteel", (0.30, 0.32, 0.35, 1.0), roughness=0.35, metallic=0.90)

    # 1. Main cubical cast-iron gearbox casing (0.64m cube)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    casing = bpy.context.active_object
    casing.scale = (0.62, 0.62, 0.58)
    casing.data.materials.append(mat_iron)

    # Outer reinforcement ribs
    for i in [-0.31, 0.31]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(i, 0, 0))
        rib_x = bpy.context.active_object
        rib_x.scale = (0.04, 0.66, 0.62)
        rib_x.data.materials.append(mat_iron)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, i, 0))
        rib_y = bpy.context.active_object
        rib_y.scale = (0.66, 0.04, 0.62)
        rib_y.data.materials.append(mat_iron)

    # 2. Four shaft collar ports protruding from faces (+X, -X, +Y, -Y)
    collar_offsets = [
        (0.35, 0, 0, 0, math.radians(90), 0),
        (-0.35, 0, 0, 0, math.radians(90), 0),
        (0, 0.35, 0, math.radians(90), 0, 0),
        (0, -0.35, 0, math.radians(90), 0, 0)
    ]
    for x, y, z, rx, ry, rz in collar_offsets:
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.09, depth=0.14, location=(x, y, z))
        collar = bpy.context.active_object
        collar.rotation_euler = (rx, ry, rz)
        collar.data.materials.append(mat_iron)

        # Protruding stub shaft
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.05, depth=0.22, location=(x * 1.15, y * 1.15, z))
        stub = bpy.context.active_object
        stub.rotation_euler = (rx, ry, rz)
        stub.data.materials.append(mat_steel)

    # 3. Top inspection dome / bevel gear viewing recess
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=0.12, location=(0, 0, 0.30))
    dome = bpy.context.active_object
    dome.data.materials.append(mat_iron)

    # 4. Interlocking Conical Bevel Gears (45-degree miter gears inside top)
    # Gear 1 along X axis
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.18, radius2=0.08, depth=0.10, location=(-0.05, 0, 0.28))
    gear1 = bpy.context.active_object
    gear1.rotation_euler = (0, math.radians(90), 0)
    gear1.data.materials.append(mat_bronze)

    # Gear 2 along Y axis interlocking at 90 degrees
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.18, radius2=0.08, depth=0.10, location=(0, -0.05, 0.28))
    gear2 = bpy.context.active_object
    gear2.rotation_euler = (math.radians(-90), 0, 0)
    gear2.data.materials.append(mat_bronze)

    # 5. Base Mounting Flange
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.30))
    mount = bpy.context.active_object
    mount.scale = (0.72, 0.72, 0.04)
    mount.data.materials.append(mat_iron)

    # Corner mounting bolts
    for bx in [-0.32, 0.32]:
        for by in [-0.32, 0.32]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.08, location=(bx, by, -0.28))
            b = bpy.context.active_object
            b.data.materials.append(mat_steel)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "bevel_gearbox.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def create_mechanical_clutch():
    clear_scene()

    mat_iron = create_material("ClutchIron", (0.20, 0.20, 0.22, 1.0), roughness=0.55, metallic=0.75)
    mat_steel = create_material("ShaftSteel", (0.30, 0.32, 0.35, 1.0), roughness=0.35, metallic=0.85)
    mat_wood = create_material("LeverWood", (0.42, 0.26, 0.14, 1.0), roughness=0.80, metallic=0.0)
    mat_brass = create_material("LeverKnob", (0.82, 0.65, 0.22, 1.0), roughness=0.25, metallic=0.90)

    # 1. Base mount platform
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.16))
    base = bpy.context.active_object
    base.scale = (0.88, 0.36, 0.08)
    base.data.materials.append(mat_wood)

    # Side bearing stanchions
    for x in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, -0.04))
        stanchion = bpy.context.active_object
        stanchion.scale = (0.08, 0.24, 0.24)
        stanchion.data.materials.append(mat_iron)

    # 2. Input and Output Split Shafts (X axis)
    # Left (Input) shaft
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.05, depth=0.45, location=(-0.25, 0, 0))
    s_in = bpy.context.active_object
    s_in.rotation_euler = (0, math.radians(90), 0)
    s_in.data.materials.append(mat_steel)

    # Right (Output) shaft
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.05, depth=0.45, location=(0.25, 0, 0))
    s_out = bpy.context.active_object
    s_out.rotation_euler = (0, math.radians(90), 0)
    s_out.data.materials.append(mat_steel)

    # 3. Dual Cast-Iron Friction Clutch Discs
    # Driving disc (Input side)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.22, depth=0.05, location=(-0.035, 0, 0))
    disc1 = bpy.context.active_object
    disc1.rotation_euler = (0, math.radians(90), 0)
    disc1.data.materials.append(mat_iron)

    # Driven sliding disc (Output side with friction lining)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.22, depth=0.05, location=(0.035, 0, 0))
    disc2 = bpy.context.active_object
    disc2.rotation_euler = (0, math.radians(90), 0)
    disc2.data.materials.append(mat_iron)

    # 4. Heavy Spring Tensioner (Splined sleeve on output side)
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.09, depth=0.14, location=(0.14, 0, 0))
    sleeve = bpy.context.active_object
    sleeve.rotation_euler = (0, math.radians(90), 0)
    sleeve.data.materials.append(mat_steel)

    # Coil spring ribs
    for x_s in [0.09, 0.12, 0.15, 0.18]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.095, minor_radius=0.012, location=(x_s, 0, 0))
        coil = bpy.context.active_object
        coil.rotation_euler = (0, math.radians(90), 0)
        coil.data.materials.append(mat_steel)

    # 5. Clutch Shifting Fork & Mechanical Hand Lever
    # Shift yoke collar ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.016, location=(0.04, 0, 0))
    yoke = bpy.context.active_object
    yoke.rotation_euler = (0, math.radians(90), 0)
    yoke.data.materials.append(mat_iron)

    # Fork arms reaching down to pivot pin
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.018, depth=0.24, location=(0.04, 0.12, -0.06))
    arm1 = bpy.context.active_object
    arm1.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.018, depth=0.24, location=(0.04, -0.12, -0.06))
    arm2 = bpy.context.active_object
    arm2.data.materials.append(mat_iron)

    # Pivot cross-pin
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.32, location=(0.04, 0, -0.16))
    pin = bpy.context.active_object
    pin.rotation_euler = (math.radians(90), 0, 0)
    pin.data.materials.append(mat_steel)

    # Tall engagement hand lever angled up
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.022, depth=0.65, location=(0.04, 0.16, 0.22))
    lever = bpy.context.active_object
    lever.rotation_euler = (math.radians(-15), 0, math.radians(-10))
    lever.data.materials.append(mat_wood)

    # Brass handle knob atop the lever
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=8, radius=0.045, location=(0.08, 0.24, 0.52))
    knob = bpy.context.active_object
    knob.data.materials.append(mat_brass)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "mechanical_clutch.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def main():
    print("[BLENDER] Starting Milestone 32 3D Model Generation...")
    create_drive_shaft()
    create_bevel_gearbox()
    create_mechanical_clutch()
    print("[BLENDER] Milestone 32 3D Models Complete!")

if __name__ == "__main__":
    main()
