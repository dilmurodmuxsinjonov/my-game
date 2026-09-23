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

if __name__ == "__main__":
    print("[BLENDER SCRIPT] Starting procedural 3D medieval model generation...")
    build_pickaxe()
    build_axe()
    build_sword()
    build_workbench()
    build_campfire()
    build_crate()
    build_citizen()
    print("[BLENDER SCRIPT] All models generated successfully!")
