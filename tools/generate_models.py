"""Procedural 3D Medieval Asset Generator for Voxel Lord: Feudal Realm.
Executed via Headless Blender 5.2 LTS:
    blender.exe -b --python tools/generate_models.py
Exports high-quality low-poly .glb models into res://assets/models/
"""

import bpy
import os
import math

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Ensure a collection exists
    if not bpy.data.collections:
        col = bpy.data.collections.new("Collection")
        bpy.context.scene.collection.children.link(col)

def create_material(name, color_rgba, roughness=0.8, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color_rgba
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def export_glb(filename):
    out_path = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"[EXPORTED] {out_path} ({os.path.getsize(out_path)} bytes)")

# -------------------------------------------------------------
# 1. Medieval Pickaxe
# -------------------------------------------------------------
def build_pickaxe():
    reset_scene()
    mat_wood = create_material("WoodHandle", (0.38, 0.22, 0.10, 1.0), roughness=0.9)
    mat_iron = create_material("IronHead", (0.55, 0.58, 0.62, 1.0), roughness=0.35, metallic=0.85)

    # Handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.8, vertices=8, location=(0, 0, 0.4))
    handle = bpy.context.active_object
    handle.name = "PickaxeHandle"
    handle.data.materials.append(mat_wood)

    # Pickaxe Head (curved iron beam)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.78))
    head = bpy.context.active_object
    head.name = "PickaxeHead"
    head.scale = (0.45, 0.05, 0.05)
    head.data.materials.append(mat_iron)

    # Beveled tips
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.15, vertices=4, location=(0.25, 0, 0.78), rotation=(0, math.radians(90), 0))
    tip1 = bpy.context.active_object
    tip1.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.15, vertices=4, location=(-0.25, 0, 0.78), rotation=(0, math.radians(-90), 0))
    tip2 = bpy.context.active_object
    tip2.data.materials.append(mat_iron)

    export_glb("pickaxe.glb")

# -------------------------------------------------------------
# 2. Medieval Axe
# -------------------------------------------------------------
def build_axe():
    reset_scene()
    mat_wood = create_material("AxeWood", (0.42, 0.25, 0.12, 1.0), roughness=0.88)
    mat_steel = create_material("AxeSteel", (0.68, 0.70, 0.73, 1.0), roughness=0.3, metallic=0.9)

    # Haft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.85, vertices=8, location=(0, 0, 0.42))
    haft = bpy.context.active_object
    haft.name = "AxeHaft"
    haft.data.materials.append(mat_wood)

    # Blade body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.08, 0, 0.78))
    blade = bpy.context.active_object
    blade.name = "AxeBlade"
    blade.scale = (0.16, 0.04, 0.18)
    blade.data.materials.append(mat_steel)

    # Sharp cutting edge
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.03, vertices=8, location=(0.18, 0, 0.78), rotation=(0, math.radians(90), 0))
    edge = bpy.context.active_object
    edge.scale = (1.0, 0.8, 1.0)
    edge.data.materials.append(mat_steel)

    export_glb("axe.glb")

# -------------------------------------------------------------
# 3. Medieval Sword
# -------------------------------------------------------------
def build_sword():
    reset_scene()
    mat_blade = create_material("BladeSteel", (0.82, 0.84, 0.88, 1.0), roughness=0.2, metallic=0.95)
    mat_guard = create_material("CrossguardBrass", (0.75, 0.60, 0.20, 1.0), roughness=0.3, metallic=0.8)
    mat_grip = create_material("LeatherGrip", (0.28, 0.15, 0.08, 1.0), roughness=0.95)

    # Blade
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.55))
    blade = bpy.context.active_object
    blade.name = "SwordBlade"
    blade.scale = (0.07, 0.015, 0.65)
    blade.data.materials.append(mat_blade)

    # Crossguard
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.22))
    guard = bpy.context.active_object
    guard.name = "SwordGuard"
    guard.scale = (0.24, 0.04, 0.03)
    guard.data.materials.append(mat_guard)

    # Grip
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.18, vertices=8, location=(0, 0, 0.11))
    grip = bpy.context.active_object
    grip.name = "SwordGrip"
    grip.data.materials.append(mat_grip)

    # Pommel
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, segments=8, ring_count=6, location=(0, 0, 0.01))
    pommel = bpy.context.active_object
    pommel.name = "SwordPommel"
    pommel.data.materials.append(mat_guard)

    export_glb("sword.glb")

# -------------------------------------------------------------
# 4. Medieval Workbench
# -------------------------------------------------------------
def build_workbench():
    reset_scene()
    mat_timber = create_material("TimberPlank", (0.50, 0.33, 0.18, 1.0), roughness=0.85)
    mat_iron = create_material("ViseIron", (0.35, 0.35, 0.38, 1.0), roughness=0.4, metallic=0.7)

    # Table Top
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.8))
    top = bpy.context.active_object
    top.name = "TableTop"
    top.scale = (1.2, 0.8, 0.1)
    top.data.materials.append(mat_timber)

    # 4 Legs
    leg_coords = [(-0.5, -0.3), (-0.5, 0.3), (0.5, -0.3), (0.5, 0.3)]
    for i, (lx, ly) in enumerate(leg_coords):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.38))
        leg = bpy.context.active_object
        leg.name = f"TableLeg_{i}"
        leg.scale = (0.1, 0.1, 0.75)
        leg.data.materials.append(mat_timber)

    # Table vise / anvil
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.45, 0.25, 0.92))
    vise = bpy.context.active_object
    vise.name = "WorkbenchVise"
    vise.scale = (0.18, 0.18, 0.14)
    vise.data.materials.append(mat_iron)

    export_glb("workbench.glb")

# -------------------------------------------------------------
# 5. Medieval Campfire
# -------------------------------------------------------------
def build_campfire():
    reset_scene()
    mat_stone = create_material("CampStone", (0.45, 0.45, 0.48, 1.0), roughness=0.9)
    mat_log = create_material("CampLog", (0.32, 0.20, 0.10, 1.0), roughness=0.92)
    mat_fire = create_material("FireGlow", (1.0, 0.45, 0.05, 1.0), roughness=0.1)

    # Stone Ring (8 stones)
    for i in range(8):
        angle = i * (2.0 * math.pi / 8.0)
        sx = 0.45 * math.cos(angle)
        sy = 0.45 * math.sin(angle)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, segments=6, ring_count=5, location=(sx, sy, 0.1))
        stone = bpy.context.active_object
        stone.scale = (1.0, 1.0, 0.7)
        stone.data.materials.append(mat_stone)

    # Firewood logs (teepee/cross)
    for angle_deg in [0, 60, 120]:
        rad = math.radians(angle_deg)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.6, vertices=6, location=(0, 0, 0.12), rotation=(0, math.radians(45), rad))
        log = bpy.context.active_object
        log.data.materials.append(mat_log)

    # Stylized Fire Flame Peak
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.45, vertices=6, location=(0, 0, 0.28))
    flame = bpy.context.active_object
    flame.name = "FlameMesh"
    flame.data.materials.append(mat_fire)

    export_glb("campfire.glb")

# -------------------------------------------------------------
# 6. Wooden Storage Crate
# -------------------------------------------------------------
def build_crate():
    reset_scene()
    mat_plank = create_material("CrateWood", (0.60, 0.44, 0.24, 1.0), roughness=0.85)
    mat_iron_strap = create_material("CrateIron", (0.25, 0.25, 0.28, 1.0), roughness=0.4, metallic=0.8)

    # Box body
    bpy.ops.mesh.primitive_cube_add(size=0.9, location=(0, 0, 0.45))
    box = bpy.context.active_object
    box.name = "CrateBody"
    box.data.materials.append(mat_plank)

    # Corner metal brackets
    bpy.ops.mesh.primitive_cube_add(size=0.92, location=(0, 0, 0.45))
    bracket = bpy.context.active_object
    bracket.name = "CrateBrackets"
    bracket.scale = (1.02, 1.02, 0.1)
    bracket.data.materials.append(mat_iron_strap)

    export_glb("crate.glb")

# -------------------------------------------------------------
# 7. Low-Poly Medieval Citizen / Peasant
# -------------------------------------------------------------
def build_citizen():
    reset_scene()
    mat_skin = create_material("PeasantSkin", (0.85, 0.70, 0.58, 1.0), roughness=0.8)
    mat_tunic = create_material("PeasantTunic", (0.28, 0.45, 0.35, 1.0), roughness=0.85)
    mat_pants = create_material("PeasantPants", (0.35, 0.28, 0.20, 1.0), roughness=0.9)
    mat_hat = create_material("PeasantHat", (0.50, 0.38, 0.22, 1.0), roughness=0.92)

    # Torso (Tunic)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.05))
    torso = bpy.context.active_object
    torso.name = "Torso"
    torso.scale = (0.42, 0.25, 0.55)
    torso.data.materials.append(mat_tunic)

    # Head
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 0, 1.5))
    head = bpy.context.active_object
    head.name = "Head"
    head.data.materials.append(mat_skin)

    # Brimmed Hat
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.08, vertices=8, location=(0, 0, 1.68))
    hat = bpy.context.active_object
    hat.name = "Hat"
    hat.data.materials.append(mat_hat)

    # Left Leg
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0, 0.4))
    lleg = bpy.context.active_object
    lleg.scale = (0.14, 0.18, 0.75)
    lleg.data.materials.append(mat_pants)

    # Right Leg
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.12, 0, 0.4))
    rleg = bpy.context.active_object
    rleg.scale = (0.14, 0.18, 0.75)
    rleg.data.materials.append(mat_pants)

    # Arms
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.28, 0, 1.05))
    larm = bpy.context.active_object
    larm.scale = (0.1, 0.12, 0.5)
    larm.data.materials.append(mat_tunic)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, 0, 1.05))
    rarm = bpy.context.active_object
    rarm.scale = (0.1, 0.12, 0.5)
    rarm.data.materials.append(mat_tunic)

    export_glb("citizen.glb")

# -------------------------------------------------------------
# 8. Smelting Furnace Workstation
# -------------------------------------------------------------
def build_furnace():
    reset_scene()
    mat_stone = create_material("FurnaceStone", (0.35, 0.35, 0.37, 1.0), roughness=0.9)
    mat_hearth = create_material("FurnaceFire", (1.0, 0.35, 0.05, 1.0), roughness=0.2)
    bsdf = mat_hearth.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.3, 0.02, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 4.0
    mat_iron = create_material("FurnaceGrate", (0.2, 0.2, 0.2, 1.0), roughness=0.5, metallic=0.9)

    # Base stone body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    base = bpy.context.active_object
    base.name = "FurnaceBase"
    base.scale = (0.9, 0.9, 1.0)
    base.data.materials.append(mat_stone)

    # Hearth opening / interior fire
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.42, 0.35))
    fire = bpy.context.active_object
    fire.name = "HearthFire"
    fire.scale = (0.45, 0.2, 0.35)
    fire.data.materials.append(mat_hearth)

    # Iron Grate bars
    for i in [-0.15, 0.0, 0.15]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.35, vertices=6, location=(i, -0.45, 0.35))
        bar = bpy.context.active_object
        bar.data.materials.append(mat_iron)

    # Chimney stack
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.5, vertices=8, location=(0, 0, 1.25))
    chimney = bpy.context.active_object
    chimney.name = "Chimney"
    chimney.data.materials.append(mat_stone)

    export_glb("furnace.glb")

# -------------------------------------------------------------
# 9. Mine Structural Support Beam
# -------------------------------------------------------------
def build_support_beam():
    reset_scene()
    mat_wood = create_material("BeamWood", (0.32, 0.20, 0.10, 1.0), roughness=0.92)
    mat_bracket = create_material("IronBracket", (0.25, 0.25, 0.27, 1.0), roughness=0.4, metallic=0.8)

    # Vertical post
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.0))
    post = bpy.context.active_object
    post.name = "SupportPost"
    post.scale = (0.22, 0.22, 2.0)
    post.data.materials.append(mat_wood)

    # Top crossbeam
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.95))
    cross = bpy.context.active_object
    cross.name = "TopCrossbeam"
    cross.scale = (0.9, 0.25, 0.18)
    cross.data.materials.append(mat_wood)

    # Diagonal braces
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.25, 0, 1.65), rotation=(0, math.radians(45), 0))
    brace1 = bpy.context.active_object
    brace1.scale = (0.1, 0.18, 0.4)
    brace1.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.25, 0, 1.65), rotation=(0, math.radians(-45), 0))
    brace2 = bpy.context.active_object
    brace2.scale = (0.1, 0.18, 0.4)
    brace2.data.materials.append(mat_wood)

    # Iron bracket bands
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.85))
    bracket = bpy.context.active_object
    bracket.scale = (0.26, 0.26, 0.08)
    bracket.data.materials.append(mat_bracket)

    export_glb("support_beam.glb")

# -------------------------------------------------------------
# 10. Bandit Raider Entity
# -------------------------------------------------------------
def build_bandit():
    reset_scene()
    mat_tunic = create_material("BanditTunic", (0.25, 0.12, 0.12, 1.0), roughness=0.85)
    mat_pants = create_material("BanditPants", (0.18, 0.16, 0.15, 1.0), roughness=0.88)
    mat_hood = create_material("BanditHood", (0.15, 0.10, 0.10, 1.0), roughness=0.9)
    mat_steel = create_material("BanditSteel", (0.6, 0.6, 0.65, 1.0), roughness=0.3, metallic=0.85)

    # Torso
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.05))
    torso = bpy.context.active_object
    torso.scale = (0.44, 0.26, 0.55)
    torso.data.materials.append(mat_tunic)

    # Head & Hood
    bpy.ops.mesh.primitive_cube_add(size=0.34, location=(0, 0, 1.5))
    head = bpy.context.active_object
    head.data.materials.append(mat_hood)

    # Spiked helmet tip
    bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.15, vertices=6, location=(0, 0, 1.72))
    spike = bpy.context.active_object
    spike.data.materials.append(mat_steel)

    # Left & Right Legs
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0, 0.4))
    lleg = bpy.context.active_object
    lleg.scale = (0.14, 0.18, 0.75)
    lleg.data.materials.append(mat_pants)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.12, 0, 0.4))
    rleg = bpy.context.active_object
    rleg.scale = (0.14, 0.18, 0.75)
    rleg.data.materials.append(mat_pants)

    # Weapon in hand (Dagger)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.32, -0.2, 0.85), rotation=(math.radians(35), 0, 0))
    dagger = bpy.context.active_object
    dagger.scale = (0.04, 0.04, 0.4)
    dagger.data.materials.append(mat_steel)

    export_glb("bandit.glb")

# -------------------------------------------------------------
# 11. Feudal Merchant Trade Caravan Cart
# -------------------------------------------------------------
def build_caravan_cart():
    reset_scene()
    mat_wood = create_material("CartWood", (0.38, 0.24, 0.12, 1.0), roughness=0.88)
    mat_iron = create_material("CartIron", (0.28, 0.28, 0.30, 1.0), roughness=0.4, metallic=0.85)
    mat_canvas = create_material("CartCanvas", (0.85, 0.82, 0.74, 1.0), roughness=0.95)

    # Cart chassis base
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.6))
    chassis = bpy.context.active_object
    chassis.name = "CartBed"
    chassis.scale = (1.4, 2.2, 0.15)
    chassis.data.materials.append(mat_wood)

    # Axle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.8, vertices=8, location=(0, 0, 0.45), rotation=(0, math.radians(90), 0))
    axle = bpy.context.active_object
    axle.data.materials.append(mat_iron)

    # Left & Right Spoked Wooden Wheels
    for x_side in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.08, vertices=12, location=(x_side, 0, 0.45), rotation=(0, math.radians(90), 0))
        wheel = bpy.context.active_object
        wheel.data.materials.append(mat_wood)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.46, depth=0.06, vertices=12, location=(x_side, 0, 0.45), rotation=(0, math.radians(90), 0))
        rim = bpy.context.active_object
        rim.data.materials.append(mat_iron)

    # Front Hitch Shafts
    for x_hitch in [-0.4, 0.4]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_hitch, 1.6, 0.55))
        shaft = bpy.context.active_object
        shaft.scale = (0.08, 1.4, 0.08)
        shaft.data.materials.append(mat_wood)

    # Arched Canvas Canopy Cover
    bpy.ops.mesh.primitive_cylinder_add(radius=0.72, depth=2.0, vertices=12, location=(0, 0, 1.2), rotation=(math.radians(90), 0, 0))
    canopy = bpy.context.active_object
    canopy.name = "CanvasCanopy"
    canopy.scale = (1.0, 1.0, 0.75)
    canopy.data.materials.append(mat_canvas)

    export_glb("caravan_cart.glb")

# -------------------------------------------------------------
# 12. Hunting Bow
# -------------------------------------------------------------
def build_bow():
    reset_scene()
    mat_wood = create_material("BowWood", (0.35, 0.20, 0.08, 1.0), roughness=0.7)
    mat_grip = create_material("BowGrip", (0.20, 0.12, 0.05, 1.0), roughness=0.6)
    mat_string = create_material("BowString", (0.9, 0.9, 0.85, 1.0), roughness=0.4)

    # Central grip handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.18, vertices=8, location=(0, 0, 0))
    grip = bpy.context.active_object
    grip.name = "BowGrip"
    grip.data.materials.append(mat_grip)

    # Upper curved limb (3 angled segments)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.35, vertices=8, location=(0, 0.06, 0.24), rotation=(math.radians(20), 0, 0))
    u1 = bpy.context.active_object
    u1.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, vertices=8, location=(0, 0.16, 0.52), rotation=(math.radians(40), 0, 0))
    u2 = bpy.context.active_object
    u2.data.materials.append(mat_wood)

    # Lower curved limb (3 angled segments)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.35, vertices=8, location=(0, 0.06, -0.24), rotation=(math.radians(-20), 0, 0))
    l1 = bpy.context.active_object
    l1.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.35, vertices=8, location=(0, 0.16, -0.52), rotation=(math.radians(-40), 0, 0))
    l2 = bpy.context.active_object
    l2.data.materials.append(mat_wood)

    # Taut Bowstring (connecting upper tip and lower tip)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=1.35, vertices=6, location=(0, 0.26, 0))
    bstring = bpy.context.active_object
    bstring.name = "BowString"
    bstring.data.materials.append(mat_string)

    export_glb("hunting_bow.glb")

# -------------------------------------------------------------
# 13. Bodkin Arrow
# -------------------------------------------------------------
def build_arrow():
    reset_scene()
    mat_wood = create_material("ArrowWood", (0.55, 0.40, 0.22, 1.0), roughness=0.6)
    mat_iron = create_material("ArrowIron", (0.2, 0.22, 0.25, 1.0), metallic=0.9, roughness=0.3)
    mat_feather = create_material("ArrowFletch", (0.85, 0.82, 0.75, 1.0), roughness=0.5)

    # Arrow Shaft (0.8m long)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.8, vertices=8, location=(0, 0, 0))
    shaft = bpy.context.active_object
    shaft.name = "ArrowShaft"
    shaft.data.materials.append(mat_wood)

    # Iron Bodkin Point (tapered cone)
    bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.0, depth=0.1, vertices=6, location=(0, 0, 0.44))
    head = bpy.context.active_object
    head.name = "ArrowHead"
    head.data.materials.append(mat_iron)

    # 3 Fletching Feathers (120 degrees apart)
    for angle in [0, 120, 240]:
        rad = math.radians(angle)
        fx = math.cos(rad) * 0.025
        fy = math.sin(rad) * 0.025
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, fy, -0.32), rotation=(0, 0, rad))
        fletch = bpy.context.active_object
        fletch.scale = (0.004, 0.04, 0.12)
        fletch.data.materials.append(mat_feather)

    export_glb("arrow.glb")

# -------------------------------------------------------------
# 14. Watchtower Workstation / Defensive Structure
# -------------------------------------------------------------
def build_watchtower():
    reset_scene()
    mat_post = create_material("TowerPost", (0.32, 0.18, 0.08, 1.0), roughness=0.8)
    mat_plank = create_material("TowerPlank", (0.42, 0.26, 0.12, 1.0), roughness=0.7)
    mat_roof = create_material("TowerRoof", (0.28, 0.15, 0.06, 1.0), roughness=0.85)

    # 4 Main Vertical Posts (4.5m tall)
    post_coords = [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)]
    for x, y in post_coords:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=4.5, vertices=8, location=(x, y, 2.25))
        post = bpy.context.active_object
        post.data.materials.append(mat_post)

    # Elevated Timber Floor Platform (at Z = 3.5m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 3.5))
    floor = bpy.context.active_object
    floor.name = "PlatformFloor"
    floor.scale = (2.4, 2.4, 0.15)
    floor.data.materials.append(mat_plank)

    # Platform Guard Railing / Crenellations (Z = 4.0m)
    rail_configs = [
        (0, 1.15, 2.4, 0.08),
        (0, -1.15, 2.4, 0.08),
        (-1.15, 0, 0.08, 2.4),
        (1.15, 0, 0.08, 2.4)
    ]
    for rx, ry, sx, sy in rail_configs:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, ry, 4.0))
        rail = bpy.context.active_object
        rail.scale = (sx, sy, 0.8)
        rail.data.materials.append(mat_plank)

    # Access Ladder on Back Face
    for lz in [0.6, 1.2, 1.8, 2.4, 3.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -1.0, lz))
        rung = bpy.context.active_object
        rung.scale = (0.6, 0.08, 0.05)
        rung.data.materials.append(mat_post)

    # Roof Canopy (Pyramid at Z = 5.2m)
    bpy.ops.mesh.primitive_cone_add(radius1=1.6, radius2=0.0, depth=1.2, vertices=4, location=(0, 0, 5.2), rotation=(0, 0, math.radians(45)))
    roof = bpy.context.active_object
    roof.name = "TowerRoof"
    roof.data.materials.append(mat_roof)

    export_glb("watchtower.glb")

# -------------------------------------------------------------
# 15. Enchanter's Table Workstation
# -------------------------------------------------------------
def build_enchanter_table():
    reset_scene()
    mat_wood = create_material("TableWood", (0.22, 0.12, 0.06, 1.0), roughness=0.6)
    mat_cloth = create_material("TableCloth", (0.15, 0.10, 0.35, 1.0), roughness=0.8)
    mat_crystal = create_material("ArcaneCrystal", (0.75, 0.25, 1.0, 1.0), roughness=0.1)
    bsdf = mat_crystal.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Emission Color"].default_value = (0.8, 0.3, 1.0, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 2.5
    mat_page = create_material("TomePage", (0.92, 0.88, 0.78, 1.0), roughness=0.9)

    # Table Top
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.75))
    top = bpy.context.active_object
    top.scale = (1.4, 1.0, 0.12)
    top.data.materials.append(mat_wood)

    # 4 Legs
    for x, y in [(-0.55, -0.38), (0.55, -0.38), (-0.55, 0.38), (0.55, 0.38)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 0.35))
        leg = bpy.context.active_object
        leg.scale = (0.12, 0.12, 0.7)
        leg.data.materials.append(mat_wood)

    # Cloth runner over table
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.82))
    cloth = bpy.context.active_object
    cloth.scale = (0.7, 1.02, 0.02)
    cloth.data.materials.append(mat_cloth)

    # Open Tome on left
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.35, 0, 0.88), rotation=(0, 0, math.radians(10)))
    book = bpy.context.active_object
    book.scale = (0.42, 0.32, 0.05)
    book.data.materials.append(mat_page)

    # Floating Arcane Crystal on right
    bpy.ops.mesh.primitive_cone_add(radius1=0.12, radius2=0.0, depth=0.35, location=(0.35, 0, 1.05), rotation=(math.radians(15), 0, 0))
    crystal = bpy.context.active_object
    crystal.name = "FloatingCrystal"
    crystal.data.materials.append(mat_crystal)

    export_glb("enchanter_table.glb")

# -------------------------------------------------------------
# 16. Bandit Warlord (Raid Boss)
# -------------------------------------------------------------
def build_bandit_warlord():
    reset_scene()
    mat_armor = create_material("WarlordPlate", (0.15, 0.15, 0.17, 1.0), metallic=0.9, roughness=0.3)
    mat_gold = create_material("WarlordGold", (0.9, 0.75, 0.15, 1.0), metallic=0.95, roughness=0.2)
    mat_cape = create_material("WarlordCape", (0.55, 0.08, 0.08, 1.0), roughness=0.8)
    mat_axe = create_material("WarlordAxe", (0.25, 0.25, 0.28, 1.0), metallic=0.85, roughness=0.35)

    # Heavy Armored Torso (scaled up)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.2))
    torso = bpy.context.active_object
    torso.scale = (0.55, 0.32, 0.65)
    torso.data.materials.append(mat_armor)

    # Gold Trim Belt
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.9))
    belt = bpy.context.active_object
    belt.scale = (0.57, 0.34, 0.1)
    belt.data.materials.append(mat_gold)

    # Armored Head & Horned Helmet
    bpy.ops.mesh.primitive_cube_add(size=0.36, location=(0, 0, 1.68))
    head = bpy.context.active_object
    head.data.materials.append(mat_armor)

    # Left & Right Helmet Horns
    bpy.ops.mesh.primitive_cone_add(radius1=0.06, radius2=0.0, depth=0.28, location=(-0.24, 0, 1.85), rotation=(0, math.radians(-35), 0))
    lhorn = bpy.context.active_object
    lhorn.data.materials.append(mat_gold)

    bpy.ops.mesh.primitive_cone_add(radius1=0.06, radius2=0.0, depth=0.28, location=(0.24, 0, 1.85), rotation=(0, math.radians(35), 0))
    rhorn = bpy.context.active_object
    rhorn.data.materials.append(mat_gold)

    # Crimson Battle Cape
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.22, 1.05))
    cape = bpy.context.active_object
    cape.scale = (0.52, 0.06, 0.9)
    cape.data.materials.append(mat_cape)

    # Heavy Legs
    for x in [-0.16, 0.16]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, 0, 0.45))
        leg = bpy.context.active_object
        leg.scale = (0.18, 0.22, 0.85)
        leg.data.materials.append(mat_armor)

    # Massive Battleaxe
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.6, vertices=8, location=(0.48, -0.1, 1.1), rotation=(math.radians(20), 0, 0))
    axe_haft = bpy.context.active_object
    axe_haft.data.materials.append(mat_armor)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.48, -0.15, 1.65), rotation=(math.radians(20), 0, 0))
    axe_blade = bpy.context.active_object
    axe_blade.scale = (0.04, 0.45, 0.35)
    axe_blade.data.materials.append(mat_axe)

    export_glb("bandit_warlord.glb")

# -------------------------------------------------------------
# 17. Enchanted Runestone Tablet
# -------------------------------------------------------------
def build_runestone():
    reset_scene()
    mat_slate = create_material("RuneSlate", (0.18, 0.18, 0.20, 1.0), roughness=0.6)
    mat_rune = create_material("RuneGlow", (1.0, 0.82, 0.25, 1.0), roughness=0.2)
    bsdf = mat_rune.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.85, 0.3, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0

    # Polished Slate Tablet (0.35m x 0.45m x 0.06m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.03))
    tablet = bpy.context.active_object
    tablet.scale = (0.35, 0.45, 0.06)
    tablet.data.materials.append(mat_slate)

    # Glowing Rune Inscription on top
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.07, vertices=8, location=(0, 0, 0.035))
    rune = bpy.context.active_object
    rune.data.materials.append(mat_rune)

    export_glb("runestone.glb")

if __name__ == "__main__":
    print("[BLENDER SCRIPT] Starting procedural 3D medieval model generation...")
    build_pickaxe()
    build_axe()
    build_sword()
    build_workbench()
    build_campfire()
    build_crate()
    build_citizen()
    build_furnace()
    build_support_beam()
    build_bandit()
    build_caravan_cart()
    build_bow()
    build_arrow()
    build_watchtower()
    build_enchanter_table()
    build_bandit_warlord()
    build_runestone()
    print("[BLENDER SCRIPT] All models generated successfully!")


