# tools/generate_milestone40_models.py
# Procedural 3D model generator for Milestone 40: Grand Imperial Clockwork Observatory
# Overhauled with high-poly micro-details, precision clockwork kinematics, and rich PBR materials
# 1. astronomical_clock.glb - Prague-Style Astronomical Clockwork Tower Facade
# 2. armillary_sphere.glb - Renaissance Brass Pivoting Armillary Sphere on Walnut Tripod
# 3. celestial_orrery.glb - Kinetic Clockwork Planetary Orrery with Epicyclic Gear Train

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
# 1. ASTRONOMICAL CLOCK (PRAGUE ORLOJ STYLE)
# ==========================================
def build_astronomical_clock():
    clear_scene()

    # Rich PBR Shaders
    mat_stone = create_pbr_material("GothicSandstone", (0.42, 0.40, 0.36, 1.0), roughness=0.88, bump_type='noise', bump_strength=0.18, bump_scale=20.0)
    mat_darkstone = create_pbr_material("MouldingBasalt", (0.22, 0.21, 0.20, 1.0), roughness=0.82, bump_type='noise', bump_strength=0.15, bump_scale=25.0)
    mat_gold = create_pbr_material("GildedClockworkGold", (1.0, 0.82, 0.22, 1.0), roughness=0.18, metallic=0.96, clearcoat=0.3)
    mat_brass = create_pbr_material("InstrumentBrass", (0.86, 0.70, 0.26, 1.0), roughness=0.28, metallic=0.92)
    mat_blue = create_pbr_material("CelestialLapisLazuli", (0.04, 0.12, 0.35, 1.0), roughness=0.35, bump_type='noise', bump_strength=0.08, bump_scale=30.0)
    mat_parchment = create_pbr_material("CalendarParchment", (0.88, 0.82, 0.68, 1.0), roughness=0.75)
    mat_silver = create_pbr_material("MoonlitSilver", (0.94, 0.95, 0.98, 1.0), roughness=0.15, metallic=0.92)
    mat_darkmoon = create_pbr_material("MoonUmbraIron", (0.12, 0.12, 0.14, 1.0), roughness=0.65, metallic=0.60)
    mat_iron = create_pbr_material("ForgedWroughtIron", (0.18, 0.18, 0.20, 1.0), roughness=0.55, metallic=0.88)
    mat_bell = create_pbr_material("CastBellBronze", (0.76, 0.56, 0.22, 1.0), roughness=0.32, metallic=0.92)
    mat_rope = create_pbr_material("HempDriveRope", (0.45, 0.38, 0.26, 1.0), roughness=0.90)

    # --- 1. Architectural Stone Masonry Frame ---
    # Moulded Foundation Plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.20))
    plinth_base = bpy.context.active_object
    plinth_base.scale = (1.75, 0.90, 0.40)
    plinth_base.data.materials.append(mat_darkstone)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.50))
    plinth_mid = bpy.context.active_object
    plinth_mid.scale = (1.60, 0.80, 0.30)
    plinth_mid.data.materials.append(mat_stone)

    # Flanking Gothic Buttress Pilasters
    for x in [-0.75, 0.75]:
        # Main vertical buttress shaft
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 1.95))
        pillar = bpy.context.active_object
        pillar.scale = (0.24, 0.70, 2.70)
        pillar.data.materials.append(mat_darkstone)

        # Stepped weatherings / setbacks
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 1.30))
        setback1 = bpy.context.active_object
        setback1.scale = (0.28, 0.74, 0.08)
        setback1.data.materials.append(mat_stone)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 2.65))
        setback2 = bpy.context.active_object
        setback2.scale = (0.28, 0.74, 0.08)
        setback2.data.materials.append(mat_stone)

        # Gothic Crocketed Pinnacles
        bpy.ops.mesh.primitive_cone_add(radius1=0.18, radius2=0.0, depth=0.65, location=(x, 0.0, 3.45))
        finial = bpy.context.active_object
        finial.data.materials.append(mat_gold)

        # Finial cross fleur-de-lis
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.06, location=(x, 0.0, 3.82))
        fleur = bpy.context.active_object
        fleur.data.materials.append(mat_gold)

    # Recessed Central Gothic Tower Wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.06, 1.95))
    backplate = bpy.context.active_object
    backplate.scale = (1.30, 0.48, 2.60)
    backplate.data.materials.append(mat_stone)

    # Peaked Gothic Gable Arch Pediment (Recessed behind dial)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.62, depth=0.25, location=(0.0, -0.10, 3.15))
    arch = bpy.context.active_object
    arch.rotation_euler = (math.radians(90), 0, 0)
    arch.data.materials.append(mat_darkstone)

    # Trefoil / Tracery Gable Crown
    bpy.ops.mesh.primitive_cone_add(radius1=0.75, radius2=0.0, depth=0.65, location=(0.0, -0.05, 3.65))
    gable = bpy.context.active_object
    gable.scale = (1.0, 0.45, 1.0)
    gable.data.materials.append(mat_stone)

    # Decorative Gothic Cresting Ridge along Gable
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.05, 3.98))
    ridge = bpy.context.active_object
    ridge.scale = (0.20, 0.35, 0.08)
    ridge.data.materials.append(mat_gold)

    # --- 2. Upper Astronomical Astrolabe Dial ---
    dial_center_z = 2.15
    dial_y = 0.25

    # Lapis Lazuli Deep Sky Background Disc
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.58, depth=0.06, location=(0.0, dial_y, dial_center_z))
    sky_disc = bpy.context.active_object
    sky_disc.rotation_euler = (math.radians(90), 0, 0)
    sky_disc.data.materials.append(mat_blue)

    # Outer 24-Hour Gilded Dial Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.60, minor_radius=0.035, location=(0.0, dial_y + 0.03, dial_center_z))
    ring_24h = bpy.context.active_object
    ring_24h.rotation_euler = (math.radians(90), 0, 0)
    ring_24h.data.materials.append(mat_gold)

    # 24 Roman Numeral Radial Indices (I-XII twice)
    for i in range(24):
        angle = (i / 24.0) * 2.0 * math.pi
        rad = 0.54
        px = rad * math.sin(angle)
        pz = dial_center_z + rad * math.cos(angle)
        is_major = (i % 6 == 0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, dial_y + 0.04, pz))
        numeral = bpy.context.active_object
        numeral.scale = (0.016, 0.02, 0.065 if is_major else 0.038)
        numeral.rotation_euler = (0, -angle, 0)
        numeral.data.materials.append(mat_gold)

    # Stereographic Projection Astrolabe Rings (Tropic of Cancer, Equator, Capricorn)
    for cr, cz_shift in [(0.46, 0.0), (0.34, 0.02), (0.22, 0.04)]:
        bpy.ops.mesh.primitive_torus_add(major_radius=cr, minor_radius=0.012, location=(0.0, dial_y + 0.02, dial_center_z + cz_shift))
        c_ring = bpy.context.active_object
        c_ring.rotation_euler = (math.radians(90), 0, 0)
        c_ring.data.materials.append(mat_brass)

    # Eccentric Zodiac Band (Tilted & Offset Ring with 12 Constellation Markers)
    zodiac_center_x = 0.04
    zodiac_center_z = dial_center_z - 0.05
    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.022, location=(zodiac_center_x, dial_y + 0.05, zodiac_center_z))
    zodiac_ring = bpy.context.active_object
    zodiac_ring.rotation_euler = (math.radians(90), 0, math.radians(22))
    zodiac_ring.data.materials.append(mat_gold)

    for z in range(12):
        z_ang = (z / 12.0) * 2.0 * math.pi
        zx = zodiac_center_x + 0.35 * math.sin(z_ang)
        zz = zodiac_center_z + 0.35 * math.cos(z_ang)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.022, location=(zx, dial_y + 0.065, zz))
        z_star = bpy.context.active_object
        z_star.data.materials.append(mat_gold)

    # Rete Curved Flame Pointers (Astrolabe Star Pointers)
    for r_ang in [0.8, 1.9, 3.2, 4.5, 5.4]:
        rx = 0.24 * math.sin(r_ang)
        rz = dial_center_z + 0.24 * math.cos(r_ang)
        bpy.ops.mesh.primitive_cone_add(radius1=0.02, radius2=0.0, depth=0.12, location=(rx, dial_y + 0.05, rz))
        pointer = bpy.context.active_object
        pointer.rotation_euler = (0, -r_ang, 0)
        pointer.data.materials.append(mat_gold)

    # Golden Sun Hand (Long Pointer Arm + Radiant Solar Emblem)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.14, dial_y + 0.07, dial_center_z + 0.18))
    sun_arm = bpy.context.active_object
    sun_arm.scale = (0.025, 0.015, 0.44)
    sun_arm.rotation_euler = (0, math.radians(-38), 0)
    sun_arm.data.materials.append(mat_gold)

    # Solar Radiant Disk
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.065, location=(0.28, dial_y + 0.08, dial_center_z + 0.34))
    sun_core = bpy.context.active_object
    sun_core.data.materials.append(mat_gold)

    for s_ray in range(8):
        s_ang = (s_ray / 8.0) * 2.0 * math.pi
        srx = 0.28 + 0.08 * math.sin(s_ang)
        srz = dial_center_z + 0.34 + 0.08 * math.cos(s_ang)
        bpy.ops.mesh.primitive_cone_add(radius1=0.015, radius2=0.0, depth=0.06, location=(srx, dial_y + 0.08, srz))
        ray = bpy.context.active_object
        ray.rotation_euler = (0, -s_ang, 0)
        ray.data.materials.append(mat_gold)

    # Rotating Moon Sphere (Two-Tone Half Silver / Half Dark Iron Phase)
    moon_x = -0.18
    moon_z = dial_center_z - 0.22
    # Silver lit hemisphere
    bpy.ops.mesh.primitive_cylinder_add(radius=0.048, depth=0.035, location=(moon_x, dial_y + 0.075, moon_z))
    moon_silver = bpy.context.active_object
    moon_silver.rotation_euler = (math.radians(90), 0, 0)
    moon_silver.data.materials.append(mat_silver)
    # Dark shadow hemisphere
    bpy.ops.mesh.primitive_cylinder_add(radius=0.048, depth=0.035, location=(moon_x, dial_y + 0.045, moon_z))
    moon_dark = bpy.context.active_object
    moon_dark.rotation_euler = (math.radians(90), 0, 0)
    moon_dark.data.materials.append(mat_darkmoon)
    # Bevelled aperture bezel
    bpy.ops.mesh.primitive_torus_add(major_radius=0.054, minor_radius=0.010, location=(moon_x, dial_y + 0.08, moon_z))
    m_bezel = bpy.context.active_object
    m_bezel.rotation_euler = (math.radians(90), 0, 0)
    m_bezel.data.materials.append(mat_gold)

    # Center Astrolabe Axis Boss & Retaining Rosette
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.10, location=(0.0, dial_y + 0.08, dial_center_z))
    boss = bpy.context.active_object
    boss.rotation_euler = (math.radians(90), 0, 0)
    boss.data.materials.append(mat_gold)

    # --- 3. Lower Calendar & Zodiac Dial ---
    cal_center_z = 1.05
    cal_y = 0.22

    # Parchment Calendar Disc
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.48, depth=0.05, location=(0.0, cal_y, cal_center_z))
    cal_disc = bpy.context.active_object
    cal_disc.rotation_euler = (math.radians(90), 0, 0)
    cal_disc.data.materials.append(mat_parchment)

    # Gilded Outer Border Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.50, minor_radius=0.025, location=(0.0, cal_y + 0.02, cal_center_z))
    cal_ring = bpy.context.active_object
    cal_ring.rotation_euler = (math.radians(90), 0, 0)
    cal_ring.data.materials.append(mat_gold)

    # 12 Month Radial Division Rays & Golden Bosses
    for m in range(12):
        m_ang = (m / 12.0) * 2.0 * math.pi
        mx = 0.42 * math.sin(m_ang)
        mz = cal_center_z + 0.42 * math.cos(m_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx * 0.7, cal_y + 0.025, cal_center_z + (mz - cal_center_z) * 0.7))
        m_spoke = bpy.context.active_object
        m_spoke.scale = (0.012, 0.015, 0.25)
        m_spoke.rotation_euler = (0, -m_ang, 0)
        m_spoke.data.materials.append(mat_brass)

        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.02, location=(mx, cal_y + 0.03, mz))
        m_node = bpy.context.active_object
        m_node.data.materials.append(mat_gold)

    # Calendar Needle Indicator
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, cal_y + 0.04, cal_center_z + 0.20))
    cal_needle = bpy.context.active_object
    cal_needle.scale = (0.018, 0.012, 0.38)
    cal_needle.data.materials.append(mat_gold)

    # Center Calendar Boss
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.06, location=(0.0, cal_y + 0.04, cal_center_z))
    cal_boss = bpy.context.active_object
    cal_boss.rotation_euler = (math.radians(90), 0, 0)
    cal_boss.data.materials.append(mat_brass)

    # --- 4. Upper Bellcote & Clockwork Escapement Crown ---
    # Twin Arched Bellcote Chamber
    for bx in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0.0, 3.45))
        bpost = bpy.context.active_object
        bpost.scale = (0.10, 0.35, 0.85)
        bpost.data.materials.append(mat_darkstone)

    # Horizontal Timber Bell Support Beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 3.82))
    bbeam = bpy.context.active_object
    bbeam.scale = (0.86, 0.16, 0.10)
    bbeam.data.materials.append(mat_stone)

    # Twin Cast Bronze Chime Bells with Suspension Straps
    for bx in [-0.19, 0.19]:
        # Bronze bell body
        bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.06, depth=0.25, location=(bx, 0.0, 3.55))
        bell = bpy.context.active_object
        bell.data.materials.append(mat_bell)

        # Bell crown suspension yoke
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0.0, 3.73))
        yoke = bpy.context.active_object
        yoke.scale = (0.12, 0.08, 0.08)
        yoke.data.materials.append(mat_iron)

        # Bell strike hammer
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.18, location=(bx + 0.14, 0.08, 3.55))
        hammer_arm = bpy.context.active_object
        hammer_arm.rotation_euler = (0, math.radians(-30), 0)
        hammer_arm.data.materials.append(mat_iron)

        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.03, location=(bx + 0.10, 0.08, 3.48))
        hammer_head = bpy.context.active_object
        hammer_head.data.materials.append(mat_iron)

    # Visible Verge & Foliot Escapement in Back Gallery
    # Crown escapement wheel
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.24, depth=0.06, location=(0.0, -0.32, 2.25))
    c_wheel = bpy.context.active_object
    c_wheel.data.materials.append(mat_brass)

    # Crown wheel teeth rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.24, minor_radius=0.02, location=(0.0, -0.32, 2.25))
    c_rim = bpy.context.active_object
    c_rim.data.materials.append(mat_brass)

    # Vertical verge arbor spindle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.75, location=(0.0, -0.32, 2.50))
    verge_spindle = bpy.context.active_object
    verge_spindle.data.materials.append(mat_iron)

    # Foliot horizontal oscillating balance bar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.32, 2.82))
    foliot_bar = bpy.context.active_object
    foliot_bar.scale = (0.72, 0.032, 0.032)
    foliot_bar.data.materials.append(mat_iron)

    # Adjustable lead regulation weights at foliot extremities
    for fx in [-0.31, 0.31]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.09, location=(fx, -0.32, 2.82))
        fweight = bpy.context.active_object
        fweight.data.materials.append(mat_darkstone)

    # Hanging Drive Weight System (Twin hemp ropes + heavy lead cylinders)
    for wx, wz_top in [(-0.35, 2.10), (0.35, 1.70)]:
        # Rope
        bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=1.20, location=(wx, -0.25, wz_top - 0.60))
        rope = bpy.context.active_object
        rope.data.materials.append(mat_rope)

        # Drive Weight
        bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.42, location=(wx, -0.25, wz_top - 1.20))
        d_weight = bpy.context.active_object
        d_weight.data.materials.append(mat_darkstone)

        # Weight top ring
        bpy.ops.mesh.primitive_torus_add(major_radius=0.04, minor_radius=0.012, location=(wx, -0.25, wz_top - 0.98))
        w_ring = bpy.context.active_object
        w_ring.data.materials.append(mat_iron)

    export_gltf(get_output_path("astronomical_clock.glb"))

# ==========================================
# 2. BRASS PIVOTING ARMILLARY SPHERE
# ==========================================
def build_armillary_sphere():
    clear_scene()

    mat_walnut = create_pbr_material("CarvedWalnut", (0.30, 0.16, 0.08, 1.0), roughness=0.55, bump_type='wood', bump_strength=0.22, bump_scale=12.0, clearcoat=0.25)
    mat_brass = create_pbr_material("InstrumentBrass", (0.90, 0.74, 0.25, 1.0), roughness=0.22, metallic=0.96, clearcoat=0.2)
    mat_bronze = create_pbr_material("ArmillaryBronze", (0.72, 0.52, 0.22, 1.0), roughness=0.35, metallic=0.90)
    mat_lapis = create_pbr_material("GlobeOceanLapis", (0.08, 0.25, 0.65, 1.0), roughness=0.30, bump_type='noise', bump_strength=0.10, bump_scale=30.0)
    mat_gold_continents = create_pbr_material("GlobeGoldLand", (0.98, 0.82, 0.20, 1.0), roughness=0.25, metallic=0.88)
    mat_iron = create_pbr_material("AlidadeIronPin", (0.20, 0.20, 0.22, 1.0), roughness=0.48, metallic=0.85)

    # --- 1. Carved Walnut Tripod Stand with Cabriole Legs ---
    # Central Fluted Pedestal Column
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.13, depth=0.58, location=(0.0, 0.0, 0.46))
    col = bpy.context.active_object
    col.data.materials.append(mat_walnut)

    # Column Upper Turned Brass Capital
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.16, depth=0.09, location=(0.0, 0.0, 0.77))
    capital = bpy.context.active_object
    capital.data.materials.append(mat_brass)

    # Base Column Moulded Ring
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.18, depth=0.08, location=(0.0, 0.0, 0.18))
    base_ring = bpy.context.active_object
    base_ring.data.materials.append(mat_walnut)

    # 3 Curved Cabriole Legs with Bronze Claw Feet
    for i in range(3):
        angle = (i / 3.0) * 2.0 * math.pi
        lx = 0.30 * math.cos(angle)
        ly = 0.30 * math.sin(angle)

        # Upper curved hip
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx * 0.75, ly * 0.75, 0.32))
        hip = bpy.context.active_object
        hip.scale = (0.10, 0.09, 0.36)
        hip.rotation_euler = (-math.radians(32) * math.sin(angle), math.radians(32) * math.cos(angle), angle)
        hip.data.materials.append(mat_walnut)

        # Lower tapering shin
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx * 1.25, ly * 1.25, 0.14))
        shin = bpy.context.active_object
        shin.scale = (0.08, 0.07, 0.28)
        shin.rotation_euler = (math.radians(20) * math.sin(angle), -math.radians(20) * math.cos(angle), angle)
        shin.data.materials.append(mat_walnut)

        # Cast Bronze Ball-and-Claw Foot
        claw_x = 0.45 * math.cos(angle)
        claw_y = 0.45 * math.sin(angle)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.055, location=(claw_x, claw_y, 0.045))
        claw = bpy.context.active_object
        claw.data.materials.append(mat_bronze)

    # Circular Stretcher Shelf with Moulded Rim
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.28, depth=0.035, location=(0.0, 0.0, 0.22))
    stretcher = bpy.context.active_object
    stretcher.data.materials.append(mat_walnut)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.015, location=(0.0, 0.0, 0.22))
    stretcher_rim = bpy.context.active_object
    stretcher_rim.data.materials.append(mat_brass)

    # --- 2. Meridian Support Cradle & Latitude Quadrant ---
    sphere_center_z = 0.96

    # Brass cradle pivot yoke
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.18, location=(0.0, 0.0, 0.84))
    yoke_base = bpy.context.active_object
    yoke_base.data.materials.append(mat_brass)

    # Tilting Meridian Cradle Bracket with Latitude Degree Arc
    bpy.ops.mesh.primitive_torus_add(major_radius=0.58, minor_radius=0.024, location=(0.0, 0.0, sphere_center_z))
    cradle_arc = bpy.context.active_object
    cradle_arc.rotation_euler = (math.radians(90), 0, 0)
    cradle_arc.data.materials.append(mat_bronze)

    # Latitude Locking Thumbscrew
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.08, location=(0.0, -0.60, sphere_center_z))
    thumbscrew = bpy.context.active_object
    thumbscrew.rotation_euler = (math.radians(90), 0, 0)
    thumbscrew.data.materials.append(mat_brass)

    # --- 3. Calibrated Horizon Ring with Compass Rose ---
    # Broad Brass Horizon Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.042, location=(0.0, 0.0, sphere_center_z))
    h_ring = bpy.context.active_object
    h_ring.data.materials.append(mat_brass)

    # 4 Cardinal Support Spiders
    for c in range(4):
        c_ang = (c / 4.0) * 2.0 * math.pi
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.32 * math.cos(c_ang), 0.32 * math.sin(c_ang), sphere_center_z - 0.04))
        c_arm = bpy.context.active_object
        c_arm.scale = (0.26, 0.038, 0.045)
        c_arm.rotation_euler = (0, 0, c_ang)
        c_arm.data.materials.append(mat_bronze)

    # 8-Point Compass Rose Index Plates (N, NE, E, SE, S, SW, W, NW)
    for cp in range(8):
        cp_ang = (cp / 8.0) * 2.0 * math.pi
        cpx = 0.55 * math.cos(cp_ang)
        cpy = 0.55 * math.sin(cp_ang)
        is_cardinal = (cp % 2 == 0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cpx, cpy, sphere_center_z + 0.022))
        cp_marker = bpy.context.active_object
        cp_marker.scale = (0.045 if is_cardinal else 0.028, 0.02, 0.015)
        cp_marker.rotation_euler = (0, 0, cp_ang)
        cp_marker.data.materials.append(mat_gold_continents if is_cardinal else mat_brass)

    # 360-degree calibration tick notches (36 markers for 10-degree steps)
    for tick in range(36):
        t_ang = (tick / 36.0) * 2.0 * math.pi
        tx = 0.52 * math.cos(t_ang)
        ty = 0.52 * math.sin(t_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, ty, sphere_center_z + 0.018))
        t_obj = bpy.context.active_object
        t_obj.scale = (0.025, 0.008, 0.008)
        t_obj.rotation_euler = (0, 0, t_ang)
        t_obj.data.materials.append(mat_iron)

    # --- 4. Nested Armillary Brass Rings ---
    # Primary Meridian Ring (Engraved 0-90-0-90 degrees)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.50, minor_radius=0.026, location=(0.0, 0.0, sphere_center_z))
    meridian = bpy.context.active_object
    meridian.rotation_euler = (math.radians(90), 0, 0)
    meridian.data.materials.append(mat_brass)

    # Equinoctial / Celestial Equator Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.48, minor_radius=0.024, location=(0.0, 0.0, sphere_center_z))
    equator = bpy.context.active_object
    equator.data.materials.append(mat_brass)

    # Solstitial Colure Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.47, minor_radius=0.022, location=(0.0, 0.0, sphere_center_z))
    solstice = bpy.context.active_object
    solstice.rotation_euler = (0, math.radians(90), 0)
    solstice.data.materials.append(mat_bronze)

    # Arctic & Antarctic Polar Circle Rings
    for p_z in [-0.28, 0.28]:
        p_rad = math.sqrt(0.46**2 - p_z**2)
        bpy.ops.mesh.primitive_torus_add(major_radius=p_rad, minor_radius=0.016, location=(0.0, 0.0, sphere_center_z + p_z))
        p_ring = bpy.context.active_object
        p_ring.data.materials.append(mat_brass)

    # Tropics of Cancer & Capricorn Rings
    for t_z in [-0.18, 0.18]:
        t_rad = math.sqrt(0.47**2 - t_z**2)
        bpy.ops.mesh.primitive_torus_add(major_radius=t_rad, minor_radius=0.018, location=(0.0, 0.0, sphere_center_z + t_z))
        t_ring = bpy.context.active_object
        t_ring.data.materials.append(mat_brass)

    # Oblique Ecliptic Zodiac Band (Tilted 23.44°, Wide Ribbon with 12 Constellation Plates)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.44, minor_radius=0.038, location=(0.0, 0.0, sphere_center_z))
    ecliptic = bpy.context.active_object
    ecliptic.rotation_euler = (math.radians(23.44), 0, math.radians(35))
    ecliptic.data.materials.append(mat_brass)

    for z_sym in range(12):
        z_sym_ang = (z_sym / 12.0) * 2.0 * math.pi
        # transform to tilted ecliptic plane
        ex_local = 0.44 * math.sin(z_sym_ang)
        ey_local = 0.44 * math.cos(z_sym_ang)
        # Apply 23.44 deg tilt around X axis
        ey_tilted = ey_local * math.cos(math.radians(23.44))
        ez_tilted = ey_local * math.sin(math.radians(23.44))
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.024, location=(ex_local, ey_tilted, sphere_center_z + ez_tilted))
        z_plate = bpy.context.active_object
        z_plate.data.materials.append(mat_gold_continents)

    # Polar Axis Sighting Spindle (52° Latitude Incline)
    lat_tilt = 38.0  # angle from vertical
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=1.18, location=(0.0, 0.0, sphere_center_z))
    polar_axis = bpy.context.active_object
    polar_axis.rotation_euler = (math.radians(lat_tilt), 0, 0)
    polar_axis.data.materials.append(mat_iron)

    # Sighting Diopter Pinholes & Knurled Finials
    for pole_dir in [-0.58, 0.58]:
        pz = sphere_center_z + pole_dir * math.cos(math.radians(lat_tilt))
        py = pole_dir * math.sin(math.radians(lat_tilt))
        bpy.ops.mesh.primitive_cone_add(radius1=0.035, radius2=0.0, depth=0.08, location=(0.0, py, pz))
        finial = bpy.context.active_object
        finial.rotation_euler = (math.radians(lat_tilt if pole_dir > 0 else lat_tilt + 180), 0, 0)
        finial.data.materials.append(mat_brass)

        # Diopter sighting plate
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, py * 0.92, pz * 0.92 + (sphere_center_z * 0.08)))
        diopter = bpy.context.active_object
        diopter.scale = (0.05, 0.04, 0.015)
        diopter.rotation_euler = (math.radians(lat_tilt), 0, 0)
        diopter.data.materials.append(mat_brass)

    # --- 5. Central Terrestrial Earth Globe ---
    # Lapis Lazuli Deep Ocean Sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.095, location=(0.0, 0.0, sphere_center_z))
    earth = bpy.context.active_object
    earth.data.materials.append(mat_lapis)

    # Gilded Continent Relief Patches
    for cont_ang, cont_z in [(0.5, 0.03), (2.2, 0.04), (3.8, -0.02), (5.1, 0.02)]:
        cx = 0.090 * math.sin(cont_ang)
        cy = 0.090 * math.cos(cont_ang)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.035, location=(cx, cy, sphere_center_z + cont_z))
        continent = bpy.context.active_object
        continent.scale = (1.2, 0.8, 0.6)
        continent.data.materials.append(mat_gold_continents)

    # Miniature Earth Equatorial Brass Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.098, minor_radius=0.008, location=(0.0, 0.0, sphere_center_z))
    earth_eq = bpy.context.active_object
    earth_eq.data.materials.append(mat_brass)

    export_gltf(get_output_path("armillary_sphere.glb"))

# ==========================================
# 3. CLOCKWORK CELESTIAL ORRERY
# ==========================================
def build_celestial_orrery():
    clear_scene()

    mat_mahogany = create_pbr_material("FrenchPolishedMahogany", (0.34, 0.12, 0.06, 1.0), roughness=0.38, bump_type='wood', bump_strength=0.18, bump_scale=14.0, clearcoat=0.6)
    mat_brass = create_pbr_material("ClockmakerBrass", (0.88, 0.72, 0.24, 1.0), roughness=0.22, metallic=0.96, clearcoat=0.2)
    mat_gold = create_pbr_material("SolarRadiantGold", (1.0, 0.84, 0.18, 1.0), roughness=0.12, metallic=0.98, emission_color=(1.0, 0.85, 0.3, 1.0), emission_strength=0.8)
    mat_iron = create_pbr_material("CutGearSteel", (0.24, 0.25, 0.28, 1.0), roughness=0.45, metallic=0.90)
    mat_ivory = create_pbr_material("CarvedIvoryCrank", (0.92, 0.90, 0.82, 1.0), roughness=0.35)
    # Planetary Materials
    mat_mercury = create_pbr_material("PlanetMercury", (0.56, 0.52, 0.48, 1.0), roughness=0.65, bump_type='noise', bump_strength=0.25)
    mat_venus = create_pbr_material("PlanetVenus", (0.92, 0.88, 0.76, 1.0), roughness=0.25, clearcoat=0.4)
    mat_earth = create_pbr_material("PlanetEarth", (0.12, 0.42, 0.78, 1.0), roughness=0.35, clearcoat=0.3)
    mat_moon = create_pbr_material("PlanetMoon", (0.86, 0.86, 0.88, 1.0), roughness=0.55)
    mat_mars = create_pbr_material("PlanetMars", (0.84, 0.28, 0.12, 1.0), roughness=0.60, bump_type='noise', bump_strength=0.20)
    mat_jupiter = create_pbr_material("PlanetJupiter", (0.86, 0.68, 0.42, 1.0), roughness=0.30, bump_type='wood', bump_strength=0.15, bump_scale=25.0)
    mat_saturn = create_pbr_material("PlanetSaturn", (0.88, 0.78, 0.48, 1.0), roughness=0.28)
    mat_saturn_rings = create_pbr_material("SaturnRings", (0.82, 0.72, 0.45, 0.9), roughness=0.25, metallic=0.3)

    # --- 1. Octagonal Polished Mahogany Pedestal Cabinet ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.72, depth=0.76, location=(0.0, 0.0, 0.38))
    cabinet = bpy.context.active_object
    cabinet.data.materials.append(mat_mahogany)

    # Raised Boiserie Wall Panels & Mouldings on 8 Faces
    for f in range(8):
        f_ang = (f / 8.0) * 2.0 * math.pi + (math.pi / 8.0)
        fx = 0.68 * math.cos(f_ang)
        fy = 0.68 * math.sin(f_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, fy, 0.38))
        panel = bpy.context.active_object
        panel.scale = (0.36, 0.04, 0.52)
        panel.rotation_euler = (0, 0, f_ang + (math.pi / 2.0))
        panel.data.materials.append(mat_mahogany)

        # Brass panel border beading
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx * 1.02, fy * 1.02, 0.38))
        bead = bpy.context.active_object
        bead.scale = (0.38, 0.02, 0.54)
        bead.rotation_euler = (0, 0, f_ang + (math.pi / 2.0))
        bead.data.materials.append(mat_brass)

    # Brass Bracket Feet on All 8 Corners
    for b in range(8):
        b_ang = (b / 8.0) * 2.0 * math.pi
        bx = 0.71 * math.cos(b_ang)
        by = 0.71 * math.sin(b_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, 0.04))
        foot = bpy.context.active_object
        foot.scale = (0.08, 0.08, 0.08)
        foot.rotation_euler = (0, 0, b_ang)
        foot.data.materials.append(mat_brass)

    # Side Manual Input Crank with Turned Ivory Handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.22, location=(0.76, 0.0, 0.48))
    crank_hub = bpy.context.active_object
    crank_hub.rotation_euler = (0, math.radians(90), 0)
    crank_hub.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.88, 0.0, 0.56))
    crank_arm = bpy.context.active_object
    crank_arm.scale = (0.03, 0.04, 0.20)
    crank_arm.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.14, location=(0.94, 0.0, 0.65))
    ivory_grip = bpy.context.active_object
    ivory_grip.rotation_euler = (0, math.radians(90), 0)
    ivory_grip.data.materials.append(mat_ivory)

    # --- 2. Octagonal Brass Calendar Deck Plate ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.76, depth=0.05, location=(0.0, 0.0, 0.785))
    deck = bpy.context.active_object
    deck.data.materials.append(mat_brass)

    # Engraved Calendar Circle on Deck Rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.70, minor_radius=0.018, location=(0.0, 0.0, 0.812))
    cal_rim = bpy.context.active_object
    cal_rim.data.materials.append(mat_gold)

    # 12 Zodiac Month Sector Bosses
    for m in range(12):
        m_ang = (m / 12.0) * 2.0 * math.pi
        mx = 0.66 * math.cos(m_ang)
        my = 0.66 * math.sin(m_ang)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.018, location=(mx, my, 0.815))
        m_boss = bpy.context.active_object
        m_boss.data.materials.append(mat_brass)

    # --- 3. Kinetic Epicyclic Clockwork Gear Train ---
    # Central Cluster Gears (Multiple Stepped Spur Gears with cut teeth profiles)
    gear_radii = [0.18, 0.24, 0.30, 0.36]
    gear_z = [0.83, 0.87, 0.91, 0.95]
    for gr, gz in zip(gear_radii, gear_z):
        # Gear Body
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=gr, depth=0.028, location=(0.0, 0.0, gz))
        gear = bpy.context.active_object
        gear.data.materials.append(mat_brass)

        # 4-Spoke Hub Cutouts (Lightening Spokes)
        bpy.ops.mesh.primitive_torus_add(major_radius=gr * 0.7, minor_radius=0.012, location=(0.0, 0.0, gz))
        spoke_ring = bpy.context.active_object
        spoke_ring.data.materials.append(mat_iron)

        # Gear Teeth along Perimeter
        num_teeth = int(gr * 50)
        for t in range(0, num_teeth, 2):
            t_ang = (t / float(num_teeth)) * 2.0 * math.pi
            tx = gr * math.cos(t_ang)
            ty = gr * math.sin(t_ang)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, ty, gz))
            tooth = bpy.context.active_object
            tooth.scale = (0.015, 0.012, 0.028)
            tooth.rotation_euler = (0, 0, t_ang)
            tooth.data.materials.append(mat_brass)

    # Planetary Idler Pinion Clusters (Epicyclic Gear Train)
    for p_id in range(3):
        p_ang = (p_id / 3.0) * 2.0 * math.pi
        px = 0.32 * math.cos(p_ang)
        py = 0.32 * math.sin(p_ang)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.08, depth=0.08, location=(px, py, 0.88))
        pinion = bpy.context.active_object
        pinion.data.materials.append(mat_iron)

        # Pinion pivot post
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.16, location=(px, py, 0.90))
        post = bpy.context.active_object
        post.data.materials.append(mat_brass)

    # --- 4. Central Sun & Planetary Radial Arm Assembly ---
    # Central Sun Pillar Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.55, location=(0.0, 0.0, 1.20))
    sun_shaft = bpy.context.active_object
    sun_shaft.data.materials.append(mat_brass)

    # Radiant Golden Sun Sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.17, location=(0.0, 0.0, 1.48))
    sun = bpy.context.active_object
    sun.data.materials.append(mat_gold)

    # 12 Coronal Solar Flare Rays
    for s in range(12):
        s_ang = (s / 12.0) * 2.0 * math.pi
        s_elev = math.sin(s * 1.5) * 0.4
        sx = 0.22 * math.cos(s_ang)
        sy = 0.22 * math.sin(s_ang)
        sz = 1.48 + (s_elev * 0.10)
        bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.0, depth=0.14, location=(sx, sy, sz))
        flare = bpy.context.active_object
        flare.rotation_euler = (s_elev, -s_ang, math.radians(90))
        flare.data.materials.append(mat_gold)

    # Concentric Brass Planetary Sleeve Rings & Support Arms
    def add_detailed_planet(radius_dist, angle_deg, upright_h, planet_mat, planet_r, name, has_moon=False, rings=False):
        rad = math.radians(angle_deg)
        px = radius_dist * math.cos(rad)
        py = radius_dist * math.sin(rad)

        # Horizontal Brass Radial Carrier Arm
        arm_z = 0.98 + (radius_dist * 0.07)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px * 0.5, py * 0.5, arm_z))
        arm = bpy.context.active_object
        arm.scale = (radius_dist, 0.022, 0.022)
        arm.rotation_euler = (0, 0, rad)
        arm.data.materials.append(mat_brass)

        # Counterweight Boss on Opposite Side
        c_px = -0.10 * math.cos(rad)
        c_py = -0.10 * math.sin(rad)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.04, location=(c_px, c_py, arm_z))
        c_boss = bpy.context.active_object
        c_boss.data.materials.append(mat_brass)

        # Vertical Upright Spindle
        pz = arm_z + upright_h * 0.5
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=upright_h, location=(px, py, pz))
        rod = bpy.context.active_object
        rod.data.materials.append(mat_brass)

        # Planet Body
        planet_z = pz + upright_h * 0.5 + planet_r
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=planet_r, location=(px, py, planet_z))
        planet = bpy.context.active_object
        planet.data.materials.append(planet_mat)

        # Epicyclic Moon System (Earth)
        if has_moon:
            # Moon orbit gear ring
            bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.006, location=(px, py, planet_z))
            m_ring = bpy.context.active_object
            m_ring.data.materials.append(mat_brass)

            # Moon arm
            m_ang = rad + math.radians(65)
            mx = px + 0.09 * math.cos(m_ang)
            my = py + 0.09 * math.sin(m_ang)
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=((px + mx) * 0.5, (py + my) * 0.5, planet_z))
            m_arm = bpy.context.active_object
            m_arm.scale = (0.09, 0.008, 0.008)
            m_arm.rotation_euler = (0, 0, m_ang)
            m_arm.data.materials.append(mat_brass)

            # Silver Moon Sphere
            bpy.ops.mesh.primitive_ico_sphere_add(radius=0.018, location=(mx, my, planet_z))
            moon = bpy.context.active_object
            moon.data.materials.append(mat_moon)

        # Concentric Planar Rings (Saturn)
        if rings:
            # Dual concentric rings (Ring A & Ring B)
            for r_rad, r_thick in [(0.14, 0.012), (0.17, 0.010)]:
                bpy.ops.mesh.primitive_torus_add(major_radius=r_rad, minor_radius=r_thick, location=(px, py, planet_z))
                s_ring = bpy.context.active_object
                s_ring.rotation_euler = (math.radians(26.7), math.radians(12.0), 0)
                s_ring.data.materials.append(mat_saturn_rings)

        return (px, py, planet_z)

    # 1. Mercury (Slate, innermost, fast)
    add_detailed_planet(radius_dist=0.25, angle_deg=45, upright_h=0.18, planet_mat=mat_mercury, planet_r=0.038, name="Mercury")

    # 2. Venus (Pearlescent pale gold)
    add_detailed_planet(radius_dist=0.36, angle_deg=140, upright_h=0.25, planet_mat=mat_venus, planet_r=0.048, name="Venus")

    # 3. Earth & Moon (Azure blue Earth with epicyclic orbit ring & silver Moon)
    add_detailed_planet(radius_dist=0.48, angle_deg=225, upright_h=0.32, planet_mat=mat_earth, planet_r=0.054, name="Earth", has_moon=True)

    # 4. Mars (Ochre-red sphere)
    add_detailed_planet(radius_dist=0.62, angle_deg=315, upright_h=0.38, planet_mat=mat_mars, planet_r=0.044, name="Mars")

    # 5. Jupiter (Amber striped giant with 4 Galilean moon satellite pins)
    jx, jy, jz = add_detailed_planet(radius_dist=0.74, angle_deg=110, upright_h=0.44, planet_mat=mat_jupiter, planet_r=0.075, name="Jupiter")
    for g_id, g_dist in enumerate([0.10, 0.13, 0.16, 0.19]):
        g_ang = (g_id / 4.0) * 2.0 * math.pi
        gx = jx + g_dist * math.cos(g_ang)
        gy = jy + g_dist * math.sin(g_ang)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.006, depth=0.03, location=(gx, gy, jz))
        g_pin = bpy.context.active_object
        g_pin.data.materials.append(mat_brass)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.010, location=(gx, gy, jz + 0.02))
        g_moon = bpy.context.active_object
        g_moon.data.materials.append(mat_moon)

    # 6. Saturn (Golden banded planet with dual concentric rings)
    add_detailed_planet(radius_dist=0.88, angle_deg=70, upright_h=0.50, planet_mat=mat_saturn, planet_r=0.070, name="Saturn", rings=True)

    export_gltf(get_output_path("celestial_orrery.glb"))

def main():
    print("=== Generating Milestone 40 Models (High-Fidelity Detailing) ===")
    build_astronomical_clock()
    build_armillary_sphere()
    build_celestial_orrery()
    print("=== Milestone 40 Generation Complete ===")

if __name__ == "__main__":
    main()
