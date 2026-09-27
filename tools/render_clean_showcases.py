# tools/render_clean_showcases.py
# High-quality cinematic vignette renders for key architectural and engineering milestones
import bpy
import os
import math
from mathutils import Vector

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_vignette_scene(sky_color=(0.58, 0.76, 0.96), ground_type="stone"):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngineEEVEE_NEXT') else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100

    # Ambient World
    world = bpy.data.worlds.new("VignetteWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (sky_color[0], sky_color[1], sky_color[2], 1.0)
        bg.inputs["Strength"].default_value = 1.0

    # Ground
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    ground = bpy.context.active_object
    mat_g = bpy.data.materials.new("VignetteGround")
    mat_g.use_nodes = True
    bsdf = mat_g.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if ground_type == "stone":
            bsdf.inputs["Base Color"].default_value = (0.35, 0.35, 0.36, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.85
        elif ground_type == "water":
            bsdf.inputs["Base Color"].default_value = (0.12, 0.38, 0.65, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.15
        elif ground_type == "grass":
            bsdf.inputs["Base Color"].default_value = (0.24, 0.52, 0.18, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.90
        elif ground_type == "gravel":
            bsdf.inputs["Base Color"].default_value = (0.38, 0.34, 0.30, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.92
    ground.data.materials.append(mat_g)

    # Key Sunlight
    bpy.ops.object.light_add(type='SUN', location=(6, -8, 12))
    sun = bpy.context.active_object
    sun.data.energy = 4.2
    sun.rotation_euler = (math.radians(52), math.radians(18), math.radians(-32))

    # Fill Light
    bpy.ops.object.light_add(type='SUN', location=(-8, 6, 8))
    fill = bpy.context.active_object
    fill.data.energy = 1.2
    fill.data.color = (0.85, 0.92, 1.0)
    fill.rotation_euler = (math.radians(45), math.radians(-30), math.radians(120))

def import_model(name, loc, rot_z=0, scale=1.0):
    path = os.path.join(MODELS_DIR, name)
    if not os.path.exists(path):
        print(f"MISSING ASSET: {path}")
        return None
    bpy.ops.import_scene.gltf(filepath=path)
    objs = bpy.context.selected_objects
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc)
    parent = bpy.context.active_object
    parent.rotation_euler.z = math.radians(rot_z)
    parent.scale = (scale, scale, scale)
    for o in objs:
        o.parent = parent
    return parent

def set_camera(location, target, lens=35):
    scene = bpy.context.scene
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.active_object
    cam.data.lens = lens
    scene.camera = cam

    direction = Vector(target) - Vector(location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

def render(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    bpy.context.scene.render.filepath = path
    print(f"[RENDER] Rendering vignette to {path}...")
    bpy.ops.render.render(write_still=True)
    print(f"[RENDER] Done: {path}")

# ============================================================
# 1. OBSERVATORY COMPLEX (Milestone 40 Grand Jubilee)
# ============================================================
def render_observatory():
    setup_vignette_scene(sky_color=(0.50, 0.65, 0.88), ground_type="stone")
    
    # Astronomical Clock tower in center-left (rotated 180 so astrolabe dial faces camera)
    import_model("astronomical_clock.glb", loc=(-1.8, 0.3, 0.0), rot_z=180, scale=0.85)
    # Armillary Sphere on pedestal in foreground-center
    import_model("armillary_sphere.glb", loc=(0.2, -0.6, 0.0), rot_z=-20, scale=1.0)
    # Celestial Orrery on right
    import_model("celestial_orrery.glb", loc=(2.2, 0.2, 0.0), rot_z=35, scale=0.9)

    set_camera(location=(0.2, -6.5, 2.5), target=(0.1, 0.0, 1.3), lens=35)
    render("showcase_observatory.png")

# ============================================================
# 2. STEAM POWER COMPLEX (Milestone 39)
# ============================================================
def render_steam_power():
    setup_vignette_scene(sky_color=(0.52, 0.68, 0.90), ground_type="stone")
    
    # Steam Boiler with brass straps on left
    import_model("steam_boiler.glb", loc=(-2.2, 0.2, 0.0), rot_z=-25, scale=0.95)
    # Stationary Steam Engine Drive with large flywheel in center
    import_model("steam_engine_drive.glb", loc=(0.2, 0.0, 0.0), rot_z=15, scale=0.95)
    # Centrifugal Flyball Governor on right
    import_model("centrifugal_governor.glb", loc=(2.2, -0.4, 0.0), rot_z=-15, scale=1.0)

    set_camera(location=(0.0, -6.5, 2.4), target=(0.0, 0.0, 1.1), lens=35)
    render("showcase_steam_power.png")

# ============================================================
# 3. HARBOR & SHIPBUILDING (Milestone 38)
# ============================================================
def render_harbor():
    setup_vignette_scene(sky_color=(0.45, 0.70, 0.92), ground_type="water")
    
    # Quayside dock pier
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -2.5, 0.2))
    pier = bpy.context.active_object
    pier.scale = (14.0, 5.0, 0.6)
    mat_pier = bpy.data.materials.new("PierStone")
    mat_pier.use_nodes = True
    bsdf = mat_pier.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.42, 0.40, 0.38, 1.0)
    pier.data.materials.append(mat_pier)

    # Drydock Slipway
    import_model("drydock_slipway.glb", loc=(-4.0, 0.0, 0.2), rot_z=20, scale=0.85)
    # Quayside Crane on dock
    import_model("quayside_crane.glb", loc=(1.0, -1.0, 0.5), rot_z=-45, scale=0.9)
    # Fluyt Cargo Ship floating in water
    import_model("fluyt_cargo_ship.glb", loc=(-0.5, 4.2, 0.0), rot_z=-85, scale=0.85)

    set_camera(location=(3.5, -8.0, 4.5), target=(-0.8, 1.2, 1.5), lens=34)
    render("showcase_harbor_and_navy.png")

# ============================================================
# 4. MINING & RAILWAY LOGISTICS (Milestone 36 & 37)
# ============================================================
def render_mining_rail():
    setup_vignette_scene(sky_color=(0.50, 0.65, 0.85), ground_type="gravel")
    
    # Geared Steam Locomotive on rails
    import_model("mine_locomotive.glb", loc=(-2.2, 0.0, 0.0), rot_z=15, scale=0.95)
    # Rail Switch turnout
    import_model("rail_switch.glb", loc=(0.5, -0.2, 0.0), rot_z=15, scale=0.95)
    # Hopper Discharge Station
    import_model("hopper_unloader.glb", loc=(2.8, 0.5, 0.0), rot_z=-15, scale=0.85)
    # Dewatering Pump in background
    import_model("mine_dewatering_pump.glb", loc=(-4.0, 2.2, 0.0), rot_z=20, scale=0.8)
    # Mine Ventilator
    import_model("mine_ventilator.glb", loc=(4.0, 1.8, 0.0), rot_z=-35, scale=0.85)

    set_camera(location=(0.2, -6.5, 2.6), target=(0.2, 0.2, 1.0), lens=36)
    render("showcase_mining_rail.png")

# ============================================================
# 5. CASTLE DEFENSES & SIEGE ENGINES (Milestones 33 & 34)
# ============================================================
def render_siege_and_castle():
    setup_vignette_scene(sky_color=(0.48, 0.68, 0.90), ground_type="grass")
    
    # Castle Gate with Drawbridge & Portcullis
    import_model("castle_gate.glb", loc=(0.0, 4.5, 0.0), rot_z=0, scale=0.85)
    # Counterweight Trebuchet on flank
    import_model("trebuchet_siege.glb", loc=(-3.8, 0.0, 0.0), rot_z=45, scale=0.85)
    # Heavy Battering Ram rolling toward gate
    import_model("battering_ram.glb", loc=(0.0, -0.5, 0.0), rot_z=90, scale=0.9)
    # Mangonel Catapult on right
    import_model("mangonel.glb", loc=(3.5, 0.0, 0.0), rot_z=-35, scale=0.85)

    set_camera(location=(3.5, -8.5, 4.2), target=(0.0, 1.0, 1.5), lens=34)
    render("showcase_siege_and_castle.png")

# ============================================================
# 6. PANORAMIC REALM SHOWCASE (Spaced Out Grand Layout)
# ============================================================
def render_spaced_realm():
    setup_vignette_scene(sky_color=(0.55, 0.75, 0.95), ground_type="grass")
    
    # Water river canal
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 7.0, 0.02))
    river = bpy.context.active_object
    river.scale = (35.0, 6.0, 1.0)
    mat_r = bpy.data.materials.new("RiverWater")
    mat_r.use_nodes = True
    bsdf = mat_r.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.15, 0.42, 0.72, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.12
    river.data.materials.append(mat_r)

    # 1. Harbor & Ships along river (Top Left)
    import_model("fluyt_cargo_ship.glb", loc=(-8.0, 7.5, 0.0), rot_z=-45, scale=0.7)
    import_model("quayside_crane.glb", loc=(-5.0, 4.5, 0.0), rot_z=-30, scale=0.75)
    import_model("drydock_slipway.glb", loc=(-9.0, 4.0, 0.0), rot_z=30, scale=0.7)

    # 2. Castle & Fortifications (Top Center)
    import_model("castle_gate.glb", loc=(0.0, 3.5, 0.0), rot_z=0, scale=0.75)
    import_model("watchtower.glb", loc=(-3.0, 3.5, 0.0), rot_z=20, scale=0.75)
    import_model("drawbridge.glb", loc=(0.0, 1.8, 0.0), rot_z=0, scale=0.75)

    # 3. Windmill & Agriculture (Top Right)
    import_model("windmill.glb", loc=(8.0, 4.5, 0.0), rot_z=35, scale=0.75)
    import_model("flour_silo.glb", loc=(6.0, 4.0, 0.0), rot_z=-15, scale=0.75)
    import_model("bakery_oven.glb", loc=(7.0, 1.8, 0.0), rot_z=25, scale=0.8)

    # 4. Steam Power & Foundry (Mid Left)
    import_model("steam_boiler.glb", loc=(-7.0, -1.0, 0.0), rot_z=-20, scale=0.8)
    import_model("steam_engine_drive.glb", loc=(-5.0, -1.0, 0.0), rot_z=30, scale=0.75)
    import_model("centrifugal_governor.glb", loc=(-5.5, -2.8, 0.0), rot_z=10, scale=0.85)

    # 5. Grand Observatory & Science (Center)
    import_model("astronomical_clock.glb", loc=(-1.8, -0.5, 0.0), rot_z=180, scale=0.75)
    import_model("armillary_sphere.glb", loc=(0.2, -1.2, 0.0), rot_z=20, scale=0.85)
    import_model("celestial_orrery.glb", loc=(2.0, -0.6, 0.0), rot_z=-25, scale=0.75)

    # 6. Industrial Workshop & Blacksmith (Mid Right)
    import_model("foundry_furnace.glb", loc=(5.5, -1.0, 0.0), rot_z=-15, scale=0.8)
    import_model("steam_bellows.glb", loc=(7.0, -1.0, 0.0), rot_z=15, scale=0.8)
    import_model("anvil.glb", loc=(4.5, -2.5, 0.0), rot_z=25, scale=0.9)

    # 7. Mining & Railway (Foreground Center & Right)
    import_model("mine_locomotive.glb", loc=(-1.5, -5.0, 0.0), rot_z=-75, scale=0.8)
    import_model("rail_switch.glb", loc=(0.8, -5.0, 0.0), rot_z=-75, scale=0.8)
    import_model("hopper_unloader.glb", loc=(3.0, -5.0, 0.0), rot_z=-75, scale=0.75)

    # 8. Siege Weapons (Foreground Left)
    import_model("trebuchet_siege.glb", loc=(-6.0, -5.0, 0.0), rot_z=35, scale=0.75)
    import_model("battering_ram.glb", loc=(-3.8, -5.2, 0.0), rot_z=60, scale=0.75)

    # Camera: High elevated panoramic shot
    set_camera(location=(15.0, -18.0, 12.0), target=(0.0, 0.5, 1.2), lens=28)
    render("showcase_realm.png")

def main():
    print("=== RENDERING HIGH-QUALITY SHOWCASE VIGNETTES ===")
    render_observatory()
    render_steam_power()
    render_harbor()
    render_mining_rail()
    render_siege_and_castle()
    render_spaced_realm()
    print("=== ALL VIGNETTES COMPLETE ===")

if __name__ == "__main__":
    main()
