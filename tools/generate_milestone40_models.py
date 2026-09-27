# tools/generate_milestone40_models.py
# Procedural 3D model generator for Milestone 40: Grand Imperial Clockwork Observatory
# 1. astronomical_clock.glb - Prague-Style Astronomical Clockwork Tower Facade
# 2. armillary_sphere.glb - Renaissance Brass Pivoting Armillary Sphere on Walnut Tripod
# 3. celestial_orrery.glb - Kinetic Clockwork Planetary Orrery with Epicyclic Gear Train

import bpy
import os
import math

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
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

    mat_stone = create_material("GothicStone", (0.35, 0.34, 0.32, 1.0), roughness=0.92)
    mat_darkstone = create_material("DarkMoulding", (0.22, 0.21, 0.20, 1.0), roughness=0.88)
    mat_gold = create_material("ClockworkGold", (0.95, 0.78, 0.20, 1.0), roughness=0.25, metallic=0.95)
    mat_brass = create_material("ClockBrass", (0.80, 0.65, 0.25, 1.0), roughness=0.35, metallic=0.90)
    mat_blue = create_material("CelestialLapis", (0.05, 0.12, 0.32, 1.0), roughness=0.40)
    mat_silver = create_material("MoonSilver", (0.90, 0.92, 0.95, 1.0), roughness=0.20, metallic=0.85)
    mat_darkmoon = create_material("MoonDark", (0.10, 0.10, 0.12, 1.0), roughness=0.70)
    mat_iron = create_material("VergeIron", (0.25, 0.25, 0.26, 1.0), roughness=0.55, metallic=0.85)
    mat_bell = create_material("BellBronze", (0.75, 0.55, 0.20, 1.0), roughness=0.30, metallic=0.92)

    # 1. Stone Masonry Clock Tower Frame
    # Base Pedestal plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.35))
    plinth = bpy.context.active_object
    plinth.scale = (1.6, 0.8, 0.7)
    plinth.data.materials.append(mat_stone)

    # Flanking pilasters / buttress pillars
    for x in [-0.72, 0.72]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 1.8))
        pillar = bpy.context.active_object
        pillar.scale = (0.22, 0.65, 2.4)
        pillar.data.materials.append(mat_darkstone)

        # Decorative pinnacles / finials on top of pillars
        bpy.ops.mesh.primitive_cone_add(radius1=0.16, radius2=0.0, depth=0.5, location=(x, 0.0, 3.25))
        finial = bpy.context.active_object
        finial.data.materials.append(mat_gold)

    # Main Dial Backplate (Recessed gothic wall frame)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.05, 1.85))
    backplate = bpy.context.active_object
    backplate.scale = (1.25, 0.45, 1.9)
    backplate.data.materials.append(mat_stone)

    # Peaked Gothic Arch Pediment Roof
    bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=0.7, location=(0.0, 0.0, 2.7))
    arch = bpy.context.active_object
    arch.rotation_euler = (math.radians(90), 0, 0)
    arch.data.materials.append(mat_darkstone)

    # 2. Astrolabe Astronomical Dial Face
    # Deep Blue Celestial Background Disc
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.06, location=(0.0, 0.22, 1.85))
    sky_disc = bpy.context.active_object
    sky_disc.rotation_euler = (math.radians(90), 0, 0)
    sky_disc.data.materials.append(mat_blue)

    # Outer 24-Hour Gold Dial Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.64, minor_radius=0.04, location=(0.0, 0.25, 1.85))
    ring_24h = bpy.context.active_object
    ring_24h.rotation_euler = (math.radians(90), 0, 0)
    ring_24h.data.materials.append(mat_gold)

    # 24 Hour Roman Numeral / Radial Spoke Indices
    for i in range(24):
        angle = (i / 24.0) * 2.0 * math.pi
        rad = 0.58
        px = rad * math.sin(angle)
        pz = 1.85 + rad * math.cos(angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0.26, pz))
        spoke = bpy.context.active_object
        spoke.scale = (0.015, 0.02, 0.06 if i % 6 == 0 else 0.035)
        spoke.rotation_euler = (0, -angle, 0)
        spoke.data.materials.append(mat_gold)

    # Eccentric Zodiac Band (Off-center gold ring)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.38, minor_radius=0.025, location=(0.05, 0.28, 1.80))
    zodiac_ring = bpy.context.active_object
    zodiac_ring.rotation_euler = (math.radians(90), 0, math.radians(15))
    zodiac_ring.data.materials.append(mat_gold)

    # 12 Zodiac Division markers
    for z in range(12):
        z_angle = (z / 12.0) * 2.0 * math.pi
        zx = 0.05 + 0.38 * math.sin(z_angle)
        zz = 1.80 + 0.38 * math.cos(z_angle)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.025, location=(zx, 0.29, zz))
        z_node = bpy.context.active_object
        z_node.data.materials.append(mat_brass)

    # Central Golden Astrolabe Sun Hand Pointer
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.14, 0.30, 2.05))
    sun_hand = bpy.context.active_object
    sun_hand.scale = (0.03, 0.015, 0.45)
    sun_hand.rotation_euler = (0, math.radians(-35), 0)
    sun_hand.data.materials.append(mat_gold)

    # Sun Effigy Symbol (Golden starburst)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.06, location=(0.28, 0.31, 2.25))
    sun_effigy = bpy.context.active_object
    sun_effigy.data.materials.append(mat_gold)

    # Rotating Moon Sphere (Two-tone: half silver, half dark)
    # Silver lit hemisphere
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.04, location=(-0.18, 0.31, 1.62))
    moon_lit = bpy.context.active_object
    moon_lit.rotation_euler = (math.radians(90), 0, 0)
    moon_lit.data.materials.append(mat_silver)

    # Center Astrolabe Axis Boss
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.08, location=(0.0, 0.31, 1.85))
    center_boss = bpy.context.active_object
    center_boss.rotation_euler = (math.radians(90), 0, 0)
    center_boss.data.materials.append(mat_gold)

    # 3. Escapement & Bell Chime Mechanism at Crown
    # Open timber bellcote frame
    for bx in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0.0, 3.4))
        post = bpy.context.active_object
        post.scale = (0.08, 0.08, 0.7)
        post.data.materials.append(mat_stone)

    # Bell Beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 3.7))
    bbeam = bpy.context.active_object
    bbeam.scale = (0.78, 0.1, 0.08)
    bbeam.data.materials.append(mat_stone)

    # Cast Bronze Bells (Twin chime bells)
    for bx in [-0.18, 0.18]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.06, depth=0.22, location=(bx, 0.0, 3.48))
        bell = bpy.context.active_object
        bell.data.materials.append(mat_bell)

    # Verge & Foliot Escapement (Visible in back arch)
    # Crown wheel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.08, location=(0.0, -0.32, 2.2))
    crown_wheel = bpy.context.active_object
    crown_wheel.data.materials.append(mat_brass)

    # Foliot horizontal balance arm with twin adjustable lead weights
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.32, 2.5))
    foliot_arm = bpy.context.active_object
    foliot_arm.scale = (0.65, 0.03, 0.03)
    foliot_arm.data.materials.append(mat_iron)

    for fx in [-0.28, 0.28]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.08, location=(fx, -0.32, 2.5))
        fweight = bpy.context.active_object
        fweight.data.materials.append(mat_darkstone)

    # Drive Counterweight (Descending lead cylindrical weight on ropes)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.45, location=(-0.35, -0.25, 0.6))
    cweight = bpy.context.active_object
    cweight.data.materials.append(mat_darkstone)

    export_gltf(get_output_path("astronomical_clock.glb"))

# ==========================================
# 2. BRASS PIVOTING ARMILLARY SPHERE
# ==========================================
def build_armillary_sphere():
    clear_scene()

    mat_walnut = create_material("CarvedWalnut", (0.28, 0.16, 0.09, 1.0), roughness=0.65)
    mat_brass = create_material("ArmillaryBrass", (0.88, 0.72, 0.26, 1.0), roughness=0.25, metallic=0.95)
    mat_bronze = create_material("ArmillaryBronze", (0.70, 0.52, 0.22, 1.0), roughness=0.38, metallic=0.90)
    mat_lapis = create_material("TerrestrialGlobe", (0.12, 0.35, 0.65, 1.0), roughness=0.30)
    mat_iron = create_material("AlidadeSightPin", (0.20, 0.20, 0.22, 1.0), roughness=0.50, metallic=0.85)

    # 1. Carved Walnut Tripod Pedestal Stand
    # Central fluted walnut column
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.55, location=(0.0, 0.0, 0.45))
    pillar = bpy.context.active_object
    pillar.data.materials.append(mat_walnut)

    # Upper brass mounting collar
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.08, location=(0.0, 0.0, 0.74))
    collar = bpy.context.active_object
    collar.data.materials.append(mat_brass)

    # 3 Arched curved tripod legs with brass claw feet
    for i in range(3):
        angle = (i / 3.0) * 2.0 * math.pi
        leg_rot = angle

        # Curved leg strut
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28 * math.cos(angle), 0.28 * math.sin(angle), 0.25))
        leg = bpy.context.active_object
        leg.scale = (0.08, 0.08, 0.48)
        leg.rotation_euler = (-math.radians(35) * math.sin(angle), math.radians(35) * math.cos(angle), 0)
        leg.data.materials.append(mat_walnut)

        # Brass claw foot
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, location=(0.42 * math.cos(angle), 0.42 * math.sin(angle), 0.04))
        claw = bpy.context.active_object
        claw.data.materials.append(mat_bronze)

    # Circular walnut stretcher shelf (Triangular spreader ring)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=0.03, location=(0.0, 0.0, 0.22))
    stretcher = bpy.context.active_object
    stretcher.data.materials.append(mat_walnut)

    # 2. Horizon Ring (Calibrated 360-degree Azimuth Ring)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.035, location=(0.0, 0.0, 0.88))
    h_ring = bpy.context.active_object
    h_ring.data.materials.append(mat_brass)

    # 4 Cardinal direction support brackets
    for c in range(4):
        c_angle = (c / 4.0) * 2.0 * math.pi
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.32 * math.cos(c_angle), 0.32 * math.sin(c_angle), 0.81))
        c_bracket = bpy.context.active_object
        c_bracket.scale = (0.24, 0.04, 0.05)
        c_bracket.rotation_euler = (0, 0, c_angle)
        c_bracket.data.materials.append(mat_bronze)

    # 3. Nested Brass Armillary Rings
    # Vertical Meridian Ring (Mounted perpendicular to horizon)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.50, minor_radius=0.025, location=(0.0, 0.0, 0.88))
    m_ring = bpy.context.active_object
    m_ring.rotation_euler = (math.radians(90), 0, 0)
    m_ring.data.materials.append(mat_brass)

    # Equator Ring (Horizontal inside the sphere)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.46, minor_radius=0.022, location=(0.0, 0.0, 0.88))
    eq_ring = bpy.context.active_object
    eq_ring.data.materials.append(mat_brass)

    # Solstitial Colure Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.020, location=(0.0, 0.0, 0.88))
    sol_ring = bpy.context.active_object
    sol_ring.rotation_euler = (0, math.radians(90), 0)
    sol_ring.data.materials.append(mat_bronze)

    # Oblique Ecliptic Band (Tilted at 23.4 degrees, wide engraved band)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.43, minor_radius=0.038, location=(0.0, 0.0, 0.88))
    ecliptic_band = bpy.context.active_object
    ecliptic_band.rotation_euler = (math.radians(23.4), 0, math.radians(45))
    ecliptic_band.data.materials.append(mat_brass)

    # Polar Axis Brass Sighting Spindle (Rod passing through the center at 52 deg latitude angle)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=1.12, location=(0.0, 0.0, 0.88))
    polar_spindle = bpy.context.active_object
    polar_spindle.rotation_euler = (math.radians(38), 0, 0)
    polar_spindle.data.materials.append(mat_iron)

    # Sighting Diopter Pinholes / Alidade Vanes on polar ends
    for end in [-0.52, 0.52]:
        dz = 0.88 + end * math.cos(math.radians(38))
        dy = end * math.sin(math.radians(38))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, dy, dz))
        vane = bpy.context.active_object
        vane.scale = (0.05, 0.05, 0.02)
        vane.rotation_euler = (math.radians(38), 0, 0)
        vane.data.materials.append(mat_brass)

    # 4. Central Terrestrial Globe
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.09, location=(0.0, 0.0, 0.88))
    earth_globe = bpy.context.active_object
    earth_globe.data.materials.append(mat_lapis)

    export_gltf(get_output_path("armillary_sphere.glb"))

# ==========================================
# 3. CLOCKWORK CELESTIAL ORRERY
# ==========================================
def build_celestial_orrery():
    clear_scene()

    mat_mahogany = create_material("PolishedMahogany", (0.32, 0.12, 0.08, 1.0), roughness=0.45)
    mat_brass = create_material("OrreryBrass", (0.90, 0.74, 0.24, 1.0), roughness=0.22, metallic=0.96)
    mat_gold = create_material("SolarGold", (1.0, 0.85, 0.15, 1.0), roughness=0.15, metallic=0.98)
    mat_mercury = create_material("PlanetMercury", (0.55, 0.48, 0.40, 1.0), roughness=0.40, metallic=0.85)
    mat_venus = create_material("PlanetVenus", (0.92, 0.90, 0.82, 1.0), roughness=0.20, metallic=0.75)
    mat_earth = create_material("PlanetEarth", (0.15, 0.45, 0.75, 1.0), roughness=0.35)
    mat_moon = create_material("PlanetMoon", (0.85, 0.85, 0.88, 1.0), roughness=0.30)
    mat_mars = create_material("PlanetMars", (0.82, 0.28, 0.14, 1.0), roughness=0.50, metallic=0.30)
    mat_saturn = create_material("PlanetSaturn", (0.82, 0.72, 0.45, 1.0), roughness=0.30, metallic=0.80)
    mat_iron = create_material("OrreryGearIron", (0.28, 0.28, 0.30, 1.0), roughness=0.45, metallic=0.85)

    # 1. Octagonal Polished Mahogany Pedestal Cabinet
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.70, depth=0.75, location=(0.0, 0.0, 0.375))
    cabinet = bpy.context.active_object
    cabinet.data.materials.append(mat_mahogany)

    # Brass corner bracket trim
    for b in range(8):
        b_angle = (b / 8.0) * 2.0 * math.pi
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.68 * math.cos(b_angle), 0.68 * math.sin(b_angle), 0.375))
        trim = bpy.context.active_object
        trim.scale = (0.04, 0.04, 0.72)
        trim.rotation_euler = (0, 0, b_angle)
        trim.data.materials.append(mat_brass)

    # Brass table deck plate atop cabinet
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.74, depth=0.06, location=(0.0, 0.0, 0.78))
    deck = bpy.context.active_object
    deck.data.materials.append(mat_brass)

    # Kinetic Input Shaft Coupling (Side bevel gearbox connection for 16 SU power)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.32, location=(0.75, 0.0, 0.50))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (0, math.radians(90), 0)
    shaft.data.materials.append(mat_iron)

    # Bevel gear casing
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.62, 0.0, 0.50))
    casing = bpy.context.active_object
    casing.scale = (0.16, 0.20, 0.20)
    casing.data.materials.append(mat_brass)

    # 2. Epicyclic Brass Gear Train on Deck
    # Central spur gear cluster
    for gz in [0.82, 0.88, 0.94]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.04, location=(0.0, 0.0, gz))
        c_gear = bpy.context.active_object
        c_gear.data.materials.append(mat_brass)

    # Intermediate planetary idler gears
    for ip in range(3):
        ip_angle = (ip / 3.0) * 2.0 * math.pi
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.03, location=(0.28 * math.cos(ip_angle), 0.28 * math.sin(ip_angle), 0.84))
        p_gear = bpy.context.active_object
        p_gear.data.materials.append(mat_iron)

    # 3. Central Sun Sphere
    # Central support column
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.45, location=(0.0, 0.0, 1.15))
    sun_column = bpy.context.active_object
    sun_column.data.materials.append(mat_brass)

    # Glowing Gold Sun
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15, location=(0.0, 0.0, 1.38))
    sun = bpy.context.active_object
    sun.data.materials.append(mat_gold)

    # 4. Concentric Planetary Radial Arms & Celestial Spheres
    # Helper to construct a radial planetary arm
    def add_planet_arm(radius_dist, angle_deg, upright_h, planet_mat, planet_r, ring_r=0.0):
        rad = math.radians(angle_deg)
        px = radius_dist * math.cos(rad)
        py = radius_dist * math.sin(rad)

        # Horizontal brass arm from center
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px * 0.5, py * 0.5, 0.98 + (radius_dist * 0.08)))
        arm = bpy.context.active_object
        arm.scale = (radius_dist, 0.02, 0.02)
        arm.rotation_euler = (0, 0, rad)
        arm.data.materials.append(mat_brass)

        # Vertical upright rod
        pz = 0.98 + (radius_dist * 0.08) + upright_h * 0.5
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=upright_h, location=(px, py, pz))
        rod = bpy.context.active_object
        rod.data.materials.append(mat_brass)

        # Planetary Sphere
        planet_z = pz + upright_h * 0.5 + planet_r
        bpy.ops.mesh.primitive_ico_sphere_add(radius=planet_r, location=(px, py, planet_z))
        planet = bpy.context.active_object
        planet.data.materials.append(planet_mat)

        # Optional Planetary Ring (Saturn)
        if ring_r > 0.0:
            bpy.ops.mesh.primitive_torus_add(major_radius=ring_r, minor_radius=0.012, location=(px, py, planet_z))
            ring = bpy.context.active_object
            ring.rotation_euler = (math.radians(25), math.radians(15), 0)
            ring.data.materials.append(mat_brass)

        return (px, py, planet_z)

    # 1. Mercury (fast, closest)
    add_planet_arm(radius_dist=0.24, angle_deg=40, upright_h=0.18, planet_mat=mat_mercury, planet_r=0.035)

    # 2. Venus (bright silver)
    add_planet_arm(radius_dist=0.35, angle_deg=130, upright_h=0.24, planet_mat=mat_venus, planet_r=0.045)

    # 3. Earth & Moon (blue globe with white satellite moon)
    ex, ey, ez = add_planet_arm(radius_dist=0.48, angle_deg=220, upright_h=0.30, planet_mat=mat_earth, planet_r=0.052)
    # Earth-Moon orbit arm
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ex + 0.05, ey + 0.05, ez))
    m_arm = bpy.context.active_object
    m_arm.scale = (0.10, 0.01, 0.01)
    m_arm.rotation_euler = (0, 0, math.radians(45))
    m_arm.data.materials.append(mat_brass)

    # Moon
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.016, location=(ex + 0.10, ey + 0.10, ez))
    moon = bpy.context.active_object
    moon.data.materials.append(mat_moon)

    # 4. Mars (copper red)
    add_planet_arm(radius_dist=0.62, angle_deg=310, upright_h=0.36, planet_mat=mat_mars, planet_r=0.042)

    # 5. Saturn (ringed planet, outermost)
    add_planet_arm(radius_dist=0.78, angle_deg=75, upright_h=0.42, planet_mat=mat_saturn, planet_r=0.068, ring_r=0.13)

    export_gltf(get_output_path("celestial_orrery.glb"))

def main():
    print("=== Generating Milestone 40 Models ===")
    build_astronomical_clock()
    build_armillary_sphere()
    build_celestial_orrery()
    print("=== Milestone 40 Generation Complete ===")

if __name__ == "__main__":
    main()
