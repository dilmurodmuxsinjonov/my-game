"""Blender 5.2 Headless Model Generator for Milestone 15:
1. bloomery.glb (TerraFirmaCraft Refractory Shaft Bloomery Smelting Furnace)
2. charcoal_pit.glb (TerraFirmaCraft Sealed Pyrolysis Charcoal Burning Mound)
3. crucible.glb (TerraFirmaCraft Fireclay Crucible Pot with Molten Bronze & Tongs)
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_material(name, color, roughness=0.7, metallic=0.0, emission=None, emission_strength=1.0):
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
# 35. TerraFirmaCraft Bloomery Furnace (bloomery.glb)
# -------------------------------------------------------------
def build_bloomery():
    reset_scene()
    mat_stone = create_material("RefractoryStone", (0.32, 0.28, 0.25, 1.0), roughness=0.9)
    mat_firebrick = create_material("TerracottaFirebrick", (0.52, 0.24, 0.16, 1.0), roughness=0.85)
    mat_iron = create_material("WroughtIronHoop", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.9)
    mat_ember = create_material("SmeltingEmberGlow", (1.0, 0.42, 0.05, 1.0), roughness=0.2,
                                emission=(1.0, 0.42, 0.05, 1.0), emission_strength=3.5)
    mat_slag = create_material("VitreousSlag", (0.15, 0.13, 0.10, 1.0), roughness=0.2, metallic=0.3)

    # 1. Base Hearth Foundation (Square stepped stone base)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    base = bpy.context.active_object
    base.scale = (1.5, 1.5, 0.3)
    base.data.materials.append(mat_stone)

    # 2. Lower Cylindrical Hearth Chamber
    bpy.ops.mesh.primitive_cylinder_add(radius=0.68, depth=0.7, vertices=16, location=(0, 0, 0.65))
    hearth = bpy.context.active_object
    hearth.data.materials.append(mat_firebrick)

    # 3. Upper Tapering Chimney Stack (Shaft)
    bpy.ops.mesh.primitive_cone_add(radius1=0.64, radius2=0.42, depth=1.4, vertices=16, location=(0, 0, 1.70))
    shaft = bpy.context.active_object
    shaft.data.materials.append(mat_firebrick)

    # 4. Top Chimney Crown Rim
    bpy.ops.mesh.primitive_torus_add(major_radius=0.42, minor_radius=0.06, location=(0, 0, 2.40))
    crown = bpy.context.active_object
    crown.data.materials.append(mat_stone)

    # 5. Glowing Top Flue Exhaust Opening
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.08, vertices=12, location=(0, 0, 2.38))
    top_ember = bpy.context.active_object
    top_ember.data.materials.append(mat_ember)

    # 6. Front Bloom Tap Hole & Archway (Lower Front Door)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.62, 0.45))
    tap_door = bpy.context.active_object
    tap_door.scale = (0.38, 0.22, 0.42)
    tap_door.data.materials.append(mat_stone)

    # Glowing Molten Bloom / Slag inside tap hole
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.60, 0.35))
    tap_glow = bpy.context.active_object
    tap_glow.scale = (0.28, 0.12, 0.20)
    tap_glow.data.materials.append(mat_ember)

    # Vitreous slag puddle at doorstep
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.04, vertices=10, location=(0, 0.78, 0.16))
    slag_puddle = bpy.context.active_object
    slag_puddle.scale = (1.2, 0.8, 1.0)
    slag_puddle.data.materials.append(mat_slag)

    # 7. Rear Tuyere Bellows Air Pipe
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.45, vertices=12, location=(0, -0.68, 0.50))
    tuyere = bpy.context.active_object
    tuyere.rotation_euler = (math.radians(90), 0, 0)
    tuyere.data.materials.append(mat_iron)

    # Tuyere mounting flange
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.06, vertices=12, location=(0, -0.58, 0.50))
    flange = bpy.context.active_object
    flange.rotation_euler = (math.radians(90), 0, 0)
    flange.data.materials.append(mat_stone)

    # 8. Structural Iron Reinforcing Hoops (preventing thermal splitting)
    hoop_heights = [0.85, 1.35, 1.85]
    hoop_radii = [0.65, 0.56, 0.48]
    for h, r in zip(hoop_heights, hoop_radii):
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.025, location=(0, 0, h))
        hoop = bpy.context.active_object
        hoop.data.materials.append(mat_iron)

    export_glb("bloomery.glb")

# -------------------------------------------------------------
# 36. TerraFirmaCraft Charcoal Pit (charcoal_pit.glb)
# -------------------------------------------------------------
def build_charcoal_pit():
    reset_scene()
    mat_sod = create_material("EarthenSodClay", (0.28, 0.22, 0.16, 1.0), roughness=0.95)
    mat_bark = create_material("OakLogBark", (0.24, 0.16, 0.10, 1.0), roughness=0.9)
    mat_charred = create_material("CharredWoodCore", (0.08, 0.08, 0.08, 1.0), roughness=0.85)
    mat_ash = create_material("PitAshGray", (0.45, 0.45, 0.43, 1.0), roughness=0.98)
    mat_smolder = create_material("SmolderingCoalVent", (0.95, 0.28, 0.05, 1.0), roughness=0.3,
                                  emission=(0.95, 0.28, 0.05, 1.0), emission_strength=2.8)

    # 1. Outer Earthen Mound / Clay Sod Dome
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=10, location=(0, 0, 0))
    mound = bpy.context.active_object
    mound.scale = (1.2, 1.15, 0.55)
    mound.data.materials.append(mat_sod)

    # 2. Exposed Stacked Log Layers beneath the sod skirt
    log_offsets = [
        (-0.75, -0.4, 0.15, 0.2),
        (-0.72, 0.35, 0.15, -0.1),
        (0.74, -0.3, 0.15, 0.3),
        (0.72, 0.4, 0.15, -0.2),
        (0.0, 0.85, 0.15, 1.57),
        (0.0, -0.85, 0.15, 1.57)
    ]
    for x, y, z, rot in log_offsets:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=0.8, vertices=8, location=(x, y, z))
        log = bpy.context.active_object
        log.rotation_euler = (0, math.radians(90), rot)
        log.data.materials.append(mat_bark)

        # Charred log end
        bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=0.02, vertices=8, location=(x + math.cos(rot)*0.4, y + math.sin(rot)*0.4, z))
        end = bpy.context.active_object
        end.rotation_euler = (0, math.radians(90), rot)
        end.data.materials.append(mat_charred)

    # 3. Central Exhaust Vent Chimney (clay flue cone)
    bpy.ops.mesh.primitive_cone_add(radius1=0.28, radius2=0.18, depth=0.35, vertices=10, location=(0, 0, 0.65))
    vent_chimney = bpy.context.active_object
    vent_chimney.data.materials.append(mat_sod)

    # Smoldering flue interior
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.08, vertices=8, location=(0, 0, 0.78))
    flue_glow = bpy.context.active_object
    flue_glow.data.materials.append(mat_smolder)

    # 4. Small draft vent holes along flank with glowing embers
    vent_angles = [0.6, 1.8, 3.2, 4.4, 5.5]
    for a in vent_angles:
        vx = math.cos(a) * 0.75
        vy = math.sin(a) * 0.75
        vz = 0.32
        bpy.ops.mesh.primitive_cube_add(size=0.12, location=(vx, vy, vz))
        hole = bpy.context.active_object
        hole.data.materials.append(mat_smolder)

    # 5. Surrounding ring of ash and loam sod
    bpy.ops.mesh.primitive_torus_add(major_radius=1.1, minor_radius=0.08, location=(0, 0, 0.05))
    ash_ring = bpy.context.active_object
    ash_ring.data.materials.append(mat_ash)

    export_glb("charcoal_pit.glb")

# -------------------------------------------------------------
# 37. TerraFirmaCraft Ceramic Crucible (crucible.glb)
# -------------------------------------------------------------
def build_crucible():
    reset_scene()
    mat_clay = create_material("RefractoryFireclay", (0.48, 0.34, 0.22, 1.0), roughness=0.85)
    mat_clay_lip = create_material("SootyClayLip", (0.28, 0.22, 0.18, 1.0), roughness=0.9)
    mat_iron = create_material("BlacksmithTongsIron", (0.16, 0.16, 0.18, 1.0), roughness=0.35, metallic=0.9)
    mat_molten_bronze = create_material("MoltenBronzeBath", (0.98, 0.58, 0.12, 1.0), roughness=0.15,
                                        emission=(0.98, 0.58, 0.12, 1.0), emission_strength=3.2)
    mat_dross = create_material("OxidizedDross", (0.35, 0.32, 0.18, 1.0), roughness=0.6, metallic=0.4)

    # 1. Main Fireclay Crucible Body (Tapered pot)
    bpy.ops.mesh.primitive_cone_add(radius1=0.22, radius2=0.35, depth=0.55, vertices=16, location=(0, 0, 0.30))
    pot = bpy.context.active_object
    pot.data.materials.append(mat_clay)

    # 2. Heavy Round Base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.23, depth=0.08, vertices=16, location=(0, 0, 0.04))
    base = bpy.context.active_object
    base.data.materials.append(mat_clay)

    # 3. Reinforced Rim Collar
    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.035, location=(0, 0, 0.57))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_clay_lip)

    # 4. Triangular Pouring Spout
    bpy.ops.mesh.primitive_cone_add(radius1=0.08, radius2=0.02, depth=0.14, vertices=3, location=(0, 0.38, 0.56))
    spout = bpy.context.active_object
    spout.rotation_euler = (math.radians(-65), 0, 0)
    spout.data.materials.append(mat_clay_lip)

    # 5. Molten Bronze Alloy Liquid Pool
    bpy.ops.mesh.primitive_cylinder_add(radius=0.30, depth=0.04, vertices=16, location=(0, 0, 0.50))
    bath = bpy.context.active_object
    bath.data.materials.append(mat_molten_bronze)

    # Dross / slag floating at surface
    bpy.ops.mesh.primitive_cube_add(size=0.12, location=(-0.10, 0.08, 0.51))
    dross = bpy.context.active_object
    dross.scale = (1.4, 0.6, 0.2)
    dross.data.materials.append(mat_dross)

    # 6. Forged Iron Tongs Ring (Enclosing waist)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.30, minor_radius=0.022, location=(0, 0, 0.38))
    tongs_ring = bpy.context.active_object
    tongs_ring.data.materials.append(mat_iron)

    # Tongs dual lifting handles
    for side in [-1, 1]:
        # Handle shaft
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.45, vertices=8, location=(side * 0.48, 0, 0.38))
        handle = bpy.context.active_object
        handle.rotation_euler = (0, math.radians(90), 0)
        handle.data.materials.append(mat_iron)

        # Handle hook grip
        bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.015, location=(side * 0.70, 0, 0.38))
        hook = bpy.context.active_object
        hook.rotation_euler = (math.radians(90), 0, 0)
        hook.data.materials.append(mat_iron)

    export_glb("crucible.glb")

if __name__ == "__main__":
    print("[BUILD] Generating Milestone 15 3D Models via Blender 5.2...")
    build_bloomery()
    build_charcoal_pit()
    build_crucible()
    print("[SUCCESS] Milestone 15 3D Models successfully generated!")
