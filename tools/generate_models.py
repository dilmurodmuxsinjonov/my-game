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

# -------------------------------------------------------------
# 18. Create-Style Kinetic Windmill & Milling Tower
# -------------------------------------------------------------
def build_windmill():
    reset_scene()
    mat_stone = create_material("MillStone", (0.35, 0.35, 0.36, 1.0), roughness=0.9)
    mat_wood = create_material("MillWood", (0.42, 0.26, 0.14, 1.0), roughness=0.8)
    mat_roof = create_material("MillRoof", (0.55, 0.45, 0.30, 1.0), roughness=0.95)
    mat_sail = create_material("MillSail", (0.88, 0.86, 0.80, 1.0), roughness=0.9)
    mat_iron = create_material("MillIron", (0.25, 0.25, 0.27, 1.0), roughness=0.4, metallic=0.9)

    # 1. Stone Round Tower Base (Height 2.8m, Radius 1.1m)
    bpy.ops.mesh.primitive_cylinder_add(radius=1.1, depth=2.8, vertices=12, location=(0, 0, 1.4))
    tower = bpy.context.active_object
    tower.data.materials.append(mat_stone)

    # 2. Upper Timber Machinery Loft (Height 1.2m, Radius 0.95m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.95, depth=1.2, vertices=10, location=(0, 0, 3.4))
    loft = bpy.context.active_object
    loft.data.materials.append(mat_wood)

    # 3. Conical Thatched / Shingle Roof
    bpy.ops.mesh.primitive_cone_add(radius1=1.2, depth=1.1, vertices=12, location=(0, 0, 4.55))
    roof = bpy.context.active_object
    roof.data.materials.append(mat_roof)

    # 4. Central Horizontal Rotor Hub
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.45, vertices=8, location=(0, 1.05, 3.4), rotation=(math.radians(90), 0, 0))
    hub = bpy.context.active_object
    hub.data.materials.append(mat_iron)

    # 5. Four Kinetic Lattice Sails (Cross configuration, 1.8m span)
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        # Wooden sail spar beam
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 1.2, 3.4))
        spar = bpy.context.active_object
        spar.scale = (0.06, 0.04, 1.8)
        spar.rotation_euler = (0, rad, 0)
        spar.data.materials.append(mat_wood)

        # Cloth wind-catching sail vane
        sx = 0.45 * math.cos(rad)
        sz = 0.45 * math.sin(rad)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(sx, 1.22, 3.4 + sz))
        sail = bpy.context.active_object
        sail.scale = (0.45, 0.02, 0.75)
        sail.rotation_euler = (0, rad, 0)
        sail.data.materials.append(mat_sail)

    export_glb("windmill.glb")

# -------------------------------------------------------------
# 19. Farmer's Delight Cast Iron Cooking Pot & Hearth
# -------------------------------------------------------------
def build_cooking_pot():
    reset_scene()
    mat_iron = create_material("PotIron", (0.18, 0.18, 0.20, 1.0), roughness=0.5, metallic=0.8)
    mat_ember = create_material("PotEmber", (0.95, 0.45, 0.1, 1.0), roughness=0.3)
    bsdf_e = mat_ember.node_tree.nodes.get("Principled BSDF")
    if bsdf_e:
        bsdf_e.inputs["Emission Color"].default_value = (1.0, 0.4, 0.05, 1.0)
        bsdf_e.inputs["Emission Strength"].default_value = 2.5
    mat_stew = create_material("StewBroth", (0.68, 0.38, 0.15, 1.0), roughness=0.2)
    mat_wood = create_material("LadleWood", (0.48, 0.32, 0.18, 1.0), roughness=0.8)

    # 1. Hot glowing embers base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.08, vertices=8, location=(0, 0, 0.04))
    embers = bpy.context.active_object
    embers.data.materials.append(mat_ember)

    # 2. Three Iron Tripod Legs
    for i in range(3):
        angle = math.radians(i * 120.0)
        lx = 0.32 * math.cos(angle)
        ly = 0.32 * math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.4, vertices=6, location=(lx, ly, 0.2), rotation=(math.radians(15) * math.sin(angle), -math.radians(15) * math.cos(angle), 0))
        leg = bpy.context.active_object
        leg.data.materials.append(mat_iron)

    # 3. Main Cauldron Body (Round bottom pot)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.36, vertices=12, location=(0, 0, 0.38))
    cauldron = bpy.context.active_object
    cauldron.data.materials.append(mat_iron)

    # 4. Pot Rim & Handles
    bpy.ops.mesh.primitive_torus_add(major_radius=0.39, minor_radius=0.03, location=(0, 0, 0.56))
    rim = bpy.context.active_object
    rim.data.materials.append(mat_iron)

    for side in [-0.42, 0.42]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.015, location=(side, 0, 0.48), rotation=(0, math.radians(90), 0))
        handle = bpy.context.active_object
        handle.data.materials.append(mat_iron)

    # 5. Hearty Simmering Stew Surface
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.02, vertices=10, location=(0, 0, 0.50))
    stew = bpy.context.active_object
    stew.data.materials.append(mat_stew)

    # 6. Wooden Stew Stirring Ladle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.55, vertices=6, location=(0.18, 0.12, 0.62), rotation=(math.radians(-25), math.radians(20), 0))
    ladle = bpy.context.active_object
    ladle.data.materials.append(mat_wood)

    export_glb("cooking_pot.glb")

# -------------------------------------------------------------
# 20. Royal Feudal War Horn (Colony Alarm & Rally Heraldry)
# -------------------------------------------------------------
def build_war_horn():
    reset_scene()
    mat_horn = create_material("HornBone", (0.75, 0.70, 0.60, 1.0), roughness=0.6)
    mat_gold = create_material("HornGold", (0.95, 0.78, 0.25, 1.0), roughness=0.3, metallic=0.9)
    mat_strap = create_material("HornLeather", (0.35, 0.20, 0.12, 1.0), roughness=0.9)

    # Segmented curved horn body (tapering from 0.08m bell down to 0.025m mouthpiece)
    segments = 6
    for i in range(segments):
        t = i / float(segments)
        radius = 0.08 * (1.0 - t * 0.7)
        angle = math.radians(t * 55.0)
        hx = t * 0.38
        hy = math.sin(angle) * 0.14
        hz = 0.05 + (1.0 - math.cos(angle)) * 0.08

        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=0.08, vertices=8, location=(hx, hy, hz), rotation=(0, angle, 0))
        seg = bpy.context.active_object
        seg.data.materials.append(mat_horn)

    # Gilded brass bell rim at wide opening
    bpy.ops.mesh.primitive_torus_add(major_radius=0.085, minor_radius=0.015, location=(0, 0, 0.05), rotation=(0, 0, 0))
    bell = bpy.context.active_object
    bell.data.materials.append(mat_gold)

    # Brass mouthpiece at narrow end
    t_end = 1.0
    end_angle = math.radians(55.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.06, vertices=8, location=(0.38, math.sin(end_angle)*0.14, 0.05 + (1.0 - math.cos(end_angle))*0.08), rotation=(0, end_angle, 0))
    mouthpiece = bpy.context.active_object
    mouthpiece.data.materials.append(mat_gold)

    # Decorative leather hanging cord
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.01, location=(0.20, 0.08, 0.14), rotation=(math.radians(45), 0, 0))
    cord = bpy.context.active_object
    cord.data.materials.append(mat_strap)

    export_glb("war_horn.glb")

# -------------------------------------------------------------
# 21. Hauler Wheelbarrow (Logistical Transport Hand-Cart)
# -------------------------------------------------------------
def build_wheelbarrow():
    reset_scene()
    mat_wood = create_material("BarrowWood", (0.35, 0.22, 0.12, 1.0), roughness=0.7)
    mat_plank = create_material("BarrowPlank", (0.28, 0.17, 0.09, 1.0), roughness=0.8)
    mat_iron = create_material("BarrowIron", (0.18, 0.18, 0.20, 1.0), roughness=0.4, metallic=0.85)
    mat_cargo = create_material("BarrowCargo", (0.75, 0.68, 0.42, 1.0), roughness=0.9)

    for side in [-0.28, 0.28]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.7, 0.05, 0.32), rotation=(math.radians(8), 0, 0))
        shaft = bpy.context.active_object
        shaft.scale = (0.07, 1.45, 0.07)
        shaft.data.materials.append(mat_wood)

    for side in [-0.28, 0.28]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.18, vertices=8, location=(side * 0.95, -0.68, 0.45), rotation=(0, math.radians(90), 0))
        grip = bpy.context.active_object
        grip.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.07, vertices=12, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    wheel = bpy.context.active_object
    wheel.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.24, minor_radius=0.02, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    tire = bpy.context.active_object
    tire.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.46, vertices=8, location=(0, 0.72, 0.24), rotation=(0, math.radians(90), 0))
    axle = bpy.context.active_object
    axle.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.12, 0.38))
    bed = bpy.context.active_object
    bed.scale = (0.64, 0.78, 0.05)
    bed.data.materials.append(mat_plank)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.50, 0.52), rotation=(math.radians(-22), 0, 0))
    f_wall = bpy.context.active_object
    f_wall.scale = (0.64, 0.05, 0.32)
    f_wall.data.materials.append(mat_plank)

    for side in [-0.32, 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, 0.12, 0.50), rotation=(0, math.radians(side * -35), 0))
        sideboard = bpy.context.active_object
        sideboard.scale = (0.05, 0.76, 0.28)
        sideboard.data.materials.append(mat_plank)

    for side in [-0.25, 0.25]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side, -0.28, 0.16))
        leg = bpy.context.active_object
        leg.scale = (0.06, 0.06, 0.32)
        leg.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.12, 0.46))
    cargo = bpy.context.active_object
    cargo.scale = (0.52, 0.62, 0.18)
    cargo.data.materials.append(mat_cargo)

    export_glb("wheelbarrow.glb")

# -------------------------------------------------------------
# 22. Architect's Drafting Desk (Colony Blueprint Station)
# -------------------------------------------------------------
def build_architect_desk():
    reset_scene()
    mat_wood = create_material("DeskOak", (0.28, 0.18, 0.10, 1.0), roughness=0.65)
    mat_tabletop = create_material("DeskTop", (0.34, 0.22, 0.13, 1.0), roughness=0.6)
    mat_parchment = create_material("BlueprintParchment", (0.86, 0.82, 0.72, 1.0), roughness=0.9)
    mat_ink = create_material("BlueprintInk", (0.12, 0.55, 0.85, 1.0), roughness=0.5)
    mat_brass = create_material("DeskBrass", (0.85, 0.72, 0.25, 1.0), roughness=0.3, metallic=0.85)
    mat_stone = create_material("InkpotStone", (0.15, 0.15, 0.17, 1.0), roughness=0.7)
    mat_feather = create_material("QuillFeather", (0.95, 0.95, 0.92, 1.0), roughness=0.8)

    for x, y in [(-0.65, -0.45), (0.65, -0.45), (-0.65, 0.45), (0.65, 0.45)]:
        lz = 0.36 if y < 0 else 0.42
        lheight = 0.72 if y < 0 else 0.84
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, lz))
        leg = bpy.context.active_object
        leg.scale = (0.11, 0.11, lheight)
        leg.data.materials.append(mat_wood)

    for y in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y, 0.22))
        brace = bpy.context.active_object
        brace.scale = (1.20, 0.06, 0.08)
        brace.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.84), rotation=(math.radians(10), 0, 0))
    top = bpy.context.active_object
    top.scale = (1.55, 1.12, 0.09)
    top.data.materials.append(mat_tabletop)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.54, 0.79), rotation=(math.radians(10), 0, 0))
    lip = bpy.context.active_object
    lip.scale = (1.55, 0.06, 0.06)
    lip.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0.02, 0.895), rotation=(math.radians(10), 0, 0))
    parchment = bpy.context.active_object
    parchment.scale = (1.05, 0.78, 0.015)
    parchment.data.materials.append(mat_parchment)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.12, 0.02, 0.905), rotation=(math.radians(10), 0, 0))
    plan_lines = bpy.context.active_object
    plan_lines.scale = (0.85, 0.58, 0.01)
    plan_lines.data.materials.append(mat_ink)

    for roffset in [0.0, 0.07]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.72, vertices=10, location=(0.58, 0.22 + roffset, 0.94), rotation=(0, math.radians(90), math.radians(15)))
        scroll = bpy.context.active_object
        scroll.data.materials.append(mat_parchment)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.28, vertices=6, location=(0.34, -0.15, 0.89), rotation=(math.radians(10), math.radians(25), 0))
    leg1 = bpy.context.active_object
    leg1.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.28, vertices=6, location=(0.42, -0.18, 0.89), rotation=(math.radians(10), math.radians(-25), 0))
    leg2 = bpy.context.active_object
    leg2.data.materials.append(mat_brass)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.09, vertices=8, location=(0.58, -0.32, 0.86), rotation=(math.radians(10), 0, 0))
    inkpot = bpy.context.active_object
    inkpot.data.materials.append(mat_stone)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.35, vertices=6, location=(0.60, -0.36, 0.98), rotation=(math.radians(-35), math.radians(20), 0))
    quill = bpy.context.active_object
    quill.data.materials.append(mat_feather)

    export_glb("architect_desk.glb")

# -------------------------------------------------------------
# 23. Tinkers' Blacksmith Anvil & Quenching Tank
# -------------------------------------------------------------
def build_anvil():
    reset_scene()
    mat_iron = create_material("AnvilIron", (0.16, 0.17, 0.19, 1.0), roughness=0.35, metallic=0.9)
    mat_stump = create_material("AnvilStump", (0.26, 0.16, 0.08, 1.0), roughness=0.8)
    mat_band = create_material("IronBand", (0.12, 0.12, 0.14, 1.0), roughness=0.4, metallic=0.8)
    mat_water = create_material("QuenchWater", (0.15, 0.35, 0.65, 0.8), roughness=0.1)
    mat_wood = create_material("TroughWood", (0.32, 0.20, 0.10, 1.0), roughness=0.7)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.48, vertices=10, location=(0, 0, 0.24))
    stump = bpy.context.active_object
    stump.data.materials.append(mat_stump)

    for bz in [0.10, 0.38]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.43, minor_radius=0.02, location=(0, 0, bz))
        band = bpy.context.active_object
        band.data.materials.append(mat_band)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.52))
    base = bpy.context.active_object
    base.scale = (0.58, 0.36, 0.08)
    base.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.62))
    waist = bpy.context.active_object
    waist.scale = (0.34, 0.22, 0.14)
    waist.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.04, 0, 0.74))
    face = bpy.context.active_object
    face.scale = (0.50, 0.26, 0.12)
    face.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cone_add(radius1=0.12, radius2=0.02, depth=0.32, vertices=8, location=(-0.34, 0, 0.74), rotation=(0, math.radians(-90), 0))
    horn = bpy.context.active_object
    horn.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.36, 0, 0.70))
    heel = bpy.context.active_object
    heel.scale = (0.16, 0.22, 0.08)
    heel.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.38, 0.22))
    trough = bpy.context.active_object
    trough.scale = (0.32, 0.44, 0.44)
    trough.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.58, 0.38, 0.38))
    water = bpy.context.active_object
    water.scale = (0.28, 0.40, 0.04)
    water.data.materials.append(mat_water)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.36, vertices=6, location=(0.06, -0.04, 0.82), rotation=(0, 0, math.radians(25)))
    handle = bpy.context.active_object
    handle.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.18, 0.02, 0.82))
    h_head = bpy.context.active_object
    h_head.scale = (0.08, 0.06, 0.06)
    h_head.data.materials.append(mat_iron)

    export_glb("anvil.glb")

# -------------------------------------------------------------
# 24. TerraFirmaCraft Timber Smoke Rack & Embers
# -------------------------------------------------------------
def build_smoke_rack():
    reset_scene()
    mat_timber = create_material("RackTimber", (0.30, 0.18, 0.09, 1.0), roughness=0.75)
    mat_meat = create_material("SmokedMeat", (0.45, 0.15, 0.10, 1.0), roughness=0.6)
    mat_iron = create_material("PotIron", (0.15, 0.15, 0.16, 1.0), roughness=0.5, metallic=0.85)
    mat_embers = create_material("HotEmbers", (1.0, 0.3, 0.05, 1.0), roughness=0.3)
    bsdf = mat_embers.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.35, 0.05, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0

    for side in [-0.65, 0.65]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.65, vertices=6, location=(side, -0.32, 0.78), rotation=(math.radians(22), 0, 0))
        leg1 = bpy.context.active_object
        leg1.data.materials.append(mat_timber)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.65, vertices=6, location=(side, 0.32, 0.78), rotation=(math.radians(-22), 0, 0))
        leg2 = bpy.context.active_object
        leg2.data.materials.append(mat_timber)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.65, vertices=6, location=(side, 0, 0.52), rotation=(math.radians(90), 0, 0))
        tie = bpy.context.active_object
        tie.data.materials.append(mat_timber)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=1.55, vertices=8, location=(0, 0, 1.48), rotation=(0, math.radians(90), 0))
    top_beam = bpy.context.active_object
    top_beam.data.materials.append(mat_timber)

    for i, hx in enumerate([-0.42, -0.15, 0.12, 0.38]):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.008, depth=0.24, vertices=4, location=(hx, 0, 1.34))
        twine = bpy.context.active_object
        twine.data.materials.append(mat_timber)

        if i % 2 == 0:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, 0, 1.12))
            meat = bpy.context.active_object
            meat.scale = (0.11, 0.16, 0.28)
            meat.data.materials.append(mat_meat)
        else:
            for sz in [1.18, 1.05]:
                bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.10, vertices=8, location=(hx, 0, sz))
                saus = bpy.context.active_object
                saus.data.materials.append(mat_meat)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.18, vertices=8, location=(0, 0, 0.09))
    pot = bpy.context.active_object
    pot.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.24, depth=0.06, vertices=8, location=(0, 0, 0.16))
    coals = bpy.context.active_object
    coals.data.materials.append(mat_embers)

    export_glb("smoke_rack.glb")

# -------------------------------------------------------------
# 25. Kinetic Water Wheel (water_wheel.glb)
# -------------------------------------------------------------
def build_water_wheel():
    reset_scene()
    mat_wood_dark = create_material("DarkTimber", (0.24, 0.15, 0.08, 1.0), roughness=0.8)
    mat_wood_plank = create_material("PlankWood", (0.42, 0.28, 0.16, 1.0), roughness=0.7)
    mat_iron = create_material("BearingIron", (0.18, 0.19, 0.21, 1.0), roughness=0.35, metallic=0.85)
    mat_gear = create_material("BrassCog", (0.55, 0.42, 0.15, 1.0), roughness=0.4, metallic=0.8)

    for side_x in [-0.85, 0.85]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 1.1))
        post = bpy.context.active_object
        post.scale = (0.16, 0.20, 2.2)
        post.data.materials.append(mat_wood_dark)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 0.08))
        sill = bpy.context.active_object
        sill.scale = (0.20, 1.4, 0.16)
        sill.data.materials.append(mat_wood_dark)

        for s_sign in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, s_sign * 0.45, 0.6), rotation=(math.radians(s_sign * -40), 0, 0))
            strut = bpy.context.active_object
            strut.scale = (0.12, 0.12, 1.2)
            strut.data.materials.append(mat_wood_dark)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side_x, 0, 2.22))
        bearing = bpy.context.active_object
        bearing.scale = (0.20, 0.26, 0.12)
        bearing.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=2.1, vertices=10, location=(0, 0, 2.2), rotation=(0, math.radians(90), 0))
    axle = bpy.context.active_object
    axle.data.materials.append(mat_wood_dark)

    for ax_x in [-0.95, -0.65, 0.65, 0.95]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.155, depth=0.12, vertices=10, location=(ax_x, 0, 2.2), rotation=(0, math.radians(90), 0))
        ring = bpy.context.active_object
        ring.data.materials.append(mat_iron)

    for hub_x in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.16, vertices=8, location=(hub_x, 0, 2.2), rotation=(0, math.radians(90), 0))
        hub = bpy.context.active_object
        hub.data.materials.append(mat_wood_dark)

    num_blades = 8
    radius_wheel = 1.7
    for i in range(num_blades):
        angle = (2.0 * math.pi / num_blades) * i
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        for sp_x in [-0.45, 0.45]:
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=(sp_x, (radius_wheel * 0.5) * cos_a, 2.2 + (radius_wheel * 0.5) * sin_a),
                rotation=(-angle, 0, 0)
            )
            spoke = bpy.context.active_object
            spoke.scale = (0.08, radius_wheel * 0.95, 0.08)
            spoke.data.materials.append(mat_wood_dark)

        blade_pos_y = radius_wheel * cos_a
        blade_pos_z = 2.2 + radius_wheel * sin_a
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(0, blade_pos_y, blade_pos_z),
            rotation=(-angle, 0, 0)
        )
        paddle = bpy.context.active_object
        paddle.scale = (0.96, 0.42, 0.06)
        paddle.data.materials.append(mat_wood_plank)

        for rm_x in [-0.45, 0.45]:
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=(rm_x, radius_wheel * 0.92 * cos_a, 2.2 + radius_wheel * 0.92 * sin_a),
                rotation=(-angle, 0, 0)
            )
            rim_seg = bpy.context.active_object
            rim_seg.scale = (0.09, 0.10, 0.65)
            rim_seg.data.materials.append(mat_wood_dark)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.10, vertices=16, location=(1.05, 0, 2.2), rotation=(0, math.radians(90), 0))
    gear = bpy.context.active_object
    gear.data.materials.append(mat_gear)

    for t in range(12):
        t_angle = (2.0 * math.pi / 12) * t
        t_y = 0.48 * math.cos(t_angle)
        t_z = 2.2 + 0.48 * math.sin(t_angle)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(1.05, t_y, t_z), rotation=(-t_angle, 0, 0))
        tooth = bpy.context.active_object
        tooth.scale = (0.10, 0.10, 0.10)
        tooth.data.materials.append(mat_gear)

    export_glb("water_wheel.glb")

# -------------------------------------------------------------
# 26. Mechanical Millstone (millstone.glb)
# -------------------------------------------------------------
def build_millstone():
    reset_scene()
    mat_wood = create_material("MillWood", (0.34, 0.22, 0.12, 1.0), roughness=0.7)
    mat_stone_bed = create_material("BedStone", (0.28, 0.28, 0.30, 1.0), roughness=0.9)
    mat_stone_run = create_material("RunnerStone", (0.48, 0.47, 0.45, 1.0), roughness=0.85)
    mat_iron = create_material("MillIron", (0.16, 0.17, 0.19, 1.0), roughness=0.35, metallic=0.85)
    mat_flour = create_material("FlourMeal", (0.92, 0.90, 0.82, 1.0), roughness=0.95)

    for lx in [-0.55, 0.55]:
        for ly in [-0.55, 0.55]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(lx, ly, 0.32))
            leg = bpy.context.active_object
            leg.scale = (0.14, 0.14, 0.64)
            leg.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.66))
    frame = bpy.context.active_object
    frame.scale = (1.30, 1.30, 0.10)
    frame.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.48, vertices=12, location=(0, 0, 0.94))
    vat = bpy.context.active_object
    vat.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.18, vertices=12, location=(0, 0, 0.82))
    bedstone = bpy.context.active_object
    bedstone.data.materials.append(mat_stone_bed)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.53, depth=0.20, vertices=12, location=(0, 0, 1.02))
    runner = bpy.context.active_object
    runner.data.materials.append(mat_stone_run)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.22, vertices=8, location=(0, 0, 1.04))
    eye = bpy.context.active_object
    eye.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.60, vertices=8, location=(0, 0, 1.15))
    spindle = bpy.context.active_object
    spindle.data.materials.append(mat_iron)

    for hx in [-0.28, 0.28]:
        for hy in [-0.28, 0.28]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(hx, hy, 1.40))
            stave = bpy.context.active_object
            stave.scale = (0.05, 0.05, 0.45)
            stave.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cone_add(radius1=0.38, radius2=0.12, depth=0.36, vertices=4, location=(0, 0, 1.54), rotation=(0, 0, math.radians(45)))
    hopper = bpy.context.active_object
    hopper.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.65, 0.72), rotation=(math.radians(30), 0, 0))
    spout = bpy.context.active_object
    spout.scale = (0.22, 0.28, 0.10)
    spout.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.26, vertices=8, location=(0, 0.74, 0.14))
    bucket = bpy.context.active_object
    bucket.data.materials.append(mat_wood)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.05, vertices=8, location=(0, 0.74, 0.22))
    flour_pile = bpy.context.active_object
    flour_pile.data.materials.append(mat_flour)

    export_glb("millstone.glb")

# -------------------------------------------------------------
# 27. Industrial Cam-Driven Trip Hammer (trip_hammer.glb)
# -------------------------------------------------------------
def build_trip_hammer():
    reset_scene()
    mat_stone_base = create_material("StoneBase", (0.25, 0.25, 0.26, 1.0), roughness=0.9)
    mat_oak_beam = create_material("OakBeam", (0.30, 0.18, 0.09, 1.0), roughness=0.75)
    mat_iron_heavy = create_material("HeavyIron", (0.14, 0.15, 0.16, 1.0), roughness=0.3, metallic=0.92)
    mat_crushed_ore = create_material("CrushedIronOre", (0.45, 0.26, 0.18, 1.0), roughness=0.85)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.14))
    foundation = bpy.context.active_object
    foundation.scale = (1.40, 2.40, 0.28)
    foundation.data.materials.append(mat_stone_base)

    for fx in [-0.48, 0.48]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, 0, 0.90))
        gallows = bpy.context.active_object
        gallows.scale = (0.18, 0.22, 1.30)
        gallows.data.materials.append(mat_oak_beam)

        for b_sign in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, b_sign * 0.40, 0.60), rotation=(math.radians(b_sign * -35), 0, 0))
            brace = bpy.context.active_object
            brace.scale = (0.12, 0.12, 0.85)
            brace.data.materials.append(mat_oak_beam)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.20, vertices=10, location=(0, 0, 1.45), rotation=(0, math.radians(90), 0))
    pivot = bpy.context.active_object
    pivot.data.materials.append(mat_iron_heavy)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.10, 1.48), rotation=(math.radians(-6), 0, 0))
    arm = bpy.context.active_object
    arm.scale = (0.22, 1.95, 0.24)
    arm.data.materials.append(mat_oak_beam)

    for b_y in [-0.35, 0.10, 0.65]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, b_y, 1.48), rotation=(math.radians(-6), 0, 0))
        band = bpy.context.active_object
        band.scale = (0.24, 0.08, 0.26)
        band.data.materials.append(mat_iron_heavy)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 1.32))
    hammer_head = bpy.context.active_object
    hammer_head.scale = (0.42, 0.42, 0.55)
    hammer_head.data.materials.append(mat_iron_heavy)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.50))
    anvil_block = bpy.context.active_object
    anvil_block.scale = (0.65, 0.65, 0.45)
    anvil_block.data.materials.append(mat_oak_beam)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.78))
    die_plate = bpy.context.active_object
    die_plate.scale = (0.50, 0.50, 0.12)
    die_plate.data.materials.append(mat_iron_heavy)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.98, 0.86))
    ore_pile = bpy.context.active_object
    ore_pile.scale = (0.36, 0.36, 0.05)
    ore_pile.data.materials.append(mat_crushed_ore)

    for cx in [-0.45, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, -0.85, 0.65))
        cpost = bpy.context.active_object
        cpost.scale = (0.16, 0.18, 0.75)
        cpost.data.materials.append(mat_oak_beam)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.10, depth=1.15, vertices=8, location=(0, -0.85, 0.98), rotation=(0, math.radians(90), 0))
    cshaft = bpy.context.active_object
    cshaft.data.materials.append(mat_iron_heavy)

    for c_idx in range(3):
        c_ang = (2.0 * math.pi / 3.0) * c_idx
        cy = -0.85 + 0.18 * math.cos(c_ang)
        cz = 0.98 + 0.18 * math.sin(c_ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, cy, cz), rotation=(-c_ang, 0, 0))
        cam_tooth = bpy.context.active_object
        cam_tooth.scale = (0.14, 0.22, 0.08)
        cam_tooth.data.materials.append(mat_iron_heavy)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.10, vertices=12, location=(0.60, -0.85, 0.98), rotation=(0, math.radians(90), 0))
    pulley = bpy.context.active_object
    pulley.data.materials.append(mat_oak_beam)

    export_glb("trip_hammer.glb")

# -------------------------------------------------------------
# 28. Farmer's Delight Organic Compost Bin (compost_bin.glb)
# -------------------------------------------------------------
def build_compost_bin():
    reset_scene()
    mat_timber = create_material("SlattedTimber", (0.34, 0.22, 0.12, 1.0), roughness=0.75)
    mat_compost = create_material("RichSoilCompost", (0.16, 0.11, 0.07, 1.0), roughness=0.95)
    mat_iron = create_material("CornerIron", (0.15, 0.16, 0.18, 1.0), roughness=0.4, metallic=0.85)
    mat_greens = create_material("PlantMatter", (0.28, 0.48, 0.16, 1.0), roughness=0.8)

    post_height = 0.85
    for cx in [-0.42, 0.42]:
        for cy in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, post_height * 0.5))
            post = bpy.context.active_object
            post.scale = (0.10, 0.10, post_height)
            post.data.materials.append(mat_timber)

            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, post_height - 0.02))
            cap = bpy.context.active_object
            cap.scale = (0.11, 0.11, 0.06)
            cap.data.materials.append(mat_iron)

    plank_tiers = [0.12, 0.32, 0.52, 0.72]
    for z in plank_tiers:
        for wy in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, wy, z))
            plank = bpy.context.active_object
            plank.scale = (0.84, 0.05, 0.14)
            plank.data.materials.append(mat_timber)

        for wx in [-0.42, 0.42]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0, z))
            plank = bpy.context.active_object
            plank.scale = (0.05, 0.74, 0.14)
            plank.data.materials.append(mat_timber)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.04))
    floor = bpy.context.active_object
    floor.scale = (0.80, 0.80, 0.06)
    floor.data.materials.append(mat_timber)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.42))
    soil = bpy.context.active_object
    soil.scale = (0.76, 0.76, 0.68)
    soil.data.materials.append(mat_compost)

    for gx, gy in [(-0.15, -0.12), (0.18, 0.10), (-0.10, 0.22), (0.20, -0.18)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(gx, gy, 0.77), rotation=(0, 0, math.radians(25)))
        leaf = bpy.context.active_object
        leaf.scale = (0.12, 0.14, 0.03)
        leaf.data.materials.append(mat_greens)

    export_glb("compost_bin.glb")

# -------------------------------------------------------------
# 29. Farmer's Delight Culinary Cutting Board (cutting_board.glb)
# -------------------------------------------------------------
def build_cutting_board():
    reset_scene()
    mat_board = create_material("ButcherBlock", (0.52, 0.35, 0.20, 1.0), roughness=0.6)
    mat_iron = create_material("CleaverSteel", (0.22, 0.24, 0.26, 1.0), roughness=0.3, metallic=0.92)
    mat_knife_handle = create_material("KnifeHandle", (0.18, 0.12, 0.07, 1.0), roughness=0.7)
    mat_cabbage = create_material("SlicedCabbage", (0.35, 0.65, 0.25, 1.0), roughness=0.5)
    mat_meat_cube = create_material("MincedMeat", (0.60, 0.18, 0.15, 1.0), roughness=0.5)
    mat_onion = create_material("DicedOnion", (0.85, 0.82, 0.72, 1.0), roughness=0.6)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.06))
    board = bpy.context.active_object
    board.scale = (0.68, 0.48, 0.09)
    board.data.materials.append(mat_board)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.41, 0, 0.06))
    handle = bpy.context.active_object
    handle.scale = (0.14, 0.16, 0.06)
    handle.data.materials.append(mat_board)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.14, -0.05, 0.14), rotation=(0, math.radians(12), math.radians(-15)))
    cleaver = bpy.context.active_object
    cleaver.scale = (0.02, 0.26, 0.10)
    cleaver.data.materials.append(mat_iron)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.18, vertices=8, location=(0.18, -0.22, 0.17), rotation=(math.radians(75), 0, math.radians(-15)))
    k_handle = bpy.context.active_object
    k_handle.data.materials.append(mat_knife_handle)

    for i in range(4):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.16 + i * 0.03, 0.08, 0.12), rotation=(0, 0, math.radians(i * 15)))
        cab = bpy.context.active_object
        cab.scale = (0.04, 0.12, 0.02)
        cab.data.materials.append(mat_cabbage)

    for mx, my in [(-0.12, -0.08), (-0.05, -0.10), (-0.08, -0.04)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx, my, 0.12))
        m_cube = bpy.context.active_object
        m_cube.scale = (0.05, 0.05, 0.04)
        m_cube.data.materials.append(mat_meat_cube)

    for ox, oy in [(-0.24, -0.04), (-0.22, 0.04), (-0.26, 0.02)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, 0.12))
        onion = bpy.context.active_object
        onion.scale = (0.03, 0.03, 0.03)
        onion.data.materials.append(mat_onion)

    export_glb("cutting_board.glb")

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
    build_windmill()
    build_cooking_pot()
    build_war_horn()
    build_wheelbarrow()
    build_architect_desk()
    build_anvil()
    build_smoke_rack()
    build_water_wheel()
    build_millstone()
    build_trip_hammer()
    build_compost_bin()
    build_cutting_board()
    print("[BLENDER SCRIPT] All models generated successfully!")




