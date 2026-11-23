#!/usr/bin/env python3
"""Render the Monday 23 November 2026 news poster (1024x1024 PNG).

Drawn entirely with PIL shapes and DejaVu type — no photos, no assets
fetched from anywhere. Run once at build time; main.py ships the PNG.
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (246, 241, 230)
INK = (24, 24, 30)
CARD = (255, 252, 244)
EDGE = (198, 188, 166)
RED = (176, 32, 32)
NAVY = (26, 44, 86)
GOLD = (186, 136, 12)
GOLD_LT = (242, 202, 92)
BODY = (52, 52, 60)
SEA = (72, 112, 162)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def fnt(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, text, font, x, y, max_w, fill, leading):
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centred(d, text, font, y, fill):
    w = d.textlength(text, font=font)
    d.text(((SIZE - w) / 2, y), text, font=font, fill=fill)


# ---------------- icons (all simple PIL geometry) ----------------

def icon_cracked_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 150, 190),
              outline=INK, width=4)
    # crude continents
    d.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.02],
              fill=(96, 160, 90))
    d.ellipse([cx + r * 0.05, cy + r * 0.08, cx + r * 0.62, cy + r * 0.58],
              fill=(96, 160, 90))
    d.ellipse([cx - r * 0.25, cy + r * 0.15, cx + r * 0.12, cy + r * 0.62],
              fill=(110, 170, 100))
    # jagged crack top to bottom
    pts = [(cx - r * 0.08, cy - r), (cx + r * 0.16, cy - r * 0.55),
           (cx - r * 0.14, cy - r * 0.12), (cx + r * 0.12, cy + r * 0.3),
           (cx - r * 0.05, cy + r * 0.68), (cx + r * 0.06, cy + r)]
    d.line(pts, fill=INK, width=6)
    # heat sun, top right
    sx, sy, sr = cx + r * 0.78, cy - r * 0.78, r * 0.3
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 150, 30),
              outline=INK, width=3)
    for k in range(8):
        a = k * math.pi / 4
        d.line([(sx + sr * 1.25 * math.cos(a), sy + sr * 1.25 * math.sin(a)),
                (sx + sr * 1.6 * math.cos(a), sy + sr * 1.6 * math.sin(a))],
               fill=(240, 150, 30), width=5)


def icon_tanker(d, cx, cy, s):
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 0.7, cy + s * 0.4),
               (cx - s * 0.7, cy + s * 0.4)], fill=NAVY)
    d.rectangle([cx - s * 0.5, cy - s * 0.3, cx + s * 0.15, cy], fill=NAVY)
    d.rectangle([cx + s * 0.38, cy - s * 0.46, cx + s * 0.6, cy], fill=NAVY)
    fx, fy = cx - s * 0.18, cy - s * 0.62
    d.polygon([(fx, fy - s * 0.5), (fx + s * 0.3, fy + s * 0.12),
               (fx + s * 0.1, fy + s * 0.28), (fx - s * 0.1, fy + s * 0.28),
               (fx - s * 0.3, fy + s * 0.12)], fill=RED)
    d.ellipse([fx - s * 0.09, fy - s * 0.02, fx + s * 0.09, fy + s * 0.22],
              fill=(242, 142, 32))
    for i in range(3):
        wy = cy + s * (0.56 + i * 0.17)
        pts = [(cx - s + j * s * 0.25, wy + (s * 0.05 if j % 2 else -s * 0.05))
               for j in range(9)]
        d.line(pts, fill=SEA, width=4)


def icon_factory(d, cx, cy, s):
    # sawtooth factory block
    d.rectangle([cx - s * 0.85, cy - s * 0.05, cx + s * 0.85, cy + s * 0.75],
                fill=(120, 92, 70), outline=INK, width=3)
    d.polygon([(cx - s * 0.85, cy - s * 0.05), (cx - s * 0.42, cy - s * 0.38),
               (cx - s * 0.42, cy - s * 0.05)], fill=(96, 72, 54))
    d.polygon([(cx - s * 0.42, cy - s * 0.05), (cx, cy - s * 0.38),
               (cx, cy - s * 0.05)], fill=(96, 72, 54))
    d.polygon([(cx, cy - s * 0.05), (cx + s * 0.42, cy - s * 0.38),
               (cx + s * 0.42, cy - s * 0.05)], fill=(96, 72, 54))
    d.polygon([(cx + s * 0.42, cy - s * 0.05), (cx + s * 0.85, cy - s * 0.38),
               (cx + s * 0.85, cy - s * 0.05)], fill=(96, 72, 54))
    # chimney + smoke (kept left so it never reaches the card text)
    d.rectangle([cx + s * 0.4, cy - s * 0.78, cx + s * 0.58, cy - s * 0.3],
                fill=(96, 72, 54), outline=INK, width=3)
    for dx, dy, rr in [(0.49, -0.95, 0.12), (0.4, -1.08, 0.16)]:
        d.ellipse([cx + s * (dx - rr), cy + s * (dy - rr),
                   cx + s * (dx + rr), cy + s * (dy + rr)], fill=(150, 150, 155))
    # windows, one lit by fire
    for wx in (-0.62, -0.28, 0.06):
        d.rectangle([cx + s * wx, cy + s * 0.18, cx + s * (wx + 0.2),
                     cy + s * 0.42], fill=(220, 230, 240), outline=INK, width=2)
    fx, fy = cx + s * 0.42, cy + s * 0.28
    d.polygon([(fx, fy - s * 0.42), (fx + s * 0.22, fy + s * 0.12),
               (fx + s * 0.07, fy + s * 0.24), (fx - s * 0.07, fy + s * 0.24),
               (fx - s * 0.22, fy + s * 0.12)], fill=RED)
    d.ellipse([fx - s * 0.07, fy + s * 0.02, fx + s * 0.07, fy + s * 0.2],
              fill=(242, 142, 32))


def icon_flats(d, cx, cy, s):
    # five-storey block, right corner sheared off
    d.polygon([(cx - s * 0.7, cy - s * 0.85), (cx + s * 0.15, cy - s * 0.85),
               (cx + s * 0.15, cy - s * 0.3), (cx + s * 0.7, cy + s * 0.25),
               (cx + s * 0.7, cy + s * 0.8), (cx - s * 0.7, cy + s * 0.8)],
              fill=(168, 156, 140), outline=INK, width=3)
    for row in range(4):
        for col in range(3):
            wx = cx - s * 0.55 + col * s * 0.34
            wy = cy - s * 0.68 + row * s * 0.34
            if col == 2 and row < 2:
                continue  # collapsed corner
            d.rectangle([wx, wy, wx + s * 0.2, wy + s * 0.22],
                        fill=(60, 66, 80))
    # rubble
    for dx, rr in [(-0.3, 0.16), (0.05, 0.2), (0.42, 0.15)]:
        d.ellipse([cx + s * (dx - rr), cy + s * (0.78 - rr * 0.6),
                   cx + s * (dx + rr), cy + s * (0.78 + rr * 0.6)],
                  fill=(130, 120, 108), outline=INK, width=2)
    # small drone, top right
    dx0, dy0 = cx + s * 0.62, cy - s * 0.72
    d.rectangle([dx0 - s * 0.14, dy0 - s * 0.07, dx0 + s * 0.14, dy0 + s * 0.07],
                fill=INK)
    for sgn in (-1, 1):
        d.line([(dx0 + sgn * s * 0.14, dy0), (dx0 + sgn * s * 0.3, dy0 - s * 0.1)],
               fill=INK, width=4)
        d.ellipse([dx0 + sgn * s * 0.3 - s * 0.09, dy0 - s * 0.16,
                   dx0 + sgn * s * 0.3 + s * 0.09, dy0 - s * 0.04],
                  outline=INK, width=3)


def icon_trophy(d, cx, cy, s):
    d.polygon([(cx - s * 0.5, cy - s * 0.8), (cx + s * 0.5, cy - s * 0.8),
               (cx + s * 0.34, cy - s * 0.05), (cx - s * 0.34, cy - s * 0.05)],
              fill=GOLD, outline=INK, width=3)
    d.arc([cx - s * 0.78, cy - s * 0.74, cx - s * 0.34, cy - s * 0.24],
          start=90, end=270, fill=GOLD, width=6)
    d.arc([cx + s * 0.34, cy - s * 0.74, cx + s * 0.78, cy - s * 0.24],
          start=270, end=90, fill=GOLD, width=6)
    d.rectangle([cx - s * 0.1, cy - s * 0.05, cx + s * 0.1, cy + s * 0.35],
                fill=GOLD, outline=INK, width=3)
    d.rectangle([cx - s * 0.42, cy + s * 0.35, cx + s * 0.42, cy + s * 0.55],
                fill=(110, 74, 40), outline=INK, width=3)
    eight = fnt(SANS_B, int(s * 0.62))
    tw = d.textlength("8", font=eight)
    d.text((cx - tw / 2, cy - s * 0.72), "8", font=eight, fill=PAPER)
    # chequered flag strip under the base
    fx0, fy0, cell = cx - s * 0.6, cy + s * 0.66, s * 0.2
    for r in range(2):
        for c in range(6):
            col = INK if (r + c) % 2 == 0 else PAPER
            d.rectangle([fx0 + c * cell, fy0 + r * cell,
                         fx0 + (c + 1) * cell, fy0 + (r + 1) * cell],
                        fill=col, outline=INK, width=1)


# ---------------- poster ----------------

def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, SIZE, 150], fill=INK)
    centred(d, "THE WORLD TODAY", fnt(SERIF_B, 62), 16, PAPER)
    centred(d, "MONDAY, 23 NOVEMBER 2026", fnt(SANS_B, 28), 98, GOLD_LT)
    d.rectangle([0, 150, SIZE, 158], fill=RED)

    # lead panel: COP31
    y = 174
    d.rounded_rectangle([36, y, SIZE - 36, y + 258], radius=14, fill=CARD,
                        outline=EDGE, width=2)
    d.rectangle([36, y, 48, y + 258], fill=RED)
    d.text((68, y + 18), "LEAD STORY  ·  CLIMATE  ·  ANTALYA, TURKEY",
           font=fnt(SANS_B, 21), fill=RED)
    yy = para(d, "COP31 climate pact collapses", fnt(SERIF_B, 42),
              68, y + 50, 620, INK, 50)
    para(d,
         "Nearly 200 nations reject a draft deal that never mentions "
         "fossil fuels. The longest COP ever ends with no agreement "
         "after about 49 hours of overtime.",
         fnt(SANS, 22), 68, yy + 4, 650, BODY, 30)
    icon_cracked_globe(d, 845, y + 132, 88)

    # four story cards
    cards = [
        ("WAR  ·  STRAIT OF HORMUZ", "Trump warns of new Iran strikes",
         "Tankers hit in the strait; Iran says it downed US drones. "
         "Strikes could resume after 1 January.",
         icon_tanker),
        ("DISASTER  ·  BANTEN, INDONESIA", "Candy factory fire: 29 missing",
         "24 body bags recovered from the Cikande plant; DNA tests to "
         "identify victims. Search resumes Monday.",
         icon_factory),
        ("WAR  ·  KYIV REGION, UKRAINE", "Drone collapses flats; 14 trapped",
         "A Russian drone partly brings down a five-storey block in "
         "Dymer. Nine evacuated, rescue under way.",
         icon_flats),
        ("SPORT  ·  PORTIMAO, PORTUGAL", "Marquez wins 8th MotoGP crown",
         "Marc Marquez seals a record-equalling eighth world title, "
         "levelling Giacomo Agostini.",
         icon_trophy),
    ]
    top = y + 280
    cw = (SIZE - 72 - 24) // 2
    ch = 190
    for i, (kick, head, body, icon) in enumerate(cards):
        cx = 36 + (i % 2) * (cw + 24)
        cy = top + (i // 2) * (ch + 24)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12, fill=CARD,
                            outline=EDGE, width=2)
        icon(d, cx + 62, cy + 94, 46)
        d.text((cx + 118, cy + 15), kick, font=fnt(SANS_B, 16), fill=RED)
        yy = para(d, head, fnt(SERIF_B, 25), cx + 118, cy + 40, cw - 134,
                  INK, 31)
        para(d, body, fnt(SANS, 18), cx + 118, yy + 2, cw - 134, BODY, 24)

    # also-today strip
    fy = top + 2 * ch + 24 + 20
    d.rectangle([0, fy, SIZE, SIZE], fill=NAVY)
    d.text((36, fy + 12), "ALSO TODAY", font=fnt(SANS_B, 22), fill=GOLD_LT)
    briefs = [
        "South Korea: education minister quits over AI exam-cheating scandal",
        "India and Nepal PMs hold talks on energy, hydropower and rail links",
        "DR Congo: WHO chief pleads for peace so Ebola fight can proceed",
    ]
    by = fy + 48
    for b in briefs:
        d.ellipse([40, by + 7, 50, by + 17], fill=GOLD_LT)
        d.text((62, by), b, font=fnt(SANS, 19), fill=PAPER)
        by += 31

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()
