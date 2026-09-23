import bpy
import os
import math

def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngineEEVEE_NEXT') else 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100

    # World background
    world = bpy.data.worlds.new("ShowcaseWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.55, 0.75, 0.95, 1.0) # Medieval blue sky
        bg.inputs["Strength"].default_value = 1.0

    # Ground plane (Green grass meadow)
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    ground = bpy.context.active_object
    mat_ground = bpy.data.materials.new("GrassGround")
    mat_ground.use_nodes = True
    g_bsdf = mat_ground.node_tree.nodes.get("Principled BSDF")
    if g_bsdf:
        g_bsdf.inputs["Base Color"].default_value = (0.24, 0.55, 0.18, 1.0)
        g_bsdf.inputs["Roughness"].default_value = 0.9
    ground.data.materials.append(mat_ground)

    # Sunlight
    bpy.ops.object.light_add(type='SUN', location=(10, -10, 15))
    sun = bpy.context.active_object
    sun.data.energy = 3.5
    sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-35))

    # Camera
    bpy.ops.object.camera_add(location=(7.5, -8.5, 4.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(68), 0, math.radians(40))
    scene.camera = cam

def import_asset(name, loc, rot_z=0, scale=1.0):
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "models"))
    path = os.path.join(models_dir, name)
    if not os.path.exists(path):
        print(f"Asset missing: {path}")
        return None
    
    # Import GLB
    bpy.ops.import_scene.gltf(filepath=path)
    imported_objs = bpy.context.selected_objects
    
    # Group under an empty or parent object
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc)
    parent = bpy.context.active_object
    parent.name = name.replace(".glb", "_Root")
    parent.rotation_euler.z = math.radians(rot_z)
    parent.scale = (scale, scale, scale)
    
    for obj in imported_objs:
        obj.parent = parent
        
    return parent

def build_diorama():
    setup_scene()
    
    # 1. Watchtower in back-left
    import_asset("watchtower.glb", (-3.0, 3.0, 0.0), rot_z=25)
    
    # 2. Caravan Cart in mid-ground
    import_asset("caravan_cart.glb", (2.5, 1.0, 0.0), rot_z=-35)
    
    # 3. Campfire in center
    import_asset("campfire.glb", (0.0, -0.5, 0.0))
    
    # 4. Smelting Furnace near campfire
    import_asset("furnace.glb", (-1.8, -0.8, 0.0), rot_z=20)
    
    # 5. Carpentry Workbench
    import_asset("workbench.glb", (1.2, -1.8, 0.0), rot_z=-15)
    
    # 6. Timber Crate
    import_asset("crate.glb", (2.2, -1.5, 0.0), rot_z=10)
    
    # 7. Citizen (Lord's loyal subject) standing near workbench
    import_asset("citizen.glb", (0.8, -1.2, 0.0), rot_z=150)
    
    # 8. Bandit Raider approaching from right
    import_asset("bandit.glb", (3.8, -2.5, 0.0), rot_z=-70)
    
    # 9. Support Beam standing as mine entrance marker
    import_asset("support_beam.glb", (-4.2, -0.5, 0.0), rot_z=90)

    # Render output path
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
    output_path = os.path.join(output_dir, "showcase_realm.png")
    
    bpy.context.scene.render.filepath = output_path
    print(f"[RENDER] Rendering 3D showcase diorama to {output_path}...")
    bpy.ops.render.render(write_still=True)
    print(f"[RENDER] Render complete: {output_path}")

if __name__ == "__main__":
    build_diorama()
