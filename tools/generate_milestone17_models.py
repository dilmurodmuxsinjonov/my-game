"""Blender 5.2 Headless Model Generator for Milestone 17:
1. town_hall_desk.glb (MineColonies Town Hall Magistrate Desk & Heraldic Charter)
2. treasury_vault.glb (Royal Treasury Coin Vault & Iron-Banded Strongbox)
3. guard_post.glb (Barracks Sentry Weapons Rack with Halberds & Shield)
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
# 41. MineColonies Town Hall Desk (town_hall_desk.glb)
# -------------------------------------------------------------
def build_town_hall_desk():
    reset_scene()
    mat_wood = create_material("MagistrateOak", (0.30, 0.18, 0.10, 1.0), roughness=0.65)
    mat_parchment = create_material("CharterParchment", (0.88, 0.82, 0.68, 1.0), roughness=0.9)
    mat_wax = create_material("RoyalWaxSeal", (0.85, 0.10, 0.12, 1.0), roughness=0.3)
    mat_gold = create_material("InsigniaGold", (0.92, 0.75, 0.22, 1.0), roughness=0.25, metallic=0.92)
    mat_banner = create_material("HeraldicBanner", (0.15, 0.25, 0.65, 1.0), roughness=0.8)

    # 1. Main Desk Tabletop
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.85))
    top = bpy.context.active_object
    top.scale = (1.50, 0.90, 0.08)
    top.data.materials.append(mat_wood)

    # 2. Four Carved Heavy Legs
    for x in [-0.62, 0.62]:
        for y in [-0.35, 0.35]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.42))
            leg = bpy.context.active_object
            leg.scale = (0.12, 0.12, 0.82)
            leg.data.materials.append(mat_wood)

    # Side Pedestal Modesty Panels
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.36, 0.50))
    panel = bpy.context.active_object
    panel.scale = (1.20, 0.04, 0.60)
    panel.data.materials.append(mat_wood)

    # 3. Unrolled Royal Charter Document on Desk
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.15, 0.05, 0.90))
    parch = bpy.context.active_object
    parch.scale = (0.55, 0.42, 0.015)
    parch.rotation_euler.z = math.radians(8)
    parch.data.materials.append(mat_parchment)

    # Rolled top edge of parchment
    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.44, vertices=12, location=(-0.41, 0.08, 0.915))
    roll = bpy.context.active_object
    roll.rotation_euler = (math.radians(98), 0, 0)
    roll.data.materials.append(mat_parchment)

    # Red Wax Sovereign Seal Stamp on Charter
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.015, vertices=12, location=(-0.05, -0.05, 0.915))
    seal = bpy.context.active_object
    seal.data.materials.append(mat_wax)

    # 4. Brass Inkwell and Quill Pen
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.06, vertices=12, location=(0.45, 0.22, 0.92))
    inkwell = bpy.context.active_object
    inkwell.data.materials.append(mat_gold)

    # Goose Quill (slanted in inkwell)
    bpy.ops.mesh.primitive_cone_add(radius1=0.015, radius2=0.002, depth=0.35, vertices=8, location=(0.48, 0.24, 1.05))
    quill = bpy.context.active_object
    quill.rotation_euler = (math.radians(-25), math.radians(15), 0)
    quill.data.materials.append(mat_parchment)

    # 5. Heraldic Realm Banner Flagpole on Desk Corner
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.85, vertices=10, location=(0.60, -0.28, 1.25))
    pole = bpy.context.active_object
    pole.data.materials.append(mat_gold)

    # Hanging Silk Banner Flag
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, -0.28, 1.45))
    flag = bpy.context.active_object
    flag.scale = (0.02, 0.28, 0.35)
    flag.data.materials.append(mat_banner)

    # Gold Finial Eagle Spearhead at top of flagpole
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, radius2=0.005, depth=0.10, vertices=8, location=(0.60, -0.28, 1.72))
    finial = bpy.context.active_object
    finial.data.materials.append(mat_gold)

    export_glb("town_hall_desk.glb")

# -------------------------------------------------------------
# 42. Royal Treasury Vault (treasury_vault.glb)
# -------------------------------------------------------------
def build_treasury_vault():
    reset_scene()
    mat_stone = create_material("VaultGranite", (0.32, 0.32, 0.34, 1.0), roughness=0.85)
    mat_iron = create_material("ReinforcedIronStraps", (0.16, 0.16, 0.18, 1.0), roughness=0.35, metallic=0.92)
    mat_gold_coins = create_material("MintedGoldCoinsGlow", (0.95, 0.78, 0.18, 1.0), roughness=0.2, metallic=0.95,
                                    emission=(0.95, 0.78, 0.18, 1.0), emission_strength=1.5)
    mat_brass_lock = create_material("OrnatePadlockBrass", (0.85, 0.65, 0.20, 1.0), roughness=0.25, metallic=0.9)

    # 1. Main Vault Plinth / Strongbox Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.45))
    chest = bpy.context.active_object
    chest.scale = (1.30, 0.90, 0.70)
    chest.data.materials.append(mat_stone)

    # 2. Vault Arched Lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=1.30, vertices=16, location=(0, 0, 0.80))
    lid = bpy.context.active_object
    lid.rotation_euler = (0, math.radians(90), 0)
    lid.scale = (1.0, 1.0, 0.70)
    lid.data.materials.append(mat_stone)

    # 3. Heavy Riveted Iron Reinforcing Straps (Horizontal & Vertical)
    for x in [-0.48, 0.0, 0.48]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.52))
        strap = bpy.context.active_object
        strap.scale = (0.08, 0.94, 0.88)
        strap.data.materials.append(mat_iron)

    # Horizontal Iron Girdles
    for z in [0.25, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, z))
        girdle = bpy.context.active_object
        girdle.scale = (1.34, 0.94, 0.06)
        girdle.data.materials.append(mat_iron)

    # 4. Heavy Brass Master Padlock Latch
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.48, 0.65))
    hasp = bpy.context.active_object
    hasp.scale = (0.16, 0.06, 0.22)
    hasp.data.materials.append(mat_brass_lock)

    # Padlock Shackle Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.02, location=(0, 0.49, 0.78))
    shackle = bpy.context.active_object
    shackle.data.materials.append(mat_iron)

    # 5. Overflowing Mounds of Minted Gold Coins on Top & Flanks
    coin_piles = [
        (0.25, 0.15, 0.92, 0.22),
        (-0.20, -0.10, 0.94, 0.18),
        (0.55, 0.42, 0.20, 0.25),
        (-0.52, 0.40, 0.15, 0.20)
    ]
    for cx, cy, cz, cr in coin_piles:
        bpy.ops.mesh.primitive_cylinder_add(radius=cr, depth=0.08, vertices=12, location=(cx, cy, cz))
        pile = bpy.context.active_object
        pile.data.materials.append(mat_gold_coins)

        # Loose coins scattered
        for a in range(4):
            ang = a * 1.57
            bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.015, vertices=8,
                                               location=(cx + math.cos(ang)*cr*0.8, cy + math.sin(ang)*cr*0.8, cz + 0.04))
            loose = bpy.context.active_object
            loose.rotation_euler = (math.radians(12), math.radians(-8), ang)
            loose.data.materials.append(mat_gold_coins)

    export_glb("treasury_vault.glb")

# -------------------------------------------------------------
# 43. Barracks Guard Sentry Post (guard_post.glb)
# -------------------------------------------------------------
def build_guard_post():
    reset_scene()
    mat_wood = create_material("TimberRack", (0.28, 0.16, 0.08, 1.0), roughness=0.8)
    mat_steel = create_material("WeaponSteel", (0.75, 0.75, 0.78, 1.0), roughness=0.25, metallic=0.95)
    mat_iron = create_material("ForgedIronMount", (0.16, 0.16, 0.18, 1.0), roughness=0.35, metallic=0.9)
    mat_shield = create_material("HeaterShieldPaint", (0.75, 0.12, 0.15, 1.0), roughness=0.5)
    mat_shield_rim = create_material("ShieldBrassRim", (0.88, 0.72, 0.22, 1.0), roughness=0.3, metallic=0.9)
    mat_torch_glow = create_material("SentryTorchGlow", (1.0, 0.50, 0.08, 1.0), roughness=0.2,
                                     emission=(1.0, 0.50, 0.08, 1.0), emission_strength=3.0)

    # 1. Heavy Timber A-Frame Sentry Rack
    # Base Skids
    for y in [-0.35, 0.35]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, 0.08))
        skid = bpy.context.active_object
        skid.scale = (1.40, 0.14, 0.16)
        skid.data.materials.append(mat_wood)

    # Upright A-Frame Columns
    for x in [-0.55, 0.55]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.90))
        post = bpy.context.active_object
        post.scale = (0.12, 0.14, 1.65)
        post.data.materials.append(mat_wood)

    # Horizontal Rest Bars
    for z in [0.45, 1.35]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, z))
        bar = bpy.context.active_object
        bar.scale = (1.30, 0.08, 0.08)
        bar.data.materials.append(mat_wood)

    # 2. Resting Painted Heater Shield (Leaning against rack)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.15, -0.18, 0.65))
    shield = bpy.context.active_object
    shield.scale = (0.48, 0.04, 0.70)
    shield.rotation_euler = (math.radians(-14), 0, math.radians(5))
    shield.data.materials.append(mat_shield)

    # Brass Shield Boss & Cross
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.03, vertices=12, location=(-0.15, -0.16, 0.72))
    boss = bpy.context.active_object
    boss.rotation_euler = (math.radians(76), 0, math.radians(5))
    boss.data.materials.append(mat_shield_rim)

    # 3. Two Upright Poleaxes / Halberds in Rack Slots
    for hx in [0.22, 0.42]:
        # Halberd Shaft
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=2.10, vertices=10, location=(hx, 0.02, 1.05))
        h_shaft = bpy.context.active_object
        h_shaft.rotation_euler = (math.radians(5), 0, 0)
        h_shaft.data.materials.append(mat_wood)

        # Halberd Axe Blade & Spear Point Head
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx + 0.08, 0.12, 2.05))
        h_blade = bpy.context.active_object
        h_blade.scale = (0.22, 0.015, 0.28)
        h_blade.data.materials.append(mat_steel)

        # Spear tip spike
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0.005, depth=0.35, vertices=8, location=(hx, 0.12, 2.25))
        h_spike = bpy.context.active_object
        h_spike.data.materials.append(mat_steel)

    # 4. Sentry Iron Wall-Lantern / Torch Brazier
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.18, vertices=8, location=(-0.58, -0.12, 1.55))
    brazier = bpy.context.active_object
    brazier.data.materials.append(mat_iron)

    # Glowing Flame Ember Core
    bpy.ops.mesh.primitive_cone_add(radius1=0.06, radius2=0.01, depth=0.16, vertices=8, location=(-0.58, -0.12, 1.66))
    flame = bpy.context.active_object
    flame.data.materials.append(mat_torch_glow)

    export_glb("guard_post.glb")

if __name__ == "__main__":
    print("[BUILD] Generating Milestone 17 3D Models via Blender 5.2...")
    build_town_hall_desk()
    build_treasury_vault()
    build_guard_post()
    print("[SUCCESS] Milestone 17 3D Models successfully generated!")
