# tools/render_closeups.py
# High-definition close-up cinematic renders of key mechanical and architectural zones
# 1. showcase_observatory.png
# 2. showcase_steam_power.png
# 3. showcase_harbor_and_navy.png
# 4. showcase_mining_rail.png

import bpy
import os
import math

def set_camera(location, target):
    cam = bpy.context.scene.camera
    cam.location = location
    dx = target[0] - location[0]
    dy = target[1] - location[1]
    dz = target[2] - location[2]
    
    # Distance in XY
    dist_xy = math.sqrt(dx*dx + dy*dy)
    pitch = math.atan2(dz, dist_xy)
    yaw = math.atan2(dy, dx) - math.pi / 2.0
    
    # Rotations for Blender camera (-Z forward, +Y up)
    cam.rotation_euler = (math.pi / 2.0 - pitch, 0, yaw)

def render_image(filepath):
    bpy.context.scene.render.filepath = filepath
    print(f"[CLOSEUP] Rendering {filepath}...")
    bpy.ops.render.render(write_still=True)
    print(f"[CLOSEUP] Saved: {filepath}")

def main():
    import sys
    # Add tools directory to sys.path to reuse render_showcase logic
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    if tools_dir not in sys.path:
        sys.path.append(tools_dir)
        
    import render_showcase
    
    # 1. Build the full diorama scene with all 112 assets
    render_showcase.build_diorama()
    
    output_dir = os.path.abspath(os.path.join(tools_dir, "..", "assets"))
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Close-up: Observatory Complex (Astronomical Clock, Armillary Sphere, Celestial Orrery)
    set_camera(location=(-0.2, -2.8, 1.8), target=(-0.9, -0.1, 1.2))
    render_image(os.path.join(output_dir, "showcase_observatory.png"))
    
    # 2. Close-up: High-Pressure Steam Power (Boiler, Stationary Engine, Flyball Governor)
    set_camera(location=(1.0, -0.3, 1.6), target=(-0.5, 1.5, 1.0))
    render_image(os.path.join(output_dir, "showcase_steam_power.png"))
    
    # 3. Close-up: Coastal Maritime Port & Shipbuilding (Slipway, Quayside Crane, Fluyt Cargo Ship)
    set_camera(location=(-2.5, 1.8, 3.0), target=(-5.0, 4.2, 1.5))
    render_image(os.path.join(output_dir, "showcase_harbor_and_navy.png"))
    
    # 4. Close-up: Mine Railway Logistics (Steam Locomotive, Rail Switch, Hopper Unloader)
    set_camera(location=(4.0, -3.8, 1.6), target=(1.6, -1.8, 0.7))
    render_image(os.path.join(output_dir, "showcase_mining_rail.png"))
    
    print("=== All close-up renders successfully generated! ===")

if __name__ == "__main__":
    main()
