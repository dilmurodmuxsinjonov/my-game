# tools/generate_milestone35_models.py
# Procedural 3D model generator for Milestone 35: Industrial Foundry Mechanization
# 1. mechanical_bellows.glb - Cam-Driven Mechanical Leather Accordion Bellows
# 2. furnace_tuyere.glb - Blast Furnace Refractory Tuyere Air Injection Assembly
# 3. industrial_trip_hammer.glb - Heavy Water-Powered Camshaft Helve Tilt-Hammer

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
# 1. MECHANICAL CAM-DRIVEN BELLOWS
# ==========================================
def build_mechanical_bellows():
    clear_scene()

    mat_wood = create_material("BellowsOak", (0.35, 0.22, 0.12, 1.0), roughness=0.85)
    mat_leather = create_material("TannedLeather", (0.48, 0.32, 0.18, 1.0), roughness=0.75)
    mat_iron = create_material("CastIron", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)
    mat_brass = create_material("ForgedBrass", (0.78, 0.62, 0.26, 1.0), roughness=0.35, metallic=0.85)

    # Base timber skid frame
    for side in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 0.1))
        skid = bpy.context.active_object
        skid.scale = (2.4, 0.18, 0.2)
        skid.data.materials.append(mat_wood)

    # Cross ties
    for x in [-0.9, 0.9]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 0.12))
        cross = bpy.context.active_object
        cross.scale = (0.18, 1.25, 0.18)
        cross.data.materials.append(mat_wood)

    # Stationary center divider board
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.2, 0.0, 0.75))
    center_board = bpy.context.active_object
    center_board.scale = (1.6, 0.9, 0.1)
    center_board.data.materials.append(mat_wood)

    # Top hinged moving board (angled up)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.2, 0.0, 1.15))
    top_board = bpy.context.active_object
    top_board.scale = (1.6, 0.9, 0.09)
    top_board.rotation_euler = (0.0, math.radians(-14), 0.0)
    top_board.data.materials.append(mat_wood)

    # Bottom hinged moving board (angled down)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.2, 0.0, 0.35))
    bot_board = bpy.context.active_object
    bot_board.scale = (1.6, 0.9, 0.09)
    bot_board.rotation_euler = (0.0, math.radians(14), 0.0)
    bot_board.data.materials.append(mat_wood)

    # Accordion pleated leather chamber (Top chamber)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.42, location=(0.25, 0.0, 0.95))
    leather_top = bpy.context.active_object
    leather_top.scale = (1.4, 0.85, 0.85)
    leather_top.data.materials.append(mat_leather)

    # Accordion pleated leather chamber (Bottom chamber)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.42, location=(0.25, 0.0, 0.55))
    leather_bot = bpy.context.active_object
    leather_bot.scale = (1.4, 0.85, 0.85)
    leather_bot.data.materials.append(mat_leather)

    # Front Air Blast Snout Nozzle (Brass conical pipe at X = 1.3)
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, radius2=0.08, depth=0.6, location=(1.3, 0.0, 0.75))
    nozzle = bpy.context.active_object
    nozzle.rotation_euler = (0.0, math.radians(90), 0.0)
    nozzle.data.materials.append(mat_brass)

    # Rear Eccentric Cam Rocker Mechanism
    # Camshaft support pillars
    for side in [-0.5, 0.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.95, side, 0.75))
        pillar = bpy.context.active_object
        pillar.scale = (0.2, 0.16, 1.1)
        pillar.data.materials.append(mat_iron)

    # Rotating input camshaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.35, location=(-0.95, 0.0, 0.75))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (math.radians(90), 0.0, 0.0)
    shaft.data.materials.append(mat_iron)

    # Eccentric iron cam lobes (egg-shaped cams)
    for dy in [-0.22, 0.22]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.08, location=(-0.95, dy, 0.82))
        cam = bpy.context.active_object
        cam.rotation_euler = (math.radians(90), 0.0, 0.0)
        cam.data.materials.append(mat_iron)

    # Rocker arm follower bar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.7, 0.0, 0.85))
    rocker = bpy.context.active_object
    rocker.scale = (0.45, 0.1, 0.7)
    rocker.data.materials.append(mat_iron)

    export_gltf(get_output_path("mechanical_bellows.glb"))

# ==========================================
# 2. BLAST FURNACE TUYERE AIR INJECTION ASSEMBLY
# ==========================================
def build_furnace_tuyere():
    clear_scene()

    mat_copper = create_material("ForgedCopper", (0.85, 0.45, 0.28, 1.0), roughness=0.35, metallic=0.9)
    mat_ceramic = create_material("RefractoryCeramic", (0.75, 0.70, 0.62, 1.0), roughness=0.85)
    mat_iron = create_material("TuyereIron", (0.18, 0.19, 0.20, 1.0), roughness=0.5, metallic=0.9)
    mat_brass = create_material("BrassFittings", (0.78, 0.65, 0.28, 1.0), roughness=0.3, metallic=0.85)

    # Refractory firebrick mounting flange / wall collar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.5))
    flange = bpy.context.active_object
    flange.scale = (0.35, 1.1, 1.1)
    flange.data.materials.append(mat_ceramic)

    # Bolt circle studs on flange
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        y = 0.42 * math.cos(rad)
        z = 0.5 + 0.42 * math.sin(rad)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.4, location=(0.0, y, z))
        stud = bpy.context.active_object
        stud.rotation_euler = (0.0, math.radians(90), 0.0)
        stud.data.materials.append(mat_iron)

    # Central Copper Water-Jacketed Tuyere Nozzle Body
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.4, location=(0.2, 0.0, 0.5))
    tuyere_body = bpy.context.active_object
    tuyere_body.rotation_euler = (0.0, math.radians(90), 0.0)
    tuyere_body.data.materials.append(mat_copper)

    # Tapered furnace hearth injector tip (protruding into fire hearth at +X)
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, radius2=0.10, depth=0.45, location=(1.05, 0.0, 0.5))
    tip = bpy.context.active_object
    tip.rotation_euler = (0.0, math.radians(90), 0.0)
    tip.data.materials.append(mat_copper)

    # Blast Air Inlet Pipe (entering from rear at -X)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.8, location=(-0.7, 0.0, 0.5))
    inlet = bpy.context.active_object
    inlet.rotation_euler = (0.0, math.radians(90), 0.0)
    inlet.data.materials.append(mat_iron)

    # Butterfly Damper Control Valve Housing
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.18, location=(-0.6, 0.0, 0.5))
    valve_housing = bpy.context.active_object
    valve_housing.rotation_euler = (0.0, math.radians(90), 0.0)
    valve_housing.data.materials.append(mat_iron)

    # Butterfly Valve Throttle Lever (Brass)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.45, location=(-0.6, 0.0, 0.72))
    lever = bpy.context.active_object
    lever.rotation_euler = (0.0, math.radians(25), 0.0)
    lever.data.materials.append(mat_brass)

    # Lever knob handle
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.06, subdivisions=2, location=(-0.5, 0.0, 0.92))
    knob = bpy.context.active_object
    knob.data.materials.append(mat_brass)

    # Blast Pressure Manometer Gauge (mounted on top of tuyere)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.08, location=(-0.15, 0.0, 0.82))
    gauge = bpy.context.active_object
    gauge.rotation_euler = (math.radians(90), 0.0, 0.0)
    gauge.data.materials.append(mat_brass)

    # Water cooling feed pipe fittings
    for side in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.35, location=(0.3, side, 0.68))
        water_pipe = bpy.context.active_object
        water_pipe.data.materials.append(mat_copper)

    export_gltf(get_output_path("furnace_tuyere.glb"))

# ==========================================
# 3. HEAVY INDUSTRIAL TILT-HAMMER (HELVE HAMMER)
# ==========================================
def build_industrial_trip_hammer():
    clear_scene()

    mat_oak = create_material("MassiveOak", (0.32, 0.20, 0.11, 1.0), roughness=0.85)
    mat_steel = create_material("ForgedSteelHead", (0.24, 0.25, 0.28, 1.0), roughness=0.38, metallic=0.95)
    mat_cast_iron = create_material("AnvilCastIron", (0.15, 0.16, 0.18, 1.0), roughness=0.55, metallic=0.9)
    mat_brass = create_material("JournalBushings", (0.75, 0.60, 0.25, 1.0), roughness=0.35, metallic=0.85)

    # Ground foundation sleeper balks
    for y in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.2, y, 0.15))
        balk = bpy.context.active_object
        balk.scale = (3.6, 0.35, 0.3)
        balk.data.materials.append(mat_oak)

    # Massive Cast-Iron Anvil Block (at striking end around X = 1.4)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.4, 0.0, 0.55))
    anvil = bpy.context.active_object
    anvil.scale = (0.8, 0.8, 0.8)
    anvil.data.materials.append(mat_cast_iron)

    # Anvil strike horn
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, radius2=0.08, depth=0.45, location=(1.9, 0.0, 0.75))
    horn = bpy.context.active_object
    horn.rotation_euler = (0.0, math.radians(90), 0.0)
    horn.data.materials.append(mat_cast_iron)

    # Center Fulcrum Trunnion Pivot Posts
    for side in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 0.75))
        post = bpy.context.active_object
        post.scale = (0.45, 0.25, 1.2)
        post.data.materials.append(mat_oak)

        # Cast-iron trunnion pillow block cap
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 1.35))
        cap = bpy.context.active_object
        cap.scale = (0.5, 0.28, 0.22)
        cap.data.materials.append(mat_cast_iron)

    # Transverse Trunnion Pivot Axle (Steel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.4, location=(0.0, 0.0, 1.35))
    trunnion = bpy.context.active_object
    trunnion.rotation_euler = (math.radians(90), 0.0, 0.0)
    trunnion.data.materials.append(mat_steel)

    # Massive 800kg Oak Helve Hammer Beam
    # Slanted down towards anvil at +X
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.2, 0.0, 1.25))
    helve = bpy.context.active_object
    helve.scale = (2.8, 0.35, 0.38)
    helve.rotation_euler = (0.0, math.radians(-5), 0.0)
    helve.data.materials.append(mat_oak)

    # Iron Helve Reinforcement Straps & Pivot Collar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 1.35))
    collar = bpy.context.active_object
    collar.scale = (0.55, 0.42, 0.48)
    collar.data.materials.append(mat_cast_iron)

    # Giant Forged Steel Hammer Head (at front tip X = 1.4, Z = 1.05)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.4, 0.0, 1.08))
    head = bpy.context.active_object
    head.scale = (0.65, 0.55, 0.75)
    head.data.materials.append(mat_steel)

    # Striking face insert (hardened tool steel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.18, location=(1.4, 0.0, 0.72))
    face = bpy.context.active_object
    face.data.materials.append(mat_steel)

    # Rotating Camshaft Assembly at rear (X = -1.2)
    # Camshaft Bearing Posts
    for side in [-0.65, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.2, side, 0.65))
        cpost = bpy.context.active_object
        cpost.scale = (0.35, 0.22, 1.0)
        cpost.data.materials.append(mat_oak)

    # Heavy Rotating Camshaft (Iron)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.6, location=(-1.2, 0.0, 0.95))
    cshaft = bpy.context.active_object
    cshaft.rotation_euler = (math.radians(90), 0.0, 0.0)
    cshaft.data.materials.append(mat_cast_iron)

    # 3 Curved Iron Lifting Cams (offset at 120 degrees around camshaft)
    cam_angles = [0, 120, 240]
    for i, angle in enumerate(cam_angles):
        rad = math.radians(angle)
        # Curved cam arm
        dx = 0.22 * math.cos(rad)
        dz = 0.22 * math.sin(rad)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.2 + dx, (i - 1) * 0.18, 0.95 + dz))
        cam_arm = bpy.context.active_object
        cam_arm.scale = (0.16, 0.12, 0.42)
        cam_arm.rotation_euler = (math.radians(90), rad, 0.0)
        cam_arm.data.materials.append(mat_cast_iron)

    # Tail Tappet (Iron skid on helve tail at X = -1.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.05, 0.0, 1.45))
    tail_tappet = bpy.context.active_object
    tail_tappet.scale = (0.35, 0.38, 0.22)
    tail_tappet.data.materials.append(mat_steel)

    export_gltf(get_output_path("industrial_trip_hammer.glb"))

if __name__ == "__main__":
    print("[M35] Generating 3D Models for Milestone 35...")
    build_mechanical_bellows()
    build_furnace_tuyere()
    build_industrial_trip_hammer()
    print("[M35] All 3 models generated successfully!")
