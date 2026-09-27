# tools/generate_milestone39_models.py
# Procedural 3D model generator for Milestone 39: High-Pressure Steam Power
# Overhauled with high-poly industrial micro-details, glowing firebox embers, and rich PBR materials
# 1. steam_boiler.glb - High-Pressure Multi-Tube Steam Boiler
# 2. steam_engine_drive.glb - Horizontal Stationary Double-Acting Steam Engine
# 3. centrifugal_governor.glb - James Watt Flyball Centrifugal Speed Governor

import bpy
import os
import math

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_pbr_material(name, color, roughness=0.5, metallic=0.0,
                        emission_color=(0.0, 0.0, 0.0, 1.0), emission_strength=0.0,
                        bump_type=None, bump_strength=0.2, bump_scale=15.0,
                        clearcoat=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if 'Coat Weight' in bsdf.inputs and clearcoat > 0:
            bsdf.inputs['Coat Weight'].default_value = clearcoat
        if emission_strength > 0:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission_color
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = emission_strength

        if bump_type == 'noise':
            noise = nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = bump_scale
            noise.inputs['Detail'].default_value = 4.0
            bump = nodes.new('ShaderNodeBump')
            bump.inputs['Strength'].default_value = bump_strength
            links.new(noise.outputs['Fac'], bump.inputs['Height'])
            links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
        elif bump_type == 'wood':
            wave = nodes.new('ShaderNodeTexWave')
            wave.inputs['Scale'].default_value = bump_scale
            wave.inputs['Distortion'].default_value = 2.0
            bump = nodes.new('ShaderNodeBump')
            bump.inputs['Strength'].default_value = bump_strength
            links.new(wave.outputs['Fac'], bump.inputs['Height'])
            links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

def get_output_path(filename):
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, filename)

def export_gltf(filepath):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORT] Generated: {filepath}")

# ==========================================
# 1. HIGH-PRESSURE STEAM BOILER
# ==========================================
def build_steam_boiler():
    clear_scene()

    mat_brick = create_pbr_material("RefractoryBrick", (0.50, 0.22, 0.14, 1.0), roughness=0.88, bump_type='noise', bump_strength=0.25, bump_scale=18.0)
    mat_brass = create_pbr_material("BoilerBrassShell", (0.86, 0.68, 0.22, 1.0), roughness=0.24, metallic=0.95, clearcoat=0.2)
    mat_copper = create_pbr_material("SteamCopperPipe", (0.92, 0.48, 0.32, 1.0), roughness=0.28, metallic=0.92)
    mat_iron = create_pbr_material("BoilerCastIron", (0.16, 0.17, 0.19, 1.0), roughness=0.52, metallic=0.88)
    mat_glass = create_pbr_material("SightGlassTube", (0.88, 0.96, 1.0, 0.8), roughness=0.10, metallic=0.05, clearcoat=0.9)
    mat_dial = create_pbr_material("ManometerFace", (0.94, 0.94, 0.90, 1.0), roughness=0.25)
    mat_fire = create_pbr_material("GlowingCoalEmbers", (1.0, 0.35, 0.05, 1.0), roughness=0.9, emission_color=(1.0, 0.38, 0.05, 1.0), emission_strength=5.0)

    # --- 1. Brick Firebox Hearth Foundation ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.45))
    hearth = bpy.context.active_object
    hearth.scale = (1.85, 1.85, 0.90)
    hearth.data.materials.append(mat_brick)

    # Plinth Base Moulding
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.08))
    plinth = bpy.context.active_object
    plinth.scale = (2.00, 2.00, 0.16)
    plinth.data.materials.append(mat_iron)

    # Cast Iron Firebox Door Frame & Double Doors
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.94, 0.0, 0.48))
    door_frame = bpy.context.active_object
    door_frame.scale = (0.08, 0.78, 0.65)
    door_frame.data.materials.append(mat_iron)

    # Hinged Firedoor Leaves
    for dy in [-0.18, 0.18]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.97, dy, 0.48))
        fdoor = bpy.context.active_object
        fdoor.scale = (0.04, 0.32, 0.54)
        fdoor.data.materials.append(mat_iron)

        # Cooling Louver Ribs on Door
        for lz in [-0.15, -0.05, 0.05, 0.15]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.99, dy, 0.48 + lz))
            louver = bpy.context.active_object
            louver.scale = (0.015, 0.24, 0.025)
            louver.data.materials.append(mat_iron)

    # Firedoor Locking Latch Wheel
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.018, location=(1.02, 0.0, 0.48))
    latch = bpy.context.active_object
    latch.rotation_euler = (0, math.radians(90), 0)
    latch.data.materials.append(mat_brass)

    # Lower Ashpit Cleanout Door & Air Shutter
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.94, 0.0, 0.14))
    ash_door = bpy.context.active_object
    ash_door.scale = (0.06, 0.60, 0.18)
    ash_door.data.materials.append(mat_iron)

    # Glowing Coal Firebed inside (visible through draft openings)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.40, 0.0, 0.28))
    coals = bpy.context.active_object
    coals.scale = (0.90, 1.20, 0.15)
    coals.data.materials.append(mat_fire)

    # --- 2. Main Vertical Boiler Shell (Brass Cylindrical Drum) ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.74, depth=1.65, location=(0.0, 0.0, 1.72))
    drum = bpy.context.active_object
    drum.data.materials.append(mat_brass)

    # Circumferential Riveted Iron Retaining Bands
    band_elevations = [1.12, 1.72, 2.32]
    for bz in band_elevations:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.75, minor_radius=0.032, location=(0.0, 0.0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_iron)

        # 24 Hexagonal Rivet Heads along each band
        for r_i in range(24):
            r_ang = (r_i / 24.0) * 2.0 * math.pi
            rx = 0.77 * math.cos(r_ang)
            ry = 0.77 * math.sin(r_ang)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.018, depth=0.035, location=(rx, ry, bz))
            rivet = bpy.context.active_object
            rivet.rotation_euler = (0, math.radians(90), r_ang)
            rivet.data.materials.append(mat_iron)

    # --- 3. Upper Conical Smokebox & Flared Chimney ---
    bpy.ops.mesh.primitive_cone_add(vertices=36, radius1=0.74, radius2=0.28, depth=0.48, location=(0.0, 0.0, 2.78))
    sbox = bpy.context.active_object
    sbox.data.materials.append(mat_iron)

    # Tall Riveted Chimney Stack
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.22, depth=0.92, location=(0.0, 0.0, 3.46))
    stack = bpy.context.active_object
    stack.data.materials.append(mat_iron)

    # Flared Copper Spark Arrestor Crown
    bpy.ops.mesh.primitive_torus_add(major_radius=0.26, minor_radius=0.045, location=(0.0, 0.0, 3.90))
    crown = bpy.context.active_object
    crown.data.materials.append(mat_copper)

    # Chimney Draft Damper Counterweight Lever
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.45, location=(0.22, 0.0, 3.30))
    damper_rod = bpy.context.active_object
    damper_rod.rotation_euler = (0, math.radians(45), 0)
    damper_rod.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.04, location=(0.36, 0.0, 3.44))
    damper_weight = bpy.context.active_object
    damper_weight.data.materials.append(mat_iron)

    # --- 4. Water Level Column & Glass Sight Tube ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.98, location=(0.36, 0.78, 1.72))
    col_body = bpy.context.active_object
    col_body.data.materials.append(mat_brass)

    # Glass Tube with Water Level Line
    bpy.ops.mesh.primitive_cylinder_add(radius=0.026, depth=0.78, location=(0.36, 0.81, 1.72))
    col_glass = bpy.context.active_object
    col_glass.data.materials.append(mat_glass)

    # Top & Bottom Brass Isolation Petcocks
    for gz in [1.28, 2.16]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.14, location=(0.36, 0.82, gz))
        cock = bpy.context.active_object
        cock.rotation_euler = (0, math.radians(90), 0)
        cock.data.materials.append(mat_brass)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.03, minor_radius=0.008, location=(0.43, 0.82, gz))
        c_handle = bpy.context.active_object
        c_handle.rotation_euler = (0, math.radians(90), 0)
        c_handle.data.materials.append(mat_brass)

    # --- 5. Pressure Manometer & Safety Valve Levers ---
    # Manometer Bezel on Front Face
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.06, location=(0.78, 0.35, 2.10))
    gauge_bezel = bpy.context.active_object
    gauge_bezel.rotation_euler = (0, math.radians(90), 0)
    gauge_bezel.data.materials.append(mat_brass)

    # Manometer Dial Face
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.02, location=(0.82, 0.35, 2.10))
    gauge_dial = bpy.context.active_object
    gauge_dial.rotation_euler = (0, math.radians(90), 0)
    gauge_dial.data.materials.append(mat_dial)

    # Gauge Pointer Needle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.835, 0.37, 2.14))
    g_pointer = bpy.context.active_object
    g_pointer.scale = (0.01, 0.08, 0.01)
    g_pointer.rotation_euler = (math.radians(35), 0, 0)
    g_pointer.data.materials.append(mat_iron)

    # Siphon Pigtail Copper Pipe underneath Gauge
    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.015, location=(0.78, 0.35, 1.95))
    siphon = bpy.context.active_object
    siphon.data.materials.append(mat_copper)

    # Twin Weighted Popoff Safety Relief Valves on Boiler Crown
    for vy in [-0.28, 0.28]:
        # Valve Base Flange
        bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.28, location=(-0.36, vy, 2.68))
        v_base = bpy.context.active_object
        v_base.data.materials.append(mat_brass)

        # Fulcrum Arm Lever
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.36 + 0.15, vy, 2.84))
        v_lever = bpy.context.active_object
        v_lever.scale = (0.42, 0.025, 0.03)
        v_lever.data.materials.append(mat_iron)

        # Cylindrical Poise Counterweight
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.10, location=(-0.36 + 0.32, vy, 2.84))
        v_weight = bpy.context.active_object
        v_weight.rotation_euler = (math.radians(90), 0, 0)
        v_weight.data.materials.append(mat_iron)

    # High-Pressure Copper Steam Manifold Pipe with Flanged Handwheel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.75, location=(-0.78, 0.0, 2.22))
    steam_out = bpy.context.active_object
    steam_out.rotation_euler = (0, math.radians(90), 0)
    steam_out.data.materials.append(mat_copper)

    # Main Steam Isolation Valve Handwheel
    bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.02, location=(-0.92, 0.0, 2.22))
    valve_wheel = bpy.context.active_object
    valve_wheel.rotation_euler = (0, math.radians(90), 0)
    valve_wheel.data.materials.append(mat_iron)

    # Flange Connecting Rings
    for fx in [-0.55, -0.85]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.04, location=(fx, 0.0, 2.22))
        flange = bpy.context.active_object
        flange.rotation_euler = (0, math.radians(90), 0)
        flange.data.materials.append(mat_brass)

    export_gltf(get_output_path("steam_boiler.glb"))

# ==========================================
# 2. HORIZONTAL STATIONARY STEAM ENGINE
# ==========================================
def build_steam_engine_drive():
    clear_scene()

    mat_green_bed = create_pbr_material("IndustrialGreenCast", (0.12, 0.24, 0.16, 1.0), roughness=0.48, metallic=0.75, clearcoat=0.35)
    mat_machined_steel = create_pbr_material("BrightMachinedSteel", (0.80, 0.82, 0.85, 1.0), roughness=0.18, metallic=0.98)
    mat_teak = create_pbr_material("TeakCylinderLagging", (0.36, 0.18, 0.09, 1.0), roughness=0.62, bump_type='wood', bump_strength=0.22, bump_scale=14.0)
    mat_bronze = create_pbr_material("PhosphorBronzeBearings", (0.75, 0.54, 0.22, 1.0), roughness=0.28, metallic=0.92)
    mat_brass = create_pbr_material("EngineBrassFittings", (0.88, 0.70, 0.24, 1.0), roughness=0.22, metallic=0.96)
    mat_flywheel = create_pbr_material("CastIronFlywheel", (0.18, 0.19, 0.21, 1.0), roughness=0.42, metallic=0.92)

    # --- 1. Heavy Cast-Iron Engine Bedplate ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.18))
    bed = bpy.context.active_object
    bed.scale = (3.50, 1.35, 0.36)
    bed.data.materials.append(mat_green_bed)

    # 4 Foundation Hold-Down Anchor Bolts with Square Washers
    for ax, ay in [(-1.55, -0.55), (-1.55, 0.55), (1.55, -0.55), (1.55, 0.55)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ax, ay, 0.37))
        washer = bpy.context.active_object
        washer.scale = (0.10, 0.10, 0.03)
        washer.data.materials.append(mat_machined_steel)

        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.035, depth=0.06, location=(ax, ay, 0.40))
        nut = bpy.context.active_object
        nut.data.materials.append(mat_machined_steel)

    # Machined Bright Steel Top Guideways
    for gy in [-0.14, 0.14]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.10, gy, 0.38))
        guideway = bpy.context.active_object
        guideway.scale = (1.15, 0.08, 0.04)
        guideway.data.materials.append(mat_machined_steel)

    # --- 2. Steam Cylinder Assembly with Wood Lagging ---
    cyl_center_x = -1.18
    cyl_center_z = 0.68

    # Main Steam Cylinder (Wooden Stave Lagging)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.44, depth=1.15, location=(cyl_center_x, 0.0, cyl_center_z))
    cylinder = bpy.context.active_object
    cylinder.rotation_euler = (0, math.radians(90), 0)
    cylinder.data.materials.append(mat_teak)

    # Twin Polished Brass Retention Bands with Tension Screws
    for bx in [cyl_center_x - 0.32, cyl_center_x + 0.32]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.02, location=(bx, 0.0, cyl_center_z))
        c_band = bpy.context.active_object
        c_band.rotation_euler = (0, math.radians(90), 0)
        c_band.data.materials.append(mat_brass)

    # Flanged Bronze Front & Rear Cylinder Head Covers with Stud Bolts
    for cx in [cyl_center_x - 0.60, cyl_center_x + 0.60]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.47, depth=0.09, location=(cx, 0.0, cyl_center_z))
        chead = bpy.context.active_object
        chead.rotation_euler = (0, math.radians(90), 0)
        chead.data.materials.append(mat_bronze)

        # 8 Perimeter Stud Bolts on each head
        for s_i in range(8):
            s_ang = (s_i / 8.0) * 2.0 * math.pi
            sy = 0.40 * math.sin(s_ang)
            sz = cyl_center_z + 0.40 * math.cos(s_ang)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.02, depth=0.04, location=(cx + (0.05 if cx > cyl_center_x else -0.05), sy, sz))
            stud = bpy.context.active_object
            stud.rotation_euler = (0, math.radians(90), 0)
            stud.data.materials.append(mat_machined_steel)

    # Top Steam Slide-Valve Chest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cyl_center_x, 0.0, cyl_center_z + 0.54))
    vchest = bpy.context.active_object
    vchest.scale = (0.80, 0.40, 0.36)
    vchest.data.materials.append(mat_green_bed)

    # Valve Stem & Stuffing Box Gland
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.65, location=(cyl_center_x + 0.48, 0.0, cyl_center_z + 0.54))
    vstem = bpy.context.active_object
    vstem.rotation_euler = (0, math.radians(90), 0)
    vstem.data.materials.append(mat_machined_steel)

    # --- 3. Piston Rod, Crosshead & Machined Slipper ---
    # Precision Machined Piston Rod
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=1.15, location=(-0.15, 0.0, cyl_center_z))
    piston_rod = bpy.context.active_object
    piston_rod.rotation_euler = (0, math.radians(90), 0)
    piston_rod.data.materials.append(mat_machined_steel)

    # Crosshead Box Slider
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.10, 0.0, cyl_center_z))
    crosshead = bpy.context.active_object
    crosshead.scale = (0.32, 0.24, 0.24)
    crosshead.data.materials.append(mat_machined_steel)

    # Bronze Slipper Shoes (Top and Bottom)
    for sz in [cyl_center_z - 0.13, cyl_center_z + 0.13]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.10, 0.0, sz))
        shoe = bpy.context.active_object
        shoe.scale = (0.34, 0.14, 0.035)
        shoe.data.materials.append(mat_bronze)

    # Brass Crosshead Lubricator Cup
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.08, location=(-0.10, 0.0, cyl_center_z + 0.20))
    x_cup = bpy.context.active_object
    x_cup.data.materials.append(mat_brass)

    # --- 4. Forged Steel Connecting Rod with Marine-Pattern Brasses ---
    conrod_center_x = 0.58
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(conrod_center_x, 0.0, cyl_center_z))
    conrod = bpy.context.active_object
    conrod.scale = (1.20, 0.065, 0.12)
    conrod.data.materials.append(mat_machined_steel)

    # Big-End Split Bronze Bearing Shells & Retaining Strap
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.12, location=(1.18, 0.0, cyl_center_z))
    big_end = bpy.context.active_object
    big_end.rotation_euler = (math.radians(90), 0, 0)
    big_end.data.materials.append(mat_bronze)

    # Steel Strap Cotter Wedge & Gib Key
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.10, 0.0, cyl_center_z + 0.09))
    cotter = bpy.context.active_object
    cotter.scale = (0.04, 0.08, 0.14)
    cotter.data.materials.append(mat_machined_steel)

    # --- 5. Balanced Crankshaft, Twin Webs & Main Bearings ---
    crank_x = 1.25

    # Twin Counterbalanced Crank Webs (Crescent Counterweights)
    for cwy in [-0.14, 0.14]:
        # Rectangular crank arm
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(crank_x, cwy, cyl_center_z + 0.12))
        c_arm = bpy.context.active_object
        c_arm.scale = (0.16, 0.06, 0.44)
        c_arm.data.materials.append(mat_machined_steel)

        # Counterbalance crescent weight on opposite side
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.26, depth=0.06, location=(crank_x, cwy, cyl_center_z - 0.18))
        c_weight = bpy.context.active_object
        c_weight.rotation_euler = (math.radians(90), 0, 0)
        c_weight.scale = (1.2, 0.7, 1.0)
        c_weight.data.materials.append(mat_green_bed)

    # Crankpin between Webs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.22, location=(crank_x, 0.0, cyl_center_z + 0.30))
    crankpin = bpy.context.active_object
    crankpin.rotation_euler = (math.radians(90), 0, 0)
    crankpin.data.materials.append(mat_machined_steel)

    # Main Ground Steel Crankshaft Transverse Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.095, depth=1.75, location=(crank_x, 0.38, cyl_center_z))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (math.radians(90), 0, 0)
    shaft.data.materials.append(mat_machined_steel)

    # Pillow Block Bearing Pedestals with Split Bronze Bushings & Brass Oilers
    for py in [0.26, 0.60]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(crank_x, py, 0.48))
        pedestal = bpy.context.active_object
        pedestal.scale = (0.34, 0.20, 0.32)
        pedestal.data.materials.append(mat_green_bed)

        # Bronze Bearing Cap
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.18, location=(crank_x, py, cyl_center_z))
        bcap = bpy.context.active_object
        bcap.rotation_euler = (math.radians(90), 0, 0)
        bcap.data.materials.append(mat_bronze)

        # Brass Sight-Feed Drip Lubricator on Pedestal
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.08, location=(crank_x, py, cyl_center_z + 0.18))
        oiler = bpy.context.active_object
        oiler.data.materials.append(mat_brass)

    # --- 6. Heavy 1.8m Cast-Iron Flywheel with Oval Spoke Profiles ---
    flywheel_y = 0.95
    # Heavy Outer Rim with Machined Face
    bpy.ops.mesh.primitive_torus_add(major_radius=0.92, minor_radius=0.11, location=(crank_x, flywheel_y, cyl_center_z))
    flywheel_rim = bpy.context.active_object
    flywheel_rim.rotation_euler = (math.radians(90), 0, 0)
    flywheel_rim.data.materials.append(mat_flywheel)

    # Heavy Central Hub with Keyway
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.28, depth=0.24, location=(crank_x, flywheel_y, cyl_center_z))
    fhub = bpy.context.active_object
    fhub.rotation_euler = (math.radians(90), 0, 0)
    fhub.data.materials.append(mat_flywheel)

    # Sunken Steel Shaft Key
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(crank_x, flywheel_y, cyl_center_z + 0.10))
    skey = bpy.context.active_object
    skey.scale = (0.025, 0.26, 0.025)
    skey.data.materials.append(mat_machined_steel)

    # 6 Oval-Section Spoke Profiles
    for i in range(6):
        s_angle = math.radians(i * 60)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.82, location=(crank_x, flywheel_y, cyl_center_z))
        spoke = bpy.context.active_object
        spoke.scale = (0.7, 1.0, 1.0)
        spoke.rotation_euler = (s_angle, 0, 0)
        spoke.data.materials.append(mat_flywheel)

    # Flanged Power Takeoff Belt Pulley on Outboard Shaft End
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.38, depth=0.22, location=(crank_x, 1.18, cyl_center_z))
    pulley = bpy.context.active_object
    pulley.rotation_euler = (math.radians(90), 0, 0)
    pulley.data.materials.append(mat_flywheel)

    export_gltf(get_output_path("steam_engine_drive.glb"))

# ==========================================
# 3. CENTRIFUGAL FLYBALL GOVERNOR
# ==========================================
def build_centrifugal_governor():
    clear_scene()

    mat_brass_balls = create_pbr_material("MirrorGovernorBrass", (0.92, 0.74, 0.22, 1.0), roughness=0.18, metallic=0.96, clearcoat=0.3)
    mat_steel = create_pbr_material("GovernorSpindleSteel", (0.80, 0.82, 0.84, 1.0), roughness=0.22, metallic=0.96)
    mat_pedestal = create_pbr_material("GovernorCastPlinth", (0.16, 0.17, 0.19, 1.0), roughness=0.55, metallic=0.85)
    mat_bronze = create_pbr_material("GovernorPhosphorBronze", (0.74, 0.54, 0.22, 1.0), roughness=0.28, metallic=0.92)
    mat_valve = create_pbr_material("ThrottleValveCasing", (0.24, 0.25, 0.27, 1.0), roughness=0.48, metallic=0.90)

    # --- 1. Classical Architectural Fluted Column Pedestal ---
    # Moulded Plinth Base
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.48, depth=0.12, location=(0.0, 0.0, 0.06))
    base_plinth = bpy.context.active_object
    base_plinth.data.materials.append(mat_pedestal)

    # Classical Tapered Fluted Column Shaft
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.18, depth=0.65, location=(0.0, 0.0, 0.44))
    column = bpy.context.active_object
    column.data.materials.append(mat_pedestal)

    # Column Capital & Bronze Bearing Housing
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.22, depth=0.10, location=(0.0, 0.0, 0.78))
    capital = bpy.context.active_object
    capital.data.materials.append(mat_bronze)

    # --- 2. Bevel Miter Gear Foot Drive Assembly ---
    # Vertical Miter Bevel Gear on Spindle Base
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.20, depth=0.10, location=(0.0, 0.0, 0.24))
    vert_gear = bpy.context.active_object
    vert_gear.data.materials.append(mat_bronze)

    # Horizontal Intermeshing Miter Bevel Gear
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.20, depth=0.10, location=(-0.16, 0.0, 0.24))
    horiz_gear = bpy.context.active_object
    horiz_gear.rotation_euler = (0, math.radians(-90), 0)
    horiz_gear.data.materials.append(mat_bronze)

    # Horizontal Drive Input Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.55, location=(-0.42, 0.0, 0.24))
    in_shaft = bpy.context.active_object
    in_shaft.rotation_euler = (0, math.radians(90), 0)
    in_shaft.data.materials.append(mat_steel)

    # Input Flat Belt Drive Pulley
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.22, depth=0.09, location=(-0.65, 0.0, 0.24))
    in_pulley = bpy.context.active_object
    in_pulley.rotation_euler = (0, math.radians(90), 0)
    in_pulley.data.materials.append(mat_pedestal)

    # --- 3. Ground Steel Vertical Spindle & Sliding Counterpoise ---
    bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=1.45, location=(0.0, 0.0, 1.25))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_steel)

    # Top Pivot Yoke Hub
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.09, depth=0.12, location=(0.0, 0.0, 1.88))
    top_yoke = bpy.context.active_object
    top_yoke.data.materials.append(mat_bronze)

    # Sliding Brass Collar Sleeve with Deep Oiler Annulus
    collar_z = 1.15
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.18, location=(0.0, 0.0, collar_z))
    collar = bpy.context.active_object
    collar.data.materials.append(mat_bronze)

    # Counterpoise Heavy Bronze Flyweight Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.045, location=(0.0, 0.0, collar_z))
    counterpoise = bpy.context.active_object
    counterpoise.data.materials.append(mat_brass_balls)

    # --- 4. Articulated Flyball Suspension Arms & Polished Flyballs ---
    for side, ang_deg in [(-1, 38), (1, -38)]:
        rad_ang = math.radians(ang_deg)

        # Upper Suspension Forged Arm from Top Yoke
        bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.65, location=(side * 0.20, 0.0, 1.62))
        u_arm = bpy.context.active_object
        u_arm.rotation_euler = (0, rad_ang, 0)
        u_arm.data.materials.append(mat_steel)

        # Top Clevis Pivot Pin
        bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.08, location=(side * 0.08, 0.0, 1.88))
        top_pin = bpy.context.active_object
        top_pin.rotation_euler = (math.radians(90), 0, 0)
        top_pin.data.materials.append(mat_steel)

        # Mirror-Polished Heavy Brass Flyball (0.24m Diameter)
        ball_x = side * 0.40
        ball_z = 1.38
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.13, location=(ball_x, 0.0, ball_z))
        ball = bpy.context.active_object
        ball.data.materials.append(mat_brass_balls)

        # Lower Articulated Drop Link Connecting Ball to Sliding Collar
        bpy.ops.mesh.primitive_cylinder_add(radius=0.020, depth=0.52, location=(side * 0.22, 0.0, 1.25))
        l_arm = bpy.context.active_object
        l_arm.rotation_euler = (0, -rad_ang, 0)
        l_arm.data.materials.append(mat_steel)

        # Collar Clevis Pin
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.08, location=(side * 0.08, 0.0, collar_z))
        bot_pin = bpy.context.active_object
        bot_pin.rotation_euler = (math.radians(90), 0, 0)
        bot_pin.data.materials.append(mat_steel)

    # --- 5. Throttle Rocker Fork, Linkage Rod & Valve Body ---
    # Rocker Yoke Fork Gripping Collar Groove
    bpy.ops.mesh.primitive_torus_add(major_radius=0.10, minor_radius=0.018, location=(0.0, 0.0, collar_z))
    yoke_ring = bpy.context.active_object
    yoke_ring.data.materials.append(mat_bronze)

    # Pivoting Rocker Beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.32, 0.0, collar_z))
    rocker = bpy.context.active_object
    rocker.scale = (0.58, 0.045, 0.045)
    rocker.data.materials.append(mat_steel)

    # Fulcrum Bracket Stanchion from Column
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.30, 0.0, 0.98))
    fulcrum = bpy.context.active_object
    fulcrum.scale = (0.06, 0.08, 0.36)
    fulcrum.data.materials.append(mat_pedestal)

    # Vertical Regulating Linkage Rod with Turnbuckle Adjuster
    bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.48, location=(0.58, 0.0, collar_z - 0.20))
    link_rod = bpy.context.active_object
    link_rod.data.materials.append(mat_steel)

    # Brass Turnbuckle Hex Body
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=0.12, location=(0.58, 0.0, collar_z - 0.20))
    turnbuckle = bpy.context.active_object
    turnbuckle.data.materials.append(mat_brass_balls)

    # Cast Throttle Valve Body
    valve_z = collar_z - 0.44
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.0, valve_z))
    vbody = bpy.context.active_object
    vbody.scale = (0.24, 0.32, 0.28)
    vbody.data.materials.append(mat_valve)

    # Flanged Steam Through-Pipe with Flange Bolt Rings
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.72, location=(0.58, 0.0, valve_z))
    vpipe = bpy.context.active_object
    vpipe.rotation_euler = (math.radians(90), 0, 0)
    vpipe.data.materials.append(mat_valve)

    for py in [-0.34, 0.34]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.04, location=(0.58, py, valve_z))
        vflange = bpy.context.active_object
        vflange.rotation_euler = (math.radians(90), 0, 0)
        vflange.data.materials.append(mat_valve)

    export_gltf(get_output_path("centrifugal_governor.glb"))

def main():
    print("=== Generating Milestone 39 Models (High-Fidelity Detailing) ===")
    build_steam_boiler()
    build_steam_engine_drive()
    build_centrifugal_governor()
    print("=== Milestone 39 Generation Complete ===")

if __name__ == "__main__":
    main()
