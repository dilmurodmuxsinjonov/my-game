# tools/generate_milestone28_models.py
# Voxel Lord: Feudal Realm - Milestone 28: Ancient Crypt Dungeon & Relics
# Generates 3D models for Crypt Entrance, Stone Sarcophagus, and Wall Sconce via Blender 5.2.1 LTS

import bpy
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.8, metallic=0.0, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if emission_color and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def create_crypt_entrance():
    clear_scene()

    mat_stone = create_material("CryptStone", (0.35, 0.34, 0.32, 1.0), roughness=0.90)
    mat_moss_stone = create_material("CryptMossStone", (0.28, 0.33, 0.25, 1.0), roughness=0.92)
    mat_iron = create_material("CryptIronGate", (0.16, 0.16, 0.17, 1.0), roughness=0.45, metallic=0.8)
    mat_void = create_material("CryptVoid", (0.02, 0.02, 0.03, 1.0), roughness=0.98)

    # 1. Foundation base & worn stone steps
    for i, z_step in enumerate([0.1, 0.25, 0.4]):
        w = 2.4 - i * 0.15
        d = 1.8 - i * 0.35
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.4 - i * 0.3, z_step / 2.0))
        step = bpy.context.active_object
        step.scale = (w, d, z_step)
        step.data.materials.append(mat_stone if i % 2 == 0 else mat_moss_stone)

    # 2. Main Crypt Facade Wall & Pilasters
    # Left Pillar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-1.15, 0.6, 1.6))
    p_left = bpy.context.active_object
    p_left.scale = (0.55, 0.7, 2.4)
    p_left.data.materials.append(mat_stone)

    # Right Pillar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.15, 0.6, 1.6))
    p_right = bpy.context.active_object
    p_right.scale = (0.55, 0.7, 2.4)
    p_right.data.materials.append(mat_stone)

    # Top Arch Lintel / Pediment
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.6, 2.85))
    lintel = bpy.context.active_object
    lintel.scale = (2.85, 0.85, 0.6)
    lintel.data.materials.append(mat_moss_stone)

    # Triangular pediment crown
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1.45, depth=0.8, location=(0, 0.6, 3.45))
    pediment = bpy.context.active_object
    pediment.rotation_euler = (0, math.radians(90), 0)
    pediment.scale = (0.45, 1.0, 1.0)
    pediment.data.materials.append(mat_stone)

    # 3. Dark interior void backdrop
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.75, 1.45))
    interior_void = bpy.context.active_object
    interior_void.scale = (1.6, 0.2, 2.1)
    interior_void.data.materials.append(mat_void)

    # 4. Heavy forged iron portcullis / gate (vertical and horizontal bars)
    for bx in [-0.65, -0.4, -0.15, 0.15, 0.4, 0.65]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=2.0, location=(bx, 0.62, 1.55))
        bar = bpy.context.active_object
        bar.data.materials.append(mat_iron)

    for bz in [0.75, 1.35, 1.95]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=1.65, location=(0, 0.62, bz))
        hbar = bpy.context.active_object
        hbar.rotation_euler = (0, math.radians(90), 0)
        hbar.data.materials.append(mat_iron)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "crypt_entrance.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_stone_sarcophagus():
    clear_scene()

    mat_sarcophagus = create_material("SarcophagusStone", (0.45, 0.43, 0.40, 1.0), roughness=0.85)
    mat_effigy = create_material("EffigyStone", (0.52, 0.50, 0.47, 1.0), roughness=0.80)
    mat_cavity = create_material("CavityDark", (0.08, 0.07, 0.06, 1.0), roughness=0.95)
    mat_gold_relic = create_material("AncientGold", (0.85, 0.68, 0.22, 1.0), roughness=0.35, metallic=0.85)

    # 1. Base pedestal plinth
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.1))
    plinth = bpy.context.active_object
    plinth.scale = (1.2, 2.4, 0.2)
    plinth.data.materials.append(mat_sarcophagus)

    # 2. Main hollowed stone sarcophagus chest (walls)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    chest = bpy.context.active_object
    chest.scale = (1.05, 2.25, 0.6)
    chest.data.materials.append(mat_sarcophagus)

    # Dark inner hollow
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.65))
    inner = bpy.context.active_object
    inner.scale = (0.8, 2.0, 0.35)
    inner.data.materials.append(mat_cavity)

    # Glimmering relic inside cavity
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.09, depth=0.04, location=(0, 0.2, 0.58))
    relic_coin = bpy.context.active_object
    relic_coin.rotation_euler = (math.radians(20), math.radians(15), 0)
    relic_coin.data.materials.append(mat_gold_relic)

    # 3. Heavy sculpted effigy lid (cracked slightly askew)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.08, 0.05, 0.88))
    lid = bpy.context.active_object
    lid.scale = (1.12, 2.3, 0.18)
    lid.rotation_euler = (0, 0, math.radians(6)) # Slightly ajar
    lid.data.materials.append(mat_sarcophagus)

    # 4. Knight Effigy relief on lid
    # Headrest cushion
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.08, 0.85, 1.01))
    cushion = bpy.context.active_object
    cushion.scale = (0.55, 0.35, 0.12)
    cushion.rotation_euler = (0, 0, math.radians(6))
    cushion.data.materials.append(mat_effigy)

    # Knight Head / Great Helm
    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.16, depth=0.28, location=(0.08, 0.85, 1.14))
    helm = bpy.context.active_object
    helm.rotation_euler = (math.radians(90), 0, math.radians(6))
    helm.data.materials.append(mat_effigy)

    # Torso plate armor relief
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.08, 0.35, 1.05))
    torso = bpy.context.active_object
    torso.scale = (0.5, 0.65, 0.15)
    torso.rotation_euler = (0, 0, math.radians(6))
    torso.data.materials.append(mat_effigy)

    # Crossed sword on effigy chest
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=1.35, location=(0.08, -0.15, 1.08))
    sword = bpy.context.active_object
    sword.rotation_euler = (math.radians(90), 0, math.radians(6))
    sword.data.materials.append(mat_effigy)

    # Effigy leg greaves
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.08, -0.65, 1.02))
    legs = bpy.context.active_object
    legs.scale = (0.42, 0.75, 0.12)
    legs.rotation_euler = (0, 0, math.radians(6))
    legs.data.materials.append(mat_effigy)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "stone_sarcophagus.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

def create_wall_sconce():
    clear_scene()

    mat_iron = create_material("ForgedIron", (0.18, 0.18, 0.19, 1.0), roughness=0.45, metallic=0.75)
    mat_wood = create_material("TorchWood", (0.32, 0.22, 0.14, 1.0), roughness=0.82)
    mat_flame = create_material("TorchFlame", (1.0, 0.55, 0.08, 1.0), roughness=0.2,
                                emission_color=(1.0, 0.52, 0.05, 1.0), emission_strength=4.5)

    # 1. Iron wall backplate
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.02, 0.45))
    plate = bpy.context.active_object
    plate.scale = (0.22, 0.04, 0.7)
    plate.data.materials.append(mat_iron)

    # 2. Forged mounting rivets
    for rz in [0.2, 0.7]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.06, location=(0, 0.01, rz))
        rivet = bpy.context.active_object
        rivet.rotation_euler = (math.radians(90), 0, 0)
        rivet.data.materials.append(mat_iron)

    # 3. Forged curved iron support bracket arm extending outward
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.42, location=(0, 0.18, 0.45))
    arm = bpy.context.active_object
    arm.rotation_euler = (math.radians(65), 0, 0)
    arm.data.materials.append(mat_iron)

    # 4. Iron torch basket ring cup
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.12, depth=0.14, location=(0, 0.36, 0.62))
    cup = bpy.context.active_object
    cup.data.materials.append(mat_iron)

    # 5. Wooden torch handle inside cup
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.65, location=(0, 0.36, 0.75))
    torch_shaft = bpy.context.active_object
    torch_shaft.rotation_euler = (math.radians(-10), 0, 0)
    torch_shaft.data.materials.append(mat_wood)

    # 6. Wrapped pitch head
    bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.18, location=(0, 0.34, 1.02))
    pitch_head = bpy.context.active_object
    pitch_head.rotation_euler = (math.radians(-10), 0, 0)
    pitch_head.data.materials.append(mat_iron)

    # 7. Stylized low-poly burning ember flame
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.11, radius2=0.01, depth=0.32, location=(0, 0.33, 1.22))
    flame = bpy.context.active_object
    flame.rotation_euler = (math.radians(-10), 0, 0)
    flame.data.materials.append(mat_flame)

    # Export GLB
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    filepath = os.path.join(output_dir, "wall_sconce.glb")
    bpy.ops.export_scene.gltf(filepath=filepath, export_format='GLB')
    print(f"[MODEL] Generated {filepath}")

if __name__ == "__main__":
    create_crypt_entrance()
    create_stone_sarcophagus()
    create_wall_sconce()
    print("Milestone 28 3D models generated successfully!")
