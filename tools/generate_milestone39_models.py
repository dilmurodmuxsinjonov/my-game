# tools/generate_milestone39_models.py
# Procedural 3D model generator for Milestone 39: High-Pressure Steam Power
# 1. steam_boiler.glb - High-Pressure Multi-Tube Steam Boiler
# 2. steam_engine_drive.glb - Horizontal Stationary Double-Acting Steam Engine
# 3. centrifugal_governor.glb - James Watt Flyball Centrifugal Speed Governor

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
# 1. HIGH-PRESSURE STEAM BOILER
# ==========================================
def build_steam_boiler():
    clear_scene()

    mat_brick = create_material("RefractoryBrick", (0.45, 0.22, 0.15, 1.0), roughness=0.88)
    mat_brass = create_material("BoilerBrassShell", (0.85, 0.68, 0.22, 1.0), roughness=0.28, metallic=0.95)
    mat_iron = create_material("BoilerCastIron", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.88)
    mat_glass = create_material("SightGlassTube", (0.85, 0.95, 1.0, 0.8), roughness=0.1, metallic=0.1)
    mat_dial = create_material("ManometerFace", (0.92, 0.92, 0.90, 1.0), roughness=0.3)

    # 1. Brick Firebox Hearth Foundation
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.45))
    hearth = bpy.context.active_object
    hearth.scale = (1.8, 1.8, 0.9)
    hearth.data.materials.append(mat_brick)

    # Cast iron firebox door with hinges
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.92, 0.0, 0.45))
    fdoor = bpy.context.active_object
    fdoor.scale = (0.08, 0.65, 0.55)
    fdoor.data.materials.append(mat_iron)

    # Firedoor latch wheel
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.02, location=(0.98, 0.0, 0.45))
    latch = bpy.context.active_object
    latch.rotation_euler = (0, math.radians(90), 0)
    latch.data.materials.append(mat_brass)

    # 2. Main Vertical Boiler Shell (Brass cylindrical pressure drum)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.72, depth=1.6, location=(0.0, 0.0, 1.7))
    drum = bpy.context.active_object
    drum.data.materials.append(mat_brass)

    # Circumferential riveted iron retaining bands
    for bz in [1.1, 1.7, 2.3]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.74, minor_radius=0.03, location=(0.0, 0.0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_iron)

    # 3. Upper Conical Smokebox & Chimney
    bpy.ops.mesh.primitive_cone_add(radius1=0.72, radius2=0.28, depth=0.45, location=(0.0, 0.0, 2.72))
    sbox = bpy.context.active_object
    sbox.data.materials.append(mat_iron)

    # Tall chimney stack
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.85, location=(0.0, 0.0, 3.35))
    stack = bpy.context.active_object
    stack.data.materials.append(mat_iron)

    # Chimney flared crown
    bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.04, location=(0.0, 0.0, 3.75))
    crown = bpy.context.active_object
    crown.data.materials.append(mat_brass)

    # 4. Water Level Sight Glass Column (on side y=0.75)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.95, location=(0.35, 0.76, 1.7))
    sg_fitting = bpy.context.active_object
    sg_fitting.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.75, location=(0.35, 0.79, 1.7))
    sg_tube = bpy.context.active_object
    sg_tube.data.materials.append(mat_glass)

    # 5. Pressure Manometer & Popoff Valves
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.06, location=(0.76, 0.35, 2.1))
    gauge = bpy.context.active_object
    gauge.rotation_euler = (0, math.radians(90), 0)
    gauge.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.02, location=(0.80, 0.35, 2.1))
    dial = bpy.context.active_object
    dial.rotation_euler = (0, math.radians(90), 0)
    dial.data.materials.append(mat_dial)

    # Dual popoff safety valves at top
    for vy in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.35, location=(-0.35, vy, 2.65))
        valve = bpy.context.active_object
        valve.data.materials.append(mat_brass)

    # Main Steam Outlet Pipe leading to engine
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.6, location=(-0.75, 0.0, 2.2))
    steam_pipe = bpy.context.active_object
    steam_pipe.rotation_euler = (0, math.radians(90), 0)
    steam_pipe.data.materials.append(mat_iron)

    export_gltf(get_output_path("steam_boiler.glb"))


# ==========================================
# 2. HORIZONTAL STATIONARY STEAM ENGINE
# ==========================================
def build_steam_engine_drive():
    clear_scene()

    mat_bed = create_material("EngineBedCast", (0.16, 0.20, 0.17, 1.0), roughness=0.55, metallic=0.75)
    mat_wood = create_material("TeakCylinderLagging", (0.38, 0.20, 0.10, 1.0), roughness=0.65)
    mat_steel = create_material("PolishedSteelRods", (0.75, 0.78, 0.80, 1.0), roughness=0.22, metallic=0.98)
    mat_flywheel = create_material("FlywheelCastIron", (0.20, 0.21, 0.23, 1.0), roughness=0.38, metallic=0.92)
    mat_brass = create_material("EngineBrassFittings", (0.85, 0.68, 0.22, 1.0), roughness=0.25, metallic=0.95)

    # 1. Cast-Iron Engine Bedplate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.18))
    bed = bpy.context.active_object
    bed.scale = (3.4, 1.3, 0.35)
    bed.data.materials.append(mat_bed)

    # 2. Horizontal Steam Cylinder (at -X end)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=1.1, location=(-1.15, 0.0, 0.65))
    cylinder = bpy.context.active_object
    cylinder.rotation_euler = (0, math.radians(90), 0)
    cylinder.data.materials.append(mat_wood)

    # Cylinder front/back brass cylinder heads
    for cx in [-1.72, -0.58]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.08, location=(cx, 0.0, 0.65))
        chead = bpy.context.active_object
        chead.rotation_euler = (0, math.radians(90), 0)
        chead.data.materials.append(mat_brass)

    # Top Steam Valve Chest
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.15, 0.0, 1.15))
    vchest = bpy.context.active_object
    vchest.scale = (0.75, 0.38, 0.35)
    vchest.data.materials.append(mat_bed)

    # 3. Piston Rod & Crosshead Guide
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.1, location=(-0.15, 0.0, 0.65))
    piston_rod = bpy.context.active_object
    piston_rod.rotation_euler = (0, math.radians(90), 0)
    piston_rod.data.materials.append(mat_steel)

    # Crosshead guide bars (top and bottom)
    for gz in [0.50, 0.80]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.1, 0.0, gz))
        guide = bpy.context.active_object
        guide.scale = (1.0, 0.12, 0.06)
        guide.data.materials.append(mat_steel)

    # Crosshead slider block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.1, 0.0, 0.65))
    crosshead = bpy.context.active_object
    crosshead.scale = (0.28, 0.22, 0.22)
    crosshead.data.materials.append(mat_brass)

    # 4. Connecting Rod (from crosshead to crank pin)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.60, 0.0, 0.65))
    conrod = bpy.context.active_object
    conrod.scale = (1.2, 0.06, 0.12)
    conrod.data.materials.append(mat_steel)

    # 5. Crankshaft, Disc & Crankpin at x=1.25
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.12, location=(1.25, -0.15, 0.65))
    crank_disc = bpy.context.active_object
    crank_disc.rotation_euler = (math.radians(90), 0, 0)
    crank_disc.data.materials.append(mat_bed)

    # Main crankshaft spanning across
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.6, location=(1.25, 0.35, 0.65))
    crankshaft = bpy.context.active_object
    crankshaft.rotation_euler = (math.radians(90), 0, 0)
    crankshaft.data.materials.append(mat_steel)

    # Main pillow block bearing pedestal
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.25, 0.25, 0.50))
    pedestal = bpy.context.active_object
    pedestal.scale = (0.35, 0.35, 0.35)
    pedestal.data.materials.append(mat_brass)

    # 6. Massive Spoked Flywheel (1.8m diameter)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.90, minor_radius=0.10, location=(1.25, 0.85, 0.65))
    flywheel_rim = bpy.context.active_object
    flywheel_rim.rotation_euler = (math.radians(90), 0, 0)
    flywheel_rim.data.materials.append(mat_flywheel)

    # Flywheel hub
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.22, location=(1.25, 0.85, 0.65))
    fhub = bpy.context.active_object
    fhub.rotation_euler = (math.radians(90), 0, 0)
    fhub.data.materials.append(mat_flywheel)

    # 6 Flywheel spokes
    for i in range(6):
        angle = math.radians(i * 60)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.85, location=(
            1.25,
            0.85,
            0.65
        ))
        spoke = bpy.context.active_object
        spoke.rotation_euler = (angle, 0, 0)
        spoke.data.materials.append(mat_flywheel)

    export_gltf(get_output_path("steam_engine_drive.glb"))


# ==========================================
# 3. CENTRIFUGAL FLYBALL GOVERNOR
# ==========================================
def build_centrifugal_governor():
    clear_scene()

    mat_brass = create_material("GovernorBrassBalls", (0.88, 0.72, 0.22, 1.0), roughness=0.22, metallic=0.96)
    mat_steel = create_material("GovernorSpindleSteel", (0.75, 0.78, 0.80, 1.0), roughness=0.25, metallic=0.95)
    mat_iron = create_material("GovernorPedestalCast", (0.18, 0.19, 0.21, 1.0), roughness=0.5, metallic=0.85)
    mat_valve = create_material("ThrottleValveIron", (0.25, 0.26, 0.28, 1.0), roughness=0.45, metallic=0.9)

    # 1. Cast-iron tripod pedestal base
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.45, depth=0.18, location=(0.0, 0.0, 0.09))
    base = bpy.context.active_object
    base.data.materials.append(mat_iron)

    # Base bevel gear drive
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, depth=0.12, location=(0.0, 0.0, 0.22))
    bgear = bpy.context.active_object
    bgear.data.materials.append(mat_brass)

    # 2. Vertical rotating spindle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=1.35, location=(0.0, 0.0, 0.90))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_steel)

    # Top pivot hub
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.10, location=(0.0, 0.0, 1.48))
    tophub = bpy.context.active_object
    tophub.data.materials.append(mat_brass)

    # Sliding collar along spindle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.14, location=(0.0, 0.0, 0.85))
    collar = bpy.context.active_object
    collar.data.materials.append(mat_brass)

    # 3. Two Articulated Flyball Arms with heavy brass balls
    for side, angle in [(-1, 35), (1, -35)]:
        # Upper suspension arm
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.6, location=(side * 0.18, 0.0, 1.25))
        uarm = bpy.context.active_object
        uarm.rotation_euler = (0, math.radians(angle), 0)
        uarm.data.materials.append(mat_brass)

        # Brass Flyball Sphere (0.16m diameter)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(side * 0.35, 0.0, 1.05))
        ball = bpy.context.active_object
        ball.data.materials.append(mat_brass)

        # Lower link arm connecting ball to sliding collar
        bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.45, location=(side * 0.18, 0.0, 0.95))
        larm = bpy.context.active_object
        larm.rotation_euler = (0, math.radians(-angle), 0)
        larm.data.materials.append(mat_brass)

    # 4. Rocker Arm & Throttle Valve Linkage
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, 0.0, 0.85))
    rocker = bpy.context.active_object
    rocker.scale = (0.55, 0.04, 0.04)
    rocker.data.materials.append(mat_brass)

    # Throttle valve casing on side
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.0, 0.85))
    vbody = bpy.context.active_object
    vbody.scale = (0.18, 0.25, 0.25)
    vbody.data.materials.append(mat_valve)

    # Flanged steam pipe passing through valve
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.6, location=(0.58, 0.0, 0.85))
    vpipe = bpy.context.active_object
    vpipe.rotation_euler = (math.radians(90), 0, 0)
    vpipe.data.materials.append(mat_valve)

    export_gltf(get_output_path("centrifugal_governor.glb"))


if __name__ == "__main__":
    print("[M39] Building high-pressure steam power models...")
    build_steam_boiler()
    build_steam_engine_drive()
    build_centrifugal_governor()
    print("[M39] All 3 models built successfully!")
