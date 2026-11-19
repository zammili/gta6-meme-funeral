#!/usr/bin/env python3
"""Hand-drawn style meme: the funeral of the 'before GTA 6' meme.
Drawn entirely with code (PIL) using wobbly double-pass strokes so it
looks sketched by a person, not rendered by an image model."""
import math, random
from PIL import Image, ImageDraw, ImageFont

random.seed(11)
W, H = 1800, 1350
FD = "/home/hatch/workspace/makefun/entry-gta6meme/fonts"
GOCHI = FD + "/GochiHand.ttf"
PATRICK = FD + "/PatrickHand.ttf"

INK = (35, 32, 56)
img = Image.new("RGB", (W, H), (247, 241, 226))
d = ImageDraw.Draw(img, "RGBA")

def font(path, size):
    return ImageFont.truetype(path, size)

def wob(pts, amp=3.0):
    return [(x + random.uniform(-amp, amp), y + random.uniform(-amp, amp)) for x, y in pts]

def line(pts, fill=INK, width=5, amp=3.0, passes=2):
    for _ in range(passes):
        d.line(wob(pts, amp), fill=fill, width=width, joint="curve")

def poly(pts, fill=None, outline=INK, width=5, amp=3.0):
    if fill:
        d.polygon(wob(pts, amp), fill=fill)
    if outline:
        line(pts + [pts[0]], fill=outline, width=width, amp=amp)

def ellipse(box, fill=None, outline=INK, width=5, amp=3.0, passes=2):
    if fill:
        d.ellipse(box, fill=fill)
    if outline:
        for _ in range(passes):
            # wobbly ellipse outline via sampled points
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            rx, ry = (box[2] - box[0]) / 2, (box[3] - box[1]) / 2
            pts = [(cx + rx * math.cos(t), cy + ry * math.sin(t))
                   for t in [i * math.pi / 24 for i in range(49)]]
            d.line(wob(pts, amp), fill=outline, width=width, joint="curve")

def scribble_band(y0, y1, color, step=13):
    y = y0
    while y < y1:
        pts = [(x, y + random.uniform(-4, 4)) for x in range(-10, W + 10, 90)]
        d.line(pts, fill=color, width=random.randint(8, 13))
        y += step

def text_layer(txt, fnt, fill, angle=0.0, stroke=0):
    tmp = Image.new("RGBA", (W, 400), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = td.textlength(txt, font=fnt)
    td.text(((W - tw) / 2, 30), txt, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=(247, 241, 226))
    if angle:
        tmp = tmp.rotate(angle, expand=False, resample=Image.BICUBIC, center=(W // 2, 200))
    return tmp, tw

def paste_text(txt, fnt, y, fill=INK, angle=0.0):
    layer, _ = text_layer(txt, fnt, fill, angle)
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))
    return y

# ---------- background: sunset sky scribbles ----------
scribble_band(150, 330, (255, 205, 140))
scribble_band(330, 470, (255, 168, 128))
scribble_band(470, 600, (250, 138, 130))
scribble_band(600, 705, (240, 130, 165))

# sun
ellipse((1330, 330, 1520, 520), fill=(255, 226, 130), outline=(240, 170, 60), width=5)
for a in range(0, 360, 45):
    x1 = 1425 + 120 * math.cos(math.radians(a)); y1 = 425 + 120 * math.sin(math.radians(a))
    x2 = 1425 + 155 * math.cos(math.radians(a)); y2 = 425 + 155 * math.sin(math.radians(a))
    line([(x1, y1), (x2, y2)], fill=(240, 170, 60), width=6)

# skyline silhouette (left horizon)
for (x, wdt, hgt) in [(60, 90, 210), (160, 60, 150), (230, 110, 260), (350, 55, 130), (415, 80, 190)]:
    poly([(x, 705), (x + wdt, 705), (x + wdt, 705 - hgt), (x, 705 - hgt)], fill=(70, 55, 105), outline=None)
    for _ in range(6):
        wx, wy = x + random.randint(8, wdt - 14), 705 - random.randint(15, hgt - 15)
        d.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 220, 120))

# sea + sand
scribble_band(705, 790, (110, 190, 200), step=12)
for _ in range(26):
    x, y = random.randint(0, W - 70), random.randint(712, 778)
    line([(x, y), (x + random.randint(30, 65), y)], fill=(235, 250, 250), width=4)
d.rectangle([0, 790, W, H], fill=(243, 224, 178))
for _ in range(900):
    x, y = random.randint(0, W), random.randint(795, H)
    d.ellipse([x, y, x + 3, y + 2], fill=(214, 188, 140))

def palm(cx, cy, s=1.0, flip=1):
    pts = [(cx + flip * i * 14, cy - i * i * 0.55 - i * 6) for i in range(0, 16)]
    line(pts, fill=(120, 84, 50), width=int(13 * s))
    tx, ty = pts[-1]
    for dx, dy, droop in [(-170, -60, 95), (-120, -95, 80), (-45, -115, 70), (45, -110, 75), (125, -85, 85), (175, -45, 100)]:
        curve = []
        for k in range(13):
            t = k / 12
            x = tx + flip * dx * s * t
            y = ty + dy * s * t + droop * s * t * t
            curve.append((x, y))
        line(curve, fill=(58, 140, 74), width=int(9 * s))

palm(90, 800, 1.05, 1)
palm(1745, 810, 0.95, -1)

# ---------- tombstone ----------
stone = Image.new("RGBA", (560, 520), (0, 0, 0, 0))
sd = ImageDraw.Draw(stone)
sd.rounded_rectangle([18, 18, 542, 502], radius=170, fill=(246, 199, 212))
for _ in range(2):
    pts = []
    for t in [i * math.pi / 40 for i in range(41)]:
        pass
    sd.rounded_rectangle([18 + random.randint(-3, 3), 18 + random.randint(-3, 3),
                          542 + random.randint(-3, 3), 502 + random.randint(-3, 3)],
                         radius=170, outline=INK, width=7)
sd.line([(120, 90), (155, 150), (128, 205), (168, 262)], fill=(120, 90, 105), width=4)
sd.line([(448, 70), (420, 128), (452, 180)], fill=(120, 90, 105), width=4)
f1 = font(PATRICK, 100); f2 = font(PATRICK, 150); f3 = font(PATRICK, 56)
for txt, fnt, yy in [("BEFORE", f1, 96), ("GTA 6", f2, 196), ("2013 - 2026", f3, 356)]:
    tw = sd.textlength(txt, font=fnt)
    sd.text(((560 - tw) / 2, yy), txt, font=fnt, fill=INK)
stone = stone.rotate(1.4, expand=True, resample=Image.BICUBIC)
img.paste(stone, (620, 520), stone)
d = ImageDraw.Draw(img, "RGBA")

# grave mound + lilies
ellipse((640, 985, 1160, 1075), fill=(150, 108, 74), outline=(110, 78, 50), width=5)
def lily(x, y, s=1.0):
    for dx in (-16, 0, 16):
        ellipse((x + dx * s - 11 * s, y - 20 * s, x + dx * s + 11 * s, y + 14 * s), fill=(252, 252, 248), outline=INK, width=3)
    line([(x, y + 12 * s), (x - 4 * s, y + 42 * s)], fill=(58, 140, 74), width=4)
lily(596, 1032, 1.15); lily(1220, 1038, 1.15)

def tear(x, y, s=1.0):
    poly([(x, y), (x - 9 * s, y + 20 * s), (x + 9 * s, y + 20 * s)], fill=(110, 180, 235), outline=None)
    ellipse((x - 10 * s, y + 12 * s, x + 10 * s, y + 30 * s), fill=(110, 180, 235), outline=None)

def suit_body(x, y, wdt, hgt):
    poly([(x, y), (x + wdt, y), (x + wdt - 14, y + hgt), (x + 14, y + hgt)], fill=(38, 36, 48))
    poly([(x + wdt / 2 - 16, y), (x + wdt / 2 + 16, y), (x + wdt / 2, y + 34)], fill=(245, 245, 245), outline=None)
    line([(x + wdt / 2, y + 34), (x + wdt / 2 - 7, y + 74), (x + wdt / 2, y + 92), (x + wdt / 2 + 7, y + 74), (x + wdt / 2, y + 34)], fill=(20, 20, 28), width=5)

# ---------- mourner: old gamer (left) ----------
suit_body(255, 905, 190, 215)
ellipse((262, 700, 438, 878), fill=(242, 194, 155))                      # head
ellipse((282, 796, 418, 902), fill=(198, 198, 198), outline=None)        # beard (lower face)
for _ in range(14):                                                      # beard strokes
    x = random.randint(300, 400); y = random.randint(812, 872)
    line([(x, y), (x + random.randint(-6, 6), y + 20)], fill=(160, 160, 160), width=3)
d.pieslice([258, 644, 442, 772], 180, 360, fill=(40, 40, 52))            # cap dome
poly([(246, 722), (454, 722), (468, 742), (232, 742)], fill=(40, 40, 52)) # brim
line([(322, 838), (338, 838)], width=5)                                  # sad mouth
line([(300, 786), (326, 786)], width=5); line([(374, 786), (400, 786)], width=5)  # closed eyes
tear(313, 800); tear(388, 800)
ellipse((404, 946, 452, 994), fill=(250, 250, 250), width=4)              # tissue in hand, on suit

# ---------- mourner: streamer girl ----------
suit_body(492, 928, 150, 192)
ellipse((500, 742, 640, 882), fill=(246, 200, 160))
ellipse((498, 730, 642, 812), fill=(112, 70, 44), outline=None)           # hair cap
ellipse((506, 762, 634, 830), fill=(246, 200, 160), outline=None)         # face again
line([(628, 770), (664, 838), (652, 906)], fill=(112, 70, 44), width=17)  # ponytail down the side
line([(528, 812), (552, 812)], width=5); line([(592, 812), (616, 812)], width=5)
tear(540, 826); tear(604, 826)
line([(548, 852), (572, 846), (596, 852)], width=4)                       # wobbly mouth
ellipse((520, 962, 566, 1006), fill=(250, 250, 250), width=4)             # tissue on suit
line([(492, 800), (486, 856)], fill=INK, width=10)                        # headphone band hint
ellipse((478, 838, 506, 884), fill=(40, 40, 52), width=3)

# ---------- mourner: cat in a suit (right) ----------
suit_body(1212, 928, 150, 192)
ellipse((1218, 748, 1392, 898), fill=(168, 168, 175))
poly([(1232, 770), (1240, 706), (1290, 748)], fill=(168, 168, 175))
poly([(1330, 748), (1380, 706), (1388, 770)], fill=(168, 168, 175))
poly([(1246, 756), (1250, 724), (1276, 748)], fill=(240, 190, 200), outline=None)
poly([(1346, 748), (1372, 724), (1376, 756)], fill=(240, 190, 200), outline=None)
ellipse((1262, 812, 1284, 830), fill=INK, outline=None); ellipse((1330, 812, 1352, 830), fill=INK, outline=None)
tear(1273, 838, 1.2); tear(1341, 838, 1.2)
ellipse((1298, 846, 1316, 858), fill=(240, 150, 165), outline=None)      # nose
for yy in (852, 866):
    line([(1230, yy), (1278, yy + 4)], width=3); line([(1336, yy + 4), (1384, yy)], width=3)  # whiskers

# ---------- mourner: little robot with a flower ----------
poly([(1422, 872), (1562, 872), (1562, 1006), (1422, 1006)], fill=(178, 186, 196))  # robot body
d.rounded_rectangle([1430, 726, 1554, 856], radius=34, fill=(196, 204, 214), outline=INK, width=5)
line([(1492, 726), (1492, 678)], width=6); ellipse((1478, 656, 1506, 684), fill=(240, 120, 130))
ellipse((1458, 776, 1480, 802), fill=INK, outline=None); ellipse((1506, 776, 1528, 802), fill=INK, outline=None)
tear(1517, 806, 0.9)
line([(1472, 836), (1512, 836)], width=4)
line([(1436, 920), (1408, 962)], fill=(120, 128, 138), width=12)          # arm down
line([(1408, 962), (1396, 1006)], fill=(58, 140, 74), width=4)            # flower stem
ellipse((1382, 976, 1410, 1004), fill=(244, 130, 165), width=3)           # flower head
ellipse((1391, 985, 1401, 995), fill=(255, 205, 90), outline=None)

# ---------- the make.fun ghost, officiant front centre ----------
gx, gy = 900, 1122
ghost_pts = []
for i in range(0, 41):  # top dome
    t = math.pi * (1 - i / 40)
    ghost_pts.append((gx + 118 * math.cos(t), gy - 128 + 118 * math.sin(t) * -1 * -1))
# rebuild dome properly: from left side over the top to right side
ghost_pts = [(gx + 118 * math.cos(math.pi - math.pi * i / 40), gy - 10 - 118 * math.sin(math.pi * i / 40)) for i in range(41)]
bottom = []
for i in range(7):
    bx = gx + 118 - i * (236 / 6)
    bottom.append((bx, gy + 118 + (14 if i % 2 == 0 else -8)))
allg = ghost_pts + bottom
d.polygon(wob(allg, 2.5), fill=(253, 253, 250))
line(allg + [allg[0]], width=6, amp=2.5)
ellipse((gx - 52, gy - 66, gx - 28, gy - 38), fill=INK, outline=None)     # eyes
ellipse((gx + 28, gy - 66, gx + 52, gy - 38), fill=INK, outline=None)
tear(gx - 40, gy - 30, 0.9); tear(gx + 40, gy - 30, 0.9)
line([(gx - 16, gy + 2), (gx, gy - 6), (gx + 16, gy + 2)], width=4)      # wobbly mouth
ellipse((gx - 84, gy - 26, gx - 48, gy - 6), fill=(248, 178, 198), outline=None)  # cheeks
ellipse((gx + 48, gy - 26, gx + 84, gy - 6), fill=(248, 178, 198), outline=None)
poly([(gx - 22, gy + 44), (gx, gy + 60), (gx - 22, gy + 76)], fill=(30, 30, 40), outline=None)  # bow tie
poly([(gx + 22, gy + 44), (gx, gy + 60), (gx + 22, gy + 76)], fill=(30, 30, 40), outline=None)
ellipse((gx - 10, gy + 50, gx + 10, gy + 70), fill=(30, 30, 40), outline=None)
# bouquet in ghost's hand
for (fx, fy, col) in [(gx + 128, gy + 30, (244, 130, 165)), (gx + 152, gy + 12, (255, 205, 90)),
                      (gx + 140, gy + 52, (250, 250, 250)), (gx + 164, gy + 38, (244, 130, 165)),
                      (gx + 118, gy + 54, (255, 205, 90))]:
    line([(gx + 96, gy + 84), (fx, fy)], fill=(58, 140, 74), width=4)
    ellipse((fx - 15, fy - 15, fx + 15, fy + 15), fill=col, width=3)
    ellipse((fx - 4, fy - 4, fx + 4, fy + 4), fill=(240, 170, 60), outline=None)

# ---------- wreath with make.fun ribbon ----------
wx, wy = 1252, 1130
for r, col in [(104, (52, 128, 66)), (88, (72, 152, 84))]:
    pts = [(wx + r * math.cos(t), wy + r * math.sin(t)) for t in [i * math.pi / 30 for i in range(61)]]
    line(pts, fill=col, width=20, amp=4)
for i in range(10):
    t = i * math.pi / 5 + 0.3
    fx, fy = wx + 96 * math.cos(t), wy + 96 * math.sin(t)
    col = [(244, 130, 165), (250, 250, 250), (255, 205, 90)][i % 3]
    ellipse((fx - 13, fy - 13, fx + 13, fy + 13), fill=col, width=3)
rib = Image.new("RGBA", (360, 120), (0, 0, 0, 0))
rd = ImageDraw.Draw(rib)
rd.polygon([(10, 26), (350, 26), (350, 84), (10, 84)], fill=(250, 214, 226), outline=INK)
rd.polygon([(10, 84), (52, 84), (30, 112)], fill=(250, 214, 226), outline=INK)
rd.polygon([(350, 84), (308, 84), (330, 112)], fill=(250, 214, 226), outline=INK)
rf = font(PATRICK, 58)
tw = rd.textlength("make.fun", font=rf)
rd.text(((360 - tw) / 2, 30), "make.fun", font=rf, fill=INK)
rib = rib.rotate(-2, expand=True, resample=Image.BICUBIC)
img.paste(rib, (wx - 178, wy - 44), rib)
d = ImageDraw.Draw(img, "RGBA")

# ---------- title (hand-lettered, slightly tilted) ----------
def fit_font(txt, path, start, maxw):
    s = start
    while s > 30 and d.textlength(txt, font=font(path, s)) > maxw:
        s -= 4
    return font(path, s)

img = img.convert("RGBA")
for txt, yy, ang in [('THE "BEFORE GTA 6" MEME', 26, -0.8), ('HAS OFFICIALLY DIED', 148, 0.7)]:
    fnt = fit_font(txt, PATRICK, 132, 1700)
    layer = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    tw = ld.textlength(txt, font=fnt)
    ld.text(((W - tw) / 2 + 4, 34), txt, font=fnt, fill=(250, 246, 235))   # chalk shadow
    ld.text(((W - tw) / 2, 28), txt, font=fnt, fill=INK)
    layer = layer.rotate(ang, resample=Image.BICUBIC, center=(W // 2, 130))
    img.alpha_composite(layer, (0, yy - 20))
img = img.convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# press F
note = Image.new("RGBA", (700, 120), (0, 0, 0, 0))
nd = ImageDraw.Draw(note)
nd.text((6, 18), "press F to pay respects", font=font(PATRICK, 52), fill=(90, 74, 60))
note = note.rotate(-2.5, expand=True, resample=Image.BICUBIC)
img.paste(note, (36, 1210), note)

# paper grain
for _ in range(1600):
    x, y = random.randint(0, W), random.randint(0, H)
    d.ellipse([x, y, x + 2, y + 2], fill=(0, 0, 0, 14))

img.save("/home/hatch/workspace/makefun/entry-gta6meme/meme-handdrawn.png")
print("saved", img.size)
