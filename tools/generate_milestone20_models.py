"""Generate 3D Low-Poly GLB Assets for Milestone 20:
Militia Armory Weapon Rack, Peasant Burgage Plot Chicken Coop, and Combat Training Dummy.
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
# 1. Militia Armory Weapon Rack (armory_rack.glb)
# -------------------------------------------------------------
def build_armory_rack(output_path):
    clear_scene()

    mat_oak = create_material("StoutOak", (0.32, 0.20, 0.11, 1.0), roughness=0.8)
    mat_dark_iron = create_material("WroughtIron", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.9)
    mat_bright_steel = create_material("SteelEdge", (0.75, 0.77, 0.80, 1.0), roughness=0.25, metallic=0.95)
    mat_shield_paint = create_material("HeraldicBlue", (0.15, 0.28, 0.65, 1.0), roughness=0.6)
    mat_leather = create_material("LeatherWrap", (0.40, 0.24, 0.14, 1.0), roughness=0.7)

    # Base timber skid frame (Length: 2.0m, Width: 0.7m, Height: 0.15m)
    for x_pos in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 0.08))
        runner = bpy.context.active_object
        runner.scale = (0.16, 0.75, 0.14)
        runner.data.materials.append(mat_oak)

    # Bottom slotted storage shelf
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.18))
    shelf = bpy.context.active_object
    shelf.scale = (1.9, 0.65, 0.06)
    shelf.data.materials.append(mat_oak)

    # Left and Right vertical timber pillars
    for x_pos in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 1.05))
        post = bpy.context.active_object
        post.scale = (0.14, 0.14, 1.8)
        post.data.materials.append(mat_oak)

    # Top notched crossbeam for spears
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.85))
    top_beam = bpy.context.active_object
    top_beam.scale = (1.95, 0.14, 0.12)
    top_beam.data.materials.append(mat_oak)

    # Middle support rail with iron brackets
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.05, 1.0))
    mid_beam = bpy.context.active_object
    mid_beam.scale = (1.85, 0.08, 0.08)
    mid_beam.data.materials.append(mat_oak)

    # Iron bracket fittings
    for x_pos in [-0.85, 0.85]:
        for z_pos in [0.2, 1.0, 1.85]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, z_pos))
            bracket = bpy.context.active_object
            bracket.scale = (0.16, 0.16, 0.04)
            bracket.data.materials.append(mat_dark_iron)

    # Upright Militia Spears (4 spears resting on rack)
    spear_xs = [-0.6, -0.2, 0.2, 0.6]
    for i, sx in enumerate(spear_xs):
        tilt = 0.06 if i % 2 == 0 else -0.06
        # Ash shaft (2.2m)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=2.2, location=(sx, 0.05, 1.15))
        shaft = bpy.context.active_object
        shaft.rotation_euler = (tilt, 0.05, 0)
        shaft.data.materials.append(mat_oak)

        # Steel spearhead
        bpy.ops.mesh.primitive_cone_add(radius1=0.045, radius2=0.005, depth=0.32, location=(sx, 0.05 + tilt * 1.1, 2.35))
        head = bpy.context.active_object
        head.rotation_euler = (tilt, 0.05, 0)
        head.data.materials.append(mat_bright_steel)

        # Leather binding
        bpy.ops.mesh.primitive_cylinder_add(radius=0.026, depth=0.15, location=(sx, 0.05, 0.9))
        grip = bpy.context.active_object
        grip.data.materials.append(mat_leather)

    # Militia Wooden Round Shields (2 resting against bottom rack)
    for shield_x, rot_z in [(-0.45, 0.2), (0.45, -0.15)]:
        # Wooden shield disc
        bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.04, location=(shield_x, -0.22, 0.45))
        shield = bpy.context.active_object
        shield.rotation_euler = (1.4, 0, rot_z)
        shield.data.materials.append(mat_shield_paint)

        # Steel boss (center dome)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(shield_x, -0.25, 0.45))
        boss = bpy.context.active_object
        boss.scale = (1.0, 0.4, 1.0)
        boss.data.materials.append(mat_bright_steel)

        # Iron rim ring
        bpy.ops.mesh.primitive_torus_add(major_radius=0.34, minor_radius=0.015, location=(shield_x, -0.22, 0.45))
        rim = bpy.context.active_object
        rim.rotation_euler = (1.4, 0, rot_z)
        rim.data.materials.append(mat_dark_iron)

    # Kettle Helmets (2 sitting on top crossbeam shelf)
    for hx in [-0.5, 0.5]:
        # Dome
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(hx, 0, 2.02))
        helm = bpy.context.active_object
        helm.scale = (1.0, 1.1, 0.9)
        helm.data.materials.append(mat_bright_steel)

        # Brim
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.02, location=(hx, 0, 1.93))
        brim = bpy.context.active_object
        brim.data.materials.append(mat_dark_iron)

    export_glb(output_path)

# -------------------------------------------------------------
# 2. Peasant Burgage Plot Chicken Coop (burgage_coop.glb)
# -------------------------------------------------------------
def build_burgage_coop(output_path):
    clear_scene()

    mat_timber = create_material("FenceTimber", (0.38, 0.25, 0.15, 1.0), roughness=0.85)
    mat_thatched = create_material("ThatchRoof", (0.58, 0.48, 0.22, 1.0), roughness=0.95)
    mat_mud = create_material("EarthFloor", (0.28, 0.20, 0.13, 1.0), roughness=0.98)
    mat_straw = create_material("StrawNesting", (0.75, 0.65, 0.30, 1.0), roughness=0.9)
    mat_wicker = create_material("WickerBasket", (0.45, 0.32, 0.18, 1.0), roughness=0.8)
    mat_egg = create_material("EggShell", (0.92, 0.88, 0.80, 1.0), roughness=0.35)

    # Backyard ground soil patch (2.2m x 1.8m x 0.05m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.02))
    dirt = bpy.context.active_object
    dirt.scale = (2.2, 1.8, 0.04)
    dirt.data.materials.append(mat_mud)

    # Fence Perimeter Posts (4 corner posts + 2 gate posts)
    fence_posts = [(-0.95, -0.75), (0.95, -0.75), (-0.95, 0.75), (0.95, 0.75), (-0.25, -0.75), (0.25, -0.75)]
    for px, py in fence_posts:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.8, location=(px, py, 0.4))
        post = bpy.context.active_object
        post.data.materials.append(mat_timber)

    # Fence Rails (Horizontal enclosure bars)
    for z_rail in [0.25, 0.6]:
        # Back wall rail
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.75, z_rail))
        r1 = bpy.context.active_object
        r1.scale = (1.9, 0.03, 0.04)
        r1.data.materials.append(mat_timber)

        # Left wall rail
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.95, 0, z_rail))
        r2 = bpy.context.active_object
        r2.scale = (0.03, 1.5, 0.04)
        r2.data.materials.append(mat_timber)

        # Right wall rail
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.95, 0, z_rail))
        r3 = bpy.context.active_object
        r3.scale = (0.03, 1.5, 0.04)
        r3.data.materials.append(mat_timber)

    # Elevated Hen House (Shelter: Width 0.9m, Depth 0.8m, Height 0.7m, raised 0.35m off ground)
    coop_x, coop_y = 0.35, 0.25

    # 4 Stilt Legs
    for lx in [coop_x - 0.38, coop_x + 0.38]:
        for ly in [coop_y - 0.32, coop_y + 0.32]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.45, location=(lx, ly, 0.22))
            stilt = bpy.context.active_object
            stilt.data.materials.append(mat_timber)

    # Hen house wooden main body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(coop_x, coop_y, 0.72))
    coop_body = bpy.context.active_object
    coop_body.scale = (0.85, 0.75, 0.55)
    coop_body.data.materials.append(mat_timber)

    # Sloped Thatched Gable Roof
    bpy.ops.mesh.primitive_cone_add(radius1=0.7, radius2=0.0, depth=0.45, vertices=4, location=(coop_x, coop_y, 1.15))
    roof = bpy.context.active_object
    roof.rotation_euler = (0, 0, 0.785) # 45 deg square alignment
    roof.scale = (0.95, 1.1, 1.0)
    roof.data.materials.append(mat_thatched)

    # Little entry hatch / ramp
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(coop_x - 0.45, coop_y, 0.24))
    ramp = bpy.context.active_object
    ramp.rotation_euler = (0, 0.45, 0)
    ramp.scale = (0.55, 0.25, 0.03)
    ramp.data.materials.append(mat_timber)

    # Feed Trough with straw
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.45, 0.1, 0.12))
    trough = bpy.context.active_object
    trough.scale = (0.5, 0.25, 0.16)
    trough.data.materials.append(mat_timber)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.45, 0.1, 0.18))
    straw = bpy.context.active_object
    straw.scale = (0.44, 0.20, 0.05)
    straw.data.materials.append(mat_straw)

    # Wicker Egg Basket at gate
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.16, location=(-0.6, -0.5, 0.1))
    basket = bpy.context.active_object
    basket.data.materials.append(mat_wicker)

    # Fresh Eggs inside basket
    for ex, ey in [(-0.62, -0.52), (-0.57, -0.48), (-0.60, -0.46)]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(ex, ey, 0.17))
        egg = bpy.context.active_object
        egg.scale = (0.9, 0.9, 1.25)
        egg.data.materials.append(mat_egg)

    export_glb(output_path)

# -------------------------------------------------------------
# 3. Combat Training Dummy (training_dummy.glb)
# -------------------------------------------------------------
def build_training_dummy(output_path):
    clear_scene()

    mat_pole = create_material("SturdyPole", (0.35, 0.22, 0.13, 1.0), roughness=0.8)
    mat_stone_base = create_material("BaseStone", (0.42, 0.42, 0.42, 1.0), roughness=0.9)
    mat_straw_body = create_material("BurlapStraw", (0.68, 0.58, 0.35, 1.0), roughness=0.95)
    mat_leather_straps = create_material("HarnessLeather", (0.30, 0.18, 0.10, 1.0), roughness=0.7)
    mat_iron_helm = create_material("DentedIron", (0.35, 0.36, 0.38, 1.0), roughness=0.4, metallic=0.9)
    mat_shield_wood = create_material("TargetShield", (0.60, 0.22, 0.18, 1.0), roughness=0.65)
    mat_shield_boss = create_material("SteelCenter", (0.7, 0.7, 0.72, 1.0), roughness=0.3, metallic=0.9)

    # Stone Weighted Foundation Plinth (0.8m x 0.8m x 0.2m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.1))
    base = bpy.context.active_object
    base.scale = (0.75, 0.75, 0.2)
    base.data.materials.append(mat_stone_base)

    # Timber Cross-skid foot bracing
    for rot in [0, 1.57]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.22))
        skid = bpy.context.active_object
        skid.rotation_euler = (0, 0, rot)
        skid.scale = (0.9, 0.16, 0.08)
        skid.data.materials.append(mat_pole)

    # Main Center Spine Pole (Height 2.1m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=2.0, location=(0, 0, 1.15))
    spine = bpy.context.active_object
    spine.data.materials.append(mat_pole)

    # Horizontal Shoulder Crossbeam (Width 1.3m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.3, location=(0, 0, 1.55))
    shoulders = bpy.context.active_object
    shoulders.rotation_euler = (0, 1.57, 0)
    shoulders.data.materials.append(mat_pole)

    # Stuffed Burlap Torso (Height 0.75m, Radius 0.22m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.75, location=(0, 0, 1.35))
    torso = bpy.context.active_object
    torso.scale = (1.1, 0.85, 1.0)
    torso.data.materials.append(mat_straw_body)

    # Leather Chest Reinforcement Straps (X harness)
    for rot_strap in [0.55, -0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.01, 1.35))
        strap = bpy.context.active_object
        strap.rotation_euler = (0, rot_strap, 0)
        strap.scale = (0.55, 0.20, 0.04)
        strap.data.materials.append(mat_leather_straps)

    # Waist Belt
    bpy.ops.mesh.primitive_torus_add(major_radius=0.21, minor_radius=0.03, location=(0, 0, 1.02))
    belt = bpy.context.active_object
    belt.data.materials.append(mat_leather_straps)

    # Dummy Head (Burlap sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(0, 0, 1.88))
    head = bpy.context.active_object
    head.scale = (0.9, 0.95, 1.1)
    head.data.materials.append(mat_straw_body)

    # Iron Kettle Helm mounted on head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(0, 0, 1.95))
    helm = bpy.context.active_object
    helm.scale = (1.0, 1.05, 0.9)
    helm.data.materials.append(mat_iron_helm)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.02, location=(0, 0, 1.87))
    brim = bpy.context.active_object
    brim.data.materials.append(mat_iron_helm)

    # Mounted Target Shield (Left arm target)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.26, depth=0.04, location=(-0.55, -0.08, 1.5))
    target_shield = bpy.context.active_object
    target_shield.rotation_euler = (1.57, 0, 0)
    target_shield.data.materials.append(mat_shield_wood)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07, location=(-0.55, -0.11, 1.5))
    boss = bpy.context.active_object
    boss.scale = (1.0, 0.4, 1.0)
    boss.data.materials.append(mat_shield_boss)

    # Wooden Training Sword (Tied to right arm)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, -0.15, 1.35))
    dummy_sword = bpy.context.active_object
    dummy_sword.rotation_euler = (0.4, 0, 0.2)
    dummy_sword.scale = (0.05, 0.04, 0.8)
    dummy_sword.data.materials.append(mat_pole)

    export_glb(output_path)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    os.makedirs(base_dir, exist_ok=True)

    build_armory_rack(os.path.join(base_dir, "armory_rack.glb"))
    build_burgage_coop(os.path.join(base_dir, "burgage_coop.glb"))
    build_training_dummy(os.path.join(base_dir, "training_dummy.glb"))
    print("\n>>> All Milestone 20 models generated successfully! <<<")
