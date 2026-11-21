# -*- coding: utf-8 -*-
"""Figure-eight knot, drawn in four steps with real over/under crossings.

The rope is one continuous path split into segments; segments are painted in z-order
(under first, over last) so each crossing reads correctly.
"""
ROPE_OUT = "#5b3a1e"
ROPE_IN = "#e0bd86"
TIP = "#9c3d1f"

# segments of the rope, start to tail
S = "M100 0 L100 120"                                   # standing part, from above
B = "M100 120 C100 170, 50 175, 45 135"                 # round the bottom of the loop
C_ = "M45 135 C48 110, 80 92, 120 82"                   # back up, OVER the standing part: the loop
D = "M120 82 C152 74, 152 30, 116 30 C106 30, 96 33, 82 40"   # round the neck, BEHIND the standing part
E1 = "M82 40 C62 52, 60 80, 70 102 C72 110, 73 116, 74 126"   # down the front, OVER the loop's top strand
E2 = "M74 126 C76 150, 78 178, 82 215"                  # out through the loop, UNDER its bottom


def rope(d, tip=False):
    s = (f'<path d="{d}" fill="none" stroke="{ROPE_OUT}" stroke-width="15" stroke-linecap="round"/>'
         f'<path d="{d}" fill="none" stroke="{ROPE_IN}" stroke-width="10" stroke-linecap="round"/>'
         f'<path d="{d}" fill="none" stroke="{ROPE_OUT}" stroke-width="1" stroke-dasharray="3 5" opacity=".45"/>')
    return s


def tip(x, y):
    return f'<circle cx="{x}" cy="{y}" r="7.5" fill="{TIP}" stroke="{ROPE_OUT}" stroke-width="2"/>'


def arrow(x1, y1, x2, y2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TIP}" stroke-width="2.5" marker-end="url(#ah)"/>')


DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
        f'<path d="M0 0L10 5L0 10Z" fill="{TIP}"/></marker></defs>')


def joints(points):
    # hide the seam where two drawn segments meet (never at a crossing)
    return "".join(f'<circle cx="{x}" cy="{y}" r="5.2" fill="{ROPE_IN}"/>' for x, y in points)


def panel(step):
    g = [DEFS]
    if step == 1:
        g += [rope(S), rope(B), rope(C_), joints([(100, 120), (45, 135)]), tip(120, 82), arrow(128, 100, 150, 84)]
    elif step == 2:
        g += [rope(D), rope(S), rope(B), rope(C_), joints([(100, 120), (45, 135), (120, 82)]), tip(82, 40), arrow(70, 22, 58, 36)]
    elif step == 3:
        g += [rope(E2), rope(D), rope(S), rope(B), rope(C_), rope(E1), joints([(100, 120), (45, 135), (120, 82), (82, 40), (74, 126)]), tip(82, 215), arrow(105, 190, 92, 212)]
    else:
        # pulled tight: same path, both ends pulled apart
        g += [rope(E2), rope(D), rope(S), rope(B), rope(C_), rope(E1), joints([(100, 120), (45, 135), (120, 82), (82, 40), (74, 126)]), tip(82, 215),
              arrow(120, 20, 120, 2), arrow(108, 200, 108, 226)]
    return f'<svg viewBox="20 -8 150 238" class="knot" role="img" aria-label="figure-eight knot step {step}">{"".join(g)}</svg>'


STEPS = [
    ("做一个圈：绳尾绕下来，从绳子<b>上面</b>压过去。", "Make a loop: bring the tail round and cross it <b>over</b> the rope."),
    ("绳尾从绳子<b>后面</b>绕一圈。", "Take the tail <b>behind</b> the rope, around its neck."),
    ("绳尾从前面<b>穿进圈里</b>，从下面出来。", "Push the tail <b>down through the loop</b> from the front."),
    ("两头一起拉紧，看起来像数字 <b>8</b>。", "Pull both ends tight: it looks like the number <b>8</b>."),
]
