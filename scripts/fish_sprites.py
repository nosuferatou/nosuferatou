#!/usr/bin/env python3
"""
Artisan Pixel-Art Fish Generator for GitHub Aquarium.
Creates 5 distinct, anatomically proportioned, hand-crafted pixel-art species
following the ArtStation reference (weenifer / le-fisheee style):
- Native resolution pixel grid (36x24 to 72x48)
- Real aquatic anatomy: dorsal, caudal, pectoral, pelvic, anal fins, rays, gill plates, lateral line, scales, layered eyes, rim lighting
- Stage 1: Azure Fry (36x24) - Compact juvenile fry, expressive large eye, translucent delicate fins, pale belly
- Stage 2: Sapphire Tetra (48x28) - Streamlined torpedo body, neon lateral stripe, forked caudal fin, fin rays
- Stage 3: Crown Discus (52x48) - Deep rounded disk body, tall sail dorsal & anal fins, vertical banding, dithered scale luster
- Stage 4: Imperial Betta (64x44) - Elaborate flowing veil plumage, flared pectoral fins, crown rays, royal violet & turquoise scales
- Stage 5: Celestial Leviathan (78x42) - Majestic serpentine dragon-fish, segmented armor scales, bioluminescent crest, dragon whiskers, celestial fins
"""

import math
from PIL import Image, ImageDraw

def create_azure_fry() -> Image.Image:
    """Stage 1: Azure Fry (Baby) - 38x26 native pixels.
    Juvenile fish proportions: large expressive eye, translucent fin webbing,
    defined mouth, gill arc, soft cyan/azure tones.
    """
    W, H = 38, 26
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.putpixel

    # Palette
    C_OUTLINE  = (10, 22, 36, 255)    # Deep oceanic outline
    C_BASE_D   = (28, 82, 120, 255)   # Dorsal shadow / base
    C_BASE_M   = (48, 138, 182, 255)  # Mid body tone
    C_BASE_L   = (84, 182, 218, 255)  # Upper highlight body
    C_RIM      = (168, 230, 248, 255) # Top rim highlight
    C_BELLY_D  = (90, 135, 155, 255)  # Belly shadow
    C_BELLY_L  = (185, 220, 235, 255) # Pale juvenile underbelly
    C_FIN_WEB  = (56, 175, 215, 160)  # Translucent fin webbing
    C_FIN_RAY  = (130, 215, 245, 220) # Fin rays
    C_FIN_EDGE = (210, 245, 255, 230) # Fin glowing tip
    C_EYE_SCL  = (225, 245, 255, 255) # Sclera
    C_EYE_IRIS = (245, 175, 55, 255)  # Amber-gold iris
    C_EYE_PUP  = (12, 16, 26, 255)    # Pupil
    C_EYE_HI   = (255, 255, 255, 255) # Specular highlight

    # 1. Caudal Fin (Tail) - Forked juvenile tail (x: 2 to 10)
    for y in range(4, 22):
        # upper lobe
        if 4 <= y <= 11:
            dx = int((11 - y) * 0.9)
            for x in range(2 + dx, 12):
                p((x, y), C_FIN_WEB)
        # lower lobe
        elif 14 <= y <= 21:
            dx = int((y - 14) * 0.9)
            for x in range(2 + dx, 12):
                p((x, y), C_FIN_WEB)
        elif 11 < y < 14:
            for x in range(7, 12):
                p((x, y), C_FIN_WEB)

    # Fin Rays
    for x in range(3, 12):
        p((x, int(4 + (12 - x) * 0.7)), C_FIN_RAY)
        p((x, 12), C_FIN_RAY)
        p((x, int(21 - (12 - x) * 0.7)), C_FIN_RAY)
    # Caudal tips
    p((2, 4), C_FIN_EDGE); p((3, 4), C_FIN_EDGE)
    p((2, 21), C_FIN_EDGE); p((3, 21), C_FIN_EDGE)

    # 2. Dorsal Fin (x: 16 to 26, y: 2 to 7)
    for x in range(16, 27):
        top_y = 6 - int(math.sin((x - 16) / 10.0 * math.pi) * 4)
        for y in range(top_y, 8):
            p((x, y), C_FIN_WEB)
        if (x - 16) % 3 == 0:
            for y in range(top_y, 8):
                p((x, y), C_FIN_RAY)
        p((x, top_y), C_FIN_EDGE)

    # 3. Anal / Pelvic Fin (x: 15 to 22, y: 19 to 24)
    for x in range(15, 23):
        bot_y = 19 + int(math.sin((x - 15) / 7.0 * math.pi) * 4)
        for y in range(19, bot_y + 1):
            p((x, y), C_FIN_WEB)
        if (x - 15) % 2 == 0:
            for y in range(19, bot_y + 1):
                p((x, y), C_FIN_RAY)
        p((x, bot_y), C_FIN_EDGE)

    # 4. Main Body Flesh (x: 10 to 34)
    for x in range(10, 35):
        # Elliptical / teardrop fish profile
        prog = (x - 10) / 24.0
        # height curve
        half_h = math.sin(prog * math.pi) * 6.5
        if prog > 0.75: # snout taper
            half_h *= (1.0 - (prog - 0.75) * 1.5)
        top_y = int(13.0 - half_h)
        bot_y = int(13.0 + half_h)
        for y in range(top_y, bot_y + 1):
            # Vertical shading gradient + scale pattern
            rel_y = (y - top_y) / max(1.0, (bot_y - top_y))
            if rel_y < 0.15:
                col = C_RIM
            elif rel_y < 0.45:
                # Top body with scale sparkle
                if (x + y) % 2 == 0 and rel_y > 0.25:
                    col = C_RIM
                else:
                    col = C_BASE_L
            elif rel_y < 0.75:
                # Mid body lateral shading
                col = C_BASE_M
            else:
                # Pale juvenile belly
                if rel_y > 0.88:
                    col = C_BELLY_L
                else:
                    col = C_BELLY_D
            p((x, y), col)

    # 5. Gill Plate Arc (x: 27 to 29)
    p((28, 11), C_BASE_D); p((28, 12), C_BASE_D)
    p((27, 13), C_BASE_D); p((27, 14), C_BASE_D)
    p((27, 15), C_BASE_D); p((28, 16), C_BASE_D)
    # Gill highlight behind groove
    p((26, 12), C_RIM); p((26, 13), C_RIM); p((26, 14), C_RIM)

    # 6. Pectoral Fin (x: 21 to 26, y: 13 to 17)
    for px in range(21, 26):
        for py in range(14, 18):
            if (px + py) % 2 == 0:
                p((px, py), C_FIN_RAY)
            else:
                p((px, py), C_FIN_WEB)
    p((25, 17), C_FIN_EDGE)

    # 7. Snout & Mouth (x: 33 to 35, y: 13 to 15)
    p((34, 13), C_BASE_L); p((35, 13), C_BASE_M)
    p((34, 14), C_OUTLINE); p((35, 14), C_OUTLINE) # mouth cleft
    p((34, 15), C_BELLY_D)

    # 8. Big Expressive Baby Eye (centered around x: 30, y: 11)
    # 4x4 eye cluster
    eye_pixels = [
        (29, 9, C_OUTLINE), (30, 9, C_OUTLINE), (31, 9, C_OUTLINE), (32, 9, C_OUTLINE),
        (29, 10, C_OUTLINE), (30, 10, C_EYE_HI), (31, 10, C_EYE_IRIS), (32, 10, C_OUTLINE),
        (29, 11, C_OUTLINE), (30, 11, C_EYE_PUP), (31, 11, C_EYE_IRIS), (32, 11, C_OUTLINE),
        (29, 12, C_OUTLINE), (30, 12, C_EYE_PUP), (31, 12, C_EYE_SCL), (32, 12, C_OUTLINE),
        (29, 13, C_OUTLINE), (30, 13, C_OUTLINE), (31, 13, C_OUTLINE), (32, 13, C_OUTLINE),
    ]
    for ex, ey, ec in eye_pixels:
        p((ex, ey), ec)

    # 9. Clean Pixel Silhouette Border (1px around outer body)
    _add_crisp_outline(im, C_OUTLINE)
    return im


def create_sapphire_tetra() -> Image.Image:
    """Stage 2: Sapphire Tetra (Growing) - 48x30 native pixels.
    Streamlined tropical fish anatomy: slender torpedo profile, electric neon
    lateral stripe, deeply forked caudal fin, red-tipped fin accents, precise scale grid.
    """
    W, H = 48, 30
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.putpixel

    # Palette
    C_OUTLINE   = (8, 18, 32, 255)
    C_DORSAL_D  = (18, 52, 85, 255)    # Dark navy back
    C_DORSAL_M  = (28, 90, 140, 255)   # Sapphire blue
    C_NEON_TOP  = (120, 235, 255, 255) # Electric cyan neon core
    C_NEON_MID  = (34, 211, 238, 255)  # Radiant cyan
    C_BELLY_RED = (205, 55, 75, 255)   # Cardinal red belly band
    C_BELLY_SIL = (215, 232, 245, 255) # Silvery reflective belly
    C_FIN_TRANS = (70, 160, 210, 140)  # Glass fin
    C_FIN_RAY   = (140, 218, 248, 220) # Fin rays
    C_FIN_ACC   = (230, 75, 95, 220)   # Crimson fin tip accent
    C_EYE_OUT   = (6, 14, 26, 255)
    C_EYE_CYAN  = (56, 220, 245, 255)  # Glowing blue upper iris
    C_EYE_PUP   = (10, 15, 24, 255)
    C_EYE_HI    = (255, 255, 255, 255)

    # 1. Caudal Fin (Forked Tail) (x: 2 to 14)
    # Slender peduncle connects at x: 13
    for y in range(4, 26):
        # upper fork
        if 4 <= y <= 13:
            dx = int((13 - y) * 1.2)
            for x in range(2 + dx, 14):
                p((x, y), C_FIN_TRANS)
        # lower fork
        elif 16 <= y <= 25:
            dx = int((y - 16) * 1.2)
            for x in range(2 + dx, 14):
                p((x, y), C_FIN_TRANS)
        else: # center fork gap
            for x in range(9, 14):
                p((x, y), C_FIN_TRANS)

    # Caudal fin rays & crimson tips
    for x in range(3, 14):
        p((x, int(4 + (13 - x) * 0.8)), C_FIN_RAY)
        p((x, int(25 - (13 - x) * 0.8)), C_FIN_RAY)
    # Red tips
    p((2, 4), C_FIN_ACC); p((3, 4), C_FIN_ACC); p((4, 5), C_FIN_ACC)
    p((2, 25), C_FIN_ACC); p((3, 25), C_FIN_ACC); p((4, 24), C_FIN_ACC)

    # 2. Dorsal Fin (x: 20 to 28, tall sail)
    for x in range(20, 29):
        top_y = 8 - int(math.sin((x - 20) / 8.0 * math.pi) * 6)
        for y in range(top_y, 10):
            p((x, y), C_FIN_TRANS)
        if (x - 20) % 2 == 0:
            for y in range(top_y, 10):
                p((x, y), C_FIN_RAY)
        # Red crest tip
        if top_y <= 4:
            p((x, top_y), C_FIN_ACC)

    # 3. Anal Fin (x: 16 to 28, sweeping lower blade)
    for x in range(16, 29):
        bot_y = 20 + int(math.sin((x - 16) / 12.0 * math.pi) * 6)
        for y in range(20, bot_y + 1):
            p((x, y), C_FIN_TRANS)
        if (x - 16) % 2 == 0:
            for y in range(20, bot_y + 1):
                p((x, y), C_FIN_RAY)
        p((x, bot_y), C_FIN_ACC)

    # 4. Streamlined Torpedo Body (x: 12 to 44)
    for x in range(12, 45):
        prog = (x - 12) / 32.0
        # Hydrodynamic fish profile (wider at front-mid, tapering smoothly to peduncle)
        half_h = math.sin(prog * math.pi) * 6.2
        if prog < 0.35: # slender tail peduncle
            half_h = 2.2 + prog * 10.0
        elif prog > 0.8: # snout taper
            half_h = 6.2 * (1.0 - (prog - 0.8) * 3.5)

        cy = 15.0
        top_y = int(cy - half_h)
        bot_y = int(cy + half_h)

        for y in range(top_y, bot_y + 1):
            rel_y = (y - top_y) / max(1.0, (bot_y - top_y))
            # Shading layers:
            # 1. Back: dark dorsal sapphire
            if rel_y < 0.28:
                col = C_DORSAL_M if (x + y) % 2 == 0 else C_DORSAL_D
            # 2. Electric Neon Lateral Stripe (hallmark of Neon/Cardinal Tetra)
            elif 0.28 <= rel_y <= 0.46:
                if 0.32 <= rel_y <= 0.40:
                    col = C_NEON_TOP # blinding bright stripe core
                else:
                    col = C_NEON_MID
            # 3. Lower half: Crimson belly band posteriorly, silvery anteriorly
            elif 0.46 < rel_y <= 0.78:
                if x < 32: # cardinal red stripe
                    col = C_BELLY_RED if (x + y) % 2 == 0 else (175, 40, 60, 255)
                else:
                    col = C_BELLY_SIL
            else: # Ventral edge
                col = C_BELLY_SIL
            p((x, y), col)

    # 5. Gill Plate & Operculum (x: 36 to 38)
    p((37, 13), C_DORSAL_D); p((37, 14), C_DORSAL_D); p((36, 15), C_DORSAL_D)
    p((36, 16), C_DORSAL_D); p((37, 17), C_DORSAL_D)
    # Silvery operculum sheen
    p((35, 14), C_BELLY_SIL); p((35, 15), C_BELLY_SIL)

    # 6. Pectoral Fin (x: 30 to 35, y: 16 to 19)
    for px in range(30, 35):
        for py in range(16, 20):
            if (px + py) % 2 == 0:
                p((px, py), C_FIN_RAY)
            else:
                p((px, py), C_FIN_TRANS)

    # 7. Eye with Neon Reflection (x: 39 to 42, y: 12 to 15)
    eye_pixels = [
        (39, 12, C_EYE_OUT), (40, 12, C_EYE_CYAN), (41, 12, C_EYE_CYAN), (42, 12, C_EYE_OUT),
        (39, 13, C_EYE_CYAN), (40, 13, C_EYE_HI), (41, 13, C_EYE_PUP), (42, 13, C_EYE_OUT),
        (39, 14, C_EYE_CYAN), (40, 14, C_EYE_PUP), (41, 14, C_EYE_PUP), (42, 14, C_EYE_OUT),
        (39, 15, C_EYE_OUT), (40, 15, C_EYE_OUT), (41, 15, C_EYE_OUT), (42, 15, C_EYE_OUT),
    ]
    for ex, ey, ec in eye_pixels:
        p((ex, ey), ec)

    # 8. Snout & Mouth (x: 43 to 45)
    p((44, 14), C_DORSAL_M); p((45, 14), C_OUTLINE)
    p((44, 15), C_OUTLINE); p((45, 15), C_OUTLINE)
    p((44, 16), C_BELLY_SIL)

    _add_crisp_outline(im, C_OUTLINE)
    return im


def create_crown_discus() -> Image.Image:
    """Stage 3: Crown Discus (Advanced) - 54x50 native pixels.
    Deep, stately circular discus anatomy: tall dorsal sail, sweeping anal fin,
    vertical turquoise tiger striations, intricate scales, rich amber/emerald tones.
    """
    W, H = 54, 50
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.putpixel

    # Palette
    C_OUTLINE   = (6, 16, 28, 255)
    C_BODY_AMB  = (175, 115, 45, 255)  # Warm amber-bronze base
    C_BODY_GOLD = (220, 165, 65, 255)  # Golden body highlight
    C_BODY_SHAD = (115, 68, 30, 255)   # Body shading
    C_STRIPE_CY = (45, 215, 210, 255)  # Electric turquoise striation
    C_STRIPE_HI = (175, 250, 245, 255) # Striation bright highlight
    C_FIN_WEB   = (25, 95, 125, 180)   # Deep teal fin webbing
    C_FIN_RAY   = (55, 185, 210, 230)  # Turquoise fin ray
    C_FIN_EDGE  = (165, 245, 255, 255) # Electric crown edge
    C_EYE_RED   = (220, 45, 45, 255)   # Discus signature ruby-red iris
    C_EYE_PUP   = (8, 12, 20, 255)
    C_EYE_HI    = (255, 255, 255, 255)

    # 1. Fan Tail (Caudal Fin) (x: 2 to 14, rounded paddle)
    for y in range(17, 33):
        dx = int(abs(y - 25) * 0.9)
        for x in range(2 + dx, 15):
            p((x, y), C_FIN_WEB)
            if (y - 17) % 2 == 0 and x > 4:
                p((x, y), C_FIN_RAY)
        p((2 + dx, y), C_FIN_EDGE)

    # 2. Grand Dorsal Sail (x: 14 to 40, y: 2 to 14)
    for x in range(14, 41):
        top_y = 13 - int(math.sin((x - 14) / 26.0 * math.pi) * 11)
        for y in range(top_y, 14):
            p((x, y), C_FIN_WEB)
        if (x - 14) % 2 == 0:
            for y in range(top_y, 14):
                p((x, y), C_FIN_RAY)
        # Crown rim
        p((x, top_y), C_FIN_EDGE)
        if top_y + 1 < 14:
            p((x, top_y + 1), C_STRIPE_CY)

    # 3. Sweeping Anal Fin (x: 14 to 38, y: 36 to 48)
    for x in range(14, 39):
        bot_y = 36 + int(math.sin((x - 14) / 24.0 * math.pi) * 11)
        for y in range(36, bot_y + 1):
            p((x, y), C_FIN_WEB)
        if (x - 14) % 2 == 0:
            for y in range(36, bot_y + 1):
                p((x, y), C_FIN_RAY)
        p((x, bot_y), C_FIN_EDGE)
        if bot_y - 1 >= 36:
            p((x, bot_y - 1), C_STRIPE_CY)

    # 4. Long Filamentous Pelvic Fins (Feelers) (x: 32 to 36, y: 38 to 48)
    for y in range(36, 48):
        fx = int(35 - (y - 36) * 0.4)
        p((fx, y), C_STRIPE_HI)
        p((fx - 1, y), C_FIN_RAY)

    # 5. Massive Round Discus Body (Disk centered around x: 28, y: 25, radius ~ 15)
    center_x = 28.0
    center_y = 25.0
    rx = 15.5
    ry = 14.5

    for x in range(12, 48):
        for y in range(10, 40):
            # Elliptical disk equation
            dx = (x - center_x) / rx
            dy = (y - center_y) / ry
            dist = dx * dx + dy * dy
            if dist <= 1.0:
                # Vertical tiger striations at specific x bands: x=18, 23, 29, 35, 41
                is_stripe = False
                for sx in [18, 23, 29, 35, 41]:
                    if abs(x - sx) <= 1:
                        # wavy striation
                        wave_offset = int(math.sin(y * 0.4) * 0.8)
                        if x == (sx + wave_offset):
                            is_stripe = True

                if is_stripe:
                    # Alternating glowing turquoise scales
                    col = C_STRIPE_HI if (x + y) % 3 == 0 else C_STRIPE_CY
                else:
                    # Shading from top-right light source
                    light_factor = (x - 12) / 36.0 * 0.5 + (40 - y) / 30.0 * 0.5
                    if light_factor > 0.65:
                        col = C_BODY_GOLD if (x + y) % 2 == 0 else C_BODY_AMB
                    elif light_factor > 0.35:
                        col = C_BODY_AMB if (x + y) % 2 == 0 else C_BODY_SHAD
                    else:
                        col = C_BODY_SHAD
                p((x, y), col)

    # 6. Snout Taper & Thick Discus Lips (x: 43 to 48, y: 23 to 27)
    for x in range(43, 49):
        p((x, 24), C_BODY_AMB)
        p((x, 25), C_OUTLINE) # mouth line
        p((x, 26), C_BODY_SHAD)
    p((48, 24), C_STRIPE_HI); p((48, 26), C_STRIPE_CY)

    # 7. Operculum (Gill Arch)
    for gy in range(20, 31):
        gx = int(39 - math.sin((gy - 20) / 10.0 * math.pi) * 3)
        p((gx, gy), C_OUTLINE)
        p((gx - 1, gy), C_STRIPE_CY)

    # 8. Pectoral Fin (translucent fan near gill) (x: 32 to 38, y: 24 to 29)
    for px in range(32, 38):
        for py in range(24, 29):
            if (px + py) % 2 == 0:
                p((px, py), C_FIN_RAY)

    # 9. Ruby-Red Discus Eye (x: 40 to 44, y: 19 to 23)
    eye_pixels = [
        (40, 19, C_OUTLINE), (41, 19, C_OUTLINE), (42, 19, C_OUTLINE), (43, 19, C_OUTLINE),
        (39, 20, C_OUTLINE), (40, 20, C_EYE_RED), (41, 20, C_EYE_HI), (42, 20, C_EYE_RED), (43, 20, C_OUTLINE),
        (39, 21, C_OUTLINE), (40, 21, C_EYE_RED), (41, 21, C_EYE_PUP), (42, 21, C_EYE_RED), (43, 21, C_OUTLINE),
        (39, 22, C_OUTLINE), (40, 22, C_EYE_RED), (41, 22, C_EYE_PUP), (42, 22, C_EYE_RED), (43, 22, C_OUTLINE),
        (40, 23, C_OUTLINE), (41, 23, C_OUTLINE), (42, 23, C_OUTLINE), (43, 23, C_OUTLINE),
    ]
    for ex, ey, ec in eye_pixels:
        p((ex, ey), ec)

    _add_crisp_outline(im, C_OUTLINE)
    return im


def create_imperial_betta() -> Image.Image:
    """Stage 4: Imperial Betta (Elite) - 66x48 native pixels.
    Showstopper Siamese fighting fish anatomy: expansive flowing veil-tail
    plumage, individual fin rays, flared royal pectoral fins, layered royal
    purple and peacock cyan scales, formidable warrior head.
    """
    W, H = 66, 48
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.putpixel

    # Palette
    C_OUTLINE   = (6, 12, 24, 255)
    C_PURP_D    = (35, 14, 52, 255)    # Imperial deep indigo-violet
    C_PURP_M    = (75, 28, 105, 255)   # Royal velvet purple
    C_CYAN_L    = (45, 210, 225, 255)  # Peacock metallic cyan
    C_CYAN_HI   = (175, 245, 255, 255) # Electric scale rim highlight
    C_FIN_BASE  = (55, 18, 78, 180)    # Deep plum fin base
    C_FIN_MID   = (28, 145, 185, 200)  # Turquoise plumage
    C_FIN_EDGE  = (135, 240, 255, 240) # Flowing luminous frill edges
    C_FIN_RAY   = (220, 110, 245, 255) # Magenta-violet ray spines
    C_EYE_GOLD  = (245, 195, 45, 255)  # Fierce gold eye
    C_EYE_PUP   = (6, 8, 15, 255)
    C_EYE_HI    = (255, 255, 255, 255)

    # 1. Flowing Massive Caudal Plumage (Veil Tail) (x: 2 to 24, y: 6 to 42)
    # Spans nearly half the sprite length with billowy folds
    for y in range(6, 43):
        # Billow curve: top and bottom lobes flare out wide
        rel_v = (y - 6) / 36.0
        # horizontal span
        span_left = int(2 + math.sin(rel_v * math.pi * 1.5) * 4)
        for x in range(span_left, 24):
            # Layered folds
            fold = math.sin((x * 0.4) + (y * 0.5))
            if fold > 0.3:
                col = C_FIN_MID
            elif fold < -0.3:
                col = C_FIN_BASE
            else:
                col = C_FIN_EDGE
            p((x, y), col)
        # Trailing edge highlights & fin rays
        p((span_left, y), C_FIN_EDGE)
        p((span_left + 1, y), C_FIN_EDGE)

    # Caudal Ray Spines radiating from peduncle (x: 20, y: 24)
    for ray_idx in range(9):
        ang = -0.9 + ray_idx * 0.22
        for r in range(2, 20):
            rx = int(20 - math.cos(ang) * r)
            ry = int(24 + math.sin(ang) * r)
            if 0 <= rx < W and 0 <= ry < H:
                p((rx, ry), C_FIN_RAY)

    # 2. Grand Flowing Dorsal Veil (x: 22 to 50, y: 2 to 16)
    for x in range(22, 51):
        rel_x = (x - 22) / 28.0
        # undulating canopy
        wave = math.sin(rel_x * math.pi * 2.0) * 2.5
        top_y = max(1, int(10 - math.sin(rel_x * math.pi) * 8 + wave))
        for y in range(top_y, 16):
            p((x, y), C_FIN_MID if (x + y) % 2 == 0 else C_FIN_BASE)
        # Rays
        if (x - 22) % 3 == 0:
            for y in range(top_y, 16):
                p((x, y), C_FIN_RAY)
        p((x, top_y), C_FIN_EDGE)
        p((x, top_y + 1), C_CYAN_L)

    # 3. Flamboyant Anal Veil (x: 20 to 48, y: 30 to 46)
    for x in range(20, 49):
        rel_x = (x - 20) / 28.0
        bot_y = min(46, int(32 + math.sin(rel_x * math.pi) * 12 + math.cos(rel_x * 8.0) * 1.5))
        for y in range(30, bot_y + 1):
            p((x, y), C_FIN_MID if (x + y) % 2 == 0 else C_FIN_BASE)
        if (x - 20) % 3 == 0:
            for y in range(30, bot_y + 1):
                p((x, y), C_FIN_RAY)
        p((x, bot_y), C_FIN_EDGE)

    # 4. Long Ventral Whisker Fins (Pelvics) (x: 40 to 44, trailing down to y: 47)
    for y in range(32, 48):
        wx = int(43 - (y - 32) * 0.5)
        p((wx, y), C_CYAN_HI)
        p((wx - 1, y), C_CYAN_L)

    # 5. Muscular Warrior Betta Body (x: 20 to 58)
    for x in range(20, 59):
        prog = (x - 20) / 38.0
        # S-curve hydrodynamic torso
        half_h = math.sin(prog * math.pi) * 7.5
        if prog < 0.2:
            half_h = 2.5 + prog * 18.0
        elif prog > 0.8:
            half_h = 7.5 * (1.0 - (prog - 0.8) * 3.5)

        cy = 23.5 - math.sin(prog * math.pi * 0.8) * 1.2
        top_y = int(cy - half_h)
        bot_y = int(cy + half_h)

        for y in range(top_y, bot_y + 1):
            rel_y = (y - top_y) / max(1.0, (bot_y - top_y))
            # Dragon-scale honeycomb pattern
            is_scale_rim = ((x * 2 + y) % 3 == 0)
            if rel_y < 0.25:
                col = C_CYAN_HI if is_scale_rim else C_CYAN_L
            elif rel_y < 0.65:
                if is_scale_rim:
                    col = C_CYAN_L
                else:
                    col = C_PURP_M if (x + y) % 2 == 0 else C_PURP_D
            else:
                col = C_PURP_D if is_scale_rim else (20, 8, 32, 255)
            p((x, y), col)

    # 6. Flared Operculum / Gill Ruffs (Signature Betta Flaring) (x: 48 to 51)
    for gy in range(18, 30):
        gx = int(50 - math.sin((gy - 18) / 11.0 * math.pi) * 2.5)
        p((gx, gy), C_OUTLINE)
        p((gx - 1, gy), C_PURP_M)
        p((gx - 2, gy), C_CYAN_HI)

    # 7. Flared Pectoral Fan (x: 42 to 48, y: 22 to 27)
    for px in range(42, 48):
        for py in range(22, 28):
            if (px + py) % 2 == 0:
                p((px, py), C_FIN_EDGE)
            else:
                p((px, py), C_CYAN_L)

    # 8. Fierce Betta Eye (x: 52 to 56, y: 19 to 23)
    eye_pixels = [
        (52, 19, C_OUTLINE), (53, 19, C_OUTLINE), (54, 19, C_OUTLINE), (55, 19, C_OUTLINE),
        (51, 20, C_OUTLINE), (52, 20, C_EYE_GOLD), (53, 20, C_EYE_HI), (54, 20, C_EYE_PUP), (55, 20, C_OUTLINE),
        (51, 21, C_OUTLINE), (52, 21, C_EYE_GOLD), (53, 21, C_EYE_PUP), (54, 21, C_EYE_PUP), (55, 21, C_OUTLINE),
        (52, 22, C_OUTLINE), (53, 22, C_EYE_GOLD), (54, 22, C_EYE_GOLD), (55, 22, C_OUTLINE),
    ]
    for ex, ey, ec in eye_pixels:
        p((ex, ey), ec)

    # 9. Aggressive Upturned Mouth & Chin (x: 57 to 61)
    p((58, 21), C_CYAN_HI); p((59, 21), C_CYAN_L)
    p((58, 22), C_OUTLINE); p((59, 22), C_OUTLINE); p((60, 22), C_OUTLINE)
    p((58, 23), C_PURP_D);  p((59, 23), C_OUTLINE)

    _add_crisp_outline(im, C_OUTLINE)
    return im


def create_celestial_leviathan() -> Image.Image:
    """Stage 5: Celestial Leviathan (Legendary) - 78x46 native pixels.
    Majestic ancient apex aquatic creature: elongated serpentine ocean dragon,
    interlocking chitinous armor plates, bioluminescent cosmic crest, sweeping
    ethereal caudal fins, barbels/whiskers, radiant star markings.
    """
    W, H = 78, 46
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.putpixel

    # Palette
    C_OUTLINE   = (4, 10, 20, 255)
    C_SCALE_D   = (12, 38, 58, 255)    # Abyssal midnight teal
    C_SCALE_M   = (22, 75, 105, 255)   # Deep oceanic jade
    C_SCALE_L   = (45, 145, 175, 255)  # Bioluminescent teal
    C_STAR_GLOW = (165, 245, 255, 255) # Radiant star-core white-cyan
    C_GOLD_RIM  = (240, 195, 60, 255)  # Celestial divine gold armor rim
    C_GOLD_HI   = (255, 240, 150, 255) # Pure golden starlight
    C_FIN_WEB   = (20, 85, 120, 170)   # Translucent astral fin
    C_FIN_RAY   = (65, 205, 235, 240)  # Luminous fin ray
    C_FIN_EDGE  = (185, 250, 255, 255) # Glowing celestial edge
    C_EYE_CORE  = (255, 250, 180, 255) # Blinding celestial star eye
    C_EYE_RING  = (40, 215, 245, 255)  # Halo ring

    # 1. Majestic Bifurcated Celestial Tail (x: 2 to 20, y: 6 to 39)
    # Sweeping dragon fluke with multiple ethereal streamers
    for y in range(6, 40):
        # upper celestial horn fluke
        if 6 <= y <= 19:
            dx = int((19 - y) * 1.3)
            for x in range(2 + dx, 20):
                p((x, y), C_FIN_WEB)
            p((2 + dx, y), C_FIN_EDGE)
            if (19 - y) % 3 == 0:
                for x in range(2 + dx, 20):
                    p((x, y), C_FIN_RAY)
        # lower celestial horn fluke
        elif 24 <= y <= 39:
            dx = int((y - 24) * 1.2)
            for x in range(2 + dx, 20):
                p((x, y), C_FIN_WEB)
            p((2 + dx, y), C_FIN_EDGE)
            if (y - 24) % 3 == 0:
                for x in range(2 + dx, 20):
                    p((x, y), C_FIN_RAY)
        else: # center peduncle connect
            for x in range(12, 20):
                p((x, y), C_FIN_WEB)

    # 2. Serrated Celestial Dorsal Spines & Crest (x: 18 to 60, y: 2 to 14)
    # Distinct jagged dorsal crest with gold tips
    for x in range(18, 62):
        rel_x = (x - 18) / 44.0
        # 6 distinct majestic dorsal crests
        spine_wave = math.sin(rel_x * math.pi * 6.0)
        crest_height = 8.0 * math.sin(rel_x * math.pi)
        top_y = int(14.0 - crest_height * (0.6 + max(0.0, spine_wave) * 0.7))
        for y in range(top_y, 15):
            p((x, y), C_FIN_WEB)
        if (x - 18) % 4 == 0:
            for y in range(top_y, 15):
                p((x, y), C_FIN_RAY)
        # Gold crown spine tip
        p((x, top_y), C_GOLD_RIM)
        if spine_wave > 0.6:
            p((x, top_y), C_GOLD_HI)
            p((x, top_y + 1), C_STAR_GLOW)

    # 3. Ventral Blade Fin (x: 22 to 50, y: 30 to 42)
    for x in range(22, 51):
        rel_x = (x - 22) / 28.0
        bot_y = int(30.0 + math.sin(rel_x * math.pi) * 8.0)
        for y in range(30, bot_y + 1):
            p((x, y), C_FIN_WEB)
        if (x - 22) % 3 == 0:
            for y in range(30, bot_y + 1):
                p((x, y), C_FIN_RAY)
        p((x, bot_y), C_FIN_EDGE)

    # 4. Colossal Serpentine Armored Torso (x: 18 to 72)
    for x in range(18, 73):
        prog = (x - 18) / 54.0
        # Powerful, elongated ocean leviathan profile
        half_h = 7.8 * math.sin(prog * math.pi * 0.85 + 0.15)
        if prog < 0.15: # tail peduncle
            half_h = 3.0 + prog * 20.0
        elif prog > 0.85: # massive dragon skull taper
            half_h = 7.0 * (1.0 - (prog - 0.85) * 4.0)

        cy = 22.5
        top_y = int(cy - half_h)
        bot_y = int(cy + half_h)

        for y in range(top_y, bot_y + 1):
            rel_y = (y - top_y) / max(1.0, (bot_y - top_y))
            # Segmented armor plates & constellation scales
            is_plate_seam = (x % 5 == 0)
            is_star_scale = ((x * 3 + y * 2) % 7 == 0) and (0.25 <= rel_y <= 0.65)

            if is_star_scale:
                col = C_STAR_GLOW # Glowing celestial star marking
            elif is_plate_seam:
                col = C_OUTLINE # Armor groove
            elif rel_y < 0.2:
                # Top gilded armor ridge
                col = C_GOLD_RIM if (x + y) % 2 == 0 else C_GOLD_HI
            elif rel_y < 0.5:
                # Upper flank
                col = C_SCALE_L if (x + y) % 2 == 0 else C_SCALE_M
            elif rel_y < 0.8:
                # Lower flank
                col = C_SCALE_M if (x + y) % 2 == 0 else C_SCALE_D
            else:
                # Abyssal belly
                col = C_SCALE_D
            p((x, y), col)

    # 5. Massive Dragon Pectoral Wing-Fin (x: 44 to 54, y: 21 to 32)
    for px in range(44, 55):
        for py in range(21, 33):
            wing_rel = (px - 44) + (py - 21)
            if wing_rel < 16:
                if (px + py) % 3 == 0:
                    p((px, py), C_FIN_RAY)
                elif wing_rel % 4 == 0:
                    p((px, py), C_GOLD_RIM)
                else:
                    p((px, py), C_FIN_WEB)
    # Glowing wing rim
    for px in range(48, 55):
        p((px, 21 + (px - 48)), C_FIN_EDGE)

    # 6. Ancient Whisker Barbels (Flowing sensory whiskers) (x: 64 to 77, y: 24 to 34)
    # Upper whisker
    for wx in range(65, 77):
        wy = int(24 + math.sin((wx - 65) * 0.4) * 3)
        p((wx, wy), C_GOLD_HI)
        p((wx, wy + 1), C_STAR_GLOW)
    # Lower whisker
    for wx in range(63, 74):
        wy = int(28 + (wx - 63) * 0.5)
        p((wx, wy), C_FIN_RAY)

    # 7. Mighty Leviathan Jaw & Maw (x: 66 to 74, y: 21 to 27)
    # Jaws with protruding razor ivory fangs
    p((69, 21), C_GOLD_RIM); p((70, 21), C_SCALE_L)
    p((71, 22), C_OUTLINE);  p((72, 22), C_OUTLINE) # mouth cleft
    p((73, 23), C_OUTLINE);  p((74, 23), C_OUTLINE)
    # Protruding fangs
    p((70, 23), (255, 255, 255, 255))
    p((72, 24), (255, 255, 255, 255))
    p((70, 26), C_SCALE_D); p((71, 26), C_SCALE_D)

    # 8. Blinding Celestial Star Eye & Radiant Halo (x: 62 to 67, y: 16 to 21)
    eye_pixels = [
        (63, 16, C_OUTLINE), (64, 16, C_EYE_RING), (65, 16, C_EYE_RING), (66, 16, C_OUTLINE),
        (62, 17, C_EYE_RING), (63, 17, C_EYE_RING), (64, 17, C_STAR_GLOW), (65, 17, C_EYE_RING), (66, 17, C_OUTLINE),
        (62, 18, C_EYE_RING), (63, 18, C_STAR_GLOW), (64, 18, C_EYE_CORE), (65, 18, C_STAR_GLOW), (66, 18, C_EYE_RING),
        (62, 19, C_EYE_RING), (63, 19, C_EYE_RING), (64, 19, C_STAR_GLOW), (65, 19, C_EYE_RING), (66, 19, C_OUTLINE),
        (63, 20, C_OUTLINE), (64, 20, C_EYE_RING), (65, 20, C_EYE_RING), (66, 20, C_OUTLINE),
    ]
    for ex, ey, ec in eye_pixels:
        p((ex, ey), ec)

    _add_crisp_outline(im, C_OUTLINE)
    return im


def _add_crisp_outline(im: Image.Image, outline_color: tuple):
    """Enforces a crisp 1-pixel outer silhouette boundary for high pixel-art readability."""
    w, h = im.size
    alpha = im.split()[3]
    border_pixels = []
    for y in range(h):
        for x in range(w):
            if alpha.getpixel((x, y)) == 0:
                # Check 8-neighborhood for filled pixels
                has_solid_neighbor = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            if alpha.getpixel((nx, ny)) > 0:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break
                if has_solid_neighbor:
                    border_pixels.append((x, y))

    for bx, by in border_pixels:
        im.putpixel((bx, by), outline_color)
