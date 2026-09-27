# tools/generate_milestone36_models.py
# Procedural 3D model generator for Milestone 36: Subterranean Mining Mechanisms
# 1. mine_dewatering_pump.glb - Chain-and-Bucket Water Lift Sump Pump
# 2. mine_ventilator.glb - Centrifugal Mine Air Impeller Fan
# 3. mining_capstan.glb - Geared Shaft Incline Capstan Hoist Winch

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
# 1. CHAIN-AND-BUCKET DEWATERING PUMP
# ==========================================
def build_mine_dewatering_pump():
    clear_scene()

    mat_oak = create_material("HeavyOakGantry", (0.34, 0.22, 0.12, 1.0), roughness=0.85)
    mat_copper = create_material("CopperBuckets", (0.85, 0.45, 0.28, 1.0), roughness=0.35, metallic=0.9)
    mat_iron = create_material("ForgedChainIron", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)
    mat_water = create_material("DischargeWater", (0.2, 0.5, 0.7, 0.8), roughness=0.1, metallic=0.1)

    # Base timber sump frame
    for side in [-0.65, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 0.15))
        sill = bpy.context.active_object
        sill.scale = (1.8, 0.22, 0.25)
        sill.data.materials.append(mat_oak)

    # Cross ties
    for x in [-0.7, 0.7]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0.0, 0.15))
        cross = bpy.context.active_object
        cross.scale = (0.22, 1.5, 0.22)
        cross.data.materials.append(mat_oak)

    # Vertical gantry posts (4 uprights)
    posts = [(-0.55, -0.55), (0.55, -0.55), (-0.55, 0.55), (0.55, 0.55)]
    for x, y in posts:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 1.6))
        post = bpy.context.active_object
        post.scale = (0.22, 0.22, 2.9)
        post.data.materials.append(mat_oak)

    # Top gantry cross beams
    for side in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 2.95))
        tbeam = bpy.context.active_object
        tbeam.scale = (1.6, 0.2, 0.22)
        tbeam.data.materials.append(mat_oak)

    # Top Drive Sprocket Wheel (Wood & Iron)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.25, location=(0.0, 0.0, 2.7))
    sprocket = bpy.context.active_object
    sprocket.rotation_euler = (math.radians(90), 0.0, 0.0)
    sprocket.data.materials.append(mat_oak)

    # Iron drive axle & sprocket teeth
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.5, location=(0.0, 0.0, 2.7))
    axle = bpy.context.active_object
    axle.rotation_euler = (math.radians(90), 0.0, 0.0)
    axle.data.materials.append(mat_iron)

    # Vertical Discharge Pipe (hollow wood riser duct)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=2.4, location=(-0.25, 0.0, 1.4))
    pipe_up = bpy.context.active_object
    pipe_up.data.materials.append(mat_oak)

    # Return chain guide
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=2.4, location=(0.25, 0.0, 1.4))
    pipe_down = bpy.context.active_object
    pipe_down.data.materials.append(mat_oak)

    # Continuous Endless Chain loops
    for side_x in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=2.5, location=(side_x, 0.0, 1.4))
        chain = bpy.context.active_object
        chain.data.materials.append(mat_iron)

    # Copper Water Scoops / Buckets along the vertical run
    bucket_heights = [0.6, 1.1, 1.6, 2.1, 2.6]
    for z in bucket_heights:
        # Scoop on lifting side (-X)
        bpy.ops.mesh.primitive_cone_add(radius1=0.12, radius2=0.06, depth=0.22, location=(-0.25, 0.0, z))
        bucket = bpy.context.active_object
        bucket.rotation_euler = (0.0, math.radians(180), 0.0) # Upright scoop
        bucket.data.materials.append(mat_copper)

    # Upper Water Discharge Trough / Flume (pouring out at +X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 0.0, 2.35))
    flume = bpy.context.active_object
    flume.scale = (1.2, 0.35, 0.18)
    flume.rotation_euler = (0.0, math.radians(8), 0.0) # Slight downhill slope
    flume.data.materials.append(mat_oak)

    # Gushing water stream in flume
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.7, 0.0, 2.4))
    water = bpy.context.active_object
    water.scale = (1.1, 0.28, 0.06)
    water.rotation_euler = (0.0, math.radians(8), 0.0)
    water.data.materials.append(mat_water)

    export_gltf(get_output_path("mine_dewatering_pump.glb"))

# ==========================================
# 2. CENTRIFUGAL MINE AIR VENTILATION IMPELLER
# ==========================================
def build_mine_ventilator():
    clear_scene()

    mat_wood = create_material("VentilatorCasing", (0.38, 0.24, 0.14, 1.0), roughness=0.80)
    mat_brass = create_material("ImpellerBrass", (0.78, 0.62, 0.26, 1.0), roughness=0.35, metallic=0.85)
    mat_iron = create_material("VentIronBands", (0.16, 0.17, 0.19, 1.0), roughness=0.45, metallic=0.92)

    # Support base feet
    for side in [-0.5, 0.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, side, 0.1))
        foot = bpy.context.active_object
        foot.scale = (1.4, 0.2, 0.18)
        foot.data.materials.append(mat_wood)

    # Snail-shell spiral centrifugal casing
    bpy.ops.mesh.primitive_cylinder_add(radius=0.65, depth=0.45, location=(0.0, 0.0, 0.8))
    casing = bpy.context.active_object
    casing.rotation_euler = (math.radians(90), 0.0, 0.0)
    casing.data.materials.append(mat_wood)

    # Iron perimeter bands on casing
    for side in [-0.22, 0.22]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.67, minor_radius=0.035, location=(0.0, side, 0.8))
        band = bpy.context.active_object
        band.rotation_euler = (math.radians(90), 0.0, 0.0)
        band.data.materials.append(mat_iron)

    # Central Air Intake Eye Aperture
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.48, location=(0.0, 0.0, 0.8))
    intake = bpy.context.active_object
    intake.rotation_euler = (math.radians(90), 0.0, 0.0)
    intake.data.materials.append(mat_iron)

    # Multi-blade radial impeller fan inside intake (Brass blades)
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28 * math.cos(rad), 0.0, 0.8 + 0.28 * math.sin(rad)))
        blade = bpy.context.active_object
        blade.scale = (0.28, 0.35, 0.04)
        blade.rotation_euler = (math.radians(90), rad, 0.0)
        blade.data.materials.append(mat_brass)

    # Tangential air discharge snout (ventilation duct connection at +X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.65, 0.0, 1.25))
    snout = bpy.context.active_object
    snout.scale = (0.65, 0.42, 0.42)
    snout.data.materials.append(mat_wood)

    # Iron connection flange collar on snout
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.95, 0.0, 1.25))
    flange = bpy.context.active_object
    flange.scale = (0.08, 0.48, 0.48)
    flange.data.materials.append(mat_iron)

    # Rear kinetic input drive shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(0.0, -0.45, 0.8))
    shaft = bpy.context.active_object
    shaft.rotation_euler = (math.radians(90), 0.0, 0.0)
    shaft.data.materials.append(mat_iron)

    export_gltf(get_output_path("mine_ventilator.glb"))

# ==========================================
# 3. UNDERGROUND INCLINE CAPSTAN HOIST WINCH
# ==========================================
def build_mining_capstan():
    clear_scene()

    mat_oak = create_material("CapstanOak", (0.32, 0.20, 0.11, 1.0), roughness=0.85)
    mat_cable = create_material("SteelWindingCable", (0.28, 0.29, 0.31, 1.0), roughness=0.5, metallic=0.9)
    mat_iron = create_material("CastPawlIron", (0.15, 0.16, 0.18, 1.0), roughness=0.45, metallic=0.92)
    mat_bronze = create_material("BevelDriveBronze", (0.75, 0.58, 0.25, 1.0), roughness=0.35, metallic=0.8)

    # Base timber cruciform balks
    for angle in [0, 90]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.12))
        balk = bpy.context.active_object
        balk.scale = (2.2, 0.35, 0.24)
        balk.rotation_euler = (0.0, 0.0, math.radians(angle))
        balk.data.materials.append(mat_oak)

    # Central Vertical Rotating Capstan Drum
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.9, location=(0.0, 0.0, 0.75))
    drum = bpy.context.active_object
    drum.data.materials.append(mat_oak)

    # Braided Cable Coil wound around mid-section of drum
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.45, location=(0.0, 0.0, 0.75))
    cable = bpy.context.active_object
    cable.data.materials.append(mat_cable)

    # Top Capstan Head with Flanged Rim
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.15, location=(0.0, 0.0, 1.25))
    top_rim = bpy.context.active_object
    top_rim.data.materials.append(mat_iron)

    # Bottom Bevel Gearbox Housing & Drive Pinion (Bronze)
    bpy.ops.mesh.primitive_cone_add(radius1=0.38, radius2=0.1, depth=0.25, location=(0.0, 0.0, 0.25))
    crown_gear = bpy.context.active_object
    crown_gear.data.materials.append(mat_bronze)

    # Horizontal input shaft entering from -X
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.1, location=(-0.75, 0.0, 0.25))
    in_shaft = bpy.context.active_object
    in_shaft.rotation_euler = (0.0, math.radians(90), 0.0)
    in_shaft.data.materials.append(mat_iron)

    # Safety Ratchet Ring and Locking Pawl
    bpy.ops.mesh.primitive_cylinder_add(radius=0.52, depth=0.08, location=(0.0, 0.0, 0.35))
    ratchet = bpy.context.active_object
    ratchet.data.materials.append(mat_iron)

    # Weighted Gravity Pawl Lever
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.48, 0.25, 0.38))
    pawl = bpy.context.active_object
    pawl.scale = (0.28, 0.1, 0.12)
    pawl.rotation_euler = (0.0, 0.0, math.radians(-25))
    pawl.data.materials.append(mat_iron)

    # Front Cable Guide Pulley Sheaves (angling down at 30 deg into incline shaft at +X)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.04, location=(0.95, 0.0, 0.45))
    sheave = bpy.context.active_object
    sheave.rotation_euler = (math.radians(90), 0.0, 0.0)
    sheave.data.materials.append(mat_iron)

    # Haulage cable extending down the incline
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=1.2, location=(1.5, 0.0, 0.15))
    lead_cable = bpy.context.active_object
    lead_cable.rotation_euler = (0.0, math.radians(60), 0.0) # 30 deg slope down
    lead_cable.data.materials.append(mat_cable)

    export_gltf(get_output_path("mining_capstan.glb"))

if __name__ == "__main__":
    print("[M36] Generating 3D Models for Milestone 36...")
    build_mine_dewatering_pump()
    build_mine_ventilator()
    build_mining_capstan()
    print("[M36] All 3 models generated successfully!")
