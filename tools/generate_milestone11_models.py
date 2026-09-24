"""Blender 5.2 Headless Model Generator for Milestone 11:
1. water_wheel.glb (Kinetic Water Wheel with Timber Paddles & Iron Axle Gear)
2. millstone.glb (Granite Millstones with Hopper Funnel & Flour Spout)
3. trip_hammer.glb (Cam-Driven Industrial Trip Hammer for Automated Ore Crushing)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def export_glb(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORT] Generated: {filepath} ({os.path.getsize(filepath)} bytes)")

# -------------------------------------------------------------
# 25. Kinetic Water Wheel (water_wheel.glb)
# -------------------------------------------------------------
def build_water_wheel():
    reset_scene()
    mat_wood_dark = create_material("DarkTimber", (0.24, 0.15, 0.08, 1.0), roughness=0.8)
    mat_wood_plank = create_material("PlankWood", (0.42, 0.28, 0.16, 1.0), roughness=0.7)
    mat_iron = create_material("BearingIron", (0.18, 0.19, 0.21, 1.0), roughness=0.35, metallic=0.85)
    mat_gear = create_material("BrassCog", (0.55, 0.42, 0.15, 1.0), roughness=0.4, metallic=0.8)

    # 1. Timber Support Framework (Two side trestles)
    for side_x in [-0.85, 0.85]:
        # Vertical Post
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 1.1))
        post = bpy.context.active_object
        post.scale = (0.16, 0.20, 2.2)
        post.data.materials.append(mat_wood_dark)

        # Base Sole Sill
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 0.08))
        sill = bpy.context.active_object
        sill.scale = (0.20, 1.4, 0.16)
        sill.data.materials.append(mat_wood_dark)

        # Diagonal Struts (Front & Back)
        for s_sign in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, s_sign * 0.45, 0.6), rotation=(math.radians(s_sign * -40), 0, 0))
            strut = bpy.context.active_object
            strut.scale = (0.12, 0.12, 1.2)
            strut.data.materials.append(mat_wood_dark)

        # Top Cast Iron Pillow Block Bearing
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 2.22))
        bearing = bpy.context.active_object
        bearing.scale = (0.20, 0.26, 0.12)
        bearing.data.materials.append(mat_iron)

    # 2. Main Horizontal Axle (passes through center at Z=2.2)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=2.1, vertices=10, location=(0, 0, 2.2), rotation=(0, math.radians(90), 0))
    axle = bpy.context.active_object
    axle.data.materials.append(mat_wood_dark)

    # Iron Axle Rings & End Journals
    for ax_x in [-0.95, -0.65, 0.65, 0.95]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.155, depth=0.12, vertices=10, location=(ax_x, 0, 2.2), rotation=(0, math.radians(90), 0))
        ring = bpy.context.active_object
        ring.data.materials.append(mat_iron)

    # 3. Central Octagonal Wheel Hubs
    for hub_x in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.16, vertices=8, location=(hub_x, 0, 2.2), rotation=(0, math.radians(90), 0))
        hub = bpy.context.active_object
        hub.data.materials.append(mat_wood_dark)

    # 4. Radial Spokes & Water Paddles (8 Spokes / Blades)
    num_blades = 8
    radius_wheel = 1.7
    for i in range(num_blades):
        angle = (2.0 * math.pi / num_blades) * i
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Timber Spokes on left and right wheel faces
        for sp_x in [-0.45, 0.45]:
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=(sp_x, (radius_wheel * 0.5) * cos_a, 2.2 + (radius_wheel * 0.5) * sin_a),
                rotation=(-angle, 0, 0)
            )
            spoke = bpy.context.active_object
            spoke.scale = (0.08, radius_wheel * 0.95, 0.08)
            spoke.data.materials.append(mat_wood_dark)

        # Cross Paddle Blade (Wide timber board between rims)
        blade_pos_y = radius_wheel * cos_a
        blade_pos_z = 2.2 + radius_wheel * sin_a
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(0, blade_pos_y, blade_pos_z),
            rotation=(-angle, 0, 0)
        )
        paddle = bpy.context.active_object
        paddle.scale = (0.96, 0.42, 0.06)
        paddle.data.materials.append(mat_wood_plank)

        # Rim perimeter chord boards connecting paddle tips
        for rm_x in [-0.45, 0.45]:
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=(rm_x, radius_wheel * 0.92 * cos_a, 2.2 + radius_wheel * 0.92 * sin_a),
                rotation=(-angle, 0, 0)
            )
            rim_seg = bpy.context.active_object
            rim_seg.scale = (0.09, 0.10, 0.65)
            rim_seg.data.materials.append(mat_wood_dark)

    # 5. Output Kinetic Spur Cog Gear on side
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.10, vertices=16, location=(1.05, 0, 2.2), rotation=(0, math.radians(90), 0))
    gear = bpy.context.active_object
    gear.data.materials.append(mat_gear)

    # Cog teeth around gear
    for t in range(12):
        t_angle = (2.0 * math.pi / 12) * t
        t_y = 0.48 * math.cos(t_angle)
        t_z = 2.2 + 0.48 * math.sin(t_angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.05, t_y, t_z), rotation=(-t_angle, 0, 0))
        tooth = bpy.context.active_object
        tooth.scale = (0.10, 0.10, 0.10)
        tooth.data.materials.append(mat_gear)

    export_glb("water_wheel.glb")

# -------------------------------------------------------------
# 26. Mechanical Millstone (millstone.glb)
# -------------------------------------------------------------
def build_millstone():
    reset_scene()
    mat_wood = create_material("MillWood", (0.34, 0.22, 0.12, 1.0), roughness=0.7)
    mat_stone_bed = create_material("BedStone", (0.28, 0.28, 0.30, 1.0), roughness=0.9)
    mat_stone_run = create_material("RunnerStone", (0.48, 0.47, 0.45, 1.0), roughness=0.85)
    mat_iron = create_material("MillIron", (0.16, 0.17, 0.19, 1.0), roughness=0.35, metallic=0.85)
    mat_flour = create_material("FlourMeal", (0.92, 0.90, 0.82, 1.0), roughness=0.95)

    # 1. Sturdy Timber Stand (4 legs + top rim platform)
    for lx in [-0.55, 0.55]:
        for ly in [-0.55, 0.55]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.32))
            leg = bpy.context.active_object
            leg.scale = (0.14, 0.14, 0.64)
            leg.data.materials.append(mat_wood)

    # Platform frame base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.66))
    frame = bpy.context.active_object
    frame.scale = (1.30, 1.30, 0.10)
    frame.data.materials.append(mat_wood)

    # 2. Wooden Round Curb / Vat Enclosure
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.48, vertices=12, location=(0, 0, 0.94))
    vat = bpy.context.active_object
    vat.data.materials.append(mat_wood)

    # 3. Lower Stationary Bedstone (Dark Granite)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.18, vertices=12, location=(0, 0, 0.82))
    bedstone = bpy.context.active_object
    bedstone.data.materials.append(mat_stone_bed)

    # 4. Upper Rotating Runner Stone (Granite with central eye hole)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.53, depth=0.20, vertices=12, location=(0, 0, 1.02))
    runner = bpy.context.active_object
    runner.data.materials.append(mat_stone_run)

    # Central feeding eye (cylinder cut look / dark center)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.22, vertices=8, location=(0, 0, 1.04))
    eye = bpy.context.active_object
    eye.data.materials.append(mat_iron)

    # Iron Drive Spindle sticking up through the eye
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.60, vertices=8, location=(0, 0, 1.15))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_iron)

    # 5. Suspended Grain Feeding Hopper Funnel above stones
    # Hopper 4 support staves
    for hx in [-0.28, 0.28]:
        for hy in [-0.28, 0.28]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, hy, 1.40))
            stave = bpy.context.active_object
            stave.scale = (0.05, 0.05, 0.45)
            stave.data.materials.append(mat_wood)

    # Inverted Pyramid Hopper (Cone with 4 vertices)
    bpy.ops.mesh.primitive_cone_add(radius1=0.38, radius2=0.12, depth=0.36, vertices=4, location=(0, 0, 1.54), rotation=(0, 0, math.radians(45)))
    hopper = bpy.context.active_object
    hopper.data.materials.append(mat_wood)

    # 6. Flour Discharge Chute & Meal Spout on Front (+Y)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.65, 0.72), rotation=(math.radians(30), 0, 0))
    spout = bpy.context.active_object
    spout.scale = (0.22, 0.28, 0.10)
    spout.data.materials.append(mat_wood)

    # Small Wooden Flour Collection Bucket below spout
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.26, vertices=8, location=(0, 0.74, 0.14))
    bucket = bpy.context.active_object
    bucket.data.materials.append(mat_wood)

    # Flour Meal inside bucket
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.05, vertices=8, location=(0, 0.74, 0.22))
    flour_pile = bpy.context.active_object
    flour_pile.data.materials.append(mat_flour)

    export_glb("millstone.glb")

# -------------------------------------------------------------
# 27. Industrial Cam-Driven Trip Hammer (trip_hammer.glb)
# -------------------------------------------------------------
def build_trip_hammer():
    reset_scene()
    mat_stone_base = create_material("StoneBase", (0.25, 0.25, 0.26, 1.0), roughness=0.9)
    mat_oak_beam = create_material("OakBeam", (0.30, 0.18, 0.09, 1.0), roughness=0.75)
    mat_iron_heavy = create_material("HeavyIron", (0.14, 0.15, 0.16, 1.0), roughness=0.3, metallic=0.92)
    mat_crushed_ore = create_material("CrushedIronOre", (0.45, 0.26, 0.18, 1.0), roughness=0.85)

    # 1. Massive Stone Foundation Bed
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.14))
    foundation = bpy.context.active_object
    foundation.scale = (1.40, 2.40, 0.28)
    foundation.data.materials.append(mat_stone_base)

    # 2. Fulcrum Gallows Post Stand (Middle of the machine, Y=0.0)
    for fx in [-0.48, 0.48]:
        # Vertical Post
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, 0, 0.90))
        gallows = bpy.context.active_object
        gallows.scale = (0.18, 0.22, 1.30)
        gallows.data.materials.append(mat_oak_beam)

        # Diagonal Braces
        for b_sign in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, b_sign * 0.40, 0.60), rotation=(math.radians(b_sign * -35), 0, 0))
            brace = bpy.context.active_object
            brace.scale = (0.12, 0.12, 0.85)
            brace.data.materials.append(mat_oak_beam)

    # Horizontal Iron Pivot Axle across the gallows
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.20, vertices=10, location=(0, 0, 1.45), rotation=(0, math.radians(90), 0))
    pivot = bpy.context.active_object
    pivot.data.materials.append(mat_iron_heavy)

    # 3. Main Wooden Hammer Beam (Lever arm angled slightly upward, pivots at (0, 0, 1.45))
    # Beam extends from Y=-0.80 (tail) to Y=+0.95 (head)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.10, 1.48), rotation=(math.radians(-6), 0, 0))
    arm = bpy.context.active_object
    arm.scale = (0.22, 1.95, 0.24)
    arm.data.materials.append(mat_oak_beam)

    # Iron reinforcement bands around hammer arm
    for b_y in [-0.35, 0.10, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, b_y, 1.48), rotation=(math.radians(-6), 0, 0))
        band = bpy.context.active_object
        band.scale = (0.24, 0.08, 0.26)
        band.data.materials.append(mat_iron_heavy)

    # 4. Massive Cast Iron Hammer Head (Front, Y=+0.95)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 1.32))
    hammer_head = bpy.context.active_object
    hammer_head.scale = (0.42, 0.42, 0.55)
    hammer_head.data.materials.append(mat_iron_heavy)

    # 5. Heavy Iron Anvil / Die Block directly underneath hammer head
    # Wooden anvil block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.50))
    anvil_block = bpy.context.active_object
    anvil_block.scale = (0.65, 0.65, 0.45)
    anvil_block.data.materials.append(mat_oak_beam)

    # Steel Strike Die Plate on top of block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.78))
    die_plate = bpy.context.active_object
    die_plate.scale = (0.50, 0.50, 0.12)
    die_plate.data.materials.append(mat_iron_heavy)

    # Crushed Ore chunks on anvil plate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.86))
    ore_pile = bpy.context.active_object
    ore_pile.scale = (0.36, 0.36, 0.05)
    ore_pile.data.materials.append(mat_crushed_ore)

    # 6. Camshaft Mechanism at Tail (Y=-0.85)
    # Camshaft Bearing Posts
    for cx in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, -0.85, 0.65))
        cpost = bpy.context.active_object
        cpost.scale = (0.16, 0.18, 0.75)
        cpost.data.materials.append(mat_oak_beam)

    # Rotating Cam Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=1.15, vertices=8, location=(0, -0.85, 0.98), rotation=(0, math.radians(90), 0))
    cshaft = bpy.context.active_object
    cshaft.data.materials.append(mat_iron_heavy)

    # Curved Lifting Cam Teeth (3 offset radial cams that strike beam tail)
    for c_idx in range(3):
        c_ang = (2.0 * math.pi / 3.0) * c_idx
        cy = -0.85 + 0.18 * math.cos(c_ang)
        cz = 0.98 + 0.18 * math.sin(c_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, cy, cz), rotation=(-c_ang, 0, 0))
        cam_tooth = bpy.context.active_object
        cam_tooth.scale = (0.14, 0.22, 0.08)
        cam_tooth.data.materials.append(mat_iron_heavy)

    # Kinetic Pulley / Drive Wheel on Camshaft End
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.10, vertices=12, location=(0.60, -0.85, 0.98), rotation=(0, math.radians(90), 0))
    pulley = bpy.context.active_object
    pulley.data.materials.append(mat_oak_beam)

    export_glb("trip_hammer.glb")

if __name__ == "__main__":
    print("[BLENDER] Starting Milestone 11 Kinetic Model Generation...")
    build_water_wheel()
    build_millstone()
    build_trip_hammer()
    print("[BLENDER] Milestone 11 Models Generated Successfully!")
