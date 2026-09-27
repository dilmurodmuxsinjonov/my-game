# tools/generate_milestone38_models.py
# Procedural 3D model generator for Milestone 38: Medieval Port Logistics & Shipbuilding
# 1. drydock_slipway.glb - Shipbuilding Slipway Cradle with Scaffolding & Keel
# 2. quayside_crane.glb - Harbor Quayside Jib Crane on Stone Plinth with Cargo Sling
# 3. fluyt_cargo_ship.glb - Ocean-Going Fluyt Merchant Cargo Vessel

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
# 1. SHIPBUILDING DRYDOCK SLIPWAY
# ==========================================
def build_drydock_slipway():
    clear_scene()

    mat_oak = create_material("WeatheredOakTimber", (0.28, 0.18, 0.10, 1.0), roughness=0.85)
    mat_skids = create_material("GreasedSkidRails", (0.12, 0.10, 0.08, 1.0), roughness=0.25, metallic=0.1)
    mat_fresh_wood = create_material("FreshShipRibs", (0.52, 0.35, 0.20, 1.0), roughness=0.72)
    mat_iron = create_material("ShipwrightIron", (0.18, 0.19, 0.21, 1.0), roughness=0.45, metallic=0.9)
    mat_tar = create_material("PitchTarPot", (0.06, 0.06, 0.07, 1.0), roughness=0.2, metallic=0.1)

    # 1. Inclined coastal timber skids (sloped -7 degrees towards water)
    for y_pos in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 0.25))
        skid = bpy.context.active_object
        skid.scale = (4.2, 0.28, 0.22)
        skid.rotation_euler = (0, math.radians(7), 0)
        skid.data.materials.append(mat_oak)

        # Greased iron runner strip on top of skid
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_pos, 0.38))
        runner = bpy.context.active_object
        runner.scale = (4.2, 0.12, 0.04)
        runner.rotation_euler = (0, math.radians(7), 0)
        runner.data.materials.append(mat_skids)

    # Cross ties under skids
    for x_pos in [-1.6, -0.8, 0.0, 0.8, 1.6]:
        z_pos = 0.15 - (x_pos * 0.12)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, z_pos))
        crosstie = bpy.context.active_object
        crosstie.scale = (0.24, 2.2, 0.16)
        crosstie.data.materials.append(mat_oak)

    # Keel blocks down center
    for x_pos in [-1.5, -0.9, -0.3, 0.3, 0.9, 1.5]:
        z_pos = 0.30 - (x_pos * 0.12)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, z_pos))
        kblock = bpy.context.active_object
        kblock.scale = (0.35, 0.45, 0.26)
        kblock.data.materials.append(mat_oak)

    # Keel timber laid on blocks
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.52))
    keel = bpy.context.active_object
    keel.scale = (3.6, 0.20, 0.24)
    keel.rotation_euler = (0, math.radians(7), 0)
    keel.data.materials.append(mat_fresh_wood)

    # Stem and stern posts
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.75, 0.0, 0.95))
    stem = bpy.context.active_object
    stem.scale = (0.18, 0.18, 0.85)
    stem.rotation_euler = (0, math.radians(-25), 0)
    stem.data.materials.append(mat_fresh_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.75, 0.0, 0.55))
    sternpost = bpy.context.active_object
    sternpost.scale = (0.18, 0.18, 0.75)
    sternpost.rotation_euler = (0, math.radians(15), 0)
    sternpost.data.materials.append(mat_fresh_wood)

    # Curved ship rib frames under construction (5 rib pairs)
    for idx, rx in enumerate([-1.2, -0.6, 0.0, 0.6, 1.2]):
        rz = 0.55 - (rx * 0.12)
        rib_width = 1.1 - abs(rx * 0.3)
        # Port rib
        bpy.ops.mesh.primitive_torus_add(major_radius=rib_width * 0.5, minor_radius=0.06, location=(rx, rib_width * 0.5, rz + 0.3))
        rib_p = bpy.context.active_object
        rib_p.rotation_euler = (0, math.radians(90), 0)
        rib_p.scale = (1.0, 1.0, 0.6)
        rib_p.data.materials.append(mat_fresh_wood)

        # Starboard rib
        bpy.ops.mesh.primitive_torus_add(major_radius=rib_width * 0.5, minor_radius=0.06, location=(rx, -rib_width * 0.5, rz + 0.3))
        rib_s = bpy.context.active_object
        rib_s.rotation_euler = (0, math.radians(90), 0)
        rib_s.scale = (1.0, 1.0, 0.6)
        rib_s.data.materials.append(mat_fresh_wood)

    # Scaffolding catwalks on port and starboard sides
    for y_side in [-1.35, 1.35]:
        # Upright scaffold poles
        for sx in [-1.4, 0.0, 1.4]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.8, location=(sx, y_side, 0.9))
            pole = bpy.context.active_object
            pole.data.materials.append(mat_oak)

        # Horizontal staging planks
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y_side, 0.75))
        plank = bpy.context.active_object
        plank.scale = (3.4, 0.35, 0.06)
        plank.data.materials.append(mat_oak)

    # Tar pitch melting kettle on tripod
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.25, location=(-1.9, 1.3, 0.28))
    pot = bpy.context.active_object
    pot.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.04, location=(-1.9, 1.3, 0.38))
    pitch = bpy.context.active_object
    pitch.data.materials.append(mat_tar)

    export_gltf(get_output_path("drydock_slipway.glb"))


# ==========================================
# 2. HARBOR QUAYSIDE JIB CRANE
# ==========================================
def build_quayside_crane():
    clear_scene()

    mat_stone = create_material("PierLimestone", (0.55, 0.53, 0.50, 1.0), roughness=0.88)
    mat_oak = create_material("CraneOakBeams", (0.34, 0.22, 0.12, 1.0), roughness=0.82)
    mat_iron = create_material("ForgedCraneIron", (0.18, 0.19, 0.21, 1.0), roughness=0.42, metallic=0.92)
    mat_ballast = create_material("CounterweightStone", (0.45, 0.42, 0.38, 1.0), roughness=0.9)
    mat_rope = create_material("HempCable", (0.52, 0.45, 0.32, 1.0), roughness=0.9)
    mat_crate = create_material("CargoCrateWood", (0.45, 0.30, 0.16, 1.0), roughness=0.78)

    # 1. Octagonal stone plinth / barbette
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.0, depth=0.45, location=(0.0, 0.0, 0.22))
    plinth = bpy.context.active_object
    plinth.data.materials.append(mat_stone)

    # Central iron pintle thrust ring
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.10, location=(0.0, 0.0, 0.50))
    thrust_ring = bpy.context.active_object
    thrust_ring.data.materials.append(mat_iron)

    # 2. Heavy central vertical mast
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.7))
    mast = bpy.context.active_object
    mast.scale = (0.28, 0.28, 2.4)
    mast.data.materials.append(mat_oak)

    # Mast iron collar bands
    for mz in [0.75, 1.6, 2.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, mz))
        band = bpy.context.active_object
        band.scale = (0.32, 0.32, 0.08)
        band.data.materials.append(mat_iron)

    # 3. Angled Jib Boom (outreach over water towards +X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.05, 0.0, 2.2))
    boom = bpy.context.active_object
    boom.scale = (2.4, 0.22, 0.22)
    boom.rotation_euler = (0, math.radians(-38), 0)
    boom.data.materials.append(mat_oak)

    # Tie rod from mast peak to boom tip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.9, location=(0.95, 0.0, 2.75))
    tierod = bpy.context.active_object
    tierod.rotation_euler = (0, math.radians(65), 0)
    tierod.data.materials.append(mat_iron)

    # Boom head pulley sheaves at tip (x=1.9, z=2.9)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.12, location=(1.95, 0.0, 2.92))
    sheave = bpy.context.active_object
    sheave.rotation_euler = (math.radians(90), 0, 0)
    sheave.data.materials.append(mat_iron)

    # 4. Rear Counterweight Ballast Box (towards -X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.85, 0.0, 1.1))
    cbox = bpy.context.active_object
    cbox.scale = (0.85, 0.85, 0.65)
    cbox.data.materials.append(mat_oak)

    # Ballast stone blocks inside box
    for bx in [-0.95, -0.75]:
        for by in [-0.2, 0.2]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, 1.45))
            bstone = bpy.context.active_object
            bstone.scale = (0.16, 0.28, 0.16)
            bstone.data.materials.append(mat_ballast)

    # 5. Dual Winch Drums & Kinetic Drive Gear
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.6, location=(0.0, -0.42, 0.95))
    winch = bpy.context.active_object
    winch.rotation_euler = (math.radians(90), 0, 0)
    winch.data.materials.append(mat_iron)

    # Ratchet gear wheel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.06, location=(0.0, -0.15, 0.95))
    gear = bpy.context.active_object
    gear.rotation_euler = (math.radians(90), 0, 0)
    gear.data.materials.append(mat_iron)

    # 6. Suspended Hoist Cable, Hook & Cargo Crate
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=1.6, location=(1.95, 0.0, 2.1))
    cable = bpy.context.active_object
    cable.data.materials.append(mat_rope)

    # Iron forged cargo hook
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.03, location=(1.95, 0.0, 1.25))
    hook = bpy.context.active_object
    hook.rotation_euler = (0, math.radians(90), 0)
    hook.data.materials.append(mat_iron)

    # Suspended banded cargo crate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.95, 0.0, 0.72))
    crate = bpy.context.active_object
    crate.scale = (0.75, 0.75, 0.75)
    crate.data.materials.append(mat_crate)

    # Crate iron banding
    for cz in [0.45, 0.98]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.95, 0.0, cz))
        cband = bpy.context.active_object
        cband.scale = (0.78, 0.78, 0.05)
        cband.data.materials.append(mat_iron)

    export_gltf(get_output_path("quayside_crane.glb"))


# ==========================================
# 3. OCEAN-GOING FLUYT CARGO VESSEL
# ==========================================
def build_fluyt_cargo_ship():
    clear_scene()

    mat_hull = create_material("FluytOakHull", (0.24, 0.16, 0.10, 1.0), roughness=0.82)
    mat_deck = create_material("FluytPineDeck", (0.52, 0.38, 0.24, 1.0), roughness=0.75)
    mat_sails = create_material("CanvasSails", (0.88, 0.85, 0.78, 1.0), roughness=0.85)
    mat_spars = create_material("SpruceSpars", (0.40, 0.26, 0.14, 1.0), roughness=0.7)
    mat_brass = create_material("SternLanternBrass", (0.82, 0.65, 0.22, 1.0), roughness=0.25, metallic=0.95)
    mat_hatch = create_material("CargoHatchCover", (0.35, 0.28, 0.18, 1.0), roughness=0.85)

    # 1. Main Hull (pear-shaped tumblehome, rounded bilge)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.65))
    hull = bpy.context.active_object
    hull.scale = (3.8, 1.45, 0.95)
    hull.data.materials.append(mat_hull)

    # Tapered bow wedge
    bpy.ops.mesh.primitive_cone_add(radius1=0.75, depth=1.3, location=(2.2, 0.0, 0.65))
    bow = bpy.context.active_object
    bow.rotation_euler = (0, math.radians(-90), 0)
    bow.scale = (1.0, 0.95, 1.0)
    bow.data.materials.append(mat_hull)

    # Raised forecastle deck
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.5, 0.0, 1.25))
    fcastle = bpy.context.active_object
    fcastle.scale = (0.9, 1.3, 0.40)
    fcastle.data.materials.append(mat_hull)

    # Raised aftcastle / quarterdeck
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.4, 0.0, 1.35))
    acastle = bpy.context.active_object
    acastle.scale = (1.2, 1.25, 0.60)
    acastle.data.materials.append(mat_hull)

    # Rounded Dutch stern transom (tuck)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.2, location=(-2.05, 0.0, 1.35))
    transom = bpy.context.active_object
    transom.rotation_euler = (0, math.radians(90), 0)
    transom.data.materials.append(mat_hull)

    # Stern transom windows
    for wy in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-2.16, wy, 1.45))
        win = bpy.context.active_object
        win.scale = (0.05, 0.18, 0.22)
        win.data.materials.append(mat_brass)

    # Stern ornate navigation lantern
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.24, location=(-2.25, 0.0, 1.85))
    slantern = bpy.context.active_object
    slantern.data.materials.append(mat_brass)

    # Main weather deck planking
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.05))
    deck = bpy.context.active_object
    deck.scale = (2.2, 1.35, 0.05)
    deck.data.materials.append(mat_deck)

    # 2 Cargo Hold Hatches on main deck
    for hx in [-0.45, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, 0.0, 1.15))
        hatch = bpy.context.active_object
        hatch.scale = (0.55, 0.75, 0.12)
        hatch.data.materials.append(mat_hatch)

    # 2. Main Mast (Center) with Square Sails
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=3.2, location=(0.1, 0.0, 2.5))
    mainmast = bpy.context.active_object
    mainmast.data.materials.append(mat_spars)

    # Lower main yardarm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=2.2, location=(0.1, 0.0, 2.1))
    mainyard = bpy.context.active_object
    mainyard.rotation_euler = (math.radians(90), 0, 0)
    mainyard.data.materials.append(mat_spars)

    # Lower square course sail (billowed curve)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0.0, 1.75))
    mainsail = bpy.context.active_object
    mainsail.scale = (0.04, 1.9, 0.65)
    mainsail.data.materials.append(mat_sails)

    # Upper topsail yardarm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.5, location=(0.1, 0.0, 3.1))
    topyard = bpy.context.active_object
    topyard.rotation_euler = (math.radians(90), 0, 0)
    topyard.data.materials.append(mat_spars)

    # Upper square topsail
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.16, 0.0, 2.65))
    topsail = bpy.context.active_object
    topsail.scale = (0.04, 1.3, 0.75)
    topsail.data.materials.append(mat_sails)

    # Crow's nest platform
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.18, location=(0.1, 0.0, 3.25))
    crowsnest = bpy.context.active_object
    crowsnest.data.materials.append(mat_hull)

    # 3. Fore Mast (Forward) with Foresail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.4, location=(1.45, 0.0, 2.1))
    foremast = bpy.context.active_object
    foremast.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(1.45, 0.0, 2.3))
    foreyard = bpy.context.active_object
    foreyard.rotation_euler = (math.radians(90), 0, 0)
    foreyard.data.materials.append(mat_spars)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.52, 0.0, 1.8))
    foresail = bpy.context.active_object
    foresail.scale = (0.04, 1.4, 0.75)
    foresail.data.materials.append(mat_sails)

    # 4. Mizzen Mast (Aft) with Lateen Triangular Sail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.9, location=(-1.25, 0.0, 2.05))
    mizzen = bpy.context.active_object
    mizzen.data.materials.append(mat_spars)

    # Lateen yard (slanted 45 degrees)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(-1.25, 0.0, 2.2))
    lateen_yard = bpy.context.active_object
    lateen_yard.rotation_euler = (0, math.radians(-42), 0)
    lateen_yard.data.materials.append(mat_spars)

    # Lateen sail
    bpy.ops.mesh.primitive_cone_add(radius1=0.65, depth=1.2, location=(-1.35, 0.0, 1.95))
    lateen_sail = bpy.context.active_object
    lateen_sail.rotation_euler = (0, math.radians(110), 0)
    lateen_sail.scale = (0.04, 0.85, 1.0)
    lateen_sail.data.materials.append(mat_sails)

    # 5. Bowsprit Spar (Forward slanting)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.8, location=(2.65, 0.0, 1.45))
    bowsprit = bpy.context.active_object
    bowsprit.rotation_euler = (0, math.radians(65), 0)
    bowsprit.data.materials.append(mat_spars)

    # Rudder and Tiller at stern
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-2.15, 0.0, 0.55))
    rudder = bpy.context.active_object
    rudder.scale = (0.24, 0.08, 0.85)
    rudder.data.materials.append(mat_hull)

    export_gltf(get_output_path("fluyt_cargo_ship.glb"))


if __name__ == "__main__":
    print("[M38] Building medieval port logistics and naval models...")
    build_drydock_slipway()
    build_quayside_crane()
    build_fluyt_cargo_ship()
    print("[M38] All 3 models built successfully!")
