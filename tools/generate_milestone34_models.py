# tools/generate_milestone34_models.py
# Procedural 3D model generator for Milestone 34: Heavy Siege Engines
# 1. trebuchet_siege.glb - Counterweight Trebuchet Siege Engine
# 2. battering_ram.glb - Armored Wheeled Battering Ram Penthouse
# 3. siege_tower.glb - Mobile Assault Belfry Siege Tower

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
# 1. COUNTERWEIGHT TREBUCHET SIEGE ENGINE
# ==========================================
def build_trebuchet_siege():
    clear_scene()
    
    mat_wood = create_material("HeavyOak", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_iron = create_material("ForgedIron", (0.15, 0.16, 0.18, 1.0), roughness=0.45, metallic=0.9)
    mat_stone = create_material("CounterweightStone", (0.45, 0.45, 0.43, 1.0), roughness=0.9)
    mat_rope = create_material("HempRope", (0.55, 0.48, 0.35, 1.0), roughness=0.9)
    mat_gold = create_material("BronzePivot", (0.75, 0.58, 0.25, 1.0), roughness=0.35, metallic=0.8)

    # Base chassis runners (left & right)
    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side * 1.0, 0.15))
        runner = bpy.context.active_object
        runner.scale = (4.8, 0.25, 0.25)
        runner.data.materials.append(mat_wood)

    # Cross ties
    for x in [-2.0, -0.8, 0.8, 2.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 0.2))
        cross = bpy.context.active_object
        cross.scale = (0.22, 2.2, 0.2)
        cross.data.materials.append(mat_wood)

    # A-frame vertical uprights
    for side in [-1.0, 1.0]:
        # Front strut
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.6, side * 1.0, 1.4))
        strut1 = bpy.context.active_object
        strut1.scale = (0.24, 0.22, 2.6)
        strut1.rotation_euler = (0.0, math.radians(24), 0.0)
        strut1.data.materials.append(mat_wood)

        # Rear strut
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.6, side * 1.0, 1.4))
        strut2 = bpy.context.active_object
        strut2.scale = (0.24, 0.22, 2.6)
        strut2.rotation_euler = (0.0, math.radians(-24), 0.0)
        strut2.data.materials.append(mat_wood)

        # Top axle bearing cap
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side * 1.0, 2.55))
        cap = bpy.context.active_object
        cap.scale = (0.45, 0.3, 0.3)
        cap.data.materials.append(mat_iron)

    # Central pivot axle (Iron)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=2.4, location=(0.0, 0.0, 2.55))
    axle = bpy.context.active_object
    axle.rotation_euler = (math.radians(90), 0.0, 0.0)
    axle.data.materials.append(mat_iron)

    # Bronze bushings
    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.18, location=(0.0, side * 0.85, 2.55))
        bushing = bpy.context.active_object
        bushing.rotation_euler = (math.radians(90), 0.0, 0.0)
        bushing.data.materials.append(mat_gold)

    # Long tapered throwing beam (tilted at ready-to-launch angle)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.1, 0.0, 2.85))
    beam = bpy.context.active_object
    beam.scale = (4.6, 0.28, 0.32)
    beam.rotation_euler = (0.0, math.radians(35), 0.0)
    beam.data.materials.append(mat_wood)

    # Iron beam reinforcement straps & hinge collar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 2.55))
    collar = bpy.context.active_object
    collar.scale = (0.5, 0.36, 0.45)
    collar.rotation_euler = (0.0, math.radians(35), 0.0)
    collar.data.materials.append(mat_iron)

    # Counterweight hopper box (hung at short front end of beam)
    # Front short arm tip is around (-1.6, 0.0, 1.7)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.6, 0.0, 1.1))
    hopper = bpy.context.active_object
    hopper.scale = (0.9, 0.9, 1.1)
    hopper.data.materials.append(mat_wood)

    # Heavy stone ballast fill inside hopper
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.6, 0.0, 1.45))
    stones = bpy.context.active_object
    stones.scale = (0.82, 0.82, 0.35)
    stones.data.materials.append(mat_stone)

    # Hopper iron corner brackets
    for dx in [-0.46, 0.46]:
        for dy in [-0.46, 0.46]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.6 + dx, dy, 1.1))
            strap = bpy.context.active_object
            strap.scale = (0.08, 0.08, 1.12)
            strap.data.materials.append(mat_iron)

    # Sling pouch and guide chute at long rear end (around X=2.8, Z=3.8)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(2.6, 0.0, 3.2))
    sling_rope = bpy.context.active_object
    sling_rope.rotation_euler = (0.0, math.radians(-40), 0.0)
    sling_rope.data.materials.append(mat_rope)

    # Boulder in sling
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.25, subdivisions=2, location=(2.2, 0.0, 2.6))
    boulder = bpy.context.active_object
    boulder.data.materials.append(mat_stone)

    # Rear hand winch spool & crank wheel
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.8, location=(1.8, 0.0, 0.45))
    winch = bpy.context.active_object
    winch.rotation_euler = (math.radians(90), 0.0, 0.0)
    winch.data.materials.append(mat_wood)

    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.04, location=(1.8, side * 0.95, 0.45))
        wheel = bpy.context.active_object
        wheel.rotation_euler = (math.radians(90), 0.0, 0.0)
        wheel.data.materials.append(mat_iron)

    export_gltf(get_output_path("trebuchet_siege.glb"))

# ==========================================
# 2. ARMORED WHEELED BATTERING RAM PENTHOUSE
# ==========================================
def build_battering_ram():
    clear_scene()

    mat_wood = create_material("AgedOak", (0.32, 0.20, 0.11, 1.0), roughness=0.88)
    mat_roof = create_material("RawhidePlating", (0.42, 0.32, 0.22, 1.0), roughness=0.75)
    mat_iron = create_material("ForgedIron", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)
    mat_chain = create_material("IronChain", (0.20, 0.21, 0.23, 1.0), roughness=0.4, metallic=0.95)

    # 4 Heavy Spoked Timber Wheels with Iron Rims
    wheel_coords = [(-1.5, -1.0), (-1.5, 1.0), (1.5, -1.0), (1.5, 1.0)]
    for x, y in wheel_coords:
        # Iron rim tyre
        bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.06, location=(x, y, 0.45))
        rim = bpy.context.active_object
        rim.rotation_euler = (math.radians(90), 0.0, 0.0)
        rim.data.materials.append(mat_iron)

        # Timber hub & spokes
        bpy.ops.mesh.primitive_cylinder_add(radius=0.40, depth=0.12, location=(x, y, 0.45))
        hub = bpy.context.active_object
        hub.rotation_euler = (math.radians(90), 0.0, 0.0)
        hub.data.materials.append(mat_wood)

    # Wheel Axles (Iron)
    for x in [-1.5, 1.5]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=2.2, location=(x, 0.0, 0.45))
        axle = bpy.context.active_object
        axle.rotation_euler = (math.radians(90), 0.0, 0.0)
        axle.data.materials.append(mat_iron)

    # Penthouse Chassis Frame (Lower Sill Beams)
    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side * 0.88, 0.65))
        sill = bpy.context.active_object
        sill.scale = (3.8, 0.22, 0.22)
        sill.data.materials.append(mat_wood)

    # 6 Vertical Uprights
    for x in [-1.6, 0.0, 1.6]:
        for y in [-0.88, 0.88]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 1.5))
            post = bpy.context.active_object
            post.scale = (0.2, 0.2, 1.6)
            post.data.materials.append(mat_wood)

    # Top Ridge Beams and Gables
    for side in [-1.0, 1.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side * 0.88, 2.3))
        plate = bpy.context.active_object
        plate.scale = (3.8, 0.2, 0.18)
        plate.data.materials.append(mat_wood)

    # Pitched Roof Ridge
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 2.9))
    ridge = bpy.context.active_object
    ridge.scale = (3.8, 0.18, 0.18)
    ridge.data.materials.append(mat_wood)

    # Armored Pitched Roof Slopes (Rawhide & Heavy Planks)
    # Left slope
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.55, 2.6))
    roof_l = bpy.context.active_object
    roof_l.scale = (3.9, 1.25, 0.10)
    roof_l.rotation_euler = (math.radians(32), 0.0, 0.0)
    roof_l.data.materials.append(mat_roof)

    # Right slope
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.55, 2.6))
    roof_r = bpy.context.active_object
    roof_r.scale = (3.9, 1.25, 0.10)
    roof_r.rotation_euler = (math.radians(-32), 0.0, 0.0)
    roof_r.data.materials.append(mat_roof)

    # Iron roof edge straps & pyramid studs
    for x in [-1.8, 0.0, 1.8]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 2.92))
        strap = bpy.context.active_object
        strap.scale = (0.12, 1.6, 0.06)
        strap.data.materials.append(mat_iron)

    # 4 Suspension Chains
    chain_positions = [(-1.0, -0.5), (-1.0, 0.5), (1.0, -0.5), (1.0, 0.5)]
    for x, y in chain_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.1, location=(x, y, 1.7))
        chain = bpy.context.active_object
        chain.data.materials.append(mat_chain)

    # Suspended Massive Oak Tree Trunk (Battering Ram)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=4.2, location=(0.2, 0.0, 1.15))
    trunk = bpy.context.active_object
    trunk.rotation_euler = (0.0, math.radians(90), 0.0)
    trunk.data.materials.append(mat_wood)

    # Forged Iron Ram Head (Front Strike Cap)
    # Located at front end (around X = 2.3)
    bpy.ops.mesh.primitive_cone_add(radius1=0.28, radius2=0.12, depth=0.55, location=(2.45, 0.0, 1.15))
    ram_head = bpy.context.active_object
    ram_head.rotation_euler = (0.0, math.radians(90), 0.0)
    ram_head.data.materials.append(mat_iron)

    # Crowned Iron Impact Boss
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.18, subdivisions=2, location=(2.72, 0.0, 1.15))
    boss = bpy.context.active_object
    boss.data.materials.append(mat_iron)

    # Iron collar bands along the trunk
    for x in [0.8, -0.2, -1.2]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.26, minor_radius=0.04, location=(x, 0.0, 1.15))
        band = bpy.context.active_object
        band.rotation_euler = (0.0, math.radians(90), 0.0)
        band.data.materials.append(mat_iron)

    export_gltf(get_output_path("battering_ram.glb"))

# ==========================================
# 3. MOBILE ASSAULT BELFRY SIEGE TOWER
# ==========================================
def build_siege_tower():
    clear_scene()

    mat_wood = create_material("TimberTower", (0.34, 0.22, 0.12, 1.0), roughness=0.85)
    mat_plank = create_material("ArmoredHoarding", (0.42, 0.28, 0.16, 1.0), roughness=0.80)
    mat_iron = create_material("IronFittings", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)
    mat_rope = create_material("AssaultRope", (0.55, 0.48, 0.35, 1.0), roughness=0.9)

    # 4 Heavy Base Wheels
    for x in [-1.4, 1.4]:
        for y in [-1.3, 1.3]:
            # Iron rim tyre
            bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.08, location=(x, y, 0.55))
            rim = bpy.context.active_object
            rim.rotation_euler = (math.radians(90), 0.0, 0.0)
            rim.data.materials.append(mat_iron)

            # Wood disc
            bpy.ops.mesh.primitive_cylinder_add(radius=0.50, depth=0.16, location=(x, y, 0.55))
            disc = bpy.context.active_object
            disc.rotation_euler = (math.radians(90), 0.0, 0.0)
            disc.data.materials.append(mat_wood)

    # Lower Platform Frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.8))
    base_deck = bpy.context.active_object
    base_deck.scale = (3.2, 2.4, 0.22)
    base_deck.data.materials.append(mat_wood)

    # 4 Main Vertical Corner Masts (Tower tapers slightly as it rises to 4.8m height)
    masts = [
        (-1.2, -0.9, 0.8), (1.2, -0.9, 0.8),
        (-1.2, 0.9, 0.8), (1.2, 0.9, 0.8)
    ]
    for x, y, z in masts:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 2.7))
        mast = bpy.context.active_object
        mast.scale = (0.24, 0.24, 3.8)
        mast.data.materials.append(mat_wood)

    # Diagonal X-Bracing on sides
    for side in [-0.92, 0.92]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 2.6))
        brace1 = bpy.context.active_object
        brace1.scale = (3.0, 0.08, 0.18)
        brace1.rotation_euler = (0.0, math.radians(35), 0.0)
        brace1.data.materials.append(mat_wood)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 2.6))
        brace2 = bpy.context.active_object
        brace2.scale = (3.0, 0.08, 0.18)
        brace2.rotation_euler = (0.0, math.radians(-35), 0.0)
        brace2.data.materials.append(mat_wood)

    # Mid Deck Platform (Floor 2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 2.5))
    mid_deck = bpy.context.active_object
    mid_deck.scale = (2.8, 2.1, 0.18)
    mid_deck.data.materials.append(mat_wood)

    # Front Armored Arrow Slit Hoardings (Protective front screen on levels 1 and 2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.25, 0.0, 2.4))
    front_screen = bpy.context.active_object
    front_screen.scale = (0.12, 1.9, 3.0)
    front_screen.data.materials.append(mat_plank)

    # Cutout Arrow Slit visual details on front screen
    for slit_z in [1.8, 2.8, 3.6]:
        for slit_y in [-0.5, 0.5]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.32, slit_y, slit_z))
            slit = bpy.context.active_object
            slit.scale = (0.06, 0.12, 0.35)
            slit.data.materials.append(mat_iron)

    # Top Assault Platform Deck (Floor 3 at Z = 4.4)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 4.4))
    top_deck = bpy.context.active_object
    top_deck.scale = (2.6, 2.0, 0.20)
    top_deck.data.materials.append(mat_wood)

    # Top Crenellated Battlements (Rear and sides)
    # Rear wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.25, 0.0, 4.9))
    rear_wall = bpy.context.active_object
    rear_wall.scale = (0.12, 2.0, 0.8)
    rear_wall.data.materials.append(mat_plank)

    # Side walls
    for side in [-0.95, 0.95]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 4.9))
        side_wall = bpy.context.active_object
        side_wall.scale = (2.4, 0.12, 0.8)
        side_wall.data.materials.append(mat_plank)

    # Front Assault Drop Gangplank (Corvus Bridge ready to bridge onto castle ramparts)
    # Hinged at (1.25, 0.0, 4.4), extended forward at 45 degree angle
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(2.1, 0.0, 3.8))
    bridge = bpy.context.active_object
    bridge.scale = (2.0, 1.6, 0.14)
    bridge.rotation_euler = (0.0, math.radians(40), 0.0)
    bridge.data.materials.append(mat_wood)

    # Iron cleats / spikes at tip of gangplank
    for dy in [-0.5, 0.0, 0.5]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.06, depth=0.25, location=(2.85, dy, 3.15))
        spike = bpy.context.active_object
        spike.rotation_euler = (0.0, math.radians(130), 0.0)
        spike.data.materials.append(mat_iron)

    # Pulley Gantry Mast at top front for lowering/raising gangplank
    for dy in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.25, dy, 5.2))
        jib = bpy.context.active_object
        jib.scale = (0.16, 0.16, 1.2)
        jib.data.materials.append(mat_wood)

    # Winch ropes running from top gantry down to gangplank
    for dy in [-0.7, 0.7]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, location=(1.9, dy, 4.5))
        rope = bpy.context.active_object
        rope.rotation_euler = (0.0, math.radians(-35), 0.0)
        rope.data.materials.append(mat_rope)

    export_gltf(get_output_path("siege_tower.glb"))

if __name__ == "__main__":
    print("[M34] Generating 3D Models for Milestone 34...")
    build_trebuchet_siege()
    build_battering_ram()
    build_siege_tower()
    print("[M34] All 3 models generated successfully!")
