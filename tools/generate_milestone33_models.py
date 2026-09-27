# tools/generate_milestone33_models.py
# Voxel Lord: Feudal Realm - Milestone 33: Castle Drawbridge Winch, Platform & Treadwheel Cargo Crane
# Generates 3D models for Drawbridge Winch, Drawbridge Platform, and Treadwheel Crane via Blender 5.2.1 LTS

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

def create_drawbridge_winch():
    clear_scene()

    mat_wood = create_material("WinchWood", (0.36, 0.22, 0.12, 1.0), roughness=0.85, metallic=0.0)
    mat_iron = create_material("WinchIron", (0.18, 0.18, 0.20, 1.0), roughness=0.55, metallic=0.80)
    mat_chain = create_material("WinchChain", (0.24, 0.25, 0.28, 1.0), roughness=0.40, metallic=0.85)

    # 1. Base skid timbers
    for y in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, -0.45))
        skid = bpy.context.active_object
        skid.scale = (1.4, 0.16, 0.12)
        skid.data.materials.append(mat_wood)

    # 2. Heavy A-frame timber upright cheeks (Left and Right)
    for y in [-0.40, 0.40]:
        # Left angled post
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.35, y, 0.05))
        p1 = bpy.context.active_object
        p1.scale = (0.14, 0.14, 1.1)
        p1.rotation_euler = (0, math.radians(-18), 0)
        p1.data.materials.append(mat_wood)

        # Right angled post
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.35, y, 0.05))
        p2 = bpy.context.active_object
        p2.scale = (0.14, 0.14, 1.1)
        p2.rotation_euler = (0, math.radians(18), 0)
        p2.data.materials.append(mat_wood)

        # Top bearing pillow block
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, 0.55))
        cap = bpy.context.active_object
        cap.scale = (0.24, 0.18, 0.16)
        cap.data.materials.append(mat_iron)

    # 3. Main horizontal cylindrical winding spool drum
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.18, depth=0.74, location=(0, 0, 0.55))
    drum = bpy.context.active_object
    drum.rotation_euler = (math.radians(90), 0, 0)
    drum.data.materials.append(mat_wood)

    # Steel central axle through drum
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.045, depth=1.1, location=(0, 0, 0.55))
    axle = bpy.context.active_object
    axle.rotation_euler = (math.radians(90), 0, 0)
    axle.data.materials.append(mat_iron)

    # 4. Spool chain coiling (Dual wrapped chains)
    for y_c in [-0.20, 0.20]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.22, depth=0.12, location=(0, y_c, 0.55))
        chain_coil = bpy.context.active_object
        chain_coil.rotation_euler = (math.radians(90), 0, 0)
        chain_coil.data.materials.append(mat_chain)

    # 5. Ratchet gear wheel & locking pawl
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.26, depth=0.04, location=(0, 0.38, 0.55))
    ratchet = bpy.context.active_object
    ratchet.rotation_euler = (math.radians(90), 0, 0)
    ratchet.data.materials.append(mat_iron)

    # Locking pawl lever
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.16, 0.40, 0.72))
    pawl = bpy.context.active_object
    pawl.scale = (0.16, 0.04, 0.04)
    pawl.rotation_euler = (0, math.radians(-35), 0)
    pawl.data.materials.append(mat_iron)

    # 6. Dual cast-iron four-spoke hand crank wheels (Left and Right)
    for y_h in [-0.56, 0.56]:
        # Center hub
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.08, depth=0.04, location=(0, y_h, 0.55))
        hub = bpy.context.active_object
        hub.rotation_euler = (math.radians(90), 0, 0)
        hub.data.materials.append(mat_iron)

        # 4 spokes
        for sp in [0, 45, 90, 135]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.65, location=(0, y_h, 0.55))
            spoke = bpy.context.active_object
            spoke.rotation_euler = (0, math.radians(sp), 0)
            spoke.data.materials.append(mat_iron)

        # Outer rim
        bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.025, location=(0, y_h, 0.55))
        rim = bpy.context.active_object
        rim.rotation_euler = (math.radians(90), 0, 0)
        rim.data.materials.append(mat_iron)

        # Hand grip knob
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.025, depth=0.14, location=(0.28, y_h + (0.07 if y_h > 0 else -0.07), 0.55))
        grip = bpy.context.active_object
        grip.rotation_euler = (math.radians(90), 0, 0)
        grip.data.materials.append(mat_wood)

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "drawbridge_winch.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def create_drawbridge_platform():
    clear_scene()

    mat_plank = create_material("BridgePlank", (0.42, 0.28, 0.16, 1.0), roughness=0.80, metallic=0.0)
    mat_beam = create_material("BridgeBeam", (0.32, 0.20, 0.10, 1.0), roughness=0.90, metallic=0.0)
    mat_iron = create_material("BridgeIron", (0.16, 0.16, 0.18, 1.0), roughness=0.50, metallic=0.85)

    # 1. Main Drawbridge platform deck (4m wide, 5m long, 0.18m thick)
    # Composed of heavy timber planks running lengthwise
    for p_x in range(-3, 4):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(p_x * 0.55, 0, 0))
        plank = bpy.context.active_object
        plank.scale = (0.50, 4.8, 0.16)
        plank.data.materials.append(mat_plank)

    # 2. Cross-reinforcement beams underneath
    for y_b in [-2.0, -0.7, 0.7, 2.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y_b, -0.16))
        beam = bpy.context.active_object
        beam.scale = (4.0, 0.24, 0.16)
        beam.data.materials.append(mat_beam)

    # Diagonal cross bracing
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.16))
    diag1 = bpy.context.active_object
    diag1.scale = (0.16, 4.4, 0.12)
    diag1.rotation_euler = (0, 0, math.radians(40))
    diag1.data.materials.append(mat_beam)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.16))
    diag2 = bpy.context.active_object
    diag2.scale = (0.16, 4.4, 0.12)
    diag2.rotation_euler = (0, 0, math.radians(-40))
    diag2.data.materials.append(mat_beam)

    # 3. Forged iron straps and perimeter binding
    for x_s in [-1.8, 1.8]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_s, 0, 0.09))
        strap = bpy.context.active_object
        strap.scale = (0.12, 4.8, 0.03)
        strap.data.materials.append(mat_iron)

    # Iron pyramid studs / spikes across deck
    for sx in [-1.4, -0.7, 0.0, 0.7, 1.4]:
        for sy in [-1.8, -0.9, 0.0, 0.9, 1.8]:
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.04, radius2=0.0, depth=0.04, location=(sx, sy, 0.10))
            stud = bpy.context.active_object
            stud.data.materials.append(mat_iron)

    # 4. Rear Hinge Pivot Lugs (at Y = -2.4m)
    for hx in [-1.6, 1.6]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.09, depth=0.22, location=(hx, -2.45, 0))
        hinge = bpy.context.active_object
        hinge.rotation_euler = (0, math.radians(90), 0)
        hinge.data.materials.append(mat_iron)

    # 5. Front Heavy Iron Chain Eyelets & Shackles (at Y = +2.3m)
    for ex in [-1.7, 1.7]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.03, location=(ex, 2.35, 0.15))
        eyelet = bpy.context.active_object
        eyelet.rotation_euler = (math.radians(90), 0, 0)
        eyelet.data.materials.append(mat_iron)

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "drawbridge_platform.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def create_treadwheel_crane():
    clear_scene()

    mat_wood = create_material("CraneTimber", (0.40, 0.25, 0.14, 1.0), roughness=0.85, metallic=0.0)
    mat_dark_wood = create_material("CraneRungs", (0.28, 0.18, 0.10, 1.0), roughness=0.90, metallic=0.0)
    mat_iron = create_material("CraneIron", (0.18, 0.18, 0.20, 1.0), roughness=0.50, metallic=0.85)
    mat_rope = create_material("CraneRope", (0.62, 0.54, 0.38, 1.0), roughness=0.95, metallic=0.0)

    # 1. Base sled platform
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.6))
    base = bpy.context.active_object
    base.scale = (2.6, 1.8, 0.18)
    base.data.materials.append(mat_wood)

    # 2. Main vertical A-frame tower gantry
    for y_t in [-0.7, 0.7]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.5, y_t, 1.0))
        post1 = bpy.context.active_object
        post1.scale = (0.20, 0.20, 3.2)
        post1.data.materials.append(mat_wood)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, y_t, 0.8))
        brace1 = bpy.context.active_object
        brace1.scale = (0.16, 0.16, 2.8)
        brace1.rotation_euler = (0, math.radians(-25), 0)
        brace1.data.materials.append(mat_wood)

    # 3. Giant Wooden Treadwheel Drum (Diameter ~2.6m, width ~1.1m)
    # Axle
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.10, depth=1.6, location=(-0.5, 0, 0.8))
    tw_axle = bpy.context.active_object
    tw_axle.rotation_euler = (math.radians(90), 0, 0)
    tw_axle.data.materials.append(mat_wood)

    # Dual outer rims of treadwheel
    for y_w in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_torus_add(major_radius=1.2, minor_radius=0.06, location=(-0.5, y_w, 0.8))
        rim = bpy.context.active_object
        rim.rotation_euler = (math.radians(90), 0, 0)
        rim.data.materials.append(mat_wood)

        # 6 spokes per wheel rim
        for a in range(6):
            ang = a * (math.pi / 3.0)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.035, depth=2.4, location=(-0.5, y_w, 0.8))
            sp = bpy.context.active_object
            sp.rotation_euler = (math.sin(ang), 0, math.cos(ang))
            sp.data.materials.append(mat_wood)

    # Walking rungs/slats around drum perimeter (connecting the two rims)
    for r in range(16):
        ang = r * (2.0 * math.pi / 16.0)
        rx = -0.5 + math.cos(ang) * 1.2
        rz = 0.8 + math.sin(ang) * 1.2
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, 0, rz))
        rung = bpy.context.active_object
        rung.scale = (0.06, 1.1, 0.03)
        rung.data.materials.append(mat_dark_wood)

    # 4. Outreaching Derrick Boom Arm / Crane Jib (reaching out to X = +2.5m, Z = 2.8m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.9, 0, 2.1))
    jib = bpy.context.active_object
    jib.scale = (0.22, 0.22, 3.4)
    jib.rotation_euler = (0, math.radians(45), 0)
    jib.data.materials.append(mat_wood)

    # 5. Top Pulley Block & Sheave Wheel (at jib tip)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.18, depth=0.08, location=(2.1, 0, 3.3))
    sheave = bpy.context.active_object
    sheave.rotation_euler = (math.radians(90), 0, 0)
    sheave.data.materials.append(mat_iron)

    # Sheave iron bracket
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(2.1, 0, 3.3))
    s_bracket = bpy.context.active_object
    s_bracket.scale = (0.28, 0.14, 0.38)
    s_bracket.data.materials.append(mat_iron)

    # 6. Hanging Heavy Hemp Hoisting Rope & Cargo Hook
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=2.4, location=(2.1, 0, 2.0))
    rope = bpy.context.active_object
    rope.data.materials.append(mat_rope)

    # Heavy iron lifting hook
    bpy.ops.mesh.primitive_torus_add(major_radius=0.10, minor_radius=0.03, location=(2.1, 0, 0.75))
    hook = bpy.context.active_object
    hook.rotation_euler = (0, math.radians(90), 0)
    hook.data.materials.append(mat_iron)

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "treadwheel_crane.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[BLENDER] Generated: {filepath}")

def main():
    print("[BLENDER] Starting Milestone 33 3D Model Generation...")
    create_drawbridge_winch()
    create_drawbridge_platform()
    create_treadwheel_crane()
    print("[BLENDER] Milestone 33 3D Models Complete!")

if __name__ == "__main__":
    main()
