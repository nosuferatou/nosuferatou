#!/usr/bin/env python3
"""
GitHub Aquarium Generator
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
    {"name": "Baby", "min": 0, "max": 24, "title": "Tiny Guppy"},
    {"name": "Growing", "min": 25, "max": 99, "title": "Reef Tetra"},
    {"name": "Advanced", "min": 100, "max": 249, "title": "Azure Angelfish"},
    {"name": "Elite", "min": 250, "max": 499, "title": "Abyssal Betta"},
    {"name": "Legendary", "min": 500, "max": None, "title": "Leviathan Wyrm"},
]


def calculate_progress(contributions: int):
    # ponytail: stage list holds 5 fixed ranks; upgrade to dynamic rank table if config-driven
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
        next_bracket = "MAX LEVEL"
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


def render_pixel_grid(grid_str: str, color_map: dict, origin_x: int, origin_y: int, px_size: int = 4) -> str:
    """Renders ASCII matrix into grouped SVG rects."""
    lines = [line.strip() for line in grid_str.strip().splitlines() if line.strip()]
    rects = []
    for r_idx, line in enumerate(lines):
        for c_idx, ch in enumerate(line):
            if ch in color_map and color_map[ch]:
                color = color_map[ch]
                x = origin_x + (c_idx * px_size)
                y = origin_y + (r_idx * px_size)
                rects.append(f'<rect x="{x}" y="{y}" width="{px_size}" height="{px_size}" fill="{color}" />')
    return "\n      ".join(rects)


def build_fish_svg(stage_index: int) -> str:
    # 5 Handcrafted distinct pixel sprites with recognizable eye, fins, scales, and tail
    if stage_index == 0:
        # Stage 1: Baby Guppy (12x9)
        grid = """
        ..####......
        .##777##....
        #7711777#...
        #77017777##.
        #7711775555#
        #7777777##..
        .##777##....
        ...####.....
        """
        cmap = {
            "#": "#0b2e4f",  # dark navy outline
            "7": "#2fe6d8",  # turquoise body
            "5": "#1aa5c8",  # mid fin
            "1": "#f5faff",  # sclera / eye highlight
            "0": "#051626",  # pupil
        }
        return render_pixel_grid(grid, cmap, origin_x=340, origin_y=165, px_size=5)

    elif stage_index == 1:
        # Stage 2: Reef Tetra (16x11)
        grid = """
        ....####........
        ...#5555#.......
        ..#777777#..##..
        .#77117777##55#.
        #77701788777555#
        #77711788877555#
        #77777778877555#
        .#77777777##55#.
        ..#777777#..##..
        ...#5555#.......
        ....####........
        """
        cmap = {
            "#": "#07203b",
            "7": "#2ce8c5",  # bright seafoam
            "8": "#0ea5b7",  # scale stripe
            "5": "#38bdf8",  # sky dorsal/ventral fin
            "1": "#f0fdfa",
            "0": "#041424",
        }
        return render_pixel_grid(grid, cmap, origin_x=320, origin_y=155, px_size=5)

    elif stage_index == 2:
        # Stage 3: Azure Angelfish (20x15)
        grid = """
        .......###..........
        ......#333#.........
        .....#33993#........
        ....#3399993#.......
        ...#339999993#......
        ..#77777777777#..##.
        .#7711772277777##33#
        #777017222272277733#
        #777117722772277733#
        .#7777777722777##33#
        ..#77777777777#..##.
        ...#339999993#......
        ....#3399993#.......
        .....#33993#........
        ......#333#.........
        """
        cmap = {
            "#": "#051b30",
            "7": "#38efc9",  # luminous mint
            "2": "#0284c7",  # deep cyan scale pattern
            "3": "#00f0ff",  # electric cyan fin rim
            "9": "#0369a1",  # deep fin body
            "1": "#ffffff",
            "0": "#02111f",
        }
        return render_pixel_grid(grid, cmap, origin_x=300, origin_y=135, px_size=5)

    elif stage_index == 3:
        # Stage 4: Abyssal Betta (24x17)
        grid = """
        .........######.........
        .......##444444##.......
        .....##4433333344##.....
        ...##44336666663344##...
        ..#777777777777777777#..
        .#77117766776677667777##
        #77701776677667766777744
        #77711766667666676677744
        #77777776677667766777744
        .#77777777777777777777##
        ..#777777667766776677#..
        ...##44336666663344##...
        .....##4433333344##.....
        .......##444444##.......
        .........######.........
        ..........####..........
        .........######.........
        """
        cmap = {
            "#": "#031526",
            "7": "#22d3ee",  # radiant cyan
            "6": "#0891b2",  # scale contrast
            "3": "#38bdf8",  # crown fin light
            "4": "#1d4ed8",  # royal abyssal blue
            "1": "#ffffff",
            "0": "#010811",
        }
        return render_pixel_grid(grid, cmap, origin_x=280, origin_y=125, px_size=5)

    else:
        # Stage 5: Legendary Leviathan Wyrm (28x18)
        grid = """
        ............########............
        ..........##44444444##..........
        ........##446666666644##........
        ......##4466333333336644##......
        ....##44663322222222336644##....
        ..##888888888888888888888888##..
        .#8811883388338833883388888888#.
        #888018833883388338833888888888#
        #888118333383333833338888888888#
        #888888833883388338833888888888#
        .#8888888888888888888888888888#.
        ..##888833883388338833888888##..
        ....##44663322222222336644##....
        ......##4466333333336644##......
        ........##446666666644##........
        ..........##44444444##..........
        ............########............
        .............######.............
        """
        cmap = {
            "#": "#020b14",
            "8": "#34d399",  # jade / legendary aqua
            "3": "#38bdf8",  # dragon crest light
            "2": "#a7f3d0",  # mystic core
            "6": "#059669",  # deep sea emerald
            "4": "#0284c7",  # azure crown
            "1": "#ffffff",
            "0": "#010408",
        }
        return render_pixel_grid(grid, cmap, origin_x=260, origin_y=120, px_size=5)


def generate_svg(info: dict) -> str:
    fish_svg = build_fish_svg(info["stage_index"])

    # Progress bar width calculation (HUD: width 240 max)
    bar_width = int(240 * (info["progress_pct"] / 100.0))

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 340" width="100%" height="100%" style="background:#050c18; border-radius:8px; font-family:'Courier New',Courier,monospace;">
  <defs>
    <!-- Underwater Depth Gradient -->
    <linearGradient id="tankWater" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a1931" />
      <stop offset="60%" stop-color="#061224" />
      <stop offset="100%" stop-color="#030813" />
    </linearGradient>

    <!-- Caustic Light Pattern -->
    <linearGradient id="caustic" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.0" />
      <stop offset="25%" stop-color="#38bdf8" stop-opacity="0.08" />
      <stop offset="50%" stop-color="#22d3ee" stop-opacity="0.02" />
      <stop offset="75%" stop-color="#38bdf8" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0" />
    </linearGradient>

    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#22d3ee" />
    </linearGradient>
  </defs>

  <!-- Tank Outer Frame -->
  <rect x="2" y="2" width="736" height="336" rx="6" fill="#040b16" stroke="#0e2a47" stroke-width="4" />

  <!-- Inner Water -->
  <rect x="10" y="10" width="720" height="320" rx="4" fill="url(#tankWater)" />

  <!-- Caustic top shimmer -->
  <rect x="10" y="10" width="720" height="40" fill="url(#caustic)" />

  <!-- Subtle Pixel Waterline -->
  <g fill="#164e63" opacity="0.6">
    <rect x="14" y="14" width="24" height="2" />
    <rect x="46" y="14" width="36" height="2" />
    <rect x="90" y="14" width="28" height="2" />
    <rect x="126" y="14" width="44" height="2" />
    <rect x="178" y="14" width="30" height="2" />
    <rect x="216" y="14" width="50" height="2" />
    <rect x="274" y="14" width="40" height="2" />
    <rect x="322" y="14" width="60" height="2" />
    <rect x="390" y="14" width="40" height="2" />
    <rect x="438" y="14" width="54" height="2" />
    <rect x="500" y="14" width="32" height="2" />
    <rect x="540" y="14" width="46" height="2" />
    <rect x="594" y="14" width="38" height="2" />
    <rect x="640" y="14" width="50" height="2" />
    <rect x="698" y="14" width="24" height="2" />
  </g>

  <!-- Aquatic Bed: Seabed and Sand Pixels -->
  <rect x="10" y="306" width="720" height="24" fill="#091a2f" />
  <g fill="#132e4f">
    <rect x="10" y="302" width="720" height="4" />
    <rect x="24" y="298" width="80" height="4" />
    <rect x="140" y="298" width="110" height="4" />
    <rect x="280" y="298" width="70" height="4" />
    <rect x="380" y="298" width="90" height="4" />
    <rect x="500" y="298" width="130" height="4" />
    <rect x="650" y="298" width="70" height="4" />
  </g>
  <g fill="#1e436d">
    <rect x="40" y="312" width="8" height="4" />
    <rect x="90" y="318" width="12" height="4" />
    <rect x="180" y="314" width="6" height="4" />
    <rect x="250" y="320" width="10" height="4" />
    <rect x="330" y="312" width="8" height="4" />
    <rect x="420" y="316" width="12" height="4" />
    <rect x="530" y="314" width="8" height="4" />
    <rect x="620" y="318" width="10" height="4" />
    <rect x="680" y="312" width="8" height="4" />
  </g>

  <!-- Pixel Aquarium Plants: Left Clump -->
  <g fill="#0e7490">
    <!-- Tall Grass Stem 1 -->
    <rect x="30" y="250" width="6" height="52" />
    <rect x="34" y="210" width="6" height="40" />
    <rect x="38" y="170" width="6" height="40" />
    <rect x="42" y="150" width="6" height="20" />
    <!-- Grass Stem 2 -->
    <rect x="50" y="260" width="6" height="42" />
    <rect x="54" y="220" width="6" height="40" />
    <rect x="50" y="190" width="6" height="30" />
    <!-- Small Shrub -->
    <rect x="66" y="276" width="6" height="26" />
    <rect x="72" y="282" width="6" height="20" />
  </g>
  <g fill="#155e75">
    <rect x="26" y="264" width="4" height="38" />
    <rect x="46" y="270" width="4" height="32" />
    <rect x="62" y="286" width="4" height="16" />
  </g>

  <!-- Pixel Aquarium Plants: Right Clump -->
  <g fill="#0e7490">
    <rect x="680" y="240" width="6" height="62" />
    <rect x="674" y="200" width="6" height="40" />
    <rect x="670" y="160" width="6" height="40" />
    <rect x="666" y="140" width="6" height="20" />
    <!-- Right Stem 2 -->
    <rect x="654" y="250" width="6" height="52" />
    <rect x="650" y="216" width="6" height="34" />
    <rect x="654" y="184" width="6" height="32" />
  </g>
  <g fill="#155e75">
    <rect x="686" y="260" width="4" height="42" />
    <rect x="644" y="268" width="4" height="34" />
    <rect x="636" y="286" width="6" height="16" />
  </g>

  <!-- Ambient Pixel Bubbles & Particles -->
  <g fill="#38bdf8" opacity="0.45">
    <rect x="64" y="130" width="4" height="4" />
    <rect x="66" y="110" width="4" height="4" />
    <rect x="64" y="90" width="4" height="4" />
    <rect x="180" y="220" width="4" height="4" />
    <rect x="220" y="100" width="4" height="4" />
    <rect x="480" y="240" width="4" height="4" />
    <rect x="520" y="160" width="4" height="4" />
    <rect x="658" y="120" width="4" height="4" />
    <rect x="656" y="96" width="4" height="4" />
    <rect x="658" y="74" width="4" height="4" />
  </g>
  <g fill="#22d3ee" opacity="0.6">
    <rect x="66" y="70" width="6" height="6" />
    <rect x="360" y="90" width="4" height="4" />
    <rect x="656" y="52" width="6" height="6" />
  </g>

  <!-- Dynamic Pixel Fish Sprite -->
  <g id="fish">
    {fish_svg}
  </g>

  <!-- 16-Bit RPG HUD Panel -->
  <g id="hud">
    <!-- HUD Box Background -->
    <rect x="24" y="24" width="280" height="96" rx="4" fill="#040d1a" stroke="#164e63" stroke-width="2" opacity="0.92" />
    <rect x="26" y="26" width="276" height="2" fill="#22d3ee" opacity="0.5" />

    <!-- Stage & Level Badge -->
    <text x="36" y="44" fill="#38bdf8" font-size="11" font-weight="bold" letter-spacing="1">STAGE {info["stage_index"] + 1}: {info["stage"].upper()}</text>
    <text x="288" y="44" text-anchor="end" fill="#22d3ee" font-size="11" font-weight="bold">LVL {info["level"]}</text>

    <!-- Fish Species Title -->
    <text x="36" y="60" fill="#e2e8f0" font-size="13" font-weight="bold">{info["title"]}</text>

    <!-- Progress Bar Frame -->
    <rect x="36" y="70" width="244" height="12" fill="#020811" stroke="#0e3a5a" stroke-width="2" />
    <rect x="38" y="72" width="{bar_width}" height="8" fill="url(#barGrad)" />

    <!-- Numeric Stats Row -->
    <text x="36" y="98" fill="#94a3b8" font-size="10">XP: <tspan fill="#38bdf8" font-weight="bold">{info["xp"]:,}</tspan></text>
    <text x="140" y="98" fill="#94a3b8" font-size="10">YEAR: <tspan fill="#38bdf8" font-weight="bold">{info["contributions"]:,}</tspan></text>
    <text x="288" y="98" text-anchor="end" fill="#67e8f9" font-size="10">{info["next_bracket"]}</text>
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
