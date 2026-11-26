#!/usr/bin/env python3
"""
GitHub Aquarium Generator - 16-Bit Retro RPG Edition
Fetches rolling 365-day contributions from GitHub GraphQL API
and renders a self-contained 16-bit retro RPG pixel-art SVG.

XP Formula:
- 1 Contribution = 100 XP
- Total XP = total_contributions * 100
- Stage Brackets (Contributions):
  1. Baby:       0 - 24    (XP: 0 - 2,400,       Range: 25)
  2. Growing:    25 - 99   (XP: 2,500 - 9,900,   Range: 75)
  3. Advanced:   100 - 249 (XP: 10,000 - 24,900, Range: 150)
  4. Elite:      250 - 499 (XP: 25,000 - 49,900, Range: 250)
  5. Legendary:  500+      (XP: 50,000+,         Range: MAX)
- Level Formula: Level = max(1, total_contributions // 10 + 1)
- Stage Progress:
  - Inside stage: (contributions - stage_min) / (stage_max - stage_min + 1) * 100%
  - Legendary stage: 100% (MAX)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

STAGES = [
    {"name": "Baby", "min": 0, "max": 24, "title": "Tadpole Fry"},
    {"name": "Growing", "min": 25, "max": 99, "title": "Neon Tetra"},
    {"name": "Advanced", "min": 100, "max": 249, "title": "Crown Angelfish"},
    {"name": "Elite", "min": 250, "max": 499, "title": "Royal Sun-Betta"},
    {"name": "Legendary", "min": 500, "max": None, "title": "Leviathan Wyrm"},
]


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
        needed = 0
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


def render_matrix_svg(matrix: list, color_map: dict, ox: int, oy: int, px: int = 4) -> str:
    """Renders pixel matrix directly into grouped SVG rects, combining contiguous row spans."""
    rects = []
    for r_idx, row in enumerate(matrix):
        current_color = None
        start_c = 0
        span = 0
        for c_idx, ch in enumerate(row):
            col = color_map.get(ch)
            if col == current_color:
                if col is not None:
                    span += 1
            else:
                if current_color is not None and span > 0:
                    x = ox + (start_c * px)
                    y = oy + (r_idx * px)
                    rects.append(f'<rect x="{x}" y="{y}" width="{span * px}" height="{px}" fill="{current_color}" />')
                current_color = col
                start_c = c_idx
                span = 1 if col is not None else 0
        if current_color is not None and span > 0:
            x = ox + (start_c * px)
            y = oy + (r_idx * px)
            rects.append(f'<rect x="{x}" y="{y}" width="{span * px}" height="{px}" fill="{current_color}" />')
    return "\n      ".join(rects)


def build_fish_sprite(stage_index: int) -> str:
    """Returns handcrafted 16-bit RPG pixel sprites for each evolution stage."""
    # Stage 0: Baby Fry (Curious little hatchling with glowing fins and bright eye)
    if stage_index == 0:
        lines = [
            "......########......",
            "....##33333333##....",
            "...#337777777733#...",
            "..#37777777777773#..",
            ".#377WW77777777773#.",
            ".#77WB077777777777#.",
            "#377WBB778877775533#",
            "#377WB0778887755333#",
            "#377WW7777887755533#",
            ".#7777777777777777#.",
            ".#3777777777777773#.",
            "..#37777777777773#..",
            "...#337777777733#...",
            "....##33333333##....",
            "......########......",
        ]
        cmap = {
            "#": "#041526",  # dark pixel border
            "3": "#0ea5e9",  # ocean azure rim
            "7": "#2dd4bf",  # bright turquoise body
            "8": "#0d9488",  # scale shade
            "5": "#38bdf8",  # dorsal/tail fin
            "W": "#ffffff",  # eye outer
            "B": "#0284c7",  # iris
            "0": "#02111d",  # pupil
        }
        return render_matrix_svg(lines, cmap, ox=390, oy=145, px=7)

    # Stage 1: Growing Neon Tetra (Elongated body, striking vibrant stripes, fin rays)
    elif stage_index == 1:
        lines = [
            "........#####...........",
            ".......#55555#..........",
            "......#5533355#.........",
            ".....#553333355#..####..",
            "...##33333333333##5555#.",
            "..#33777777777777355555#",
            ".#377WW7777777777735555#",
            "#377WB077EEEEEEEE77#55#.",
            "#777WBB77EEEEEEEE777##..",
            "#777WB077888888887775#..",
            "#377WW777888888887755#..",
            ".#37777777777777775555#.",
            "..#3377777777777355555#.",
            "...##33333333333##5555#.",
            ".....#553333355#..####..",
            "......#5533355#.........",
            ".......#55555#..........",
            "........#####...........",
        ]
        cmap = {
            "#": "#031422",
            "3": "#0284c7",  # deep marine blue
            "7": "#22d3ee",  # radiant cyan
            "E": "#a5f3fc",  # glowing dorsal neon stripe
            "8": "#0891b2",  # ventral body tone
            "5": "#38bdf8",  # translucent tail plumage
            "W": "#ffffff",
            "B": "#0369a1",
            "0": "#010c17",
        }
        return render_matrix_svg(lines, cmap, ox=360, oy=125, px=6)

    # Stage 2: Advanced Crown Angelfish (Tall majestic silhouette, vertical zebra scales, flowing ribbons)
    elif stage_index == 2:
        lines = [
            ".............###...................",
            "............#555#..................",
            "...........#55E55#.................",
            "..........#55EEE55#................",
            ".........#55EE3EE55#...............",
            "........#55EE333EE55#..............",
            ".......#55EE33333EE55#...###.......",
            "......#333333333333333#.#555#......",
            "....##33777777777777733#55E55#.....",
            "...#3377WW777227772277735EEE55#....",
            "..#3777WB07722227222277735EE55#....",
            ".#37777WBB772222722227777#555#.....",
            "#377777WB07772277722777777###......",
            "#377777WW777722777227777775555#....",
            ".#3777777777222272222777755EEE5#...",
            "..#37777777722227222277755EEEEE5#..",
            "...#3377777772277722777355EEEEEE5#.",
            "....##33777777777777733#55EEEEEE5#.",
            "......#333333333333333#..#55EEEE5#.",
            ".......#55EE33333EE55#....#5555#...",
            "........#55EE333EE55#......####....",
            ".........#55EE3EE55#...............",
            "..........#55EEE55#................",
            "...........#55E55#.................",
            "............#555#..................",
            ".............###...................",
        ]
        cmap = {
            "#": "#02101e",
            "3": "#0369a1",  # royal navy rim
            "7": "#2dd4bf",  # emerald turquoise body
            "2": "#0f766e",  # deep teal vertical scale banding
            "5": "#38bdf8",  # crown fin base
            "E": "#e0f2fe",  # iridescent ribbon tips
            "W": "#ffffff",
            "B": "#0284c7",
            "0": "#020d18",
        }
        return render_matrix_svg(lines, cmap, ox=330, oy=90, px=6)

    # Stage 3: Elite Royal Sun-Betta (Voluminous layered fins, crest spikes, multi-layer scale armour)
    elif stage_index == 3:
        lines = [
            "..................#######...................",
            "................##EEEEE44##.................",
            "..............##EE333333344##...............",
            "............##EE3388888883344##...###.......",
            "..........##EE3388222222883344##.#555#......",
            "........##EE33882299999922883344#55E55#.....",
            "......##4433882299777777992288345EEE55#....",
            "....##44337777777777777777777733#5EE55#....",
            "..##44377WW7772277227722777777333#555#.....",
            ".#443777WB077222272227222777777333###......",
            "#4337777WBB77222272227222777777775555#.....",
            "#4377777WB077722777227722777777755EEE5#....",
            "#4377777WW77772277722772277777755EEEEE5#...",
            "#4337777777772222722272227777755EEEEEEE5#..",
            ".#44377777777222272227222777755EEEEEEEEE5#.",
            "..##4437777777227772277227773#55EEEEEEEEE5#",
            "....##443377777777777777777733#55EEEEEEE5#.",
            "......##4433882299777799228834#..#55EEEE5#..",
            "........##EE338822999922883344#...#5555#...",
            "..........##EE33882222883344##.....####....",
            "............##EE33888883344##...............",
            "..............##EE33333344##................",
            "................##EEEEE44##.................",
            "..................#######...................",
        ]
        cmap = {
            "#": "#010b14",
            "4": "#1e3a8a",  # deep royal navy mantle
            "3": "#0284c7",  # cyan crest spine
            "8": "#0e7490",  # outer fin gradient
            "2": "#0891b2",  # scale contrast
            "9": "#06b6d4",  # inner body ring
            "7": "#22d3ee",  # radiant cyan belly
            "5": "#38bdf8",  # voluminous trailing fin
            "E": "#a5f3fc",  # luminous electric tip highlights
            "W": "#ffffff",
            "B": "#0284c7",
            "0": "#01070e",
        }
        return render_matrix_svg(lines, cmap, ox=300, oy=85, px=6)

    # Stage 4: Legendary Leviathan Wyrm (Colossal mythical dragon fish, ornate horns, serpentine scales, celestial crest)
    else:
        lines = [
            ".......................########.......................",
            ".....................##44EEEE44##.....................",
            "...................##44EE3333EE44##...................",
            ".................##44EE33222233EE44##.................",
            "...............##44EE332288882233EE44##...###.........",
            ".............##44EE3322886666882233EE44#.#555#........",
            "...........##44EE33228866777766882233EE4#55E55#.......",
            ".........##44EE3322886677GGGG776688223345EEE55#......",
            ".......##44EE337777777777GGGG77777777333#5EE55#......",
            ".....##44EE377WW7772277GG2222GG7722777333#555#.......",
            "...##44EE3777WB07722227GG2222GG72222777333###........",
            "..#44EE377777WBB7722227GG2222GG72222777775555#.......",
            ".#44E37777777WB07772277GG2222GG77227777755EEE5#......",
            "#44E377777777WW77772277GG2222GG7722777755EEEEE5#.....",
            "#44E3777777777777722227GG2222GG722227755EEEEEEE5#....",
            ".#44E377777777777722227GG2222GG72222755EEEEEEEEE5#...",
            "..#44EE3777777777772277GG2222GG772273#55EEEEEEEEE5#..",
            "...##44EE37777777777777GG2222GG7777333#55EEEEEEEEE5#.",
            ".....##44EE33777777777777GGGG777777333##55EEEEEEEEE5#",
            ".......##44EE3322886677GGGG776688223344#.#55EEEEEEE5#",
            ".........##44EE33228866777766882233EE44#...#55EEEEE5#",
            "...........##44EE3322886666882233EE44##.....#55EEE5#.",
            ".............##44EE332288882233EE44##........#5555#..",
            "...............##44EE33222233EE44##...........####....",
            ".................##44EE3333EE44##.....................",
            "...................##44EEEE44##.......................",
            ".....................########.........................",
        ]
        cmap = {
            "#": "#01070e",
            "4": "#0f172a",  # abyss void contour
            "E": "#67e8f9",  # celestial star glow
            "3": "#0284c7",  # royal crest spine
            "2": "#059669",  # emerald jade dragon scale
            "8": "#047857",  # deep scale shadow
            "6": "#10b981",  # bright sea dragon flank
            "7": "#34d399",  # radiant dragon pearl body
            "G": "#a7f3d0",  # core divine luminescence
            "5": "#38bdf8",  # celestial wing tail
            "W": "#ffffff",
            "B": "#0284c7",
            "0": "#01050a",
        }
        return render_matrix_svg(lines, cmap, ox=240, oy=75, px=6)


def build_dithered_light_shafts() -> str:
    """Generates authentic 16-bit underwater light shafts using clustered pixel columns."""
    shaft_rects = []
    # Angled shaft 1 (Left-Center)
    col1 = [
        (160, 10, 40, 0.08), (170, 50, 46, 0.07), (182, 95, 52, 0.06),
        (196, 145, 58, 0.05), (212, 195, 64, 0.04), (230, 245, 70, 0.03)
    ]
    # Angled shaft 2 (Right-Center)
    col2 = [
        (480, 10, 50, 0.07), (495, 55, 56, 0.06), (512, 105, 62, 0.05),
        (530, 160, 68, 0.04), (550, 215, 74, 0.03), (572, 265, 80, 0.02)
    ]
    for x, y, w, op in col1 + col2:
        shaft_rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="45" fill="#38bdf8" opacity="{op}" />')
    return "\n    ".join(shaft_rects)


def build_reef_environment() -> str:
    """Renders multi-layer 16-bit RPG coral, rocks, sea grass, and sandbed."""
    elements = []

    # Layer 1: Background Deep Silhouettes (Dark Navy/Slate Blue)
    bg_kelp = [
        # Far left kelp
        (20, 110, 8, 190, "#08253d"), (28, 130, 6, 170, "#08253d"), (14, 160, 6, 140, "#061f33"),
        # Far right backdrop kelp
        (695, 120, 8, 180, "#08253d"), (705, 140, 6, 160, "#08253d"), (685, 170, 6, 130, "#061f33")
    ]
    for x, y, w, h, col in bg_kelp:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" />')

    # Layer 2: Midground Coral Formations & Rocks
    # Left Coral Reef Cluster
    coral_blocks_left = [
        (10, 230, 60, 80, "#0d3b66"), (14, 218, 48, 14, "#0f477a"),
        (22, 204, 32, 16, "#13548a"), (30, 192, 16, 14, "#17639e"),
        (58, 240, 40, 65, "#0b3359"), (66, 226, 26, 16, "#0e4170"),
        (90, 260, 36, 45, "#092947"), (96, 250, 22, 12, "#0c355c")
    ]
    # Right Coral Reef Cluster
    coral_blocks_right = [
        (640, 220, 90, 90, "#0d3b66"), (652, 206, 68, 16, "#0f477a"),
        (668, 192, 44, 16, "#13548a"), (680, 180, 24, 14, "#17639e"),
        (610, 245, 42, 62, "#0b3359"), (618, 232, 28, 15, "#0e4170"),
        (580, 268, 38, 40, "#092947"), (588, 258, 24, 12, "#0c355c")
    ]
    for x, y, w, h, col in coral_blocks_left + coral_blocks_right:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" />')

    # Layer 3: Vibrant Sea Anemone & Seaweed Tufts (Teal / Turquoise / Sky)
    seaweed = [
        # Left vibrant fronds
        (38, 160, 6, 50, "#0d9488"), (34, 175, 4, 35, "#14b8a6"),
        (48, 145, 6, 60, "#0f766e"), (54, 165, 4, 40, "#2dd4bf"),
        (76, 210, 6, 30, "#0e7490"), (82, 225, 4, 25, "#22d3ee"),
        # Right vibrant fronds
        (660, 150, 6, 55, "#0d9488"), (654, 165, 4, 40, "#14b8a6"),
        (674, 135, 6, 60, "#0f766e"), (680, 155, 4, 40, "#2dd4bf"),
        (630, 215, 6, 30, "#0e7490"), (624, 228, 4, 25, "#22d3ee")
    ]
    for x, y, w, h, col in seaweed:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" />')

    # Layer 4: Stepped Aquarium Substrate Floor (Sand + Shading + Shell Pixels)
    floor_steps = [
        (10, 298, 720, 6, "#081d33"),
        (10, 304, 720, 8, "#0c2847"),
        (10, 312, 720, 8, "#10345c"),
        (10, 320, 720, 10, "#143f6e"),
    ]
    for x, y, w, h, col in floor_steps:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" />')

    # Pebble & Sediment Pixels
    pebbles = [
        (60, 308, 10, 4, "#225b96"), (120, 314, 8, 4, "#225b96"), (190, 306, 12, 4, "#225b96"),
        (260, 312, 8, 4, "#225b96"), (340, 308, 14, 4, "#225b96"), (430, 316, 10, 4, "#225b96"),
        (510, 306, 8, 4, "#225b96"), (590, 312, 12, 4, "#225b96"), (670, 310, 10, 4, "#225b96"),
        # Highlights
        (62, 308, 4, 2, "#38bdf8"), (192, 306, 4, 2, "#38bdf8"), (344, 308, 6, 2, "#38bdf8"),
        (594, 312, 4, 2, "#38bdf8")
    ]
    for x, y, w, h, col in pebbles:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" />')

    return "\n    ".join(elements)


def build_ambient_bubbles() -> str:
    """Renders structured pixel bubble trails rising from the corals."""
    bubbles = [
        # Left coral cluster bubble stream
        (48, 140, 4, 4, "#a5f3fc", 0.6), (46, 115, 6, 6, "#38bdf8", 0.7),
        (50, 85, 4, 4, "#e0f2fe", 0.8), (48, 55, 6, 6, "#a5f3fc", 0.7),
        (52, 30, 4, 4, "#38bdf8", 0.6),
        # Right coral cluster bubble stream
        (668, 130, 4, 4, "#a5f3fc", 0.6), (672, 105, 6, 6, "#38bdf8", 0.7),
        (666, 75, 6, 6, "#e0f2fe", 0.8), (670, 45, 4, 4, "#a5f3fc", 0.7),
        (668, 25, 4, 4, "#38bdf8", 0.6),
        # Idle deep tank bubbles
        (210, 210, 4, 4, "#38bdf8", 0.4), (214, 185, 6, 6, "#7dd3fc", 0.5),
        (520, 195, 4, 4, "#38bdf8", 0.4), (516, 170, 6, 6, "#7dd3fc", 0.5)
    ]
    res = []
    for x, y, w, h, col, op in bubbles:
        res.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity="{op}" />')
    return "\n    ".join(res)


def build_rpg_hud(info: dict) -> str:
    """Renders authentic 16-bit RPG cartridge quest/status box."""
    bar_width = int(216 * (info["progress_pct"] / 100.0))

    hud_svg = f"""
    <!-- RPG Outer Frame (Chiseled 16-Bit Border) -->
    <rect x="22" y="22" width="256" height="106" fill="#030c17" />
    <rect x="20" y="20" width="260" height="2" fill="#0f3d63" />
    <rect x="20" y="126" width="260" height="2" fill="#021422" />
    <rect x="20" y="20" width="2" height="108" fill="#0f3d63" />
    <rect x="278" y="20" width="2" height="108" fill="#021422" />

    <!-- Inset Frame Bevel -->
    <rect x="24" y="24" width="252" height="102" fill="#06182c" />
    <rect x="26" y="26" width="248" height="98" fill="#020d1a" />

    <!-- Gold-Gilded RPG Header Banner -->
    <rect x="30" y="30" width="240" height="18" fill="#082845" />
    <text x="36" y="43" fill="#38bdf8" font-size="10" font-weight="bold" letter-spacing="1">STAGE {info["stage_index"] + 1}: {info["stage"].upper()}</text>
    <text x="264" y="43" text-anchor="end" fill="#2dd4bf" font-size="10" font-weight="bold">LVL {info["level"]}</text>

    <!-- Companion Species Title -->
    <text x="36" y="61" fill="#f8fafc" font-size="12" font-weight="bold">{info["title"]}</text>

    <!-- Gauge Bevel Inset -->
    <rect x="36" y="69" width="228" height="12" fill="#01070e" />
    <rect x="36" y="69" width="228" height="1" fill="#031b2e" />
    <rect x="36" y="80" width="228" height="1" fill="#09385c" />
    
    <!-- Animated XP Energy Fill -->
    <rect x="38" y="71" width="{bar_width}" height="8" fill="url(#hudXpGrad)" />

    <!-- RPG Stat Data Insets -->
    <g font-size="9" font-family="'Courier New',Courier,monospace">
      <text x="36" y="99" fill="#94a3b8">XP</text>
      <text x="56" y="99" fill="#38bdf8" font-weight="bold">{info["xp"]:,}</text>
      
      <text x="120" y="99" fill="#94a3b8">YEAR</text>
      <text x="150" y="99" fill="#38bdf8" font-weight="bold">{info["contributions"]:,}</text>

      <!-- Quest Next Goal Bracket -->
      <text x="36" y="114" fill="#64748b">NEXT:</text>
      <text x="68" y="114" fill="#a5f3fc" font-weight="bold">{info["next_bracket"]}</text>
      <text x="264" y="114" text-anchor="end" fill="#2dd4bf" font-weight="bold">{int(info["progress_pct"])}%</text>
    </g>
    """
    return hud_svg


def generate_svg(info: dict) -> str:
    fish_svg = build_fish_sprite(info["stage_index"])
    light_shafts = build_dithered_light_shafts()
    reef_decor = build_reef_environment()
    bubbles = build_ambient_bubbles()
    hud_svg = build_rpg_hud(info)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 340" width="100%" height="100%" shape-rendering="crispEdges" style="background:#020813; border-radius:8px; font-family:'Courier New',Courier,monospace;">
  <defs>
    <!-- Deep Oceanic Abyss Gradient -->
    <linearGradient id="abyssWater" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a2540" />
      <stop offset="45%" stop-color="#05162a" />
      <stop offset="85%" stop-color="#020c18" />
      <stop offset="100%" stop-color="#01060e" />
    </linearGradient>

    <!-- HUD Gauge Gradient -->
    <linearGradient id="hudXpGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0369a1" />
      <stop offset="60%" stop-color="#06b6d4" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
  </defs>

  <!-- Chiseled Cabinet Outer Frame -->
  <rect x="0" y="0" width="740" height="340" fill="#020813" />
  <rect x="2" y="2" width="736" height="336" fill="#071a2e" />
  <rect x="6" y="6" width="728" height="328" fill="#04101e" />

  <!-- Inner Water Volume -->
  <rect x="10" y="10" width="720" height="320" fill="url(#abyssWater)" />

  <!-- 16-Bit Atmospheric Light Shafts -->
  <g id="light-shafts">
    {light_shafts}
  </g>

  <!-- Pixel Waterline Shimmer -->
  <g fill="#38bdf8" opacity="0.35">
    <rect x="14" y="12" width="28" height="2" />
    <rect x="52" y="12" width="44" height="2" />
    <rect x="106" y="12" width="36" height="2" />
    <rect x="154" y="12" width="56" height="2" />
    <rect x="220" y="12" width="40" height="2" />
    <rect x="270" y="12" width="68" height="2" />
    <rect x="350" y="12" width="50" height="2" />
    <rect x="412" y="12" width="72" height="2" />
    <rect x="496" y="12" width="46" height="2" />
    <rect x="554" y="12" width="60" height="2" />
    <rect x="626" y="12" width="48" height="2" />
    <rect x="684" y="12" width="38" height="2" />
  </g>

  <!-- Multi-Layered Coral Reef & Ocean Bed -->
  <g id="reef-environment">
    {reef_decor}
  </g>

  <!-- Ambient Rising Bubbles -->
  <g id="bubbles">
    {bubbles}
  </g>

  <!-- Hero Companion Fish (Dominant Visual Anchor) -->
  <g id="companion-fish">
    {fish_svg}
  </g>

  <!-- 16-Bit RPG HUD Panel -->
  <g id="rpg-hud">
    {hud_svg}
  </g>
</svg>
"""
    return svg_content.strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Aquarium SVG based on yearly contributions.")
    parser.add_argument("--contributions", type=int, default=None, help="Explicit contribution count for local preview")
    parser.add_argument("--output", type=str, default="assets/aquarium.svg", help="Path to output SVG file")
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
    svg_code = generate_svg(info)

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_code)

    print(f"Generated Aquarium: {info['stage']} (Level {info['level']}, {info['contributions']} contributions, {info['xp']} XP) -> {args.output}")


if __name__ == "__main__":
    main()
