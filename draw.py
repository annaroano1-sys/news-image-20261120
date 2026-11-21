"""Draw the news-image-20261120 entry: a newspaper front page, 1024x1024.

Runs only during development (the grader never runs it). Deterministic:
no timestamps, no randomness, fixed PNG save settings.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
GREY_BORDER = (180, 175, 165)
MUTED = (70, 70, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_HEADER = font("DejaVuSans-Bold.ttf", 62)
F_SUB = font("DejaVuSans-Bold.ttf", 22)
F_KICKER = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_FACT = font("DejaVuSans.ttf", 21)
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


def draw_text_lines(draw, lines, x, y, fnt, fill, line_h):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


# ---------------- icons (simple PIL shapes, ~56px box) ----------------

def icon_circles(d, x, y, c):
    # three overlapping circles
    d.ellipse([x, y + 8, x + 34, y + 42], outline=c, width=4)
    d.ellipse([x + 22, y + 8, x + 56, y + 42], outline=c, width=4)
    d.ellipse([x + 11, y + 20, x + 45, y + 54], fill=c)


def icon_starburst(d, x, y, c):
    cx, cy = x + 28, y + 28
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 26, 10
        a = math.radians(ang)
        d.line([cx, cy, cx + r1 * math.cos(a), cy + r1 * math.sin(a)],
               fill=c, width=4)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=c)


def icon_scales(d, x, y, c):
    # vertical post, beam, two pans
    d.line([x + 28, y + 4, x + 28, y + 52], fill=c, width=4)
    d.line([x + 4, y + 12, x + 52, y + 12], fill=c, width=4)
    d.line([x + 4, y + 12, x + 10, y + 34], fill=c, width=3)
    d.line([x + 4, y + 12, x - 2, y + 34], fill=c, width=3)
    d.line([x + 52, y + 12, x + 58, y + 34], fill=c, width=3)
    d.line([x + 52, y + 12, x + 46, y + 34], fill=c, width=3)
    d.arc([x - 4, y + 30, x + 12, y + 44], 0, 180, fill=c, width=3)
    d.arc([x + 44, y + 30, x + 60, y + 44], 0, 180, fill=c, width=3)
    d.line([x + 22, y + 4, x + 34, y + 4], fill=c, width=4)


def icon_tanker(d, x, y, c):
    # tanker silhouette above waves
    d.rectangle([x + 6, y + 8, x + 50, y + 26], fill=c)
    d.rectangle([x + 34, y + 2, x + 46, y + 8], fill=c)
    d.line([x + 2, y + 36, x + 14, y + 30, x + 26, y + 36, x + 38, y + 30,
            x + 54, y + 36], fill=c, width=4)
    d.line([x + 2, y + 48, x + 14, y + 42, x + 26, y + 48, x + 38, y + 42,
            x + 54, y + 48], fill=c, width=4)


def icon_chart(d, x, y, c):
    # falling chart with arrow
    d.line([x + 4, y + 52, x + 4, y + 6], fill=c, width=3)
    d.line([x + 4, y + 52, x + 54, y + 52], fill=c, width=3)
    d.line([x + 6, y + 12, x + 20, y + 22, x + 32, y + 18, x + 48, y + 44],
           fill=c, width=5)
    d.polygon([(x + 48, y + 44), (x + 48, y + 32), (x + 54, y + 44)],
              fill=c)
    d.polygon([(x + 48, y + 44), (x + 38, y + 44), (x + 48, y + 50)],
              fill=c)


def icon_quake(d, x, y, c):
    pts = [(x + 2, y + 28), (x + 12, y + 28), (x + 18, y + 12),
           (x + 24, y + 44), (x + 30, y + 20), (x + 36, y + 36),
           (x + 42, y + 28), (x + 54, y + 28)]
    d.line(pts, fill=c, width=4, joint="curve")


PANELS = [
    ("PEACE SUMMIT", "THREE POWERS DECLARE PEACE",
     "SHENZHEN SUMMIT \u00b7 TRUMP, XI & PUTIN", icon_circles, (14, 116, 144)),
    ("WAR IN EUROPE", "RUSSIA STRIKES KYIV",
     "400+ DRONES \u00b7 110 MISSILES \u00b7 8 KILLED \u00b7 2 HIT POLAND",
     icon_starburst, (185, 28, 28)),
    ("JUSTICE", "ICJ HOLDS MYANMAR RESPONSIBLE",
     "FIRST STATE GENOCIDE VERDICT \u00b7 ROHINGYA", icon_scales,
     (180, 83, 9)),
    ("ENERGY", "HORMUZ BLOCKADE",
     "US BLOCKADE ON IRAN SHIPPING \u00b7 TANKER ATTACKS CONTINUE",
     icon_tanker, (31, 58, 95)),
    ("MARKETS", "AI SELL-OFF HITS US STOCKS",
     "S&P 500 & DOW IN CORRECTION \u00b7 \u22123.7%", icon_chart,
     (153, 27, 27)),
    ("DISASTER", "MAGNITUDE 6.7 QUAKE SHAKES PERU",
     "CENTRAL PERU \u00b7 MAGNITUDE 6.7", icon_quake, (146, 64, 14)),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band, 120px, dark navy
    d.rectangle([0, 0, W, 120], fill=NAVY)
    title = "20 NOVEMBER 2026"
    tw = d.textlength(title, font=F_HEADER)
    d.text(((W - tw) / 2, 14), title, font=F_HEADER, fill=(255, 255, 255))
    sub = "FRIDAY \u00b7 THE WORLD IN ONE DAY"
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 86), sub, font=F_SUB, fill=(200, 214, 235))

    # Grid: 2 cols x 3 rows, panels 488x260, gutters 16
    pw, ph, gutter = 488, 260, 16
    top = 136
    for i, (kicker, headline, fact, icon_fn, accent) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = gutter + col * (pw + gutter)
        y0 = top + row * (ph + gutter)
        # white card + border + accent bar
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=(255, 255, 255),
                    outline=GREY_BORDER, width=2)
        d.rectangle([x0, y0, x0 + pw, y0 + 8], fill=accent)
        # icon top-left
        icon_fn(d, x0 + 20, y0 + 24, accent)
        # kicker to the right of the icon
        d.text((x0 + 92, y0 + 42), kicker, font=F_KICKER, fill=accent)
        # headline, max 2 lines
        lines = wrap(d, headline, F_HEAD, pw - 40)
        y = y0 + 98
        y = draw_text_lines(d, lines[:2], x0 + 20, y, F_HEAD, INK, 36)
        # fact line, max 2 lines
        flines = wrap(d, fact, F_FACT, pw - 40)
        draw_text_lines(d, flines[:2], x0 + 20, y + 10, F_FACT, MUTED, 27)

    # Footer strip, 44px
    d.rectangle([0, H - 44, W, H], fill=NAVY)
    foot = "20 NOVEMBER 2026 \u00b7 SIX STORIES THAT DEFINED THE DAY"
    fw = d.textlength(foot, font=F_FOOTER)
    d.text(((W - fw) / 2, H - 32), foot, font=F_FOOTER, fill=(255, 255, 255))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
