#!/usr/bin/env python3
"""Hand-authored, species-distinct pixel sprites for the aquarium hero fish."""

from PIL import Image, ImageDraw


def _fish(size, body, tail, dorsal, anal, pectoral, eye, gill, belly):
    """Construct anatomical pixel clusters on a fixed low-resolution canvas."""
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, base, bounds, belly_color, scale_color = body
    d.polygon(tail[0], fill=tail[1], outline=outline)
    for ray in tail[2] if len(tail) > 2 else ():
        d.line(ray, fill=tail[3], width=1)
    d.polygon(dorsal[0], fill=dorsal[1], outline=outline)
    for ray in dorsal[2] if len(dorsal) > 2 else ():
        d.line(ray, fill=dorsal[3], width=1)
    d.polygon(anal[0], fill=anal[1], outline=outline)
    for ray in anal[2] if len(anal) > 2 else ():
        d.line(ray, fill=anal[3], width=1)
    d.ellipse(bounds, fill=base, outline=outline)
    d.polygon(belly, fill=belly_color)
    d.polygon(pectoral[0], fill=pectoral[1], outline=outline)
    d.arc(gill[0], gill[1], gill[2], fill=gill[3], width=1)
    d.line(gill[4], fill=outline, width=1)
    x, y, r, iris = eye
    d.ellipse((x-r, y-r, x+r, y+r), fill=(228, 243, 244, 255), outline=outline)
    d.ellipse((x-1, y-1, x+1, y+1), fill=iris)
    d.point((x, y), fill=(8, 13, 22, 255))
    d.point((x-1, y-1), fill=(255, 255, 255, 255))
    x0, y0, x1, y1 = bounds
    for sy in range(y0 + 4, y1 - 2, 4):
        for sx in range(x0 + 5 + ((sy // 4) % 2) * 2, x1 - 4, 5):
            if not (x-3 <= sx <= x+3 and y-3 <= sy <= y+3):
                d.point((sx, sy), fill=scale_color)
    return im


def get_azure_fry():
    """Juvenile fry: plump head, oversized eye, tiny translucent fins."""
    return _fish(
        (36, 28),
        ((8, 22, 38, 255), (54, 151, 194, 255), (12, 7, 32, 23), (182, 222, 232, 255), (147, 218, 236, 255)),
        ([(3, 13), (10, 9), (10, 13), (10, 16), (3, 19), (6, 16)], (85, 185, 225, 180), [[(4, 13), (9, 12)], [(5, 17), (9, 15)]], (178, 230, 247, 210)),
        ([(11, 9), (15, 4), (20, 5), (22, 10), (18, 11)], (115, 205, 235, 255), [[(13, 9), (15, 5)], [(17, 9), (18, 5)]], (195, 240, 255, 255)),
        ([(14, 20), (19, 21), (22, 25), (17, 23)], (70, 150, 180, 255), [[(16, 21), (19, 24)]], (125, 205, 225, 255)),
        ([(18, 16), (24, 16), (22, 20), (19, 18)], (178, 230, 247, 170)),
        (25, 12, 3, (224, 157, 45, 255)), 
        ((21, 12, 28, 19), 235, 300, (12, 57, 82, 255), [(22, 19), (22, 20)]),
        [(11, 19), (18, 21), (22, 20), (21, 23), (13, 22)],
    )


def get_sapphire_tetra():
    """Streamlined tetra with forked tail, lateral neon band and red fin tips."""
    return _fish(
        (52, 30),
        ((7, 19, 34, 255), (40, 113, 173, 255), (14, 8, 47, 24), (185, 218, 232, 255), (94, 201, 224, 255)),
        ([(2, 8), (12, 13), (4, 8), (12, 15), (2, 22), (15, 16)], (215, 45, 65, 255), [[(3, 9), (10, 13)], [(3, 21), (10, 16)]], (245, 110, 125, 255)),
        ([(19, 10), (25, 4), (31, 7), (29, 11), (22, 13)], (50, 135, 185, 255), [[(22, 10), (25, 5)], [(27, 10), (29, 7)]], (135, 220, 250, 255)),
        ([(18, 19), (28, 19), (34, 25), (24, 22)], (70, 145, 175, 255), [[(22, 20), (28, 24)]], (135, 220, 250, 255)),
        ([(29, 16), (36, 17), (32, 20), (30, 18)], (70, 186, 217, 255)),
        (39, 12, 2, (36, 218, 237, 255)), 
        ((35, 11, 41, 18), 220, 305, (8, 37, 69, 255), [(36, 18), (35, 19)]),
        [(20, 19), (29, 21), (34, 20), (31, 23), (23, 22)],
    )


def get_crown_discus():
    """Deep-bodied discus with sail fins and vertical species markings."""
    im = Image.new("RGBA", (46, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline, amber, shade, scale = (8, 18, 31, 255), (195, 128, 52, 255), (130, 78, 39, 255), (237, 175, 76, 255)
    d.polygon([(8, 19), (11, 7), (18, 3), (28, 6), (36, 16), (39, 25), (34, 39), (24, 45), (14, 40), (8, 30)], fill=(30, 112, 151, 255), outline=outline)
    d.ellipse((11, 9, 37, 40), fill=amber, outline=outline)
    d.polygon([(13, 31), (34, 30), (32, 38), (24, 43), (16, 39)], fill=shade)
    # vertical discus bars conform to curved body
    for x in (16, 21, 27, 32):
        d.line([(x, 11), (x-1, 17), (x+1, 24), (x, 31), (x+2, 37)], fill=(35, 197, 194, 255), width=1)
    # individual dorsal / anal rays
    for x in range(12, 35, 3):
        d.line([(x, 12), (x+1, 5 if x in (18, 21, 24, 27) else 9)], fill=(93, 215, 222, 255), width=1)
        d.line([(x, 35), (x+1, 42 if x in (18, 21, 24, 27) else 38)], fill=(45, 158, 188, 255), width=1)
    d.polygon([(8, 21), (2, 17), (3, 24), (2, 31), (9, 28)], fill=(30, 107, 140, 255), outline=outline)
    d.polygon([(23, 22), (29, 24), (28, 30), (24, 28)], fill=(46, 167, 189, 255), outline=outline)
    d.arc((29, 15, 37, 26), 260, 90, fill=outline)
    d.ellipse((34, 16, 39, 21), fill=(241, 66, 50, 255), outline=outline)
    d.point((36, 17), fill=(255, 255, 255, 255)); d.point((37, 19), fill=outline)
    for x, y in ((18,16),(23,14),(28,17),(17,24),(25,27),(30,22),(19,33),(27,35)):
        d.point((x,y), fill=scale)
    return im


def get_imperial_betta():
    """Betta with layered veil tail, fin rays, gill cover and compact torso."""
    im = Image.new("RGBA", (58, 42), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    o=(8,13,28,255); violet=(95,39,139,255); plum=(48,22,79,255); teal=(37,165,195,255); hi=(142,233,239,255)
    # Separate flowing tail and dorsal/anal fans; ray structure stays visible.
    d.polygon([(4,15),(9,8),(16,11),(19,16),(16,22),(10,26),(4,22),(9,19)], fill=plum, outline=o)
    for pts in [[(5,15),(11,10)],[(5,18),(14,14)],[(5,21),(14,19)],[(7,24),(15,22)]]: d.line(pts, fill=hi, width=1)
    d.polygon([(21,13),(25,5),(32,3),(38,7),(42,13),(35,15)], fill=violet, outline=o)
    for x in range(24,39,3): d.line([(x,13),(x+1,6)], fill=hi, width=1)
    d.polygon([(20,23),(27,25),(34,28),(40,34),(34,37),(25,31)], fill=plum, outline=o)
    for x in range(24,36,3): d.line([(x,26),(x+5,34)], fill=teal, width=1)
    # Body: short, muscular, scales shaded from light-facing dorsal edge.
    d.ellipse((18,12,45,29), fill=violet, outline=o)
    d.polygon([(21,23),(38,24),(43,27),(37,30),(24,28)], fill=plum)
    for x,y in ((24,15),(29,14),(34,15),(39,16),(26,19),(31,18),(36,20),(41,20),(28,23),(34,24)):
        d.point((x,y), fill=hi if y < 20 else teal)
    d.arc((38,15,46,26), 260, 100, fill=o)
    # gill plate and eye
    d.arc((35,15,41,25), 280, 80, fill=hi, width=1)
    d.ellipse((40,14,45,19), fill=(235,182,53,255), outline=o)
    d.point((43,16), fill=(5,10,20,255)); d.point((41,15), fill=(255,255,255,255))
    d.line([(44,23),(48,23),(49,22)], fill=o, width=1)
    # pectoral fan and pelvic feeler
    d.polygon([(32,21),(38,23),(35,28),(32,25)], fill=teal, outline=o)
    for x in (33,35,37): d.line([(33,22),(x,27)], fill=hi, width=1)
    d.line([(27,28),(29,34),(31,37)], fill=hi, width=1)
    return im


def get_celestial_leviathan():
    """Elongated, believable fish anatomy with armor scales, barbels and layered fins."""
    im = Image.new("RGBA", (76, 38), (0,0,0,0)); d = ImageDraw.Draw(im)
    o=(5,14,26,255); dark=(14,52,75,255); mid=(26,103,133,255); light=(68,169,186,255); gold=(225,177,76,255); white=(191,242,240,255)
    # Caudal fork and long dorsal/anal fins.
    d.polygon([(3,14),(12,18),(4,11),(8,18),(3,24),(13,20),(6,28),(15,21)], fill=mid, outline=o)
    d.polygon([(15,13),(23,7),(35,8),(46,10),(58,12),(65,15),(65,23),(56,26),(42,28),(28,27),(16,23)], fill=mid, outline=o)
    d.polygon([(17,13),(24,9),(35,10),(44,12),(56,14),(59,17),(46,17),(31,16)], fill=light)
    d.polygon([(20,24),(31,26),(43,27),(52,25),(43,31),(34,32),(25,28)], fill=dark, outline=o)
    # Segmented scale plates following elongated body.
    for x in range(20,57,4):
        y=18 + ((x//4)%2)
        d.line([(x,y),(x+2,y+2),(x+3,y+4)], fill=(117,202,205,255), width=1)
        d.point((x+1,y+1), fill=white if x in (28,40,52) else light)
    # Distinct gill, head profile, jaw, eye and barbels.
    d.arc((53,13,63,24), 250, 100, fill=o, width=1)
    d.polygon([(60,14),(69,13),(74,16),(71,18),(75,19),(72,21),(64,22),(59,20)], fill=light, outline=o)
    d.line([(68,19),(74,19)], fill=o, width=1); d.point((70,20), fill=(255,245,218,255))
    d.ellipse((64,14,69,19), fill=gold, outline=o); d.point((67,16), fill=(5,12,20,255)); d.point((65,15), fill=(255,255,255,255))
    d.line([(69,21),(75,24),(74,26)], fill=white, width=1)
    d.line([(68,22),(73,28),(72,30)], fill=light, width=1)
    # Crest and pectoral rays, gold celestial markings.
    d.polygon([(25,10),(28,4),(31,9),(35,5),(38,10),(42,7),(45,12)], fill=dark, outline=o)
    for x in (28,35,42): d.point((x,6), fill=gold)
    d.polygon([(42,21),(49,22),(46,27),(41,25)], fill=dark, outline=o)
    for x in (43,45,47): d.line([(42,22),(x,26)], fill=light, width=1)
    return im
