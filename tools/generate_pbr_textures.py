# tools/generate_pbr_textures.py
# Voxel Lord: Feudal Realm - Milestone 31: Realistic PBR Textures & Normal Map Generator
# Generates seamless 64x64 procedural PBR textures (Albedo, Tangent Normal, Roughness)
# and packs them into a unified Voxel PBR Texture Atlas.

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

TEXTURE_SIZE = 64
ATLAS_COLS = 4
ATLAS_ROWS = 3

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "textures"))
PBR_DIR = os.path.join(OUTPUT_DIR, "pbr")
os.makedirs(PBR_DIR, exist_ok=True)

BLOCK_PALETTES = {
    "stone": {
        "base": (120, 118, 115), "noise": 25, "roughness": 200, "pattern": "speckled"
    },
    "dirt": {
        "base": (110, 78, 52), "noise": 30, "roughness": 230, "pattern": "grainy"
    },
    "grass_top": {
        "base": (75, 130, 45), "noise": 28, "roughness": 190, "pattern": "foliage"
    },
    "grass_side": {
        "base": (100, 80, 50), "top_base": (75, 130, 45), "noise": 25, "roughness": 210, "pattern": "layered"
    },
    "oak_log": {
        "base": (85, 58, 35), "noise": 20, "roughness": 180, "pattern": "bark"
    },
    "oak_planks": {
        "base": (155, 115, 75), "noise": 15, "roughness": 170, "pattern": "planks"
    },
    "cobblestone": {
        "base": (105, 103, 100), "noise": 35, "roughness": 215, "pattern": "cobble"
    },
    "brick": {
        "base": (150, 68, 50), "mortar": (180, 175, 168), "noise": 18, "roughness": 185, "pattern": "bricks"
    },
    "sand": {
        "base": (210, 195, 145), "noise": 16, "roughness": 240, "pattern": "speckled"
    },
    "water": {
        "base": (45, 115, 195), "noise": 15, "roughness": 35, "pattern": "ripples"
    },
    "iron_ore": {
        "base": (120, 118, 115), "fleck": (195, 160, 130), "noise": 25, "roughness": 195, "pattern": "mineral"
    },
    "gold_ore": {
        "base": (120, 118, 115), "fleck": (245, 195, 50), "noise": 25, "roughness": 190, "pattern": "mineral"
    }
}

def generate_height_and_albedo(block_name, config):
    w, h = TEXTURE_SIZE, TEXTURE_SIZE
    albedo = Image.new("RGB", (w, h))
    height = Image.new("L", (w, h))
    alb_pix = albedo.load()
    hgt_pix = height.load()

    random.seed(hash(block_name) & 0xFFFFFFFF)
    base_r, base_g, base_b = config["base"]
    noise_amp = config["noise"]
    pattern = config["pattern"]

    for y in range(h):
        for x in range(w):
            val = random.randint(-noise_amp, noise_amp)
            r = max(0, min(255, base_r + val))
            g = max(0, min(255, base_g + val))
            b = max(0, min(255, base_b + val))
            h_val = 128 + val * 2

            if pattern == "planks":
                # Horizontal planks with lines every 16 pixels
                if y % 16 in (0, 1):
                    r, g, b = int(r * 0.6), int(g * 0.6), int(b * 0.6)
                    h_val = 60
                elif x % 32 == 0 and (y // 16) % 2 == 0:
                    r, g, b = int(r * 0.65), int(g * 0.65), int(b * 0.65)
                    h_val = 70
            elif pattern == "bricks":
                # Running bond brick pattern
                row = y // 16
                shift = (row % 2) * 16
                if y % 16 in (0, 1) or (x + shift) % 32 in (0, 1):
                    mr, mg, mb = config["mortar"]
                    r, g, b = mr + val // 2, mg + val // 2, mb + val // 2
                    h_val = 75
            elif pattern == "cobble":
                # Circular cobblestone cells
                cx = (x % 20) - 10
                cy = (y % 20) - 10
                dist = math.sqrt(cx*cx + cy*cy)
                if dist > 8.5:
                    r, g, b = int(r * 0.55), int(g * 0.55), int(b * 0.55)
                    h_val = 50
                else:
                    h_val = int(128 + (9.0 - dist) * 10)
            elif pattern == "layered":
                # Grass hanging over dirt side
                if y < 14:
                    tr, tg, tb = config["top_base"]
                    r, g, b = max(0, min(255, tr + val)), max(0, min(255, tg + val)), max(0, min(255, tb + val))
                    h_val = 160 + val
                elif y < 20 and (x + y * 3) % 7 in (0, 1, 2):
                    tr, tg, tb = config["top_base"]
                    r, g, b = max(0, min(255, tr + val)), max(0, min(255, tg + val)), max(0, min(255, tb + val))
                    h_val = 150
            elif pattern == "mineral":
                # Sparkling flecks
                if ((x * 17 + y * 31) % 43) in (0, 1, 2):
                    fr, fg, fb = config["fleck"]
                    r, g, b = fr + val // 2, fg + val // 2, fb + val // 2
                    h_val = 220
            elif pattern == "ripples":
                ripple = math.sin(x * 0.25) * math.cos(y * 0.25) * 20
                r = max(0, min(255, int(base_r + ripple)))
                g = max(0, min(255, int(base_g + ripple)))
                b = max(0, min(255, int(base_b + ripple)))
                h_val = int(128 + ripple * 2)

            alb_pix[x, y] = (r, g, b)
            hgt_pix[x, y] = max(0, min(255, h_val))

    # Smooth height map slightly
    height = height.filter(ImageFilter.GaussianBlur(radius=0.7))
    return albedo, height

def compute_normal_map(height_img):
    w, h = height_img.size
    h_pix = height_img.load()
    normal_img = Image.new("RGB", (w, h))
    n_pix = normal_img.load()

    strength = 2.0
    for y in range(h):
        for x in range(w):
            x_prev = (x - 1) % w
            x_next = (x + 1) % w
            y_prev = (y - 1) % h
            y_next = (y + 1) % h

            # Sobel / central difference
            dx = (float(h_pix[x_next, y]) - float(h_pix[x_prev, y])) / 255.0 * strength
            dy = (float(h_pix[x, y_next]) - float(h_pix[x, y_prev])) / 255.0 * strength
            dz = 1.0

            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            nx = -dx / length
            ny = -dy / length
            nz = dz / length

            r = int((nx * 0.5 + 0.5) * 255)
            g = int((ny * 0.5 + 0.5) * 255)
            b = int((nz * 0.5 + 0.5) * 255)
            n_pix[x, y] = (r, g, b)

    return normal_img

def compute_roughness_map(config, height_img):
    w, h = height_img.size
    h_pix = height_img.load()
    rough_img = Image.new("L", (w, h))
    r_pix = rough_img.load()

    base_r = config["roughness"]
    for y in range(h):
        for x in range(w):
            h_val = h_pix[x, y]
            # Crevices are slightly less rough, peaks more rough
            mod = int((h_val - 128) * 0.2)
            val = max(0, min(255, base_r + mod))
            r_pix[x, y] = val

    return rough_img

def generate_all_textures():
    atlas_w = ATLAS_COLS * TEXTURE_SIZE # 256
    atlas_h = ATLAS_ROWS * TEXTURE_SIZE # 192

    atlas_albedo = Image.new("RGB", (atlas_w, atlas_h))
    atlas_normal = Image.new("RGB", (atlas_w, atlas_h))
    atlas_roughness = Image.new("L", (atlas_w, atlas_h))

    block_order = list(BLOCK_PALETTES.keys())
    for idx, name in enumerate(block_order):
        cfg = BLOCK_PALETTES[name]
        albedo, height = generate_height_and_albedo(name, cfg)
        normal = compute_normal_map(height)
        roughness = compute_roughness_map(cfg, height)

        # Save individual PBR textures
        albedo.save(os.path.join(PBR_DIR, f"{name}_albedo.png"))
        normal.save(os.path.join(PBR_DIR, f"{name}_normal.png"))
        roughness.save(os.path.join(PBR_DIR, f"{name}_roughness.png"))

        # Paste into atlas
        col = idx % ATLAS_COLS
        row = idx // ATLAS_COLS
        pos = (col * TEXTURE_SIZE, row * TEXTURE_SIZE)

        atlas_albedo.paste(albedo, pos)
        atlas_normal.paste(normal, pos)
        atlas_roughness.paste(roughness, pos)
        print(f"[TEXTURE] Generated PBR maps for '{name}' at atlas cell ({col}, {row})")

    # Save Atlas
    atlas_albedo.save(os.path.join(OUTPUT_DIR, "voxel_atlas_albedo.png"))
    atlas_normal.save(os.path.join(OUTPUT_DIR, "voxel_atlas_normal.png"))
    atlas_roughness.save(os.path.join(OUTPUT_DIR, "voxel_atlas_roughness.png"))
    print(f"[ATLAS] Generated unified PBR atlas ({atlas_w}x{atlas_h}) at {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_all_textures()
