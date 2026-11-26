#!/usr/bin/env python3
"""
GitHub Aquarium Generator — Professional Pixel-Art Edition
Composes high-detail CC0 pixel-art assets (Ansimuz & Kenney) using Python Pillow.
Renders a 960x540 PNG with multi-layer depth, authentic pixel anatomy, and retro RPG HUD.

XP Formula:
- 1 Contribution = 100 XP
- Total XP = total_contributions * 100
- Stage Brackets (Contributions):
  1. Baby:       0 - 24    (XP: 0 - 2,400)
  2. Growing:    25 - 99   (XP: 2,500 - 9,900)
  3. Advanced:   100 - 249 (XP: 10,000 - 24,900)
  4. Elite:      250 - 499 (XP: 25,000 - 49,900)
  5. Legendary:  500+      (XP: 50,000+)
- Level Formula: Level = max(1, total_contributions // 10 + 1)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

from pixel_species import (
    get_azure_fry, get_sapphire_tetra, get_crown_discus,
    get_imperial_betta, get_celestial_leviathan,
)

STAGES = [
    {"name": "Baby", "min": 0, "max": 24, "title": "Azure Fry"},
    {"name": "Growing", "min": 25, "max": 99, "title": "Sapphire Tetra"},
    {"name": "Advanced", "min": 100, "max": 249, "title": "Crown Discus"},
    {"name": "Elite", "min": 250, "max": 499, "title": "Imperial Betta"},
    {"name": "Legendary", "min": 500, "max": None, "title": "Celestial Leviathan"},
]

CANVAS_W = 960
CANVAS_H = 540


def calculate_progress(contributions: int):
    xp = contributions * 100
    level = max(1, (contributions // 10) + 1)

    current_stage = STAGES[0]
    stage_index = 0
    for idx, stage in enumerate(STAGES):
        if stage["max"] is None:
            if contributions >= stage["min"]:
                current_stage = stage
                stage_index = idx
                break
        elif stage["min"] <= contributions <= stage["max"]:
            current_stage = stage
            stage_index = idx
            break

    if current_stage["max"] is None:
        pct = 100.0
        next_bracket = "MAX RANK"
    else:
        span = current_stage["max"] - current_stage["min"] + 1
        curr = contributions - current_stage["min"]
        pct = min(100.0, max(0.0, (curr / span) * 100.0))
        needed = (current_stage["max"] + 1) - contributions
        next_bracket = f"{needed} to {STAGES[stage_index + 1]['name']}"

    return {
        "contributions": contributions,
        "xp": xp,
        "level": level,
        "stage": current_stage["name"],
        "title": current_stage["title"],
        "stage_index": stage_index,
        "progress_pct": pct,
        "next_bracket": next_bracket,
    }


def fetch_contributions_graphql(username: str, token: str) -> int:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    url = "https://api.github.com/graphql"
    payload = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "GitHub-Aquarium-Generator",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode("utf-8"))
            if "errors" in data:
                raise RuntimeError(f"GraphQL error: {data['errors']}")
            total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
            return int(total)
    except urllib.error.URLError as err:
        raise RuntimeError(f"Failed to fetch contributions from GitHub: {err}")


def load_sprite(rel_path: str, scale: float = 1.0, flip_x: bool = False) -> Image.Image:
    """Loads a PNG sprite, converts to RGBA, and scales using NEAREST point filtering."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, "assets", "sprites", rel_path)
    im = Image.open(full_path).convert("RGBA")
    if flip_x:
        im = ImageOps.mirror(im)
    if scale != 1.0:
        nw = max(1, int(im.width * scale))
        nh = max(1, int(im.height * scale))
        im = im.resize((nw, nh), resample=Image.Resampling.NEAREST)
    return im


def tint_sprite(im: Image.Image, color_mult: tuple) -> Image.Image:
    """Tints sprite pixels for color harmony while preserving alpha channel."""
    r_m, g_m, b_m = color_mult
    r, g, b, a = im.split()
    r = r.point(lambda p: min(255, int(p * r_m)))
    g = g.point(lambda p: min(255, int(p * g_m)))
    b = b.point(lambda p: min(255, int(p * b_m)))
    return Image.merge("RGBA", (r, g, b, a))


def draw_hud(im: Image.Image, info: dict):
    """Renders authentic 16-bit RPG status dialogue box onto the image canvas."""
    draw = ImageDraw.Draw(im, "RGBA")
    
    # Outer RPG Frame Box (top-left)
    ox, oy, w, h = 32, 28, 320, 118
    # Dark chassis
    draw.rectangle([ox, oy, ox + w, oy + h], fill=(2, 8, 18, 235), outline=(12, 45, 78, 255), width=2)
    # Inner border line
    draw.rectangle([ox + 4, oy + 4, ox + w - 4, oy + h - 4], outline=(5, 24, 46, 255), width=2)
    # Bevel highlight top-left
    draw.line([ox + 2, oy + 2, ox + w - 2, oy + 2], fill=(40, 120, 180, 200), width=1)
    draw.line([ox + 2, oy + 2, ox + 2, oy + h - 2], fill=(40, 120, 180, 200), width=1)

    # Header Ribbon
    draw.rectangle([ox + 8, oy + 8, ox + w - 8, oy + 28], fill=(6, 32, 58, 255))
    
    # Fonts: system standard mono or fallback
    font_bold = None
    font_small = None
    try:
        font_bold = ImageFont.truetype("courbd.ttf", 13)
        font_small = ImageFont.truetype("cour.ttf", 11)
        font_title = ImageFont.truetype("courbd.ttf", 15)
    except:
        try:
            font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 12)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 10)
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
        except:
            font_bold = ImageFont.load_default()
            font_small = font_bold
            font_title = font_bold

    # Stage Badge & Level
    stage_text = f"STAGE {info['stage_index'] + 1}: {info['stage'].upper()}"
    lvl_text = f"LVL {info['level']}"
    draw.text((ox + 14, oy + 11), stage_text, fill=(56, 189, 248), font=font_bold)
    draw.text((ox + w - 58, oy + 11), lvl_text, fill=(45, 212, 191), font=font_bold)

    # Companion Species Title
    draw.text((ox + 14, oy + 36), info["title"], fill=(241, 245, 249), font=font_title)

    # Progress XP Bar
    bar_x = ox + 14
    bar_y = oy + 60
    bar_w = w - 28
    bar_h = 12
    # Inset background
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(1, 6, 14, 255), outline=(10, 48, 80, 255), width=1)
    # Energy fill
    fill_w = max(0, int((bar_w - 4) * (info["progress_pct"] / 100.0)))
    if fill_w > 0:
        draw.rectangle([bar_x + 2, bar_y + 2, bar_x + 2 + fill_w, bar_y + bar_h - 2], fill=(34, 211, 238, 255))
        # Highlight gloss line
        draw.line([bar_x + 2, bar_y + 2, bar_x + 2 + fill_w, bar_y + 2], fill=(165, 243, 252, 255), width=1)

    # Numeric Metrics Row
    xp_text = f"XP: {info['xp']:,}"
    year_text = f"YEAR: {info['contributions']:,}"
    draw.text((ox + 14, oy + 80), xp_text, fill=(148, 163, 184), font=font_small)
    draw.text((ox + 130, oy + 80), year_text, fill=(148, 163, 184), font=font_small)

    # Evolution Goal Row
    goal_text = f"NEXT: {info['next_bracket']}"
    pct_text = f"{int(info['progress_pct'])}%"
    draw.text((ox + 14, oy + 98), goal_text, fill=(103, 232, 249), font=font_small)
    draw.text((ox + w - 46, oy + 98), pct_text, fill=(45, 212, 191), font=font_small)


def render_hero_fish(canvas: Image.Image, sprite: Image.Image, position: tuple[int, int], scale: int, glow_color: tuple[int, int, int]):
    """Draw pixel-sharp hero with a one-pixel outline and subtle ambient glow."""
    fish = sprite.resize((sprite.width * scale, sprite.height * scale), Image.Resampling.NEAREST)
    pad = 12
    mask = Image.new("L", (fish.width + 2 * pad, fish.height + 2 * pad), 0)
    mask.paste(fish.getchannel("A"), (pad, pad))
    glow = mask.filter(ImageFilter.GaussianBlur(4)).point(lambda value: min(48, value // 4))
    layer = Image.new("RGBA", mask.size, (*glow_color, 0))
    layer.putalpha(glow)
    canvas.alpha_composite(layer, (position[0] - pad, position[1] - pad))
    border = mask.filter(ImageFilter.MaxFilter(3))
    original = Image.new("L", mask.size, 0)
    original.paste(fish.getchannel("A"), (pad, pad))
    border = Image.eval(border, lambda value: 255 if value else 0)
    border = Image.frombytes("L", mask.size, bytes(
        0 if original.getpixel((x, y)) else border.getpixel((x, y))
        for y in range(mask.height) for x in range(mask.width)
    ))
    outline = Image.new("RGBA", mask.size, (5, 15, 28, 255))
    outline.putalpha(border)
    canvas.alpha_composite(outline, (position[0] - pad, position[1] - pad))
    canvas.alpha_composite(fish, position)


def render_aquarium_image(info: dict, out_path: str):
    """Composes multi-layered retro pixel art underwater environment."""
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (2, 8, 20, 255))

    # 1. LAYER 1: Background Gradient & Submerged Horizon
    bg_tile = load_sprite("sub_bg.png")
    bg_scaled = bg_tile.resize((CANVAS_W, CANVAS_H), resample=Image.Resampling.NEAREST)
    canvas.paste(bg_scaled, (0, 0))

    # Midground Silhouette Ridge
    midground = load_sprite("sub_mid.png")
    # Scale midground to span full width
    mg_scale = CANVAS_W / midground.width
    mg_h = int(midground.height * mg_scale)
    mg_scaled = midground.resize((CANVAS_W, mg_h), resample=Image.Resampling.NEAREST)
    mg_y = CANVAS_H - mg_h - 40
    # Blend with oceanic depth alpha
    mg_tinted = tint_sprite(mg_scaled, (0.5, 0.7, 0.9))
    canvas.alpha_composite(mg_tinted, (0, mg_y))

    # Dithered Sun Rays / Light Shafts
    overlay_rays = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    ray_draw = ImageDraw.Draw(overlay_rays, "RGBA")
    ray_polys = [
        ([(160, 0), (230, 0), (320, CANVAS_H), (210, CANVAS_H)], (56, 189, 248, 22)),
        ([(500, 0), (580, 0), (710, CANVAS_H), (600, CANVAS_H)], (34, 211, 238, 18)),
        ([(750, 0), (810, 0), (940, CANVAS_H), (860, CANVAS_H)], (56, 189, 248, 14)),
    ]
    for poly, color in ray_polys:
        ray_draw.polygon(poly, fill=color)
    canvas.alpha_composite(overlay_rays, (0, 0))

    # 2. LAYER 2: Background Biota (Distant Schooling Fish & Translucent Jellyfish)
    # High-swimming translucent jellyfish
    jelly1 = load_sprite("jelly_fish_1.png", scale=2.0)
    canvas.alpha_composite(jelly1, (740, 90))
    jelly2 = load_sprite("jelly_fish_2.png", scale=1.5)
    canvas.alpha_composite(jelly2, (260, 160))

    # Small schooling minnows (dart fish) cruising in background light beam
    dart1 = load_sprite("dart_fish_1.png", scale=2.0, flip_x=False)
    canvas.alpha_composite(dart1, (620, 140))
    dart2 = load_sprite("dart_fish_2.png", scale=1.8, flip_x=False)
    canvas.alpha_composite(dart2, (660, 120))
    dart3 = load_sprite("dart_fish_1.png", scale=1.7, flip_x=False)
    canvas.alpha_composite(dart3, (700, 155))

    # 3. LAYER 3: Midground Coral Formations & Rocks
    # Massive left coral reef base
    coral_left = load_sprite("coral_2.png", scale=0.75)
    canvas.alpha_composite(coral_left, (0, CANVAS_H - coral_left.height))

    # Midground rock outcrop (Kenney)
    rock_mid = load_sprite("kenney_rock_a.png", scale=1.6)
    canvas.alpha_composite(rock_mid, (120, CANVAS_H - rock_mid.height + 15))

    # Right massive shelf coral
    coral_right = load_sprite("coral_3.png", scale=0.75, flip_x=True)
    canvas.alpha_composite(coral_right, (CANVAS_W - coral_right.width, CANVAS_H - coral_right.height))

    # 4. LAYER 4: Sea Anemones, Seaweed & Flora
    # Left animated-style sea plants
    plant1 = load_sprite("plant_3_1.png", scale=1.8)
    canvas.alpha_composite(plant1, (45, CANVAS_H - plant1.height - 25))
    plant2 = load_sprite("plant_1.png", scale=2.2)
    canvas.alpha_composite(plant2, (150, CANVAS_H - plant2.height - 10))

    # Right vibrant kelp & seaweed
    seaweed_r1 = load_sprite("kenney_seaweed_green_a.png", scale=2.0)
    canvas.alpha_composite(seaweed_r1, (780, CANVAS_H - seaweed_r1.height + 20))
    seaweed_r2 = load_sprite("kenney_seaweed_orange_a.png", scale=1.8)
    canvas.alpha_composite(seaweed_r2, (840, CANVAS_H - seaweed_r2.height + 15))

    # 5. LAYER 5: Hand-crafted hero fish, unique anatomy per evolution
    stage_idx = info["stage_index"]
    hero_designs = [
        (get_azure_fry, 3, (0.51, 0.49), (85, 205, 240)),
        (get_sapphire_tetra, 2, (0.49, 0.47), (50, 190, 245)),
        (get_crown_discus, 2, (0.48, 0.43), (55, 215, 215)),
        (get_imperial_betta, 2, (0.47, 0.44), (170, 90, 220)),
        (get_celestial_leviathan, 2, (0.44, 0.46), (60, 205, 220)),
    ]
    sprite_fn, hero_scale, anchor, glow_color = hero_designs[stage_idx]
    hero_fish = sprite_fn()
    hero_w, hero_h = hero_fish.width * hero_scale, hero_fish.height * hero_scale
    hx = int(CANVAS_W * anchor[0] - hero_w / 2)
    hy = int(CANVAS_H * anchor[1] - hero_h / 2)
    render_hero_fish(canvas, hero_fish, (hx, hy), hero_scale, glow_color)

    # 6. LAYER 6: Foreground Rocks, Gravel Bed, Bubbles & Small Biota
    # Bottom Substrate Sandbed
    sand_overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sand_overlay, "RGBA")
    s_draw.rectangle([0, CANVAS_H - 24, CANVAS_W, CANVAS_H], fill=(6, 20, 38, 255))
    s_draw.rectangle([0, CANVAS_H - 32, CANVAS_W, CANVAS_H - 24], fill=(9, 30, 56, 230))
    s_draw.rectangle([0, CANVAS_H - 38, CANVAS_W, CANVAS_H - 32], fill=(13, 44, 78, 160))
    canvas.alpha_composite(sand_overlay, (0, 0))

    # Secondary Biota: Bottom Dwelling Cleaner Fish on substrate
    bottom_fish = load_sprite("def_fish_1.png", scale=1.7, flip_x=True)
    canvas.alpha_composite(bottom_fish, (480, CANVAS_H - 58))

    # Rising Pixel Bubble Streams (Ansimuz & Kenney)
    bub1 = load_sprite("kenney_bubble_a.png", scale=0.35)
    canvas.alpha_composite(bub1, (110, 180))
    canvas.alpha_composite(bub1, (125, 120))
    canvas.alpha_composite(bub1, (115, 60))

    bub2 = load_sprite("kenney_bubble_b.png", scale=0.4)
    canvas.alpha_composite(bub2, (830, 160))
    canvas.alpha_composite(bub2, (815, 95))
    canvas.alpha_composite(bub2, (835, 40))

    # Hero Fish Breath Bubbles
    hero_bub = load_sprite("kenney_bubble_a.png", scale=0.25)
    canvas.alpha_composite(hero_bub, (hx + hero_fish.width - 20, hy + 15))
    canvas.alpha_composite(hero_bub, (hx + hero_fish.width - 10, hy - 5))

    # 7. LAYER 7: 16-Bit RPG HUD
    draw_hud(canvas, info)

    # 8. Cabinet Glass Border & Pixel Bevel
    frame_overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(frame_overlay, "RGBA")
    # Outer dark chassis
    f_draw.rectangle([0, 0, CANVAS_W - 1, CANVAS_H - 1], outline=(3, 10, 22, 255), width=6)
    f_draw.rectangle([6, 6, CANVAS_W - 7, CANVAS_H - 7], outline=(14, 45, 78, 255), width=2)
    # Shimmer waterline at top
    f_draw.line([8, 8, CANVAS_W - 8, 8], fill=(56, 189, 248, 120), width=2)
    canvas.alpha_composite(frame_overlay, (0, 0))

    # Save finalized PNG
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    canvas.save(out_path, format="PNG", optimize=True)


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Aquarium PNG based on yearly contributions.")
    parser.add_argument("--contributions", type=int, default=None, help="Explicit contribution count for local preview")
    parser.add_argument("--output", type=str, default="assets/aquarium.png", help="Path to output PNG file")
    args = parser.parse_args()

    contributions = args.contributions

    if contributions is None:
        username = os.environ.get("GITHUB_USERNAME")
        token = os.environ.get("AQUARIUM_TOKEN")
        if not username or not token:
            print("Notice: GITHUB_USERNAME or AQUARIUM_TOKEN missing. Falling back to default preview (120 contributions).", file=sys.stderr)
            contributions = 120
        else:
            try:
                contributions = fetch_contributions_graphql(username, token)
            except Exception as err:
                print(f"Error fetching contributions: {err}", file=sys.stderr)
                sys.exit(1)

    info = calculate_progress(contributions)
    render_aquarium_image(info, args.output)

    print(f"Generated Aquarium: {info['stage']} (Level {info['level']}, {info['contributions']} contributions, {info['xp']} XP) -> {args.output}")


if __name__ == "__main__":
    main()
