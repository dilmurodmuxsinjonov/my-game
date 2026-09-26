# tools/generate_milestone25_models.py
# Voxel Lord: Feudal Realm - Milestone 25: Worldgen, Raiders & Locomotion
# Generates 3D models for Bandit Tent, Spiked Barricade, and Loot Chest via Blender 5.2.1 LTS

import bpy
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.8, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def create_bandit_tent():
    clear_scene()

    mat_canvas = create_material("TentHide", (0.35, 0.22, 0.14, 1.0), roughness=0.92)
    mat_wood = create_material("TentPoles", (0.24, 0.16, 0.08, 1.0), roughness=0.85)
    mat_bone = create_material("PikeSkull", (0.85, 0.82, 0.75, 1.0), roughness=0.7)
    mat_cloth = create_material("BeddingFur", (0.20, 0.15, 0.12, 1.0), roughness=0.95)

    # 1. Main A-frame ridge tent body (Prism shape)
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.6, depth=2.8, location=(0, 0, 1.1))
    tent = bpy.context.active_object
    tent.rotation_euler = (0, math.radians(90), 0)
    tent.scale = (0.9, 1.0, 1.0)
    tent.data.materials.append(mat_canvas)

    # 2. Wooden support ridge poles extending at front and back
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=3.2, location=(0, 0, 1.95))
    ridge_pole = bpy.context.active_object
    ridge_pole.rotation_euler = (math.radians(90), 0, 0)
    ridge_pole.data.materials.append(mat_wood)

    # Cross poles at front entrance
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.3, location=(0, -1.35, 1.05))
    pole_l = bpy.context.active_object
    pole_l.rotation_euler = (0, math.radians(35), 0)
    pole_l.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=2.3, location=(0, -1.35, 1.05))
    pole_r = bpy.context.active_object
    pole_r.rotation_euler = (0, math.radians(-35), 0)
    pole_r.data.materials.append(mat_wood)

    # 3. Ground bedding fur inside tent
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.1, 0.08))
    bedding = bpy.context.active_object
    bedding.scale = (1.2, 1.8, 0.1)
    bedding.data.materials.append(mat_cloth)

    # 4. Raider pike with trophy skull at entrance
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=2.1, location=(1.1, -1.4, 1.05))
    pike = bpy.context.active_object
    pike.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(1.1, -1.4, 2.15))
    skull = bpy.context.active_object
    skull.scale = (0.85, 1.0, 1.1)
    skull.data.materials.append(mat_bone)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "bandit_tent.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated bandit_tent.glb -> {output_path}")

def create_spiked_barricade():
    clear_scene()

    mat_wood = create_material("BarricadeWood", (0.32, 0.20, 0.10, 1.0), roughness=0.88)
    mat_iron = create_material("BarricadeIron", (0.16, 0.16, 0.18, 1.0), roughness=0.4, metallic=0.9)
    mat_spike_tip = create_material("SpikeTip", (0.28, 0.28, 0.30, 1.0), roughness=0.3, metallic=0.85)

    # 1. Main horizontal beam
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=2.6, location=(0, 0, 0.65))
    h_beam = bpy.context.active_object
    h_beam.rotation_euler = (0, math.radians(90), 0)
    h_beam.data.materials.append(mat_wood)

    # 2. Crossed leg supports (Left, Middle, Right)
    x_positions = [-0.9, 0.0, 0.9]
    for xp in x_positions:
        # Leg 1 (angled back)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.5, location=(xp, 0, 0.65))
        leg1 = bpy.context.active_object
        leg1.rotation_euler = (math.radians(35), 0, 0)
        leg1.data.materials.append(mat_wood)

        # Leg 2 (angled front)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.5, location=(xp, 0, 0.65))
        leg2 = bpy.context.active_object
        leg2.rotation_euler = (math.radians(-35), 0, 0)
        leg2.data.materials.append(mat_wood)

    # 3. Angled sharpened defensive forward spikes (6 spikes jutting toward attacker at Y = -0.8)
    spike_offsets = [-1.0, -0.6, -0.2, 0.2, 0.6, 1.0]
    for so in spike_offsets:
        bpy.ops.mesh.primitive_cone_add(radius1=0.08, depth=1.3, location=(so, -0.3, 0.75))
        spike = bpy.context.active_object
        spike.rotation_euler = (math.radians(-65), 0, 0)
        spike.data.materials.append(mat_spike_tip)

    # 4. Iron banding and binding chain loops
    for xp in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.03, location=(xp, 0, 0.65))
        band = bpy.context.active_object
        band.rotation_euler = (0, math.radians(90), 0)
        band.data.materials.append(mat_iron)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "spiked_barricade.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated spiked_barricade.glb -> {output_path}")

def create_loot_chest():
    clear_scene()

    mat_wood = create_material("ChestWood", (0.38, 0.22, 0.12, 1.0), roughness=0.8)
    mat_gold = create_material("GoldCoins", (0.95, 0.78, 0.15, 1.0), roughness=0.25, metallic=0.95)
    mat_iron = create_material("ChestIron", (0.15, 0.15, 0.18, 1.0), roughness=0.35, metallic=0.9)
    mat_lock = create_material("BrassLock", (0.80, 0.65, 0.20, 1.0), roughness=0.3, metallic=0.9)

    # 1. Main chest container base (1.2m wide, 0.8m deep, 0.55m tall)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.3))
    base = bpy.context.active_object
    base.scale = (1.2, 0.8, 0.6)
    base.data.materials.append(mat_wood)

    # 2. Curved domed lid (half-cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1.2, location=(0, 0, 0.6))
    lid = bpy.context.active_object
    lid.rotation_euler = (0, math.radians(90), 0)
    lid.data.materials.append(mat_wood)

    # 3. Reinforced wrought-iron corner brackets and banding straps
    for bx in [-0.5, 0.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, 0.3))
        strap = bpy.context.active_object
        strap.scale = (0.08, 0.84, 0.62)
        strap.data.materials.append(mat_iron)

        # Arch strap over lid
        bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.08, location=(bx, 0, 0.6))
        strap_lid = bpy.context.active_object
        strap_lid.rotation_euler = (0, math.radians(90), 0)
        strap_lid.data.materials.append(mat_iron)

    # 4. Front lock clasp and heavy padlock
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.42, 0.52))
    clasp = bpy.context.active_object
    clasp.scale = (0.12, 0.04, 0.18)
    clasp.data.materials.append(mat_lock)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.02, location=(0, -0.44, 0.44))
    shackle = bpy.context.active_object
    shackle.data.materials.append(mat_iron)

    # 5. Spilled loot & gold coins at the base of the chest
    coin_coords = [(-0.4, -0.48), (0.2, -0.52), (0.5, -0.46), (-0.1, -0.55), (0.35, -0.58)]
    for cx, cy in coin_coords:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.03, location=(cx, cy, 0.02))
        coin = bpy.context.active_object
        coin.data.materials.append(mat_gold)

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models", "loot_chest.glb"))
    bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    print(f"[MODEL] Generated loot_chest.glb -> {output_path}")

if __name__ == "__main__":
    create_bandit_tent()
    create_spiked_barricade()
    create_loot_chest()
    print("[ALL DONE] Milestone 25 models generated successfully!")
