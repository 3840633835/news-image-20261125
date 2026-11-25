# main.py — "Wednesday 25 November 2026" news front page (generator).
#
# Draws the entry image, entry.png, next to this file, using only the
# Python standard library and Pillow. Every shape, scene and letter is
# drawn in code: no photographs, no external images, no network, no
# clock, no randomness. Running this file twice writes byte-identical
# PNGs.
#
# This is the dev-time generator, NOT the graded entrypoint: the
# grading container installs nothing (standard library only), so the
# entrypoint is the tiny stdlib-only main.py beside it, which copies
# the generated entry.png to /output/entry.png — the simplest entry
# the competition rules describe ("a repository holding the image and
# a one-line program that copies it there").
#
#   python3 generate.py            # writes ./entry.png
#   MAKEFUN_OUTPUT_DIR=out python3 generate.py
#
# Fonts: DejaVu Serif / DejaVu Sans (fonts/ beside this file), freely
# licensed under the DejaVu license (see fonts/README.md). The program
# loads them from its own directory, so it needs no system fonts.

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"

W, H = 1024, 1024
PAPER = (247, 243, 232)      # warm newsprint cream
INK = (20, 20, 20)           # near-black text
RED = (169, 28, 28)          # headline red
DARKRED = (140, 20, 20)
GOLD = (201, 162, 39)
BLACKBAR = (17, 17, 17)
MUTED = (90, 84, 70)
RULE = (180, 172, 150)
CARD = (255, 253, 246)

# Region colours (used by the region bar, kickers and map pins).
REGION_COLORS = {
    "ASIA": (192, 57, 43),
    "MIDDLE EAST": (214, 137, 16),
    "EUROPE": (46, 109, 164),
    "AMERICAS": (30, 132, 73),
    "AFRICA": (125, 60, 152),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

# ---------------------------------------------------------------- fonts

def font(name, size):
    """Load a bundled font; fall back to Pillow's built-in font."""
    try:
        return ImageFont.truetype(str(FONTS / name), size)
    except OSError:
        return ImageFont.load_default()


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


# ---------------------------------------------------------------- text

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_serif_b(draw, text, max_w, start):
    """Largest serif-bold size <= start that fits max_w (deterministic)."""
    size = start
    while size > 10 and draw.textlength(text, font=serif_b(size)) > max_w:
        size -= 1
    return serif_b(size)


def centre(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- data
# Every story below was reported on Wednesday 25 November 2026 (or
# announced late Tuesday 24 Nov and reported on the 25th — those three
# are flagged in the DATE CHECK box). Sources: AP, Reuters, AFP,
# Eurostat, UN, WHO, CAF/CAS, ABC, Guardian, SCMP, Yonhap, CNBC.
# See METHODOLOGY.md for the source list.

BIG = [
    {
        "num": 1, "region": "ASIA", "label": "CONFIRMED",
        "kicker": "LIFTOFF  ·  JIUQUAN, CHINA  ·  SPACE",
        "headline": "Pakistan's first astronaut flies to Tiangong",
        "summary": ("Zeeshan Ali, 40, is the first foreigner aboard "
                    "China's space station. Shenzhou-24 docked 3\u00bd hours "
                    "after liftoff, with Tang Hongbo and Wu Yi."),
        "source": "AP  ·  REUTERS", "scene": "rocket",
    },
    {
        "num": 2, "region": "ASIA", "label": "CONFIRMED",
        "kicker": "SELL-OFF  ·  SEOUL, TAIPEI, TOKYO  ·  MARKETS",
        "headline": "Asia's chip stocks crash on AI doubts",
        "summary": ("Kospi \u22126.2%, Taiex \u22124.8%, Nikkei \u22123%. "
                    "Samsung \u22129.9%, SK Hynix \u221211.1%; Nvidia's "
                    "boardroom row fails to calm markets."),
        "source": "YONHAP  ·  CNBC", "scene": "chips",
    },
    {
        "num": 3, "region": "MIDDLE EAST", "label": "CLAIM",
        "kicker": "WAR AT SEA  ·  STRAIT OF HORMUZ  ·  IRAN",
        "headline": "Two oil tankers hit mines and burn, Iran says",
        "summary": ("The IRGC Navy says two more tankers took an "
                    "\u201cunauthorised route\u201d early on Wednesday. "
                    "Shipping fears rise; Brent slips below $90."),
        "source": "IRIB  ·  ARAB NEWS", "scene": "tanker",
    },
]

SMALL = [
    {
        "num": 4, "region": "OCEANIA", "label": "OFFICIAL",
        "kicker": "CANBERRA, AUSTRALIA",
        "headline": "Australia and Solomons sign security treaty",
        "summary": ("No foreign bases allowed; Australia becomes the "
                    "islands' main security partner. A$980m over 10 years."),
        "scene": "treaty",
    },
    {
        "num": 5, "region": "AMERICAS", "label": "OFFICIAL",
        "kicker": "NEW YORK, US",
        "headline": "Huawei guilty on 10 of 12 counts",
        "summary": ("US jury: trade secrets, bank fraud, sanctions. "
                    "Acquitted of racketeering. Verdict Tue, reported Wed."),
        "scene": "gavel",
    },
    {
        "num": 6, "region": "EUROPE", "label": "REPORTED",
        "kicker": "SAMARA, RUSSIA",
        "headline": "Ukrainian drones hit two Russian refineries",
        "summary": ("Syzran and Kuibyshev struck; Putin calls retaliation "
                    "\u201cinevitable\u201d. Kyiv also claims a warship sunk off Libya."),
        "scene": "refinery",
    },
    {
        "num": 7, "region": "AFRICA", "label": "OFFICIAL",
        "kicker": "LAUSANNE, SWITZERLAND",
        "headline": "Senegal regain AFCON title",
        "summary": ("Sport's top court overturns Morocco's 3\u20130 forfeit; "
                    "Senegal's 1\u20130 final win stands. Ruling Tue, reported Wed."),
        "scene": "trophy",
    },
    {
        "num": 8, "region": "AMERICAS", "label": "OFFICIAL",
        "kicker": "NEW YORK, US",
        "headline": "Nor'easter threatens Thanksgiving parade",
        "summary": ("Macy's parade faces heavy rain and high winds in one "
                    "of the wettest, windiest Thanksgivings in decades."),
        "scene": "storm",
    },
    {
        "num": 9, "region": "GLOBAL", "label": "REPORTED",
        "kicker": "WASHINGTON, US",
        "headline": "CIA breach: US spy systems hacked",
        "summary": ("CIA, NGA and spy chief's office hit; an open-source "
                    "intel system was exposed. NYT first reported it."),
        "scene": "breach",
    },
    {
        "num": 10, "region": "ASIA", "label": "OFFICIAL",
        "kicker": "BOGOR, INDONESIA",
        "headline": "26 trapped in flooded Java gold mine",
        "summary": ("Rescuers search a 100-metre pit at Pongkor after "
                    "a river burst its banks. Rain hampers the pumps."),
        "scene": "mine",
    },
    {
        "num": 11, "region": "AFRICA", "label": "OFFICIAL",
        "kicker": "ITURI, DR CONGO",
        "headline": "WHO evacuates Ebola staff in Congo",
        "summary": ("Health workers safe after 3 days sheltering in Akwe "
                    "hospital amid fighting; Ebola team moved out of Mongbwalu."),
        "scene": "hospital",
    },
]

# In-brief items: one terse line each (number, headline). All verified
# in 25 November 2026 reporting; see METHODOLOGY.md.
BRIEF = [
    (12, "Zelensky: Ukraine needs \u20ac115bn aid for 2027"),
    (13, "Eurozone inflation up to 4.0% (Eurostat)"),
    (14, "Australian inflation 4.9%; RBA to hold"),
    (15, "UK bills +26% to \u00a32,166 a year from January"),
    (16, "Abrego Garcia leaves US for Spain"),
    (17, "Cartagena siege ends; hostages freed"),
    (18, "UN: aid cuts threaten HIV progress"),
    (19, "EasyJet profit \u221289% as fuel costs soar"),
    (20, "Amazon buys Decart to rival Nvidia chips"),
    (21, "Hackers' AI agents broke into a US server"),
    (22, "Anthropic shares fall below IPO price"),
    (23, "Coalition strikes Houthi-held Hodeidah port"),
    (24, "Congo rebels halt march on Bunia"),
    (25, "Car bomb in Colombia injures 23"),
    (26, "Malaysia sues Google for $146m"),
    (27, "Roche cancer pill wins 2nd FDA nod"),
    (28, "China probes Shanghai chief Chen Jining"),
    (29, "EU plans \u20ac50bn tech fund"),
    (30, "Iran: ready to withstand a US blockade"),
]

# Region counts across all 30 stories (must sum to 30).
REGIONS = [("ASIA", 5), ("MIDDLE EAST", 4), ("EUROPE", 5), ("AMERICAS", 9),
           ("AFRICA", 3), ("OCEANIA", 2), ("GLOBAL", 2)]

# Map pins: (story number, longitude, latitude). Positions are
# approximate; 5/8/9 share the US east coast and are spread slightly.
PINS = [
    (1, 98.5, 39.7), (2, 127.0, 37.5), (3, 56.5, 26.5),
    (4, 149.0, -35.3), (5, -74.0, 42.0), (6, 50.0, 53.2),
    (7, -6.8, 34.0), (8, -66.0, 45.0), (9, -80.0, 35.0),
    (10, 106.9, -6.7), (11, 29.5, 1.5),
]

# ---------------------------------------------------------------- scenes
# All artwork is drawn from fixed coordinates — no random module, no
# timestamps, so the output is identical on every run.

def stars(draw, x0, y0, x1, y1):
    """Deterministic star field from a fixed arithmetic pattern."""
    for i in range(46):
        sx = x0 + ((i * 37 + 11) % max(1, (x1 - x0 - 6))) + 3
        sy = y0 + ((i * 53 + 7) % max(1, (y1 - y0 - 6))) + 3
        r = 1 if i % 3 else 2
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))


def scene_rocket(draw, x, y, w, h):
    # Night sky.
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 54))
    stars(draw, x, y, x + w, y + h - 26)
    # Moon.
    draw.ellipse([x + w - 52, y + 10, x + w - 28, y + 34], fill=(238, 232, 200))
    # Ground.
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(52, 44, 34))
    draw.rectangle([x, y + h - 30, x + w, y + h - 26], fill=(120, 110, 88))
    # Launch tower.
    tx = x + 34
    draw.rectangle([tx, y + 18, tx + 6, y + h - 26], fill=(140, 140, 140))
    for by in range(y + 24, y + h - 30, 12):
        draw.line([tx, by, tx + 6, by + 8], fill=(100, 100, 100), width=2)
    # Rocket body.
    rx, rw = x + w // 2 - 13, 26
    ry = y + 22
    draw.polygon([(rx, ry + 26), (rx + rw // 2, ry), (rx + rw, ry + 26)],
                 fill=(178, 34, 34))
    draw.rectangle([rx, ry + 26, rx + rw, ry + 62], fill=(245, 245, 240))
    draw.rectangle([rx, ry + 40, rx + rw, ry + 48], fill=(30, 90, 160))
    draw.polygon([(rx - 8, ry + 62), (rx, ry + 44), (rx, ry + 62)],
                 fill=(178, 34, 34))
    draw.polygon([(rx + rw + 8, ry + 62), (rx + rw, ry + 44),
                  (rx + rw, ry + 62)], fill=(178, 34, 34))
    # Flame.
    draw.polygon([(rx + 4, ry + 62), (rx + rw // 2, ry + h - 26),
                  (rx + rw - 4, ry + 62)], fill=(255, 140, 0))
    draw.polygon([(rx + 9, ry + 62), (rx + rw // 2, ry + h - 34),
                  (rx + rw - 9, ry + 62)], fill=(255, 220, 60))
    # Tiangong station, top right, on a dashed path.
    sx, sy = x + w - 78, y + 52
    draw.line([x + w // 2 + 20, y + 30, sx - 6, sy + 6], fill=(200, 200, 220),
              width=2)
    draw.rectangle([sx - 26, sy - 3, sx - 8, sy + 3], fill=(180, 190, 210))
    draw.rectangle([sx + 8, sy - 3, sx + 26, sy + 3], fill=(180, 190, 210))
    draw.rectangle([sx - 8, sy - 6, sx + 8, sy + 6], fill=(230, 230, 235))
    draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(30, 90, 160))
    draw.text((sx - 34, sy + 10), "TIANGONG", font=sans_b(9),
              fill=(220, 220, 230))


def scene_chips(draw, x, y, w, h):
    # Dark trading screen.
    draw.rectangle([x, y, x + w, y + h], fill=(12, 18, 38))
    # Candlesticks falling left to right (fixed heights).
    bars = [62, 58, 66, 52, 48, 40, 44, 30, 34, 22, 18]
    bw = (w - 16) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 8 + i * bw
        top = y + h - 22 - bh
        col = (220, 60, 50) if i % 3 else (60, 180, 110)
        draw.rectangle([bx + 2, top, bx + bw - 2, y + h - 22], fill=col)
        draw.line([bx + bw // 2, top - 6, bx + bw // 2, y + h - 16],
                  fill=col, width=1)
    # Red trend line.
    pts = [(x + 8 + i * bw + bw // 2, y + h - 26 - bars[i]) for i in range(len(bars))]
    draw.line(pts, fill=(255, 80, 60), width=3)
    # Chip with AI.
    cx, cy, cs = x + 14, y + 12, 52
    draw.rectangle([cx - 4, cy - 4, cx + cs + 4, cy + cs + 4], fill=(20, 40, 70),
                   outline=(90, 140, 190), width=2)
    for px in range(cx + 6, cx + cs - 4, 10):
        draw.line([px, cy - 4, px, cy], fill=(140, 180, 220), width=2)
        draw.line([px, cy + cs, px, cy + cs + 4], fill=(140, 180, 220), width=2)
    for py in range(cy + 6, cy + cs - 4, 10):
        draw.line([cx - 4, py, cx, py], fill=(140, 180, 220), width=2)
        draw.line([cx + cs, py, cx + cs + 4, py], fill=(140, 180, 220), width=2)
    draw.text((cx + 12, cy + 14), "AI", font=sans_b(20), fill=(255, 255, 255))


def scene_tanker(draw, x, y, w, h):
    # Sunset sky and sea. Hull sits low so flames and smoke stay
    # inside the panel (art height h, here 96).
    draw.rectangle([x, y, x + w, y + h], fill=(214, 120, 50))
    draw.ellipse([x + w - 70, y + 8, x + w - 26, y + 52], fill=(255, 200, 90))
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(24, 48, 84))
    # Land: Iran left, Oman right.
    draw.polygon([(x, y + h - 46), (x, y + 40), (x + 78, y + 58),
                  (x + 96, y + h - 46)], fill=(120, 86, 52))
    draw.polygon([(x + w, y + h - 46), (x + w, y + 48), (x + w - 72, y + 62),
                  (x + w - 92, y + h - 46)], fill=(120, 86, 52))
    draw.text((x + 8, y + 42), "IRAN", font=sans_b(11), fill=(255, 255, 255))
    draw.text((x + w - 56, y + 40), "OMAN", font=sans_b(11),
              fill=(255, 255, 255))
    # Tanker hull.
    hx, hy = x + 62, y + h - 40
    draw.polygon([(hx, hy), (hx + 176, hy), (hx + 164, hy + 22),
                  (hx + 12, hy + 22)], fill=(90, 30, 26))
    draw.rectangle([hx + 18, hy - 22, hx + 62, hy], fill=(200, 200, 200))
    draw.rectangle([hx + 70, hy - 14, hx + 150, hy], fill=(160, 60, 40))
    draw.rectangle([hx + 156, hy - 30, hx + 168, hy], fill=(220, 220, 220))
    # Flames (short enough to stay inside the panel) and smoke.
    for fx, fh in [(hx + 84, 26), (hx + 118, 32), (hx + 146, 22)]:
        draw.polygon([(fx - 12, hy - 12), (fx, hy - 12 - fh),
                      (fx + 12, hy - 12)], fill=(255, 140, 0))
        draw.polygon([(fx - 6, hy - 12), (fx, hy - 12 - fh + 12),
                      (fx + 6, hy - 12)], fill=(255, 220, 60))
    for fx, fh, sr in [(hx + 84, 26, 7), (hx + 118, 32, 9), (hx + 146, 22, 6)]:
        sx, sy = fx, hy - 12 - fh - 2
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 70, 70))
    # Naval mine, in open sea left of the hull, with its label.
    mx, my = x + 30, y + h - 16
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(30, 30, 30))
    for ang in range(0, 360, 45):
        import math
        dx = int(13 * math.cos(math.radians(ang)))
        dy = int(13 * math.sin(math.radians(ang)))
        draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)
    draw.text((mx + 16, my + 2), "NAVAL MINE", font=sans_b(8),
              fill=(255, 255, 255))


def small_scene(draw, kind, x, y, w, h):
    """Small drawn icon panel for one of the 8 secondary stories."""
    if kind == "treaty":
        draw.rectangle([x, y, x + w, y + h], fill=(210, 228, 240))
        draw.rectangle([x + 10, y + 10, x + 66, y + h - 12], fill=(0, 40, 104))
        for sx, sy in [(22, 18), (44, 26), (30, 38), (54, 16), (16, 34)]:
            draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                         fill=(255, 255, 255))
        draw.rectangle([x + 76, y + 10, x + 132, y + h - 12], fill=(0, 120, 80))
        draw.polygon([(x + 76, y + h - 12), (x + 132, y + 10),
                      (x + 132, y + 26), (x + 76, y + h - 12)],
                     fill=(252, 209, 22))
        draw.rectangle([x + 146, y + 12, x + w - 10, y + h - 12],
                       fill=(255, 255, 255), outline=(120, 110, 80))
        draw.line([x + 152, y + 22, x + w - 16, y + 22], fill=(30, 60, 120), width=2)
        draw.line([x + 152, y + 30, x + w - 16, y + 30], fill=(120, 120, 120), width=1)
        draw.line([x + 152, y + 38, x + w - 26, y + 38], fill=(120, 120, 120), width=1)
        draw.text((x + 152, y + 44), "SIGNED \u00b7 25 NOV", font=sans_b(9),
                  fill=(30, 60, 120))
    elif kind == "gavel":
        draw.rectangle([x, y, x + w, y + h], fill=(232, 224, 205))
        draw.rectangle([x + 16, y + 14, x + 78, y + 34], fill=(120, 72, 32))
        draw.rectangle([x + 70, y + 24, x + 150, y + 32], fill=(90, 54, 24))
        draw.ellipse([x + 150, y + 18, x + 162, y + 38], fill=(90, 54, 24))
        draw.rectangle([x + 30, y + 46, x + 120, y + 54], fill=(90, 54, 24))
    elif kind == "refinery":
        draw.rectangle([x, y, x + w, y + h], fill=(250, 220, 180))
        draw.rectangle([x + 14, y + 26, x + 34, y + h - 8], fill=(90, 90, 95))
        draw.rectangle([x + 44, y + 18, x + 64, y + h - 8], fill=(110, 110, 115))
        draw.rectangle([x + 74, y + 30, x + 118, y + h - 8], fill=(140, 140, 145))
        draw.polygon([(x + 132, y + h - 8), (x + 132, y + 34), (x + 152, y + 34),
                      (x + 152, y + h - 8)], fill=(90, 90, 95))
        draw.polygon([(x + 44, y + 18), (x + 54, y - 2), (x + 64, y + 18)],
                     fill=(255, 140, 0))
        draw.polygon([(x + 48, y + 18), (x + 54, y + 6), (x + 60, y + 18)],
                     fill=(255, 220, 60))
        draw.ellipse([x + 128, y + 2, x + 146, y + 20], fill=(120, 120, 120))
        draw.ellipse([x + 142, y + 8, x + 158, y + 24], fill=(100, 100, 100))
    elif kind == "trophy":
        draw.rectangle([x, y, x + w, y + h], fill=(20, 60, 40))
        draw.rectangle([x, y, x + w, y + 10], fill=(0, 150, 70))
        draw.rectangle([x, y + 10, x + w, y + 18], fill=(252, 209, 22))
        draw.rectangle([x, y + 18, x + w, y + 26], fill=(220, 40, 40))
        cx, cy = x + w // 2, y + 34
        draw.polygon([(cx - 26, cy), (cx + 26, cy), (cx + 18, cy + 22),
                      (cx - 18, cy + 22)], fill=(255, 200, 40))
        draw.ellipse([cx - 34, cy - 2, cx - 18, cy + 12], outline=(255, 200, 40),
                     width=4)
        draw.ellipse([cx + 18, cy - 2, cx + 34, cy + 12], outline=(255, 200, 40),
                     width=4)
        draw.rectangle([cx - 4, cy + 22, cx + 4, cy + 32], fill=(255, 200, 40))
        draw.rectangle([cx - 16, cy + 32, cx + 16, cy + 38], fill=(255, 200, 40))
    elif kind == "storm":
        draw.rectangle([x, y, x + w, y + h], fill=(190, 205, 220))
        draw.ellipse([x + 12, y + 6, x + 62, y + 34], fill=(70, 80, 100))
        draw.ellipse([x + 40, y + 2, x + 96, y + 34], fill=(90, 100, 120))
        draw.ellipse([x + 76, y + 10, x + 120, y + 34], fill=(70, 80, 100))
        for rx in range(x + 20, x + w - 20, 16):
            draw.line([rx, y + 40, rx - 5, y + 56], fill=(40, 90, 160), width=2)
        draw.ellipse([x + 140, y + 8, x + 208, y + 44], fill=(200, 60, 60))
        draw.line([x + 174, y + 44, x + 174, y + 54], fill=(80, 60, 40), width=2)
        draw.rectangle([x + 164, y + 54, x + 184, y + 62], fill=(120, 80, 40))
    elif kind == "breach":
        draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
        draw.polygon([(x + w // 2, y + 6), (x + w - 30, y + 16),
                      (x + w - 30, y + 40), (x + w // 2, y + 60),
                      (x + 30, y + 40), (x + 30, y + 16)], fill=(40, 90, 160))
        draw.polygon([(x + w // 2, y + 12), (x + w - 36, y + 20),
                      (x + w - 36, y + 38), (x + w // 2, y + 54),
                      (x + 36, y + 38), (x + 36, y + 20)], fill=(24, 32, 54))
        draw.rectangle([x + w // 2 - 12, y + 26, x + w // 2 + 12, y + 46],
                       fill=(255, 255, 255))
        draw.ellipse([x + w // 2 - 4, y + 30, x + w // 2 + 4, y + 38],
                     fill=(24, 32, 54))
        draw.rectangle([x + w // 2 - 2, y + 36, x + w // 2 + 2, y + 44],
                       fill=(24, 32, 54))
        draw.polygon([(x + 8, y + h - 8), (x + 26, y + h - 30), (x + 44, y + h - 8)],
                     fill=(255, 200, 0))
        draw.text((x + 17, y + h - 22), "!", font=sans_b(14), fill=(20, 20, 20))
    elif kind == "mine":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 200, 160))
        draw.polygon([(x, y + h), (x, y + 26), (x + 60, y + 14),
                      (x + 130, y + 26), (x + w, y + 12), (x + w, y + h)],
                     fill=(120, 100, 60))
        draw.polygon([(x + 30, y + 26), (x + 90, y + 26), (x + 110, y + h),
                      (x + 10, y + h)], fill=(90, 60, 30))
        draw.line([x + 40, y + 30, x + 34, y + h - 6], fill=(240, 220, 180), width=3)
        draw.line([x + 70, y + 28, x + 66, y + h - 6], fill=(240, 220, 180), width=3)
        draw.rectangle([x + w - 52, y + 6, x + w - 6, y + 24], fill=(178, 34, 34))
        draw.text((x + w - 46, y + 9), "100 m", font=sans_b(11),
                  fill=(255, 255, 255))
    elif kind == "hospital":
        draw.rectangle([x, y, x + w, y + h], fill=(210, 230, 220))
        draw.rectangle([x + 40, y + 14, x + 150, y + h - 6], fill=(255, 255, 255),
                       outline=(120, 130, 120))
        draw.rectangle([x + 150, y + 30, x + 190, y + h - 6], fill=(235, 235, 235),
                       outline=(120, 130, 120))
        for wx in (56, 82, 108, 160):
            draw.rectangle([x + wx, y + 28, x + wx + 14, y + 42], fill=(140, 190, 220))
        draw.rectangle([x + w // 2 - 18, y + 2, x + w // 2 - 8, y + 22],
                       fill=(200, 30, 30))
        draw.rectangle([x + w // 2 - 28, y + 7, x + w // 2 + 2, y + 17],
                       fill=(200, 30, 30))
        draw.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 6], fill=(90, 120, 90))
        draw.text((x + 8, y + 38), "WHO", font=sans_b(10), fill=(20, 90, 60))


# Simplified continent outlines (lon, lat) — stylised, recognisable.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
     (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40),
     (-75, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68),
     (45, 68), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 42), (-2, 37)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (40, 15), (48, 11), (51, 12), (45, 0), (40, -10),
     (35, -20), (32, -29), (25, -34), (18, -35), (15, -27), (12, -18),
     (9, -5), (9, 4), (-8, 5)],
    [(30, 70), (50, 70), (70, 73), (90, 75), (110, 74), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 58), (158, 52),
     (150, 59), (142, 50), (140, 45), (135, 43), (130, 42), (127, 40),
     (122, 38), (120, 32), (122, 28), (118, 25), (110, 20), (108, 12),
     (105, 9), (100, 8), (98, 12), (95, 16), (92, 21), (90, 22),
     (86, 20), (80, 15), (77, 8), (75, 12), (72, 20), (66, 25),
     (61, 25), (57, 26), (52, 28), (50, 30), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (28, 41), (27, 45), (30, 50),
     (30, 55), (30, 60)],
    [(114, -22), (122, -14), (132, -12), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (130, -32),
     (124, -33), (115, -35), (114, -22)],
]

# ---------------------------------------------------------------- layout

def label_badge(draw, x, y, text, fill):
    fnt = sans_b(10)
    w = int(draw.textlength(text, font=fnt)) + 12
    draw.rectangle([x, y, x + w, y + 16], fill=fill)
    draw.text((x + 6, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def num_badge(draw, x, y, num, fill=RED):
    r = 13
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill,
                 outline=(255, 255, 255), width=2)
    t = str(num)
    fnt = sans_b(13 if num < 10 else 11)
    tw = draw.textlength(t, font=fnt)
    draw.text((x + r - tw / 2, y + 5), t, font=fnt, fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx

    # ---- top black bar
    draw.rectangle([0, 0, W, 24], fill=BLACKBAR)
    draw.text((mx, 5), "THE WORLD IN ONE DAY", font=sans_b(11), fill=GOLD)
    right = "30 STORIES  \u00b7  ALL FROM WEDNESDAY 25 NOVEMBER 2026"
    tw = draw.textlength(right, font=sans_b(11))
    draw.text((W - mx - tw, 5), right, font=sans_b(11), fill=(255, 255, 255))

    # ---- masthead
    title = "Wednesday 25 November 2026"
    tfnt = fit_serif_b(draw, title, cw, 58)
    draw.text((mx, 30), title, font=tfnt, fill=INK)
    draw.rectangle([mx, 102, W - mx, 105], fill=RED)
    sub = ("Pakistan's first astronaut flies to Tiangong  \u25c6  "
           "Tankers burn in Hormuz  \u25c6  Asia's chip stocks crash")
    sfnt = serif(19)
    while draw.textlength(sub, font=sfnt) > cw and sfnt.size > 12:
        sfnt = serif(sfnt.size - 1)
    centre(draw, 110, sub, sfnt, DARKRED)

    # ---- stat strip: six numbers that say the day at a glance
    stats = [
        ("1st", "Pakistani astronaut\nin orbit"),
        ("\u22126.2%", "Kospi, as Asia's\nchip stocks plunge"),
        ("2", "tankers hit mines in\nHormuz, Iran's IRGC says"),
        ("\u20ac115bn", "aid Ukraine says it\nneeds for 2027"),
        ("26", "miners trapped in a\nflooded West Java pit"),
        ("+36%", "Bangladesh garment\nminimum wage"),
    ]
    sy = 132
    cell = cw // 6
    for i, (num, cap) in enumerate(stats):
        x = mx + i * cell
        if i:
            draw.line([x, sy + 4, x, sy + 42], fill=RULE, width=1)
        draw.text((x + 8, sy), num, font=serif_b(24), fill=RED)
        yy = sy + 28
        for line in cap.split("\n"):
            draw.text((x + 8, yy), line, font=sans(10), fill=INK)
            yy += 11

    # ---- region bar
    ry = 194
    total = sum(c for _, c in REGIONS)
    x = mx
    for name, count in REGIONS:
        seg = int(round(cw * count / total))
        col = REGION_COLORS[name]
        draw.rectangle([x, ry, x + seg, ry + 16], fill=col)
        lab = f"{name} {count}"
        lf = sans_b(9)
        if draw.textlength(lab, font=lf) + 6 <= seg:
            draw.text((x + 4, ry + 3), lab, font=lf, fill=(255, 255, 255))
        x += seg

    # ---- three big stories with drawn scenes
    by = 216
    bw = 317
    bxs = [mx, mx + 329, mx + 658]
    scenes = {"rocket": scene_rocket, "chips": scene_chips,
              "tanker": scene_tanker}
    for story, bx in zip(BIG, bxs):
        draw.rectangle([bx, by, bx + bw, by + 222], fill=CARD,
                       outline=RULE, width=1)
        scenes[story["scene"]](draw, bx + 1, by + 1, bw - 2, 96)
        num_badge(draw, bx + 8, by + 8, story["num"])
        lab = story["label"]
        lw = int(draw.textlength(lab, font=sans_b(10))) + 12
        draw.rectangle([bx + bw - 6 - lw, by + 8, bx + bw - 6, by + 24],
                       fill=(34, 120, 60) if lab == "CONFIRMED"
                       else (169, 28, 28))
        draw.text((bx + bw - 6 - lw + 6, by + 10), lab, font=sans_b(10),
                  fill=(255, 255, 255))
        kx = bx + 10
        ky = by + 102
        draw.text((kx, ky), story["kicker"], font=sans_b(10),
                  fill=REGION_COLORS[story["region"]])
        hl = wrap(draw, story["headline"], serif_b(23), bw - 20)
        draw_lines(draw, hl[:2], kx, ky + 14, serif_b(23), INK, 25)
        sm = wrap(draw, story["summary"], sans(12), bw - 20)
        draw_lines(draw, sm[:3], kx, ky + 14 + 2 * 25 + 2, sans(12), INK, 14)
        draw.text((kx, by + 210), story["source"], font=sans_b(8),
                  fill=MUTED)

    # ---- eight small stories, two rows of four
    sw = 238
    sxs = [mx, mx + 246, mx + 492, mx + 738]
    for row in range(2):
        ry0 = 444 + row * 162
        for col in range(4):
            story = SMALL[row * 4 + col]
            bx = sxs[col]
            draw.rectangle([bx, ry0, bx + sw, ry0 + 156], fill=CARD,
                           outline=RULE, width=1)
            small_scene(draw, story["scene"], bx + 1, ry0 + 1, sw - 2, 54)
            num_badge(draw, bx + 6, ry0 + 6, story["num"])
            label_badge(draw, bx + sw - 72, ry0 + 6, story["label"],
                        (34, 120, 60) if story["label"] == "OFFICIAL"
                        else (169, 28, 28))
            kx = bx + 8
            ky = ry0 + 60
            draw.text((kx, ky), story["kicker"], font=sans_b(9),
                      fill=REGION_COLORS[story["region"]])
            hl = wrap(draw, story["headline"], serif_b(16), sw - 16)
            draw_lines(draw, hl[:2], kx, ky + 13, serif_b(16), INK, 19)
            sm = wrap(draw, story["summary"], sans(11), sw - 16)
            draw_lines(draw, sm[:3], kx, ky + 13 + 2 * 19 + 2, sans(11),
                       INK, 14)

    # ---- map + in brief
    my = 768
    draw.text((mx, my), "WHERE IT HAPPENED  \u2014  PINS = STORY NUMBERS",
              font=sans_b(11), fill=INK)
    draw.text((336, my), "IN BRIEF  \u2014  19 MORE STORIES FROM 25 NOVEMBER",
              font=sans_b(11), fill=INK)
    map_x, map_y, map_w, map_h = mx, my + 18, 300, 158
    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                   fill=(223, 232, 234), outline=RULE, width=1)

    def project(lon, lat):
        px = map_x + (lon + 180.0) / 360.0 * map_w
        py = map_y + (90.0 - lat) / 180.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(232, 224, 200), outline=(154, 143, 106))
    for num, lon, lat in PINS:
        px, py = project(lon, lat)
        r = 6
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        fnt = sans_b(7 if num >= 10 else 8)
        tw = draw.textlength(t, font=fnt)
        draw.text((px - tw / 2, py - 4), t, font=fnt, fill=(255, 255, 255))
    # Map legend.
    ly = map_y + map_h + 4
    draw.text((map_x, ly), "1 Jiuquan  2 Seoul  3 Hormuz  4 Canberra",
              font=sans(9), fill=MUTED)
    draw.text((map_x, ly + 11), "5\u20139 US east coast  10 Java  11 Ituri, Congo",
              font=sans(9), fill=MUTED)

    # Brief columns.
    bx0, bx1 = 336, 664
    for i, (num, text) in enumerate(BRIEF):
        col_x = bx0 if i < 10 else bx1
        row = i if i < 10 else i - 10
        yy = my + 18 + row * 18
        line = f"{num}. {text}"
        draw.text((col_x, yy), line, font=sans(11), fill=INK)

    # ---- date check
    dy = 968
    draw.rectangle([mx, dy, W - mx, dy + 32], outline=RED, width=2)
    dc = ("DATE CHECK \u2014 Every story here happened, or was first reported, on "
          "Wednesday 25 November 2026 in at least one time zone. The Huawei verdict, "
          "the Senegal CAS ruling and the WHO evacuation were announced Tue 24 Nov "
          "and reported on the 25th; earlier news (Nvidia's board row, COP31) is left out.")
    dc_lines = wrap(draw, dc, sans_b(10), cw - 16)
    draw_lines(draw, dc_lines[:2], mx + 8, dy + 4, sans_b(10), DARKRED, 13)

    # ---- footer
    fy = 1006
    draw.text((mx, fy), "Sources: AP, Reuters, AFP, Eurostat, UN, WHO, CAF, ABC, "
              "Guardian, SCMP, Yonhap, CNBC.", font=sans(9), fill=MUTED)
    foot_r = "DRAWN IN CODE  \u00b7  NO PHOTOGRAPHS  \u00b7  WEDNESDAY 25 NOVEMBER 2026"
    tw = draw.textlength(foot_r, font=sans_b(9))
    draw.text((W - mx - tw, fy), foot_r, font=sans_b(9), fill=MUTED)
    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", str(HERE)))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    img = build()
    img.save(out, format="PNG", optimize=True)
    os.chmod(out, 0o644)
    return out


if __name__ == "__main__":
    path = main()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
