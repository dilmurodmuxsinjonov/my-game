"""Blender 5.2 Headless Model Generator for Milestone 13:
1. prospector_pick.glb (TerraFirmaCraft Geologist Prospector's Pickaxe)
2. mine_cart.glb (Heavy Underground Ore Transport Minecart)
3. mining_lantern.glb (Enclosed Brass Miner's Safety Oil Lantern)
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
            # Blender 4+ Principled BSDF has Emission Color and Emission Strength
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
# 30. TerraFirmaCraft Prospector's Pick (prospector_pick.glb)
# -------------------------------------------------------------
def build_prospector_pick():
    reset_scene()
    mat_bronze = create_material("ProspectorBronze", (0.78, 0.52, 0.28, 1.0), roughness=0.35, metallic=0.9)
    mat_wood = create_material("AshWoodShaft", (0.55, 0.40, 0.25, 1.0), roughness=0.7)
    mat_leather = create_material("HandleLeatherGrip", (0.28, 0.18, 0.10, 1.0), roughness=0.85)
    mat_iron = create_material("SocketIron", (0.20, 0.22, 0.25, 1.0), roughness=0.45, metallic=0.85)

    # 1. Wooden Handle Shaft (length 0.7m)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.022, depth=0.70, vertices=12, location=(0, 0, 0.35))
    handle = bpy.context.active_object
    handle.data.materials.append(mat_wood)

    # 2. Leather Grip Wrap near base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.026, depth=0.25, vertices=12, location=(0, 0, 0.18))
    grip = bpy.context.active_object
    grip.data.materials.append(mat_leather)

    # 3. Bronze Pommel Cap at base
    bpy.ops.mesh.primitive_cylinder_add(radius=0.032, depth=0.04, vertices=12, location=(0, 0, 0.03))
    pommel = bpy.context.active_object
    pommel.data.materials.append(mat_bronze)

    # 4. Iron Eye Socket Collar near head
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.68))
    socket = bpy.context.active_object
    socket.scale = (0.055, 0.055, 0.08)
    socket.data.materials.append(mat_iron)

    # 5. Prospector Bronze Pick Beak (Curved, slender point pointing forward)
    # Main curved body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.14, 0, 0.67))
    beak = bpy.context.active_object
    beak.scale = (0.24, 0.04, 0.035)
    beak.rotation_euler = (0, math.radians(-10), 0)
    beak.data.materials.append(mat_bronze)

    # Tapered pick tip
    bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.005, depth=0.10, vertices=8, location=(0.28, 0, 0.64))
    tip = bpy.context.active_object
    tip.rotation_euler = (0, math.radians(80), 0)
    tip.data.materials.append(mat_bronze)

    # 6. Geologist Hammer Butt / Probe on rear (-X)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.10, 0, 0.68))
    butt = bpy.context.active_object
    butt.scale = (0.14, 0.048, 0.048)
    butt.data.materials.append(mat_bronze)

    # Measurement graduation bands on hammer butt
    for off in [-0.06, -0.10, -0.14]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.026, depth=0.006, vertices=8, location=(off, 0, 0.68))
        ring = bpy.context.active_object
        ring.rotation_euler = (0, math.radians(90), 0)
        ring.data.materials.append(mat_iron)

    export_glb("prospector_pick.glb")

# -------------------------------------------------------------
# 31. Underground Ore Transport Minecart (mine_cart.glb)
# -------------------------------------------------------------
def build_mine_cart():
    reset_scene()
    mat_timber = create_material("CartOakPlanks", (0.38, 0.25, 0.14, 1.0), roughness=0.75)
    mat_iron = create_material("WroughtIronFrame", (0.16, 0.17, 0.19, 1.0), roughness=0.4, metallic=0.9)
    mat_wheel = create_material("CastIronWheel", (0.22, 0.23, 0.26, 1.0), roughness=0.3, metallic=0.95)
    mat_ore = create_material("OreLumpPayload", (0.50, 0.38, 0.28, 1.0), roughness=0.85)

    # 1. Base Frame Chassis (wrought iron rails)
    for y_side in [-0.32, 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y_side, 0.22))
        chassis_rail = bpy.context.active_object
        chassis_rail.scale = (1.10, 0.08, 0.06)
        chassis_rail.data.materials.append(mat_iron)

    # Cross beams
    for x_pos in [-0.45, 0.0, 0.45]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 0.22))
        cross_beam = bpy.context.active_object
        cross_beam.scale = (0.08, 0.64, 0.06)
        cross_beam.data.materials.append(mat_iron)

    # 2. Axles & 4 Flanged Wheels
    for x_axle in [-0.35, 0.35]:
        # Axle shaft
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.84, vertices=12, location=(x_axle, 0, 0.15))
        axle = bpy.context.active_object
        axle.rotation_euler = (math.radians(90), 0, 0)
        axle.data.materials.append(mat_iron)

        # Left and Right Wheels
        for y_wheel in [-0.40, 0.40]:
            # Main wheel tread
            bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.05, vertices=16, location=(x_axle, y_wheel, 0.15))
            wheel = bpy.context.active_object
            wheel.rotation_euler = (math.radians(90), 0, 0)
            wheel.data.materials.append(mat_wheel)

            # Outer flange lip
            flange_y = y_wheel - 0.028 if y_wheel < 0 else y_wheel + 0.028
            bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.015, vertices=16, location=(x_axle, flange_y, 0.15))
            flange = bpy.context.active_object
            flange.rotation_euler = (math.radians(90), 0, 0)
            flange.data.materials.append(mat_wheel)

            # Wheel hub boss
            bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.07, vertices=10, location=(x_axle, y_wheel, 0.15))
            hub = bpy.context.active_object
            hub.rotation_euler = (math.radians(90), 0, 0)
            hub.data.materials.append(mat_iron)

    # 3. Wooden Hopper Tub (Walls flared slightly outward)
    # Bottom floor
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.28))
    floor = bpy.context.active_object
    floor.scale = (0.95, 0.60, 0.05)
    floor.data.materials.append(mat_timber)

    # Long Side Walls (+Y and -Y)
    for y_sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, y_sign * 0.32, 0.52))
        side_wall = bpy.context.active_object
        side_wall.scale = (0.95, 0.05, 0.45)
        side_wall.rotation_euler = (math.radians(y_sign * 5), 0, 0)
        side_wall.data.materials.append(mat_timber)

    # End Walls (+X and -X)
    for x_sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_sign * 0.48, 0, 0.52))
        end_wall = bpy.context.active_object
        end_wall.scale = (0.05, 0.64, 0.45)
        end_wall.rotation_euler = (0, math.radians(-x_sign * 5), 0)
        end_wall.data.materials.append(mat_timber)

    # 4. Iron Corner Brackets & Reinforcement Ribs
    for cx in [-0.48, 0.48]:
        for cy in [-0.32, 0.32]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, 0.52))
            bracket = bpy.context.active_object
            bracket.scale = (0.07, 0.07, 0.46)
            bracket.data.materials.append(mat_iron)

    # 5. Top Rim Iron Band
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.74))
    rim = bpy.context.active_object
    rim.scale = (1.02, 0.68, 0.03)
    rim.data.materials.append(mat_iron)

    # 6. Push Handle Bar on rear (-X end)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.72, vertices=12, location=(-0.56, 0, 0.68))
    handle = bpy.context.active_object
    handle.rotation_euler = (math.radians(90), 0, 0)
    handle.data.materials.append(mat_iron)

    for hy in [-0.32, 0.32]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.52, hy, 0.68))
        h_support = bpy.context.active_object
        h_support.scale = (0.08, 0.03, 0.03)
        h_support.data.materials.append(mat_iron)

    # 7. Payload: Ore Mound inside cart
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.46))
    ore_mound = bpy.context.active_object
    ore_mound.scale = (0.75, 0.46, 0.22)
    ore_mound.data.materials.append(mat_ore)

    export_glb("mine_cart.glb")

# -------------------------------------------------------------
# 32. Brass Miner's Safety Lantern (mining_lantern.glb)
# -------------------------------------------------------------
def build_mining_lantern():
    reset_scene()
    mat_brass = create_material("PolishedBrass", (0.82, 0.65, 0.24, 1.0), roughness=0.3, metallic=0.9)
    mat_dark_iron = create_material("CageIron", (0.18, 0.18, 0.20, 1.0), roughness=0.45, metallic=0.85)
    mat_glass = create_material("LanternGlass", (0.92, 0.95, 0.98, 0.4), roughness=0.1, metallic=0.0)
    mat_flame = create_material("LanternFlame", (1.0, 0.85, 0.45, 1.0), roughness=0.1, metallic=0.0,
                                emission=(1.0, 0.85, 0.45, 1.0), emission_strength=4.5)

    # 1. Base Fuel Chamber (octagon / cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.12, vertices=16, location=(0, 0, 0.06))
    base = bpy.context.active_object
    base.data.materials.append(mat_brass)

    # Base rim foot
    bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.03, vertices=16, location=(0, 0, 0.015))
    foot = bpy.context.active_object
    foot.data.materials.append(mat_brass)

    # 2. Glass Combustion Cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.28, vertices=16, location=(0, 0, 0.26))
    glass = bpy.context.active_object
    glass.data.materials.append(mat_glass)

    # 3. Internal Glowing Wick / Flame
    bpy.ops.mesh.primitive_cone_add(radius1=0.03, depth=0.08, vertices=8, location=(0, 0, 0.22))
    flame = bpy.context.active_object
    flame.data.materials.append(mat_flame)

    # 4. Protective Brass Wire Cage (4 vertical pillars around glass)
    cage_r = 0.145
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        px = cage_r * math.cos(rad)
        py = cage_r * math.sin(rad)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.30, vertices=8, location=(px, py, 0.26))
        pillar = bpy.context.active_object
        pillar.data.materials.append(mat_brass)

    # Mid-height horizontal wire ring
    bpy.ops.mesh.primitive_torus_add(major_radius=cage_r, minor_radius=0.01, location=(0, 0, 0.26))
    mid_ring = bpy.context.active_object
    mid_ring.data.materials.append(mat_brass)

    # 5. Top Ventilated Chimney Hood Cap
    # Lower hood tier
    bpy.ops.mesh.primitive_cone_add(radius1=0.17, radius2=0.11, depth=0.10, vertices=16, location=(0, 0, 0.44))
    hood_low = bpy.context.active_object
    hood_low.data.materials.append(mat_brass)

    # Vent holes / middle cap
    bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.08, vertices=16, location=(0, 0, 0.52))
    vent_collar = bpy.context.active_object
    vent_collar.data.materials.append(mat_dark_iron)

    # Top heat deflector cap
    bpy.ops.mesh.primitive_cone_add(radius1=0.14, radius2=0.04, depth=0.06, vertices=16, location=(0, 0, 0.58))
    hood_top = bpy.context.active_object
    hood_top.data.materials.append(mat_brass)

    # Finial eyelet ring on top
    bpy.ops.mesh.primitive_torus_add(major_radius=0.04, minor_radius=0.01, location=(0, 0, 0.63))
    eyelet = bpy.context.active_object
    eyelet.rotation_euler = (math.radians(90), 0, 0)
    eyelet.data.materials.append(mat_brass)

    # 6. Arched Wire Carrying Bail Handle (swings over the top)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.17, minor_radius=0.012, location=(0, 0, 0.50))
    handle = bpy.context.active_object
    handle.scale = (0.4, 1.0, 1.2)
    handle.rotation_euler = (math.radians(90), 0, 0)
    handle.data.materials.append(mat_dark_iron)

    export_glb("mining_lantern.glb")

if __name__ == "__main__":
    print("--- Generating Milestone 13 Models ---")
    build_prospector_pick()
    build_mine_cart()
    build_mining_lantern()
    print("--- Milestone 13 Generation Complete ---")
