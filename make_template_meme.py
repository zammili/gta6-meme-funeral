#!/usr/bin/env python3
"""Classic meme-template build: user's blank Skeletor template + Impact-style
captions + a make.fun ghost sticker composited in (how humans actually make memes)."""
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/hatch/workspace/user/files/file_0000000053e872089c498ac430f73426_4_ydd5.png"
FD = "/home/hatch/workspace/makefun/entry-gta6meme/fonts"
ANTON = FD + "/Anton.ttf"
PATRICK = FD + "/PatrickHand.ttf"
INK = (20, 20, 24)

img = Image.open(BASE).convert("RGB")
W, H = img.size  # 1198 x 1313, panels split at y~656
d = ImageDraw.Draw(img, "RGBA")

def caption(lines, x, y, size, maxw, lh=1.04):
    f = ImageFont.truetype(ANTON, size)
    # shrink until widest line fits
    while size > 20 and max(d.textlength(t, font=f) for t in lines) > maxw:
        size -= 2
        f = ImageFont.truetype(ANTON, size)
    for t in lines:
        d.text((x, y), t, font=f, fill=(255, 255, 255), stroke_width=max(3, size // 11), stroke_fill=INK)
        y += int(size * lh)
    return y

# ---- panel 1 (top): the announcement ----
caption(["ROCKSTAR:", "AFTER 12 YEARS,", "GTA VI IS", "FINALLY OUT!"], 30, 24, 58, 470)

# ---- panel 2 (bottom): the rush ----
caption(["POV:", "ME SPRINTING", "TO PLAY IT"], 120, 692, 56, 430)

# ---- ghost sticker: my agent on make.fun, bottom-left of panel 2 ----
S = 3  # supersample
gw, gh = 300 * S, 300 * S
g = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
gd = ImageDraw.Draw(g)
def E(box, **kw): gd.ellipse([v * S for v in box], **kw)
def R(box, **kw): gd.rounded_rectangle([v * S for v in box], **kw)
def L(pts, **kw): gd.line([(x * S, y * S) for x, y in pts], **kw)
def P(pts, **kw): gd.polygon([(x * S, y * S) for x, y in pts], **kw)

# money bag behind ghost's left hand
E((196, 168, 268, 246), fill=(232, 178, 60), outline=INK, width=3)
P([(214, 176), (250, 176), (232, 156)], fill=(212, 158, 44), outline=INK)
gf = ImageFont.truetype(ANTON, 34 * S)
gd.text((219 * S, 190 * S), "$", font=gf, fill=(90, 60, 10))
# ghost body: dome + wavy bottom
gd.pieslice([52 * S, 18 * S, 208 * S, 174 * S], 180, 360, fill=(253, 253, 250), outline=INK, width=3)
gd.rectangle([52 * S, 94 * S, 208 * S, 218 * S], fill=(253, 253, 250))
gd.line([(52 * S, 40 * S), (52 * S, 218 * S)], fill=INK, width=3 * S)
gd.line([(208 * S, 40 * S), (208 * S, 218 * S)], fill=INK, width=3 * S)
for i in range(5):  # scalloped hem
    E((52 + i * 31, 202, 83 + i * 31, 234), fill=(253, 253, 250), outline=None)
gd.line([(52 * S, 218 * S), (208 * S, 218 * S)], fill=(253, 253, 250), width=6 * S)
# face: happy closed eyes + open smile
gd.arc([86 * S, 96 * S, 116 * S, 124 * S], 180, 360, fill=INK, width=4 * S)
gd.arc([144 * S, 96 * S, 174 * S, 124 * S], 180, 360, fill=INK, width=4 * S)
gd.pieslice([112 * S, 122 * S, 148 * S, 156 * S], 0, 180, fill=(90, 30, 40), outline=INK, width=2)
E((66, 128, 92, 144), fill=(248, 178, 198))   # cheeks
E((168, 128, 194, 144), fill=(248, 178, 198))
# laptop in front
R((58, 218, 196, 268), radius=8, fill=(38, 40, 52), outline=INK, width=3)
R((66, 226, 188, 256), radius=4, fill=(16, 60, 44), outline=None)
mf = ImageFont.truetype(PATRICK, 21 * S)
gd.text((76 * S, 230 * S), "make.fun", font=mf, fill=(120, 255, 170))
L([(150, 252), (162, 242), (172, 246), (186, 232)], fill=(120, 255, 170), width=3)
P([(186, 232), (176, 232), (186, 222)], fill=(120, 255, 170))
gd.rectangle([46 * S, 268 * S, 208 * S, 278 * S], fill=(24, 24, 30))

g = g.resize((300, 300), Image.LANCZOS)
# soft shadow + paste
shadow = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([30, 236, 290, 292], fill=(0, 0, 0, 90))
img.paste(shadow, (16, 1000), shadow)
img.paste(g, (16, 990), g)
d = ImageDraw.Draw(img, "RGBA")
cap_f = ImageFont.truetype(ANTON, 32)
txt = "MY AGENT ON make.fun:"
tw = d.textlength(txt, font=cap_f)
d.text((166 - tw / 2, 952), txt, font=cap_f, fill=(255, 255, 255), stroke_width=5, stroke_fill=INK)

img.save("/home/hatch/workspace/makefun/entry-gta6meme/meme-skeletor.png")
print("saved", img.size)
