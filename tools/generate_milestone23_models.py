"""Generate 3D Low-Poly GLB Assets for Milestone 23:
Castle Siege Catapult / Mangonel, Boiling Pitch Cauldron, and Spiked Portcullis Gate.
Using Blender 5.2.1 LTS Headless Python API.
"""

import bpy
import os
import math

def clear_scene():
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
            bsdf.inputs["Emission Color"].default_value = emission
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def export_glb(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORT] Successfully saved {filepath} ({os.path.getsize(filepath)} bytes)")

# -------------------------------------------------------------
# 1. Castle Siege Catapult / Mangonel (catapult.glb)
# -------------------------------------------------------------
def build_catapult(output_path):
    clear_scene()

    mat_oak = create_material("SiegeOak", (0.32, 0.20, 0.10, 1.0), roughness=0.8)
    mat_iron = create_material("WroughtIron", (0.16, 0.16, 0.18, 1.0), roughness=0.45, metallic=0.9)
    mat_rope = create_material("TorsionRope", (0.55, 0.45, 0.28, 1.0), roughness=0.9)
    mat_fire_boulder = create_material("FireBoulder", (0.25, 0.22, 0.20, 1.0), roughness=0.8, emission=(1.0, 0.45, 0.05, 1.0), emission_strength=3.0)

    # Chassis Side Runners (Length: 2.8m, Width: 1.6m)
    for x_pos in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 0.35))
        beam = bpy.context.active_object
        beam.scale = (0.16, 2.8, 0.16)
        beam.data.materials.append(mat_oak)

    # Chassis Crossbeams
    for y_pos in [-1.2, 0, 1.2]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y_pos, 0.35))
        cross = bpy.context.active_object
        cross.scale = (1.5, 0.14, 0.14)
        cross.data.materials.append(mat_oak)

    # 4 Solid Timber Wheels with Iron Bands
    wheel_coords = [(-0.85, -1.0), (0.85, -1.0), (-0.85, 1.0), (0.85, 1.0)]
    for wx, wy in wheel_coords:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.12, location=(wx, wy, 0.32))
        wheel = bpy.context.active_object
        wheel.rotation_euler = (0, 1.57, 0)
        wheel.data.materials.append(mat_oak)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.015, location=(wx, wy, 0.32))
        band = bpy.context.active_object
        band.rotation_euler = (0, 1.57, 0)
        band.data.materials.append(mat_iron)

    # Upright A-Frame Mast Supports
    for x_pos in [-0.72, 0.72]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.6, location=(x_pos, -0.15, 1.1))
        mast = bpy.context.active_object
        mast.data.materials.append(mat_oak)

    # Crossbar Buffer Stop Beam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.15, 1.85))
    stop = bpy.context.active_object
    stop.scale = (1.6, 0.20, 0.20)
    stop.data.materials.append(mat_oak)

    # Torsion Rope Bundle Cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=1.45, location=(0, -0.15, 0.55))
    rope = bpy.context.active_object
    rope.rotation_euler = (0, 1.57, 0)
    rope.data.materials.append(mat_rope)

    # Long Throwing Arm (Tilted back in primed position)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.65, 1.05))
    arm = bpy.context.active_object
    arm.rotation_euler = (-0.55, 0, 0)
    arm.scale = (0.12, 2.2, 0.12)
    arm.data.materials.append(mat_oak)

    # Spoon Bucket on Arm Tip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.14, location=(0, 1.65, 0.55))
    bucket = bpy.context.active_object
    bucket.rotation_euler = (-0.55, 0, 0)
    bucket.data.materials.append(mat_oak)

    # Flaming Incendiary Boulder resting in bucket
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.20, location=(0, 1.65, 0.65))
    rock = bpy.context.active_object
    rock.data.materials.append(mat_fire_boulder)

    # Rear Tension Winch Drum
    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=1.4, location=(0, 1.15, 0.42))
    winch = bpy.context.active_object
    winch.rotation_euler = (0, 1.57, 0)
    winch.data.materials.append(mat_iron)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Gate Boiling Pitch Cauldron (pitch_cauldron.glb)
# -------------------------------------------------------------
def build_pitch_cauldron(output_path):
    clear_scene()

    mat_stone = create_material("CorbelStone", (0.45, 0.45, 0.48, 1.0), roughness=0.9)
    mat_iron = create_material("CastIron", (0.15, 0.15, 0.17, 1.0), roughness=0.5, metallic=0.95)
    mat_pitch = create_material("BoilingPitch", (0.05, 0.05, 0.05, 1.0), roughness=0.2, emission=(0.85, 0.35, 0.05, 1.0), emission_strength=1.8)
    mat_coals = create_material("GlowingCoals", (0.15, 0.10, 0.08, 1.0), roughness=0.8, emission=(1.0, 0.25, 0.02, 1.0), emission_strength=3.5)

    # Stone Mounting Wall Bracket / Corbel
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.45, 1.35))
    bracket = bpy.context.active_object
    bracket.scale = (1.2, 0.35, 0.25)
    bracket.data.materials.append(mat_stone)

    # Heavy Iron Swivel Gallows Arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.1, location=(0, 0.05, 1.35))
    gallows = bpy.context.active_object
    gallows.rotation_euler = (1.57, 0, 0)
    gallows.data.materials.append(mat_iron)

    # Hanging Iron Chains (Left and Right)
    for cx in [-0.38, 0.38]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.65, location=(cx, 0, 1.05))
        chain = bpy.context.active_object
        chain.data.materials.append(mat_iron)

    # Large Heavy Cauldron Pot
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.55, location=(0, 0, 0.65))
    pot = bpy.context.active_object
    pot.data.materials.append(mat_iron)

    # Flanged Rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.49, minor_radius=0.035, location=(0, 0, 0.92))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_iron)

    # Bubbling Boiling Black Pitch Surface
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.04, location=(0, 0, 0.88))
    pitch = bpy.context.active_object
    pitch.data.materials.append(mat_pitch)

    # Pitch Bubbles
    for bx, by in [(-0.15, 0.1), (0.2, -0.15), (0.05, 0.25)]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(bx, by, 0.90))
        b = bpy.context.active_object
        b.data.materials.append(mat_pitch)

    # Lower Fire Grate with Glowing Coals
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.22))
    grate = bpy.context.active_object
    grate.scale = (0.85, 0.85, 0.12)
    grate.data.materials.append(mat_coals)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Spiked Portcullis Castle Gate (portcullis_gate.glb)
# -------------------------------------------------------------
def build_portcullis_gate(output_path):
    clear_scene()

    mat_stone = create_material("ArchStone", (0.50, 0.50, 0.52, 1.0), roughness=0.9)
    mat_iron = create_material("PortcullisIron", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.95)
    mat_oak = create_material("WinchWood", (0.34, 0.21, 0.11, 1.0), roughness=0.8)

    # Twin Side Stone Pillars with Guide Grooves (Width: 2.2m, Height: 3.4m)
    for px in [-1.15, 1.15]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, 1.7))
        pillar = bpy.context.active_object
        pillar.scale = (0.35, 0.55, 3.4)
        pillar.data.materials.append(mat_stone)

    # Top Stone Arch Lintels
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 3.3))
    lintel = bpy.context.active_object
    lintel.scale = (2.65, 0.55, 0.35)
    lintel.data.materials.append(mat_stone)

    # Overhead Timber Winch Axle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=2.1, location=(0, 0, 3.0))
    winch = bpy.context.active_object
    winch.rotation_euler = (0, 1.57, 0)
    winch.data.materials.append(mat_oak)

    # Side Iron Winch Wheel / Crank
    bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.025, location=(1.05, 0.25, 3.0))
    crank = bpy.context.active_object
    crank.data.materials.append(mat_iron)

    # Portcullis Grate Frame: Vertical Iron Bars (7 bars)
    for vx in [-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=2.5, location=(vx, 0, 1.45))
        vbar = bpy.context.active_object
        vbar.data.materials.append(mat_iron)

        # Bottom Sharp Triangular Iron Spike
        bpy.ops.mesh.primitive_cone_add(radius1=0.045, radius2=0.005, depth=0.25, location=(vx, 0, 0.10))
        spike = bpy.context.active_object
        spike.rotation_euler = (3.1415, 0, 0) # point downward
        spike.data.materials.append(mat_iron)

    # Portcullis Grate Frame: Horizontal Iron Bars (5 bars)
    for hy in [0.55, 1.05, 1.55, 2.05, 2.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, hy))
        hbar = bpy.context.active_object
        hbar.scale = (1.95, 0.07, 0.07)
        hbar.data.materials.append(mat_iron)

    # Iron Chains connecting Grate to Overhead Winch
    for cx in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.5, location=(cx, 0, 2.8))
        chain = bpy.context.active_object
        chain.data.materials.append(mat_iron)

    export_glb(output_path)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(base_dir, exist_ok=True)

    build_catapult(os.path.join(base_dir, "catapult.glb"))
    build_pitch_cauldron(os.path.join(base_dir, "pitch_cauldron.glb"))
    build_portcullis_gate(os.path.join(base_dir, "portcullis_gate.glb"))
    print("\n>>> All Milestone 23 models generated successfully! <<<")
