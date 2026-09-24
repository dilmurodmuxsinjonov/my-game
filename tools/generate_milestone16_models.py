"""Blender 5.2 Headless Model Generator for Milestone 16:
1. conveyor_belt.glb (Create-style Leather Mechanical Conveyor Belt)
2. chute.glb (Create-style Flanged Gravity Chute & Hopper Funnel)
3. mechanical_press.glb (Create-style Industrial Kinetic Stamping Press)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.6, metallic=0.0, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
                bsdf.inputs["Emission Strength"].default_value = emission_strength
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission
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
# 38. Create-Style Mechanical Conveyor Belt (conveyor_belt.glb)
# -------------------------------------------------------------
def build_conveyor_belt():
    reset_scene()
    mat_frame = create_material("CastIronFrame", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.85)
    mat_brass = create_material("RollerBrass", (0.85, 0.65, 0.22, 1.0), roughness=0.3, metallic=0.9)
    mat_belt = create_material("StitchedLeatherBelt", (0.24, 0.15, 0.09, 1.0), roughness=0.85)
    mat_rivet = create_material("IronRivet", (0.35, 0.35, 0.38, 1.0), roughness=0.3, metallic=0.9)

    # 1. Main Side Chassis Rails (Left & Right Cast Iron C-Channels)
    for x in [-0.42, 0.42]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.20))
        rail = bpy.context.active_object
        rail.scale = (0.08, 1.80, 0.18)
        rail.data.materials.append(mat_frame)

        # Cross bracing feet
        for y in [-0.75, 0.0, 0.75]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.06))
            foot = bpy.context.active_object
            foot.scale = (0.12, 0.10, 0.12)
            foot.data.materials.append(mat_frame)

    # 2. Dual End Rollers (Brass cylindrical pulleys)
    for y in [-0.78, 0.78]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.80, vertices=16, location=(0, y, 0.22))
        roller = bpy.context.active_object
        roller.rotation_euler = (0, math.radians(90), 0)
        roller.data.materials.append(mat_brass)

        # Roller axle hubs
        for x in [-0.45, 0.45]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.08, vertices=12, location=(x, y, 0.22))
            hub = bpy.context.active_object
            hub.rotation_euler = (0, math.radians(90), 0)
            hub.data.materials.append(mat_frame)

    # Intermediate idler rollers
    for y in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.76, vertices=12, location=(0, y, 0.22))
        idler = bpy.context.active_object
        idler.rotation_euler = (0, math.radians(90), 0)
        idler.data.materials.append(mat_frame)

    # 3. Top Stretched Leather Belt Run
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.325))
    top_belt = bpy.context.active_object
    top_belt.scale = (0.76, 1.58, 0.02)
    top_belt.data.materials.append(mat_belt)

    # Bottom return belt run
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.115))
    bot_belt = bpy.context.active_object
    bot_belt.scale = (0.76, 1.58, 0.02)
    bot_belt.data.materials.append(mat_belt)

    # 4. Belt End Curves around pulleys
    for y, rot in [(-0.78, math.radians(180)), (0.78, 0)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.108, depth=0.76, vertices=16, location=(0, y, 0.22))
        curve = bpy.context.active_object
        curve.rotation_euler = (0, math.radians(90), 0)
        curve.scale = (1.0, 1.0, 1.0)
        curve.data.materials.append(mat_belt)

    # 5. Riveted Guard Lips (keeping items centered)
    for x in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.35))
        guard = bpy.context.active_object
        guard.scale = (0.02, 1.65, 0.06)
        guard.data.materials.append(mat_frame)

    export_glb("conveyor_belt.glb")

# -------------------------------------------------------------
# 39. Create-Style Gravity Chute & Hopper Funnel (chute.glb)
# -------------------------------------------------------------
def build_chute():
    reset_scene()
    mat_brass = create_material("ChuteBrassSheet", (0.82, 0.62, 0.22, 1.0), roughness=0.35, metallic=0.85)
    mat_iron = create_material("ChuteIronFlange", (0.16, 0.16, 0.18, 1.0), roughness=0.4, metallic=0.9)
    mat_glass = create_material("InspectionWindow", (0.65, 0.85, 0.90, 0.4), roughness=0.1, metallic=0.1)

    # 1. Top Hopper Funnel (Inverted pyramid receiving mouth)
    bpy.ops.mesh.primitive_cone_add(radius1=0.55, radius2=0.32, depth=0.45, vertices=4, location=(0, 0, 1.45))
    hopper = bpy.context.active_object
    hopper.rotation_euler = (0, 0, math.radians(45))
    hopper.data.materials.append(mat_brass)

    # 2. Top Bolted Mounting Flange
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.68))
    top_flange = bpy.context.active_object
    top_flange.scale = (0.82, 0.82, 0.06)
    top_flange.data.materials.append(mat_iron)

    # 3. Main Vertical Square Shaft Column
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.85))
    shaft = bpy.context.active_object
    shaft.scale = (0.45, 0.45, 0.80)
    shaft.data.materials.append(mat_brass)

    # Reinforcing Iron Rib Bands
    for z in [0.55, 0.85, 1.15]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, z))
        band = bpy.context.active_object
        band.scale = (0.49, 0.49, 0.05)
        band.data.materials.append(mat_iron)

    # 4. Front Glass Inspection Window
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.23, 0.85))
    win = bpy.context.active_object
    win.scale = (0.24, 0.03, 0.42)
    win.data.materials.append(mat_glass)

    # Window frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.235, 0.85))
    w_frame = bpy.context.active_object
    w_frame.scale = (0.28, 0.02, 0.46)
    w_frame.data.materials.append(mat_iron)

    # 5. Bottom Discharge Funnel Spout
    bpy.ops.mesh.primitive_cone_add(radius1=0.30, radius2=0.22, depth=0.35, vertices=4, location=(0, 0, 0.28))
    spout = bpy.context.active_object
    spout.rotation_euler = (0, 0, math.radians(45))
    spout.data.materials.append(mat_brass)

    # Bottom connection collar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.06))
    bot_flange = bpy.context.active_object
    bot_flange.scale = (0.50, 0.50, 0.06)
    bot_flange.data.materials.append(mat_iron)

    export_glb("chute.glb")

# -------------------------------------------------------------
# 40. Create-Style Mechanical Stamping Press (mechanical_press.glb)
# -------------------------------------------------------------
def build_mechanical_press():
    reset_scene()
    mat_frame = create_material("PressCastIron", (0.18, 0.18, 0.20, 1.0), roughness=0.35, metallic=0.9)
    mat_brass = create_material("CamshaftBrass", (0.85, 0.65, 0.22, 1.0), roughness=0.25, metallic=0.92)
    mat_steel = create_material("HardenedPistonSteel", (0.75, 0.75, 0.78, 1.0), roughness=0.2, metallic=0.95)
    mat_copper = create_material("IndicatorCopper", (0.78, 0.42, 0.25, 1.0), roughness=0.3, metallic=0.85)

    # 1. Heavy Heavy Cast Iron Base Anvil Plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.20))
    base = bpy.context.active_object
    base.scale = (1.4, 1.2, 0.4)
    base.data.materials.append(mat_frame)

    # Hardened Steel Stamping Anvil Die Block (where ingots sit)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.45))
    die_block = bpy.context.active_object
    die_block.scale = (0.60, 0.60, 0.12)
    die_block.data.materials.append(mat_steel)

    # 2. Twin Vertical Support Pillars (A-Frame Uprights)
    for x in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 1.45))
        col = bpy.context.active_object
        col.scale = (0.18, 0.32, 2.10)
        col.data.materials.append(mat_frame)

    # 3. Top Crosshead Gantry Beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2.50))
    top_beam = bpy.context.active_object
    top_beam.scale = (1.45, 0.40, 0.35)
    top_beam.data.materials.append(mat_frame)

    # 4. Kinetic Drive Shaft & Cam (horizontal through top beam)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.60, vertices=16, location=(0, 0, 2.50))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (math.radians(90), 0, 0)
    shaft.data.materials.append(mat_brass)

    # Eccentric Lifting Cam
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.16, vertices=16, location=(0, 0.05, 2.50))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.scale = (1.0, 1.45, 1.0)
    cam.data.materials.append(mat_brass)

    # 5. Heavy Vertical Stamping Piston Rod
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=1.40, vertices=16, location=(0, 0, 1.60))
    piston = bpy.context.active_object
    piston.data.materials.append(mat_steel)

    # Heavy Rectangular Stamping Head (Press Ram)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.95))
    head = bpy.context.active_object
    head.scale = (0.52, 0.52, 0.22)
    head.data.materials.append(mat_frame)

    # Hardened Stamping Die Face
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.82))
    die_face = bpy.context.active_object
    die_face.scale = (0.46, 0.46, 0.06)
    die_face.data.materials.append(mat_steel)

    # 6. Pressure Gauge & Mechanical Lever
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.04, vertices=16, location=(0.42, 0.22, 2.30))
    gauge = bpy.context.active_object
    gauge.rotation_euler = (0, math.radians(90), 0)
    gauge.data.materials.append(mat_copper)

    export_glb("mechanical_press.glb")

if __name__ == "__main__":
    print("[BUILD] Generating Milestone 16 3D Models via Blender 5.2...")
    build_conveyor_belt()
    build_chute()
    build_mechanical_press()
    print("[SUCCESS] Milestone 16 3D Models successfully generated!")
