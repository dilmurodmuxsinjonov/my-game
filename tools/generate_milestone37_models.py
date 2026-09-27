# tools/generate_milestone37_models.py
# Procedural 3D model generator for Milestone 37: Automated Mine Railway Logistics
# 1. mine_locomotive.glb - Narrow-Gauge Geared Steam Mine Locomotive
# 2. rail_switch.glb - Mechanical Turnout Rail Switch with Counterweighted Ground-Throw Stand
# 3. hopper_unloader.glb - Trackside Bottom-Dump Hopper Discharge Station

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
# 1. GEARED MINE LOCOMOTIVE
# ==========================================
def build_mine_locomotive():
    clear_scene()

    mat_boiler = create_material("BoilerSteel", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.88)
    mat_frame = create_material("ChassisFrame", (0.12, 0.12, 0.14, 1.0), roughness=0.6, metallic=0.75)
    mat_brass = create_material("LocoBrass", (0.85, 0.68, 0.22, 1.0), roughness=0.25, metallic=0.95)
    mat_wheels = create_material("DriveWheels", (0.22, 0.22, 0.25, 1.0), roughness=0.35, metallic=0.92)
    mat_red = create_material("BufferBeamRed", (0.65, 0.15, 0.12, 1.0), roughness=0.5, metallic=0.25)
    mat_wood = create_material("CabTimber", (0.35, 0.22, 0.12, 1.0), roughness=0.82)
    mat_coal = create_material("CoalBunkerLump", (0.08, 0.08, 0.08, 1.0), roughness=0.95, metallic=0.05)
    mat_glass = create_material("HeadlampGlass", (0.9, 0.95, 1.0, 0.9), roughness=0.1, metallic=0.2)

    # Main chassis frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.42))
    chassis = bpy.context.active_object
    chassis.scale = (2.4, 0.95, 0.16)
    chassis.data.materials.append(mat_frame)

    # Buffer beams (front and rear)
    for x_pos in [-1.22, 1.22]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0.0, 0.42))
        beam = bpy.context.active_object
        beam.scale = (0.12, 1.1, 0.24)
        beam.data.materials.append(mat_red)

        # Central link-and-pin coupler
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos + (0.1 if x_pos > 0 else -0.1), 0.0, 0.40))
        coupler = bpy.context.active_object
        coupler.scale = (0.16, 0.14, 0.14)
        coupler.data.materials.append(mat_boiler)

    # 4 Drive wheels with coupling rods
    wheel_x = [-0.55, 0.55]
    for wx in wheel_x:
        for wy in [-0.52, 0.52]:
            # Wheel tire
            bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.08, location=(wx, wy, 0.32))
            wheel = bpy.context.active_object
            wheel.rotation_euler = (math.radians(90), 0, 0)
            wheel.data.materials.append(mat_wheels)

            # Counterweight hub
            bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.10, location=(wx, wy + (0.02 if wy > 0 else -0.02), 0.32))
            hub = bpy.context.active_object
            hub.rotation_euler = (math.radians(90), 0, 0)
            hub.data.materials.append(mat_frame)

    # Side coupling rods (connecting front and rear wheels on left and right)
    for wy in [-0.58, 0.58]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, wy, 0.25))
        rod = bpy.context.active_object
        rod.scale = (1.2, 0.03, 0.06)
        rod.data.materials.append(mat_boiler)

    # Horizontal cylindrical boiler
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=1.35, location=(0.32, 0.0, 0.85))
    boiler = bpy.context.active_object
    boiler.rotation_euler = (0, math.radians(90), 0)
    boiler.data.materials.append(mat_boiler)

    # Smokebox front door
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.08, location=(1.02, 0.0, 0.85))
    smokebox = bpy.context.active_object
    smokebox.rotation_euler = (0, math.radians(90), 0)
    smokebox.data.materials.append(mat_frame)

    # Smokebox door latch dogs
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.02, location=(1.07, 0.0, 0.85))
    latch = bpy.context.active_object
    latch.rotation_euler = (0, math.radians(90), 0)
    latch.data.materials.append(mat_brass)

    # Smokestack with flared rim
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.45, location=(0.85, 0.0, 1.38))
    stack = bpy.context.active_object
    stack.data.materials.append(mat_frame)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.12, minor_radius=0.03, location=(0.85, 0.0, 1.60))
    stack_rim = bpy.context.active_object
    stack_rim.data.materials.append(mat_brass)

    # Brass Steam Dome & Safety Valve
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.25, location=(0.15, 0.0, 1.25))
    dome = bpy.context.active_object
    dome.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.16, location=(0.15, 0.0, 1.42))
    safety_pipe = bpy.context.active_object
    safety_pipe.data.materials.append(mat_brass)

    # Driver Cab Structure (open rear)
    # Cab walls
    for wy in [-0.46, 0.46]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.65, wy, 1.15))
        wall = bpy.context.active_object
        wall.scale = (0.85, 0.06, 1.1)
        wall.data.materials.append(mat_boiler)

    # Cab front spectacle plate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.25, 0.0, 1.15))
    cab_front = bpy.context.active_object
    cab_front.scale = (0.06, 0.92, 1.1)
    cab_front.data.materials.append(mat_boiler)

    # Cab roof
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.68, 0.0, 1.72))
    roof = bpy.context.active_object
    roof.scale = (0.95, 1.05, 0.05)
    roof.data.materials.append(mat_wood)

    # Cab window cutouts (decorative frame)
    for wy in [-0.46, 0.46]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.60, wy, 1.35))
        win_frame = bpy.context.active_object
        win_frame.scale = (0.35, 0.08, 0.35)
        win_frame.data.materials.append(mat_brass)

    # Coal Bunker at rear of cab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.95, 0.0, 0.68))
    bunker_box = bpy.context.active_object
    bunker_box.scale = (0.45, 0.85, 0.40)
    bunker_box.data.materials.append(mat_frame)

    # Coal lumps inside bunker
    for dx in [-0.12, 0.0, 0.12]:
        for dy in [-0.25, 0.0, 0.25]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.95 + dx, dy, 0.90))
            lump = bpy.context.active_object
            lump.scale = (0.12, 0.16, 0.10)
            lump.rotation_euler = (dx * 2.0, dy * 3.0, 0.5)
            lump.data.materials.append(mat_coal)

    # Brass Headlamp on front buffer beam
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.18, location=(1.25, 0.0, 0.72))
    lamp = bpy.context.active_object
    lamp.rotation_euler = (0, math.radians(90), 0)
    lamp.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.02, location=(1.35, 0.0, 0.72))
    lens = bpy.context.active_object
    lens.rotation_euler = (0, math.radians(90), 0)
    lens.data.materials.append(mat_glass)

    export_gltf(get_output_path("mine_locomotive.glb"))


# ==========================================
# 2. TURNOUT RAIL SWITCH
# ==========================================
def build_rail_switch():
    clear_scene()

    mat_ties = create_material("CreosotedSleepers", (0.28, 0.20, 0.14, 1.0), roughness=0.88)
    mat_steel = create_material("TurnoutRailSteel", (0.25, 0.26, 0.28, 1.0), roughness=0.35, metallic=0.95)
    mat_ballast = create_material("CrushedBallastBed", (0.42, 0.40, 0.38, 1.0), roughness=0.92)
    mat_stand = create_material("GroundThrowStand", (0.15, 0.15, 0.17, 1.0), roughness=0.55, metallic=0.85)
    mat_green = create_material("SignalLanternGreen", (0.12, 0.78, 0.22, 1.0), roughness=0.25, metallic=0.15)
    mat_red = create_material("SignalLanternRed", (0.85, 0.12, 0.12, 1.0), roughness=0.25, metallic=0.15)
    mat_brass = create_material("TieRodBronze", (0.78, 0.62, 0.24, 1.0), roughness=0.32, metallic=0.92)

    # Crushed rock ballast base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.25, 0.04))
    ballast = bpy.context.active_object
    ballast.scale = (3.4, 2.2, 0.08)
    ballast.data.materials.append(mat_ballast)

    # Sleepers (Wooden track ties)
    tie_x_coords = [-1.4, -0.95, -0.5, -0.05, 0.4, 0.85, 1.3]
    for idx, tx in enumerate(tie_x_coords):
        # Ties widen as diverging track spreads out
        tie_length = 1.3 + (idx * 0.12)
        y_center = (idx * 0.06)
        if idx == 0:
            # Extended headblock tie for switch stand
            tie_length = 2.2
            y_center = -0.45

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, y_center, 0.12))
        tie = bpy.context.active_object
        tie.scale = (0.22, tie_length, 0.12)
        tie.data.materials.append(mat_ties)

        # Tie plates under rails
        for ry in [-0.38, 0.38]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, ry, 0.19))
            plate = bpy.context.active_object
            plate.scale = (0.24, 0.14, 0.02)
            plate.data.materials.append(mat_stand)

    # Continuous Straight Track Rails (Left and Right)
    for ry in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ry, 0.26))
        rail = bpy.context.active_object
        rail.scale = (3.4, 0.06, 0.12)
        rail.data.materials.append(mat_steel)

    # Curved Diverging Track Rails (branching towards +Y)
    # Outer diverging rail
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.45, 0.65, 0.26))
    div_outer = bpy.context.active_object
    div_outer.scale = (2.2, 0.06, 0.12)
    div_outer.rotation_euler = (0, 0, math.radians(18))
    div_outer.data.materials.append(mat_steel)

    # Inner diverging rail
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.60, 0.05, 0.26))
    div_inner = bpy.context.active_object
    div_inner.scale = (2.0, 0.06, 0.12)
    div_inner.rotation_euler = (0, 0, math.radians(18))
    div_inner.data.materials.append(mat_steel)

    # Cast Steel Crossing Frog (V-crossing) at x=0.85, y=0.38
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.85, 0.38, 0.27))
    frog = bpy.context.active_object
    frog.scale = (0.45, 0.18, 0.14)
    frog.data.materials.append(mat_steel)

    # Check / Guard rails
    for gy in [0.22, 0.54]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.85, gy, 0.27))
        guard = bpy.context.active_object
        guard.scale = (0.40, 0.04, 0.12)
        guard.data.materials.append(mat_steel)

    # Movable Switch Point Blades & Transverse Tie Bar at x=-1.25
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.25, 0.0, 0.20))
    tie_bar = bpy.context.active_object
    tie_bar.scale = (0.05, 0.95, 0.03)
    tie_bar.data.materials.append(mat_brass)

    # Tapered switch point blades
    for py, angle in [(-0.32, -1.5), (0.32, 1.5)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.85, py, 0.25))
        blade = bpy.context.active_object
        blade.scale = (0.85, 0.04, 0.10)
        blade.rotation_euler = (0, 0, math.radians(angle))
        blade.data.materials.append(mat_steel)

    # Ground-Throw Switch Stand (on extended tie at x=-1.4, y=-1.1)
    # Stand pedestal
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.4, -1.05, 0.28))
    stand_base = bpy.context.active_object
    stand_base.scale = (0.28, 0.28, 0.22)
    stand_base.data.materials.append(mat_stand)

    # Vertical pivot spindle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.85, location=(-1.4, -1.05, 0.65))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_stand)

    # Counterweight balance lever and ball
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.4, -0.92, 0.45))
    lever_arm = bpy.context.active_object
    lever_arm.scale = (0.04, 0.35, 0.04)
    lever_arm.rotation_euler = (math.radians(35), 0, 0)
    lever_arm.data.materials.append(mat_stand)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.10, location=(-1.4, -0.78, 0.35))
    weight_ball = bpy.context.active_object
    weight_ball.data.materials.append(mat_stand)

    # Top Signal Lantern (Square casing with lenses)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.4, -1.05, 1.15))
    lantern_body = bpy.context.active_object
    lantern_body.scale = (0.18, 0.18, 0.22)
    lantern_body.data.materials.append(mat_stand)

    # Green lens (Straight direction facing X)
    for dx in [-0.10, 0.10]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.02, location=(-1.4 + dx, -1.05, 1.15))
        lens_g = bpy.context.active_object
        lens_g.rotation_euler = (0, math.radians(90), 0)
        lens_g.data.materials.append(mat_green)

    # Red lens (Diverging direction facing Y)
    for dy in [-0.10, 0.10]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.02, location=(-1.4, -1.05 + dy, 1.15))
        lens_r = bpy.context.active_object
        lens_r.rotation_euler = (math.radians(90), 0, 0)
        lens_r.data.materials.append(mat_red)

    export_gltf(get_output_path("rail_switch.glb"))


# ==========================================
# 3. TRACKSIDE HOPPER UNLOADER
# ==========================================
def build_hopper_unloader():
    clear_scene()

    mat_oak = create_material("UnloaderOakGantry", (0.32, 0.22, 0.14, 1.0), roughness=0.85)
    mat_iron = create_material("RivetedHopperPlates", (0.22, 0.23, 0.25, 1.0), roughness=0.42, metallic=0.88)
    mat_trip = create_material("BronzeTripArms", (0.75, 0.55, 0.20, 1.0), roughness=0.35, metallic=0.92)
    mat_rails = create_material("UnloaderRails", (0.25, 0.26, 0.28, 1.0), roughness=0.35, metallic=0.95)
    mat_chute = create_material("DischargeChuteWood", (0.38, 0.26, 0.16, 1.0), roughness=0.80)
    mat_lamp = create_material("WarningRedLantern", (0.85, 0.15, 0.15, 1.0), roughness=0.25, metallic=0.1)

    # 4 Heavy vertical timber gantry uprights
    posts = [(-0.85, -0.85), (0.85, -0.85), (-0.85, 0.85), (0.85, 0.85)]
    for x, y in posts:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 1.35))
        post = bpy.context.active_object
        post.scale = (0.22, 0.22, 2.5)
        post.data.materials.append(mat_oak)

    # Top cross girders
    for y in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, y, 2.65))
        beam = bpy.context.active_object
        beam.scale = (1.95, 0.20, 0.22)
        beam.data.materials.append(mat_oak)

    for x in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 2.65))
        beam = bpy.context.active_object
        beam.scale = (0.20, 1.95, 0.22)
        beam.data.materials.append(mat_oak)

    # Diagonal knee braces
    for x, y, rot_z in [(-0.85, 0.0, 0), (0.85, 0.0, 180)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 2.35))
        brace = bpy.context.active_object
        brace.scale = (0.12, 0.8, 0.12)
        brace.data.materials.append(mat_oak)

    # Through-track rails traversing the station
    for ry in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ry, 0.28))
        rail = bpy.context.active_object
        rail.scale = (2.4, 0.06, 0.12)
        rail.data.materials.append(mat_rails)

        # Track stringers (timber beams supporting rails over pit)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ry, 0.14))
        stringer = bpy.context.active_object
        stringer.scale = (2.4, 0.16, 0.16)
        stringer.data.materials.append(mat_oak)

    # Sunken receiving hopper funnel (inverted pyramid beneath rails)
    # Upper hopper flange
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.02))
    flange = bpy.context.active_object
    flange.scale = (1.35, 1.15, 0.08)
    flange.data.materials.append(mat_iron)

    # Slanted hopper walls
    for dx, rot_y in [(-0.35, 30), (0.35, -30)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(dx, 0.0, -0.32))
        wall = bpy.context.active_object
        wall.scale = (0.05, 0.95, 0.65)
        wall.rotation_euler = (0, math.radians(rot_y), 0)
        wall.data.materials.append(mat_iron)

    for dy, rot_x in [(-0.32, -30), (0.32, 30)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, dy, -0.32))
        wall = bpy.context.active_object
        wall.scale = (0.85, 0.05, 0.65)
        wall.rotation_euler = (math.radians(rot_x), 0, 0)
        wall.data.materials.append(mat_iron)

    # Bottom discharge chute flume extending downwards and outwards
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, -0.65, -0.68))
    chute = bpy.context.active_object
    chute.scale = (0.55, 0.95, 0.14)
    chute.rotation_euler = (math.radians(-25), 0, 0)
    chute.data.materials.append(mat_chute)

    # Trackside mechanical trip linkage (trips bottom doors of passing hopper carts)
    for ry in [-0.52, 0.52]:
        # Support bracket
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ry, 0.38))
        bracket = bpy.context.active_object
        bracket.scale = (0.35, 0.06, 0.06)
        bracket.data.materials.append(mat_iron)

        # Spring trip arm lever
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, ry + (0.04 if ry > 0 else -0.04), 0.48))
        arm = bpy.context.active_object
        arm.scale = (0.12, 0.04, 0.22)
        arm.rotation_euler = (0, math.radians(20 if ry > 0 else -20), 0)
        arm.data.materials.append(mat_trip)

        # Guide roller wheel
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.05, location=(0.0, ry + (0.06 if ry > 0 else -0.06), 0.58))
        roller = bpy.context.active_object
        roller.rotation_euler = (math.radians(90), 0, 0)
        roller.data.materials.append(mat_trip)

    # Overhead warning lantern on top crossbeam
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.18, location=(0.0, 0.0, 2.38))
    lamp = bpy.context.active_object
    lamp.data.materials.append(mat_lamp)

    export_gltf(get_output_path("hopper_unloader.glb"))


if __name__ == "__main__":
    print("[M37] Building automated mine railway models...")
    build_mine_locomotive()
    build_rail_switch()
    build_hopper_unloader()
    print("[M37] All 3 models built successfully!")
