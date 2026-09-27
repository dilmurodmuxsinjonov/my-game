# tools/generate_milestone38_models.py
# Procedural 3D model generator for Milestone 38: Medieval Port Logistics & Shipbuilding
# Overhauled with high-poly micro-details, copper sheathing, rigging, and rich PBR materials
# 1. drydock_slipway.glb - Shipbuilding Slipway Cradle with Scaffolding, Ribs & Fire Pit
# 2. quayside_crane.glb - Harbor Quayside Jib Crane on Stone Plinth with Cargo Sling & Gear Reduction
# 3. fluyt_cargo_ship.glb - Ocean-Going Fluyt Merchant Cargo Vessel with Full Rigging & Billowing Canvas

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
# 1. SHIPBUILDING DRYDOCK SLIPWAY
# ==========================================
def build_drydock_slipway():
    clear_scene()

    mat_oak = create_pbr_material("WeatheredOakTimber", (0.28, 0.18, 0.10, 1.0), roughness=0.85, bump_type='wood', bump_strength=0.25, bump_scale=12.0)
    mat_skids = create_pbr_material("GreasedSkidRails", (0.12, 0.10, 0.08, 1.0), roughness=0.22, metallic=0.2, clearcoat=0.5)
    mat_fresh_wood = create_pbr_material("FreshShipRibs", (0.54, 0.36, 0.18, 1.0), roughness=0.68, bump_type='wood', bump_strength=0.20, bump_scale=16.0)
    mat_iron = create_pbr_material("ShipwrightIron", (0.16, 0.17, 0.19, 1.0), roughness=0.48, metallic=0.90)
    mat_tar = create_pbr_material("BoilingPitchTar", (0.05, 0.05, 0.06, 1.0), roughness=0.15, metallic=0.1, clearcoat=0.8)
    mat_ember = create_pbr_material("TarPitEmbers", (1.0, 0.35, 0.05, 1.0), roughness=0.9, emission_color=(1.0, 0.35, 0.05, 1.0), emission_strength=4.5)
    mat_stone = create_pbr_material("HearthStone", (0.35, 0.33, 0.30, 1.0), roughness=0.90, bump_type='noise', bump_strength=0.25)

    # --- 1. Inclined Coastal Timber Skids & Heavy Way Balks ---
    slip_slope = math.radians(7)  # Sloped towards launch water
    for y_pos in [-0.90, 0.90]:
        # Heavy ground way timber
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 0.25))
        skid = bpy.context.active_object
        skid.scale = (4.40, 0.30, 0.24)
        skid.rotation_euler = (0, slip_slope, 0)
        skid.data.materials.append(mat_oak)

        # Greased Iron Runner Strip on Top of Way
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 0.39))
        runner = bpy.context.active_object
        runner.scale = (4.40, 0.14, 0.04)
        runner.rotation_euler = (0, slip_slope, 0)
        runner.data.materials.append(mat_skids)

    # Heavy Cross Ties underneath Skids (Transverse ground sills)
    for x_pos in [-1.8, -1.0, -0.2, 0.6, 1.4, 2.0]:
        z_pos = 0.14 - (x_pos * math.sin(slip_slope))
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, z_pos))
        crosstie = bpy.context.active_object
        crosstie.scale = (0.26, 2.40, 0.18)
        crosstie.data.materials.append(mat_oak)

    # Central Stepped Keel Blocks with Oak Leveling Wedges
    for x_pos in [-1.6, -1.1, -0.6, -0.1, 0.4, 0.9, 1.4, 1.9]:
        z_pos = 0.32 - (x_pos * math.sin(slip_slope))
        # Block
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, z_pos))
        kblock = bpy.context.active_object
        kblock.scale = (0.36, 0.48, 0.26)
        kblock.data.materials.append(mat_oak)

        # Leveling wedge pair
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, z_pos + 0.16))
        wedge = bpy.context.active_object
        wedge.scale = (0.32, 0.42, 0.06)
        wedge.data.materials.append(mat_fresh_wood)

    # Bilge Shoring Props (Diagonal struts supporting hull frames)
    for px in [-1.2, -0.2, 0.8, 1.6]:
        pz = 0.35 - (px * math.sin(slip_slope))
        for py, p_ang in [(-0.82, 35), (0.82, -35)]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.75, location=(px, py * 0.75, pz + 0.35))
            prop = bpy.context.active_object
            prop.rotation_euler = (math.radians(p_ang), 0, 0)
            prop.data.materials.append(mat_oak)

    # --- 2. Ship Under Construction: Keel, Stem & Curved Rib Frames ---
    # Shaped Keel Timber
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.10, 0.0, 0.56))
    keel = bpy.context.active_object
    keel.scale = (3.80, 0.22, 0.26)
    keel.rotation_euler = (0, slip_slope, 0)
    keel.data.materials.append(mat_fresh_wood)

    # Raked Stem Post (Bow)
    stem_x = -1.82
    stem_z = 0.56 - (stem_x * math.sin(slip_slope)) + 0.35
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(stem_x, 0.0, stem_z))
    stem = bpy.context.active_object
    stem.scale = (0.20, 0.20, 0.95)
    stem.rotation_euler = (0, math.radians(-28), 0)
    stem.data.materials.append(mat_fresh_wood)

    # Curved Stern Post with Gudgeons
    stern_x = 1.95
    stern_z = 0.56 - (stern_x * math.sin(slip_slope)) + 0.25
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(stern_x, 0.0, stern_z))
    sternpost = bpy.context.active_object
    sternpost.scale = (0.20, 0.20, 0.85)
    sternpost.rotation_euler = (0, math.radians(16), 0)
    sternpost.data.materials.append(mat_fresh_wood)

    # 7 Curved Ship Frame Ribs (Futtocks) Erected along Keel
    for idx, rx in enumerate([-1.3, -0.8, -0.3, 0.2, 0.7, 1.2, 1.6]):
        rz = 0.56 - (rx * math.sin(slip_slope)) + 0.32
        rib_width = 1.25 - abs(rx * 0.22)

        # Port Rib Futtock
        bpy.ops.mesh.primitive_torus_add(major_radius=rib_width * 0.52, minor_radius=0.055, location=(rx, rib_width * 0.50, rz))
        rib_p = bpy.context.active_object
        rib_p.rotation_euler = (0, math.radians(90), 0)
        rib_p.scale = (1.0, 1.0, 0.65)
        rib_p.data.materials.append(mat_fresh_wood)

        # Starboard Rib Futtock
        bpy.ops.mesh.primitive_torus_add(major_radius=rib_width * 0.52, minor_radius=0.055, location=(rx, -rib_width * 0.50, rz))
        rib_s = bpy.context.active_object
        rib_s.rotation_euler = (0, math.radians(90), 0)
        rib_s.scale = (1.0, 1.0, 0.65)
        rib_s.data.materials.append(mat_fresh_wood)

        # Floor Timber Connecting Rib Pair across Keel
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, 0.0, rz - 0.16))
        floor = bpy.context.active_object
        floor.scale = (0.12, rib_width * 0.85, 0.08)
        floor.data.materials.append(mat_fresh_wood)

    # Wale Strake Planks Clamped along Bilge
    for wy_sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.10, wy_sign * 0.62, 0.72))
        strake = bpy.context.active_object
        strake.scale = (3.20, 0.04, 0.14)
        strake.rotation_euler = (0, slip_slope, 0)
        strake.data.materials.append(mat_fresh_wood)

    # --- 3. Two-Tier Construction Scaffolding Along Both Flanks ---
    for y_side in [-1.45, 1.45]:
        # Upright Scaffold Poles
        for sx in [-1.6, -0.6, 0.4, 1.4]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=2.10, location=(sx, y_side, 1.05))
            pole = bpy.context.active_object
            pole.data.materials.append(mat_oak)

        # Lower Staging Walkway Planks
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_side, 0.75))
        plank_low = bpy.context.active_object
        plank_low.scale = (3.60, 0.38, 0.06)
        plank_low.data.materials.append(mat_oak)

        # Upper Staging Walkway Planks
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_side, 1.45))
        plank_high = bpy.context.active_object
        plank_high.scale = (3.60, 0.38, 0.06)
        plank_high.data.materials.append(mat_oak)

        # Guard Rail
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_side + (0.18 if y_side > 0 else -0.18), 1.85))
        rail = bpy.context.active_object
        rail.scale = (3.60, 0.04, 0.04)
        rail.data.materials.append(mat_oak)

    # --- 4. Shipwright Worksite: Glowing Pitch Melting Pit & Kettle ---
    # Stone Hearth Ring
    pit_x = -2.15
    pit_y = 1.35
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.35, depth=0.18, location=(pit_x, pit_y, 0.10))
    hearth_ring = bpy.context.active_object
    hearth_ring.data.materials.append(mat_stone)

    # Glowing Charcoal Embers inside Pit
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.28, depth=0.08, location=(pit_x, pit_y, 0.15))
    embers = bpy.context.active_object
    embers.data.materials.append(mat_ember)

    # Iron Tripod Suspension Stanchions
    for trip_i in range(3):
        t_ang = (trip_i / 3.0) * 2.0 * math.pi
        tx = pit_x + 0.24 * math.cos(t_ang)
        ty = pit_y + 0.24 * math.sin(t_ang)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.65, location=(tx, ty, 0.38))
        t_leg = bpy.context.active_object
        t_leg.rotation_euler = (-0.25 * math.sin(t_ang), 0.25 * math.cos(t_ang), 0)
        t_leg.data.materials.append(mat_iron)

    # Cast Iron Pitch Melting Kettle
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.20, depth=0.26, location=(pit_x, pit_y, 0.35))
    kettle = bpy.context.active_object
    kettle.data.materials.append(mat_iron)

    # Boiling Black Pitch Liquid Surface
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.18, depth=0.04, location=(pit_x, pit_y, 0.46))
    pitch_surf = bpy.context.active_object
    pitch_surf.data.materials.append(mat_tar)

    export_gltf(get_output_path("drydock_slipway.glb"))

# ==========================================
# 2. HARBOR QUAYSIDE JIB CRANE
# ==========================================
def build_quayside_crane():
    clear_scene()

    mat_stone = create_pbr_material("PierLimestone", (0.52, 0.50, 0.46, 1.0), roughness=0.88, bump_type='noise', bump_strength=0.25, bump_scale=22.0)
    mat_oak = create_pbr_material("CraneOakBeams", (0.32, 0.20, 0.11, 1.0), roughness=0.80, bump_type='wood', bump_strength=0.22, bump_scale=12.0)
    mat_iron = create_pbr_material("ForgedCraneIron", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)
    mat_ballast = create_pbr_material("BallastGranite", (0.42, 0.40, 0.38, 1.0), roughness=0.92, bump_type='noise', bump_strength=0.30)
    mat_rope = create_pbr_material("BraidedHempCable", (0.54, 0.46, 0.34, 1.0), roughness=0.90)
    mat_crate = create_pbr_material("CargoCrateWood", (0.46, 0.32, 0.18, 1.0), roughness=0.76, bump_type='wood', bump_strength=0.20, bump_scale=16.0)

    # --- 1. Octagonal Dressed Limestone Quayside Pier Base ---
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.05, depth=0.48, location=(0.0, 0.0, 0.24))
    pier = bpy.context.active_object
    pier.data.materials.append(mat_stone)

    # Corner Mooring Bollards on Quayside
    for bx, by in [(-0.85, -0.85), (-0.85, 0.85)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.08, depth=0.32, location=(bx, by, 0.60))
        bollard = bpy.context.active_object
        bollard.data.materials.append(mat_iron)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.10, minor_radius=0.02, location=(bx, by, 0.72))
        bhead = bpy.context.active_object
        bhead.data.materials.append(mat_iron)

    # Central Cast Bronze Thrust Pintle Bearing
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.12, location=(0.0, 0.0, 0.54))
    thrust_bearing = bpy.context.active_object
    thrust_bearing.data.materials.append(mat_iron)

    # --- 2. Heavy Squared Oak Crane Mast with Iron Gussets ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.75))
    mast = bpy.context.active_object
    mast.scale = (0.30, 0.30, 2.50)
    mast.data.materials.append(mat_oak)

    # Mast Reinforcement Iron Straps & Riveted Collars
    for mz in [0.72, 1.55, 2.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, mz))
        strap = bpy.context.active_object
        strap.scale = (0.34, 0.34, 0.09)
        strap.data.materials.append(mat_iron)

    # Diagonal Mast Footing Struts
    for side_y in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side_y * 0.5, 0.95))
        m_strut = bpy.context.active_object
        m_strut.scale = (0.16, 0.16, 0.85)
        m_strut.rotation_euler = (math.radians(-32 if side_y > 0 else 32), 0, 0)
        m_strut.data.materials.append(mat_oak)

    # --- 3. Angled Oak Jib Boom & Tension Tie-Rods ---
    # 45-degree Jib Boom reaching over water
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.10, 0.0, 2.25))
    boom = bpy.context.active_object
    boom.scale = (2.50, 0.24, 0.24)
    boom.rotation_euler = (0, math.radians(-38), 0)
    boom.data.materials.append(mat_oak)

    # Iron Gusset Bracket at Jib Heel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0.0, 1.48))
    gusset = bpy.context.active_object
    gusset.scale = (0.32, 0.32, 0.32)
    gusset.data.materials.append(mat_iron)

    # Upper Forged Iron Tension Tie-Rod from Mast Peak to Jib Tip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.028, depth=2.05, location=(1.02, 0.0, 2.82))
    tierod = bpy.context.active_object
    tierod.rotation_euler = (0, math.radians(65), 0)
    tierod.data.materials.append(mat_iron)

    # Turnbuckle Adjuster on Tie-Rod
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.05, depth=0.18, location=(1.02, 0.0, 2.82))
    t_buckle = bpy.context.active_object
    t_buckle.rotation_euler = (0, math.radians(65), 0)
    t_buckle.data.materials.append(mat_iron)

    # Boom Head Dual Pulley Sheaves at Outermost Tip
    sheave_x = 2.05
    sheave_z = 3.02
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.15, location=(sheave_x, 0.0, sheave_z))
    sheave = bpy.context.active_object
    sheave.rotation_euler = (math.radians(90), 0, 0)
    sheave.data.materials.append(mat_iron)

    # Sheave Cheek Plates
    for chy in [-0.10, 0.10]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sheave_x, chy, sheave_z))
        cheek = bpy.context.active_object
        cheek.scale = (0.45, 0.03, 0.45)
        cheek.data.materials.append(mat_iron)

    # --- 4. Rear Ballast Counterweight Box ---
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.92, 0.0, 1.15))
    cbox = bpy.context.active_object
    cbox.scale = (0.92, 0.92, 0.70)
    cbox.data.materials.append(mat_oak)

    # Iron Corner Straps on Ballast Box
    for c_sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.92, c_sign * 0.44, 1.15))
        c_band = bpy.context.active_object
        c_band.scale = (0.94, 0.04, 0.72)
        c_band.data.materials.append(mat_iron)

    # Rough Ballast Granite Rocks Packed Inside
    for bx in [-1.15, -0.92, -0.70]:
        for by in [-0.25, 0.25]:
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.16, location=(bx, by, 1.55))
            rock = bpy.context.active_object
            rock.data.materials.append(mat_ballast)

    # --- 5. Manual Gear Reduction Winch Tackle ---
    winch_z = 0.98
    # Grooved Cable Drum Wound with Hemp Rope
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.55, location=(0.0, -0.45, winch_z))
    winch = bpy.context.active_object
    winch.rotation_euler = (math.radians(90), 0, 0)
    winch.data.materials.append(mat_rope)

    # Large Bull Spur Gear on Drum
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.32, depth=0.06, location=(0.0, -0.15, winch_z))
    bull_gear = bpy.context.active_object
    bull_gear.rotation_euler = (math.radians(90), 0, 0)
    bull_gear.data.materials.append(mat_iron)

    # Small Drive Pinion & Hand Crank Arbor
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.10, depth=0.08, location=(0.0, -0.15, winch_z + 0.32))
    pinion = bpy.context.active_object
    pinion.rotation_euler = (math.radians(90), 0, 0)
    pinion.data.materials.append(mat_iron)

    # Wooden Hand Crank Arms on Both Sides
    for cy in [-0.78, -0.10]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, cy, winch_z + 0.44))
        crank_arm = bpy.context.active_object
        crank_arm.scale = (0.04, 0.04, 0.26)
        crank_arm.data.materials.append(mat_iron)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.16, location=(0.0, cy + (0.08 if cy > -0.5 else -0.08), winch_z + 0.55))
        c_handle = bpy.context.active_object
        c_handle.rotation_euler = (math.radians(90), 0, 0)
        c_handle.data.materials.append(mat_oak)

    # --- 6. Suspended Hoist Cable, Snatch Block, Hook & Cargo Crate ---
    # Multi-Fall Hoist Cable
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=1.65, location=(sheave_x, 0.0, 2.15))
    cable = bpy.context.active_object
    cable.data.materials.append(mat_rope)

    # Snatch Pulley Block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sheave_x, 0.0, 1.30))
    s_block = bpy.context.active_object
    s_block.scale = (0.16, 0.12, 0.24)
    s_block.data.materials.append(mat_iron)

    # Forged Iron Cargo Swivel Hook
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.03, location=(sheave_x, 0.0, 1.12))
    hook = bpy.context.active_object
    hook.rotation_euler = (0, math.radians(90), 0)
    hook.data.materials.append(mat_iron)

    # 4-Leg Hemp Rope Cargo Sling Bridle
    for sx, sy in [(-0.35, -0.35), (0.35, -0.35), (-0.35, 0.35), (0.35, 0.35)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.48, location=(sheave_x + sx * 0.5, sy * 0.5, 0.92))
        s_leg = bpy.context.active_object
        s_leg.rotation_euler = (sy * 0.8, -sx * 0.8, 0)
        s_leg.data.materials.append(mat_rope)

    # Suspended Banded Cargo Crate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sheave_x, 0.0, 0.65))
    crate = bpy.context.active_object
    crate.scale = (0.78, 0.78, 0.78)
    crate.data.materials.append(mat_crate)

    # Blackened Iron Crate Corner Edge Straps
    for cz in [0.32, 0.98]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sheave_x, 0.0, cz))
        cband = bpy.context.active_object
        cband.scale = (0.82, 0.82, 0.04)
        cband.data.materials.append(mat_iron)

    export_gltf(get_output_path("quayside_crane.glb"))

# ==========================================
# 3. OCEAN-GOING FLUYT CARGO VESSEL
# ==========================================
def build_fluyt_cargo_ship():
    clear_scene()

    mat_hull_top = create_pbr_material("CarvelOakTopsides", (0.28, 0.18, 0.10, 1.0), roughness=0.78, bump_type='wood', bump_strength=0.22, bump_scale=14.0)
    mat_copper_bottom = create_pbr_material("PatinatedCopperHull", (0.22, 0.48, 0.38, 1.0), roughness=0.42, metallic=0.75, clearcoat=0.2)
    mat_deck = create_pbr_material("PineDeckPlanks", (0.54, 0.40, 0.25, 1.0), roughness=0.72, bump_type='wood', bump_strength=0.18, bump_scale=20.0)
    mat_sails = create_pbr_material("BillowingCanvasSails", (0.90, 0.86, 0.78, 1.0), roughness=0.82)
    mat_spars = create_pbr_material("TurnedSpruceSpars", (0.42, 0.28, 0.15, 1.0), roughness=0.68)
    mat_brass = create_pbr_material("TransomOrnateGold", (0.92, 0.76, 0.24, 1.0), roughness=0.24, metallic=0.94, clearcoat=0.3)
    mat_iron = create_pbr_material("ShipForgedIron", (0.16, 0.17, 0.19, 1.0), roughness=0.50, metallic=0.88)
    mat_tarp = create_pbr_material("TarpaulinCover", (0.32, 0.26, 0.18, 1.0), roughness=0.85)
    mat_rope = create_pbr_material("RiggingRope", (0.48, 0.40, 0.28, 1.0), roughness=0.90)
    mat_glow = create_pbr_material("SternLanternGlow", (1.0, 0.82, 0.35, 1.0), roughness=0.1, emission_color=(1.0, 0.82, 0.35, 1.0), emission_strength=4.0)

    # --- 1. Iconic Dutch Tumblehome Hull & Underwater Copper Sheathing ---
    # Underwater Copper Sheathed Belly
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.35))
    copper_hull = bpy.context.active_object
    copper_hull.scale = (4.00, 1.55, 0.50)
    copper_hull.data.materials.append(mat_copper_bottom)

    # Carvel Planked Topsides (Narrowing inward above waterline - Tumblehome)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.82))
    top_hull = bpy.context.active_object
    top_hull.scale = (3.90, 1.38, 0.50)
    top_hull.data.materials.append(mat_hull_top)

    # Tapered Raked Bow Wedge
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.76, depth=1.40, location=(2.30, 0.0, 0.65))
    bow = bpy.context.active_object
    bow.rotation_euler = (0, math.radians(-90), 0)
    bow.scale = (1.0, 0.90, 1.0)
    bow.data.materials.append(mat_hull_top)

    # Raised Forecastle Deck Structure
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.55, 0.0, 1.28))
    fcastle = bpy.context.active_object
    fcastle.scale = (0.95, 1.22, 0.44)
    fcastle.data.materials.append(mat_hull_top)

    # Raised Aftcastle / Quarterdeck Structure
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.45, 0.0, 1.38))
    acastle = bpy.context.active_object
    acastle.scale = (1.25, 1.18, 0.62)
    acastle.data.materials.append(mat_hull_top)

    # Rounded Dutch Stern Transom (Tuck)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.60, depth=0.22, location=(-2.12, 0.0, 1.38))
    transom = bpy.context.active_object
    transom.rotation_euler = (0, math.radians(90), 0)
    transom.data.materials.append(mat_hull_top)

    # Transom Leaded Windows & Gilded Escutcheon
    for wy in [-0.26, 0.26]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-2.24, wy, 1.48))
        win = bpy.context.active_object
        win.scale = (0.04, 0.18, 0.24)
        win.data.materials.append(mat_brass)

    # Ornate Brass Stern Navigation Lantern on Curved Bracket
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.26, location=(-2.32, 0.0, 1.88))
    lantern = bpy.context.active_object
    lantern.data.materials.append(mat_glow)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.02, location=(-2.32, 0.0, 2.01))
    l_cap = bpy.context.active_object
    l_cap.data.materials.append(mat_brass)

    # Stern Rudder & Pintle Hinges
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-2.22, 0.0, 0.58))
    rudder = bpy.context.active_object
    rudder.scale = (0.25, 0.08, 0.90)
    rudder.data.materials.append(mat_hull_top)

    # --- 2. Deck Planking, Hatches & Furnishings ---
    # Main Weather Deck
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.05, 0.0, 1.08))
    deck = bpy.context.active_object
    deck.scale = (2.25, 1.30, 0.05)
    deck.data.materials.append(mat_deck)

    # 2 Cargo Hatches with Tarpaulin Coamings
    for hx in [-0.42, 0.58]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, 0.0, 1.18))
        hatch = bpy.context.active_object
        hatch.scale = (0.58, 0.72, 0.14)
        hatch.data.materials.append(mat_tarp)

    # Quarterdeck Spoke Helm Wheel & Binnacle
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.02, location=(-1.35, 0.0, 1.82))
    wheel = bpy.context.active_object
    wheel.rotation_euler = (0, math.radians(90), 0)
    wheel.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.15, 0.0, 1.74))
    binnacle = bpy.context.active_object
    binnacle.scale = (0.14, 0.14, 0.22)
    binnacle.data.materials.append(mat_brass)

    # Deck Capstan Winch (Center Main Deck)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.18, depth=0.32, location=(0.08, 0.0, 1.25))
    capstan = bpy.context.active_object
    capstan.data.materials.append(mat_spars)

    # Bower Anchor Lashed at Bow Cathead
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.65, location=(2.20, 0.65, 1.10))
    anchor_shank = bpy.context.active_object
    anchor_shank.rotation_euler = (math.radians(45), 0, 0)
    anchor_shank.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.16, minor_radius=0.025, location=(2.20, 0.85, 0.85))
    anchor_fluke = bpy.context.active_object
    anchor_fluke.data.materials.append(mat_iron)

    # --- 3. 3-Masted Rigging, Billowing Canvas & Shrouds ---
    # A. MAIN MAST (Center)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=3.30, location=(0.10, 0.0, 2.55))
    mainmast = bpy.context.active_object
    mainmast.data.materials.append(mat_spars)

    # Crow's Nest Platform (Main Top)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.25, depth=0.20, location=(0.10, 0.0, 3.25))
    crowsnest = bpy.context.active_object
    crowsnest.data.materials.append(mat_hull_top)

    # Lower Main Yard & Billowed Main Course Sail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=2.35, location=(0.10, 0.0, 2.15))
    mainyard = bpy.context.active_object
    mainyard.rotation_euler = (math.radians(90), 0, 0)
    mainyard.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.20, 0.0, 1.78))
    mainsail = bpy.context.active_object
    mainsail.scale = (0.05, 2.05, 0.68)
    mainsail.data.materials.append(mat_sails)

    # Upper Topsail Yard & Billowed Topsail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=1.65, location=(0.10, 0.0, 3.12))
    topyard = bpy.context.active_object
    topyard.rotation_euler = (math.radians(90), 0, 0)
    topyard.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0.0, 2.68))
    topsail = bpy.context.active_object
    topsail.scale = (0.045, 1.45, 0.78)
    topsail.data.materials.append(mat_sails)

    # Main Mast Shrouds with Climbing Ratlines
    for s_side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=2.40, location=(0.10, s_side * 0.55, 2.15))
        shroud = bpy.context.active_object
        shroud.rotation_euler = (math.radians(12 if s_side > 0 else -12), 0, 0)
        shroud.data.materials.append(mat_rope)

    # B. FORE MAST (Bow)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=2.50, location=(1.48, 0.0, 2.15))
    foremast = bpy.context.active_object
    foremast.data.materials.append(mat_spars)

    # Fore Yard & Foresail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=1.75, location=(1.48, 0.0, 2.35))
    foreyard = bpy.context.active_object
    foreyard.rotation_euler = (math.radians(90), 0, 0)
    foreyard.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.56, 0.0, 1.85))
    foresail = bpy.context.active_object
    foresail.scale = (0.045, 1.55, 0.80)
    foresail.data.materials.append(mat_sails)

    # C. MIZZEN MAST (Aft) with Lateen Triangular Spanker Sail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=2.00, location=(-1.28, 0.0, 2.10))
    mizzen = bpy.context.active_object
    mizzen.data.materials.append(mat_spars)

    # Slanted Lateen Yardarm (42 degrees)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.032, depth=1.75, location=(-1.28, 0.0, 2.25))
    lateen_yard = bpy.context.active_object
    lateen_yard.rotation_euler = (0, math.radians(-42), 0)
    lateen_yard.data.materials.append(mat_spars)

    # Triangular Lateen Sail
    bpy.ops.mesh.primitive_cone_add(radius1=0.72, depth=1.35, location=(-1.38, 0.0, 1.98))
    lateen_sail = bpy.context.active_object
    lateen_sail.rotation_euler = (0, math.radians(112), 0)
    lateen_sail.scale = (0.04, 0.90, 1.0)
    lateen_sail.data.materials.append(mat_sails)

    # D. BOWSPRIT (Forward Protruding Spar)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=1.95, location=(2.72, 0.0, 1.48))
    bowsprit = bpy.context.active_object
    bowsprit.rotation_euler = (0, math.radians(65), 0)
    bowsprit.data.materials.append(mat_spars)

    # Forestay Rigging Cable from Bowsprit to Fore Top
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=2.20, location=(2.10, 0.0, 2.30))
    forestay = bpy.context.active_object
    forestay.rotation_euler = (0, math.radians(-48), 0)
    forestay.data.materials.append(mat_rope)

    export_gltf(get_output_path("fluyt_cargo_ship.glb"))

def main():
    print("=== Generating Milestone 38 Models (High-Fidelity Detailing) ===")
    build_drydock_slipway()
    build_quayside_crane()
    build_fluyt_cargo_ship()
    print("=== Milestone 38 Generation Complete ===")

if __name__ == "__main__":
    main()
