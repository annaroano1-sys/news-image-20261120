"""Draw the news-image-20261120 ROUND 2 entry: a newspaper front page, 1024x1024.

Round 2 redesign vs round 1 (same six stories, same facts):
- Visual hierarchy: the two biggest stories (Shenzhen peace summit, Kyiv
  strike) get large hero panels; the other four get smaller panels.
- Key numbers are the loudest element in every panel (400+, 110, -3.7%,
  6.7, 3 leaders, 1st verdict) instead of small muted fact lines.
- Icons are bigger and more distinct (drone for Kyiv, scales, tanker,
  falling chart, seismic line, interlocking circles for the summit).
- No tiny unreadable text: smallest size is 19px.

Runs only during development (the grader never runs it). Deterministic:
no timestamps, no randomness, fixed PNG save settings.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
GREY_BORDER = (180, 175, 165)
MUTED = (70, 70, 70)
TEAL = (14, 116, 144)
RED = (185, 28, 28)
DARKRED = (153, 27, 27)
ORANGE = (180, 83, 9)
BROWN = (146, 64, 14)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_HEADER = font("DejaVuSans-Bold.ttf", 58)
F_SUB = font("DejaVuSans-Bold.ttf", 20)
F_KICKER_HERO = font("DejaVuSans-Bold.ttf", 22)
F_HEAD_HERO = font("DejaVuSans-Bold.ttf", 40)
F_BIGNUM = font("DejaVuSans-Bold.ttf", 56)
F_BIGLABEL = font("DejaVuSans-Bold.ttf", 20)
F_SUBLINE = font("DejaVuSans.ttf", 20)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_SUB2 = font("DejaVuSans.ttf", 19)
F_FOOTER = font("DejaVuSans-Bold.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------- icons (PIL shapes; s = box size in px) ----------------

def icon_peace(d, x, y, s, c):
    # three interlocking circles: the summit of three powers
    lw = max(4, s // 14)
    r = int(0.30 * s)
    d.ellipse([x + int(0.30 * s) - r, y + int(0.30 * s) - r,
               x + int(0.30 * s) + r, y + int(0.30 * s) + r],
              outline=c, width=lw)
    d.ellipse([x + int(0.70 * s) - r, y + int(0.30 * s) - r,
               x + int(0.70 * s) + r, y + int(0.30 * s) + r],
              outline=c, width=lw)
    d.ellipse([x + int(0.50 * s) - r, y + int(0.58 * s) - r,
               x + int(0.50 * s) + r, y + int(0.58 * s) + r], fill=c)


def icon_drone(d, x, y, s, c):
    # quadcopter: four rotors, arms, central body
    lw = max(4, s // 16)
    cx, cy = x + s // 2, y + s // 2
    rotors = [(x + int(0.14 * s), y + int(0.14 * s)),
              (x + int(0.86 * s), y + int(0.14 * s)),
              (x + int(0.14 * s), y + int(0.86 * s)),
              (x + int(0.86 * s), y + int(0.86 * s))]
    for rx, ry in rotors:
        d.line([rx, ry, cx, cy], fill=c, width=lw)
    for rx, ry in rotors:
        rr = int(0.13 * s)
        d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], outline=c, width=lw)
        d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=c)
    d.rectangle([x + int(0.38 * s), y + int(0.43 * s),
                 x + int(0.62 * s), y + int(0.57 * s)], fill=c)
    d.ellipse([cx - 4, cy + int(0.10 * s) - 4, cx + 4,
               cy + int(0.10 * s) + 4], fill=c)


def icon_scales(d, x, y, s, c):
    # scales of justice: post, beam, two pans
    lw = max(4, s // 14)
    d.line([x + s // 2, y + int(0.06 * s), x + s // 2, y + int(0.92 * s)],
           fill=c, width=lw)
    d.line([x + int(0.08 * s), y + int(0.20 * s),
            x + int(0.92 * s), y + int(0.20 * s)], fill=c, width=lw)
    d.line([x + int(0.40 * s), y + int(0.06 * s),
            x + int(0.60 * s), y + int(0.06 * s)], fill=c, width=lw)
    for px in (int(0.08 * s), int(0.92 * s)):
        d.line([x + px, y + int(0.20 * s), x + px - int(0.08 * s),
                y + int(0.52 * s)], fill=c, width=max(3, lw - 1))
        d.line([x + px, y + int(0.20 * s), x + px + int(0.08 * s),
                y + int(0.52 * s)], fill=c, width=max(3, lw - 1))
        d.arc([x + px - int(0.10 * s), y + int(0.48 * s),
               x + px + int(0.10 * s), y + int(0.68 * s)],
              0, 180, fill=c, width=max(3, lw - 1))


def icon_tanker(d, x, y, s, c):
    # tanker silhouette above two wave lines
    d.rectangle([x + int(0.08 * s), y + int(0.16 * s),
                 x + int(0.92 * s), y + int(0.48 * s)], fill=c)
    d.rectangle([x + int(0.60 * s), y + int(0.04 * s),
                 x + int(0.82 * s), y + int(0.16 * s)], fill=c)
    for wy in (0.64, 0.84):
        pts = [(x + int(0.02 * s), y + int(wy * s)),
               (x + int(0.25 * s), y + int((wy - 0.07) * s)),
               (x + int(0.50 * s), y + int(wy * s)),
               (x + int(0.75 * s), y + int((wy - 0.07) * s)),
               (x + int(0.98 * s), y + int(wy * s))]
        d.line(pts, fill=c, width=max(3, s // 16), joint="curve")


def icon_chart(d, x, y, s, c):
    # falling chart with a down arrow
    lw = max(3, s // 18)
    d.line([x + int(0.08 * s), y + int(0.92 * s),
            x + int(0.08 * s), y + int(0.08 * s)], fill=c, width=lw)
    d.line([x + int(0.08 * s), y + int(0.92 * s),
            x + int(0.94 * s), y + int(0.92 * s)], fill=c, width=lw)
    pts = [(x + int(0.14 * s), y + int(0.18 * s)),
           (x + int(0.38 * s), y + int(0.38 * s)),
           (x + int(0.58 * s), y + int(0.30 * s)),
           (x + int(0.86 * s), y + int(0.76 * s))]
    d.line(pts, fill=c, width=max(4, s // 12), joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - int(0.16 * s), ey - int(0.02 * s)),
               (ex - int(0.02 * s), ey - int(0.16 * s))], fill=c)


def icon_quake(d, x, y, s, c):
    # seismic zigzag, large amplitude
    pts = [(x + int(0.02 * s), y + int(0.50 * s)),
           (x + int(0.18 * s), y + int(0.50 * s)),
           (x + int(0.26 * s), y + int(0.18 * s)),
           (x + int(0.34 * s), y + int(0.82 * s)),
           (x + int(0.44 * s), y + int(0.34 * s)),
           (x + int(0.54 * s), y + int(0.66 * s)),
           (x + int(0.64 * s), y + int(0.50 * s)),
           (x + int(0.98 * s), y + int(0.50 * s))]
    d.line(pts, fill=c, width=max(4, s // 12), joint="curve")


# ---------------- panel data ----------------
# hero: (kicker, headline, icon, accent, [(big_number, label), ...], subline)
HERO = [
    ("PEACE SUMMIT", "THREE POWERS DECLARE PEACE",
     icon_peace, TEAL,
     [("3", "LEADERS"), ("1", "JOINT DECLARATION")],
     "TRUMP \u00b7 XI \u00b7 PUTIN \u2014 SHENZHEN"),
    ("WAR IN EUROPE", "RUSSIA STRIKES KYIV",
     icon_drone, RED,
     [("400+", "DRONES"), ("110", "MISSILES")],
     "8 KILLED \u00b7 ~30 WOUNDED \u00b7 2 HIT POLAND"),
]

# small: (kicker, headline, icon, accent, [(text, size, color), ...], subline|None)
SMALL = [
    ("JUSTICE", "ICJ HOLDS MYANMAR RESPONSIBLE",
     icon_scales, ORANGE,
     [("1ST GENOCIDE VERDICT", 38, ORANGE)], None),
    ("ENERGY", "HORMUZ BLOCKADE",
     icon_tanker, NAVY,
     [("TANKER ATTACKS", 44, NAVY)], "US BLOCKADE ON IRAN SHIPPING"),
    ("MARKETS", "AI SELL-OFF HITS US STOCKS",
     icon_chart, DARKRED,
     [("\u22123.7%", 48, DARKRED), ("CORRECTION", 26, DARKRED)], None),
    ("DISASTER", "QUAKE SHAKES PERU",
     icon_quake, BROWN,
     [("6.7", 52, BROWN), ("MAGNITUDE", 26, BROWN)], "CENTRAL PERU"),
]


def draw_hero(d, x0, y0, pw, ph, panel):
    kicker, headline, icon_fn, accent, cells, sub = panel
    d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 255, 255),
                outline=GREY_BORDER, width=2)
    d.rectangle([x0, y0, x0 + pw, y0 + 10], fill=accent)
    icon_fn(d, x0 + 24, y0 + 26, 88, accent)
    d.text((x0 + 128, y0 + 58), kicker, font=F_KICKER_HERO, fill=accent)
    lines = wrap(d, headline, F_HEAD_HERO, pw - 48)
    y = y0 + 128
    for line in lines[:2]:
        d.text((x0 + 24, y), line, font=F_HEAD_HERO, fill=INK)
        y += 48
    # two big-number cells
    strip_y = y0 + 226
    cell_w = (pw - 48) // 2
    for i, (num, label) in enumerate(cells):
        cx = x0 + 24 + i * cell_w
        d.text((cx, strip_y), num, font=F_BIGNUM, fill=accent)
        d.text((cx, strip_y + 62), label, font=F_BIGLABEL, fill=INK)
    d.text((x0 + 24, y0 + 314), sub, font=F_SUBLINE, fill=MUTED)


def draw_small(d, x0, y0, pw, ph, panel):
    kicker, headline, icon_fn, accent, big, sub = panel
    d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 255, 255),
                outline=GREY_BORDER, width=2)
    d.rectangle([x0, y0, x0 + pw, y0 + 8], fill=accent)
    icon_fn(d, x0 + 20, y0 + 20, 64, accent)
    d.text((x0 + 100, y0 + 43), kicker, font=F_KICKER, fill=accent)
    lines = wrap(d, headline, F_HEAD, pw - 40)
    y = y0 + 92
    for line in lines[:2]:
        d.text((x0 + 20, y), line, font=F_HEAD, fill=INK)
        y += 35
    # big fact: segments left to right, shrunk to fit the panel width
    big_y = y + 8
    sizes = [s for _, s, _ in big]
    for _ in range(4):
        total = sum(d.textlength(t, font=font("DejaVuSans-Bold.ttf", s))
                    for (t, s, _), s in zip(big, sizes)) + 14 * (len(big) - 1)
        if total <= pw - 40 or max(sizes) <= 26:
            break
        sizes = [max(26, int(s * (pw - 40) / total)) for s in sizes]
    bx = x0 + 20
    for (text, _, color), size in zip(big, sizes):
        fnt = font("DejaVuSans-Bold.ttf", size)
        d.text((bx, big_y), text, font=fnt, fill=color)
        bx += d.textlength(text, font=fnt) + 14
    if sub:
        d.text((x0 + 20, big_y + max(sizes) + 6),
               sub, font=F_SUB2, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band, 112px, dark navy
    d.rectangle([0, 0, W, 112], fill=NAVY)
    title = "20 NOVEMBER 2026"
    tw = d.textlength(title, font=F_HEADER)
    d.text(((W - tw) / 2, 16), title, font=F_HEADER, fill=(255, 255, 255))
    sub = "FRIDAY \u00b7 THE WORLD IN ONE DAY"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 82), sub, font=F_SUB, fill=(200, 214, 235))

    # Hero row: 2 large panels, 496x340
    hero_y, hero_h = 128, 340
    for i, panel in enumerate(HERO):
        draw_hero(d, 16 + i * (496 + 16), hero_y, 496, hero_h, panel)

    # Small grid: 2 rows x 2 cols, panels 496x224
    small_h = 224
    for i, panel in enumerate(SMALL):
        col, row = i % 2, i // 2
        draw_small(d, 16 + col * (496 + 16), 484 + row * (224 + 16),
                   496, small_h, panel)

    # Footer strip, 60px
    d.rectangle([0, 964, W, H], fill=NAVY)
    foot = "20 NOVEMBER 2026 \u00b7 SIX STORIES THAT DEFINED THE DAY"
    fw = d.textlength(foot, font=F_FOOTER)
    d.text(((W - fw) / 2, 985), foot, font=F_FOOTER, fill=(255, 255, 255))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
