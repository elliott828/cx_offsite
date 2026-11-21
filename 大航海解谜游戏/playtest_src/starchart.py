# -*- coding: utf-8 -*-
"""The night chart for C2: an antique celestial chart drawn as SVG, cut into four square quarters.

Each ship holds one quarter. Joined edge to edge, the gold stars and their lines draw a capital A
(the fifth seal) over a compass rose that only completes at the centre.
Quarters: 1 Dolphin top-left · 2 Rose top-right · 3 Star bottom-left · 4 Eagle bottom-right.
"""
import math
import random

W = 1000          # full chart is W x W; each quarter is W/2 square
C = W / 2
INK = "#1d2f4a"   # deep chart blue
SEPIA = "#7a5a3a"
GOLD = "#b8862b"
PAPER = "#f3e9d2"
PAPER2 = "#e8d8b4"
SHIPS = {1: ("DOLPHIN", "#14284b"), 2: ("ROSE", "#6b1831"), 3: ("STAR", "#b8a36e"), 4: ("EAGLE", "#8a6a3c")}
OFFSET = {1: (0, 0), 2: (C, 0), 3: (0, C), 4: (C, C)}

# the A: apex on the vertical seam, crossbar centre on the seam too
A_STARS = [(500, 170), (430, 330), (360, 490), (290, 650), (220, 810),
           (570, 330), (640, 490), (710, 650), (780, 810),
           (395, 650), (500, 650), (605, 650)]
A_LINES = [((500, 170), (220, 810)), ((500, 170), (780, 810)), ((290, 650), (710, 650))]


def star_path(x, y, r, points=8, inner=0.38):
    pts = []
    for i in range(points * 2):
        a = math.pi * i / points - math.pi / 2
        rr = r if i % 2 == 0 else r * inner
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + "Z"


def chart_body():
    rnd = random.Random(1519)
    g = []
    # paper and vignette
    g.append(f'<rect width="{W}" height="{W}" fill="url(#paper)"/>')
    # outer double frame with degree ticks
    for r, sw in ((470, 3), (458, 1.2), (300, 1), (180, 1)):
        g.append(f'<circle cx="{C}" cy="{C}" r="{r}" fill="none" stroke="{INK}" stroke-width="{sw}" opacity="{.85 if r > 400 else .45}"/>')
    for d in range(0, 360, 5):
        a = math.radians(d)
        r1 = 458; r2 = 470 if d % 15 == 0 else 465
        g.append(f'<line x1="{C + r1 * math.cos(a):.1f}" y1="{C + r1 * math.sin(a):.1f}" x2="{C + r2 * math.cos(a):.1f}" y2="{C + r2 * math.sin(a):.1f}" stroke="{INK}" stroke-width="1.2"/>')
    # hour lines (dashed meridians)
    for d in range(0, 360, 30):
        a = math.radians(d)
        g.append(f'<line x1="{C + 180 * math.cos(a):.1f}" y1="{C + 180 * math.sin(a):.1f}" x2="{C + 458 * math.cos(a):.1f}" y2="{C + 458 * math.sin(a):.1f}" stroke="{INK}" stroke-width=".8" stroke-dasharray="4 6" opacity=".35"/>')
    # ecliptic, a tilted ellipse
    g.append(f'<ellipse cx="{C}" cy="{C}" rx="400" ry="250" transform="rotate(-23 {C} {C})" fill="none" stroke="{SEPIA}" stroke-width="1" stroke-dasharray="1 5" opacity=".7"/>')
    # numerals on the outer band
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
    for i, n in enumerate(roman):
        a = math.radians(i * 30 - 90 + 15)
        x, y = C + 484 * math.cos(a), C + 484 * math.sin(a)
        g.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="15" text-anchor="middle" dominant-baseline="middle" fill="{INK}" font-family="Georgia, serif" opacity=".8">{n}</text>')
    # background field stars, kept clear of the A strokes
    def near_a(x, y):
        for (x1, y1), (x2, y2) in A_LINES:
            dx, dy = x2 - x1, y2 - y1
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
            if math.hypot(x - (x1 + t * dx), y - (y1 + t * dy)) < 26:
                return True
        return False
    placed = 0
    while placed < 150:
        x, y = rnd.uniform(40, 960), rnd.uniform(40, 960)
        if math.hypot(x - C, y - C) > 452 or near_a(x, y) or math.hypot(x - C, y - C) < 110:
            continue
        r = rnd.choice([1.4, 1.8, 2.2, 2.2, 3, 4])
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{INK}" opacity="{rnd.uniform(.45, .9):.2f}"/>')
        placed += 1
    # two faint decoy asterisms
    for pts in ([(150, 300), (205, 260), (260, 285), (300, 230)], [(690, 220), (760, 260), (820, 230), (870, 300), (840, 360)]):
        g.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) + f'" fill="none" stroke="{INK}" stroke-width="1" opacity=".35"/>')
        for x, y in pts:
            g.append(f'<path d="{star_path(x, y, 6, 4, .45)}" fill="{INK}" opacity=".6"/>')
    # compass rose at the centre (only whole when all four cards meet)
    for i, (rr, w, col) in enumerate(((95, 15, INK), (68, 10, SEPIA))):
        for k in range(8 if i == 0 else 8):
            ang = math.radians(k * 45 + (0 if i == 0 else 22.5))
            tip = (C + rr * math.cos(ang), C + rr * math.sin(ang))
            l = (C + w * math.cos(ang + math.pi / 2), C + w * math.sin(ang + math.pi / 2))
            r_ = (C + w * math.cos(ang - math.pi / 2), C + w * math.sin(ang - math.pi / 2))
            g.append(f'<path d="M{C},{C} L{l[0]:.1f},{l[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" fill="{col}" opacity="{.9 if i == 0 else .7}"/>')
            g.append(f'<path d="M{C},{C} L{r_[0]:.1f},{r_[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" fill="{PAPER}" stroke="{col}" stroke-width="1.2"/>')
    g.append(f'<circle cx="{C}" cy="{C}" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><circle cx="{C}" cy="{C}" r="4" fill="{GOLD}"/>')
    for lab, (dx, dy) in (("N", (0, -114)), ("E", (114, 0)), ("S", (0, 114)), ("W", (-114, 0))):
        g.append(f'<text x="{C + dx}" y="{C + dy}" font-size="16" font-weight="700" text-anchor="middle" dominant-baseline="middle" fill="{INK}" font-family="Georgia, serif">{lab}</text>')
    # the A: glow, line, stars
    for (x1, y1), (x2, y2) in A_LINES:
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" stroke-width="12" opacity=".22" stroke-linecap="round"/>')
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="12 7" stroke-linecap="round"/>')
    for x, y in A_STARS:
        g.append(f'<circle cx="{x}" cy="{y}" r="20" fill="{GOLD}" opacity=".22"/>')
        g.append(f'<path d="{star_path(x, y, 17)}" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    # cartouche along the bottom, split across the two lower cards
    g.append(f'<path d="M300 905 Q500 875 700 905 L700 950 Q500 925 300 950 Z" fill="{PAPER2}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(f'<text x="{C}" y="922" font-size="19" text-anchor="middle" fill="{INK}" font-family="Georgia, serif" letter-spacing="3">CARTA NOCTVRNA · MDXIX</text>')
    g.append(f'<text x="{C}" y="944" font-size="13" text-anchor="middle" fill="{SEPIA}" font-family="Georgia, serif" letter-spacing="2">QVINTVM SIGILLVM IN STELLIS</text>')
    # title band along the top, split across the two upper cards
    g.append(f'<text x="{C}" y="60" font-size="24" text-anchor="middle" fill="{INK}" font-family="Georgia, serif" letter-spacing="6">· HEMISPHÆRIVM ·</text>')
    return "".join(g)


DEFS = (f'<defs><radialGradient id="paper" cx="50%" cy="50%" r="72%"><stop offset="0" stop-color="{PAPER}"/>'
        f'<stop offset=".78" stop-color="{PAPER}"/><stop offset="1" stop-color="{PAPER2}"/></radialGradient></defs>')


def full_svg(css_class="chart"):
    return f'<svg class="{css_class}" viewBox="0 0 {W} {W}" role="img" aria-label="night chart">{DEFS}{chart_body()}</svg>'


def quarter_svg(team, css_class="quarter", label=True):
    ox, oy = OFFSET[team]
    name, color = SHIPS[team]
    extra = ""
    if label:
        # ship badge in the card's outer corner, so it never sits on a seam
        cx = ox + (34 if ox == 0 else C - 34)
        cy = oy + (34 if oy == 0 else C - 34)
        anchor = "start" if ox == 0 else "end"
        tx = ox + (60 if ox == 0 else C - 60)
        extra = (f'<circle cx="{cx}" cy="{cy}" r="14" fill="{color}" stroke="{PAPER}" stroke-width="3"/>'
                 f'<text x="{tx}" y="{cy}" font-size="15" font-weight="700" text-anchor="{anchor}" dominant-baseline="middle" fill="{color}" font-family="Georgia, serif" letter-spacing="2">{name}</text>')
    return (f'<svg class="{css_class}" viewBox="{ox} {oy} {C:g} {C:g}" role="img" aria-label="night chart quarter {name}">'
            f'{DEFS.replace(chr(34) + "paper" + chr(34), chr(34) + "paper" + str(team) + chr(34))}'
            f'{chart_body().replace("url(#paper)", "url(#paper" + str(team) + ")")}{extra}</svg>')
