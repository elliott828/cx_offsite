# -*- coding: utf-8 -*-
"""Build an editable side-by-side review sheet of every Option A v2 puzzle for all four ships.

python build_review.py  ->  ../方案A_v2_四队题目对照.html
Rows are puzzles, columns are ships; a row that is identical for every ship spans all four.
Answers sit folded under each question; each cell has a feedback box. Text is editable in place,
autosaves in this browser, and can be exported as a new HTML file with the edits baked in.
"""
import html as H
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import content_v2 as C
from content_v2 import T

OUT = Path(__file__).parent.parent / "方案A_v2_四队题目对照.html"
BUILD = "2026-11-21c"  # bump when puzzle text changes: old in-browser text edits are dropped, feedback is kept
TEAMS = C.TEAMS
P = {p["id"]: p for p in C.PUZZLES}


def body(pid, t=0):
    b = P[pid]["body"]
    return b.get(t, b.get(0))


def star_svg(t):
    return '<div class="starq">' + C.STAR_QUARTERS[t] + '</div>'


def _old_star_svg(t):
    s = C.STAR_SHEETS[t]
    pts = s["stars"] + s["decoy"]
    def star(x, y):
        cx, cy = 15 + x * 25, 15 + y * 25
        return (f'<path d="M{cx} {cy-7}L{cx+2} {cy-2}L{cx+7} {cy}L{cx+2} {cy+2}L{cx} {cy+7}L{cx-2} {cy+2}'
                f'L{cx-7} {cy}L{cx-2} {cy-2}Z" fill="currentColor"/>')
    return '<svg class="stars" viewBox="0 0 230 230" role="img" aria-label="star chart">' + "".join(star(x, y) for x, y in pts) + "</svg>"


def circuit(t):
    i0 = C.PORTS.index(C.HOME[t])
    return [C.PORTS[(i0 + k) % 4] for k in range(4)]


A2_WHY = T("Luis = 4 号；Diego 只能是领航员（1 号）；若 Juan = 3，木匠和炮手会相邻，矛盾；所以 Juan = 2，厨师 Pedro 在 3 号。",
           "Luis = 4; Diego can only be the navigator (bunk 1); Juan = 3 would put carpenter and gunner side by side, so Juan = 2 and the cook Pedro is in bunk 3.")
HEADING = {1: T("西北", "NW"), 2: T("西", "W"), 3: T("南", "S"), 4: T("东北", "NE")}
KEYNAME = {1: T("凯撒密码 +3", "Caesar +3"), 2: T("字母数字表 A1Z26", "A1Z26 table"), 3: T("摩尔斯电码", "Morse code"), 4: T("埃特巴什码", "Atbash")}

ROWS = []


def row(rid, act, title, cells=None, span=None):
    ROWS.append({"id": rid, "act": act, "title": title, "cells": cells, "span": span})


ACT1, ACT2, ACT3, FIN, SIDE = T("第一幕 · 船上", "Act 1 · On board"), T("第二幕 · 远航", "Act 2 · The voyage"), \
    T("第三幕 · 夜航", "Act 3 · Night sailing"), T("终局", "Finale"), T("漂流瓶支线", "Bottle side quests")

row("A0", ACT1, P["A0"]["title"], span={"q": body("A0"), "a": T("没有标准答案。开场时四船各喊一次，代表起航，之后不再喊。",
                                                                 "No fixed answer. Each ship shouts its chant once at the start to set sail, and never again.")})
row("A1", ACT1, P["A1"]["title"], cells={t: {"q": body("A1", t), "a": T(f"旗子拼出 <b>{C.FLAGS[t]}</b> → 第 1 位 <b>{C.DIG1[t]}</b>",
                                                                         f"The flags spell <b>{C.FLAGS[t]}</b> → digit 1 is <b>{C.DIG1[t]}</b>")} for t in TEAMS})
row("A2", ACT1, P["A2"]["title"], span={"q": body("A2"), "a": T("<b>3</b>。" + A2_WHY["zh"], "<b>3</b>. " + A2_WHY["en"])})
row("A3", ACT1, P["A3"]["title"], cells={t: {"q": body("A3", t), "a": T(f"最终朝向{HEADING[t]['zh']} → <b>{C.DIG3[t]}</b>",
                                                                         f"Final heading {HEADING[t]['en']} → <b>{C.DIG3[t]}</b>")} for t in TEAMS})
row("A4", ACT1, P["A4"]["title"], span={"q": body("A4"), "a": T("<b>7</b>：每桶应重 = 内容 + 空桶 5 kg。6 号绳索桶多 6 kg，但记录说每卷淋湿多 1 kg，正好解释；7 号大米 5 袋应为 30 kg，过磅 42 kg，多 12 kg 无法解释。",
                                                                 "<b>7</b>: expected = contents + 5 kg barrel. Barrel 6 (rope) is 6 kg over, exactly the wet-rope note (1 kg × 6 coils); barrel 7 (5 sacks of rice) should be 30 kg but weighs 42 kg, 12 kg unexplained.")})
row("A-chest", ACT1, P["A-chest"]["title"], cells={t: {"q": body("A-chest"), "a": T(
    f"密码 <b>{C.CODE[t]}</b>。箱子里有：<div class=\"inner\">{C.chest_reveal(t, 'zh')}</div>",
    f"Code <b>{C.CODE[t]}</b>. Inside: <div class=\"inner\">{C.chest_reveal(t, 'en')}</div>")} for t in TEAMS})
row("B1", ACT2, P["B1"]["title"], cells={t: {"q": T(
    body("B1")["zh"] + f"<p>残图上的密文：<b class=\"mono\">{C.ENC[t]}</b><br>钥匙卡在：<b>{C.SHIPS[C.KEYHOLDER[t]]['zh']}</b></p>",
    body("B1")["en"] + f"<p>Cipher on the fragment: <b class=\"mono\">{C.ENC[t]}</b><br>Key card held by: <b>{C.SHIPS[C.KEYHOLDER[t]]['en']}</b></p>"),
    "a": T(f"<b>{C.HOME_ANS[t]}</b>（{KEYNAME[t]['zh']}）。解出后{C.SHIPS[C.KEYHOLDER[t]]['zh']}得 2 金币。",
           f"<b>{C.HOME_ANS[t]}</b> ({KEYNAME[t]['en']}). Once solved, {C.SHIPS[C.KEYHOLDER[t]]['en']} earns 2 doubloons.")} for t in TEAMS})
row("PORTS", ACT2, P["PORTS"]["title"], cells={t: {"q": T(
    body("PORTS")["zh"] + "<ol>" + "".join(f"<li>{C.PORT_NAME[p]['zh']}{'（母港）' if k == 0 else ''}</li>" for k, p in enumerate(circuit(t))) + "</ol>",
    body("PORTS")["en"] + "<ol>" + "".join(f"<li>{C.PORT_NAME[p]['en']}{' (home)' if k == 0 else ''}</li>" for k, p in enumerate(circuit(t))) + "</ol>"),
    "a": T("按顺序拿到的章：" + " → ".join(C.PORT_LETTER[p] for p in circuit(t)) + "。按航线重排后是 F-L-O-R。",
           "Stamps in visit order: " + " → ".join(C.PORT_LETTER[p] for p in circuit(t)) + ". Re-ordered by route: F-L-O-R.")} for t in TEAMS})
for p in C.PORTS:
    extra = C.MALACCA_Q if p == "M" else T("", "")
    row("PORT-" + p, ACT2, T(f"港口挑战 · {C.PORT_NAME[p]['zh']}", f"Port challenge · {C.PORT_NAME[p]['en']}"),
        span={"q": C.PORT_CHALLENGE[p],
              "a": T(f"盖章字母 <b>{C.PORT_LETTER[p]}</b>。港务长按卡上的标准给 2 或 3 金币。" + extra["zh"],
                     f"Stamp letter <b>{C.PORT_LETTER[p]}</b>. The Port Master awards 2 or 3 doubloons by the card." + extra["en"])})
row("C1", ACT3, P["C1"]["title"], span={
    "q": T(body("C1")["zh"] + "<ol>" + "".join(f"<li>{q['zh']}</li>" for q, _ in C.QUIZ) + "</ol>",
           body("C1")["en"] + "<ol>" + "".join(f"<li>{q['en']}</li>" for q, _ in C.QUIZ) + "</ol>"),
    "a": T("<ol>" + "".join(f"<li>{a['zh']}</li>" for _, a in C.QUIZ) + "</ol>", "<ol>" + "".join(f"<li>{a['en']}</li>" for _, a in C.QUIZ) + "</ol>")})
row("C2", ACT3, P["C2"]["title"], cells={t: {"q": T(body("C2")["zh"] + f"<p class=\"note\">这条船的星图卡（整张的四分之一）：</p>{star_svg(t)}",
                                                     body("C2")["en"] + f"<p class=\"note\">This ship's card (one quarter of the chart):</p>{star_svg(t)}"),
                                              "a": T("四张按边缘拼成整张星图，金色星星连成大写字母 <b>A</b>（第五枚印章）。", "Joined edge to edge, the gold stars form a capital <b>A</b> (the fifth seal).")} for t in TEAMS})
row("D1", FIN, P["D1"]["title"], span={"q": body("D1"), "a": T("<b>FLORA</b>（F-L-O-R 四个港口章 + 星图 A）。" + P["D1"]["gate"]["reveal"][0]["zh"],
                                                               "<b>FLORA</b> (the four port stamps F-L-O-R + the star chart's A). " + P["D1"]["gate"]["reveal"][0]["en"])})
for i, (riddle, ans, alts) in enumerate(C.BOTTLES, start=1):
    row(f"BOT{i}", SIDE, T(f"漂流瓶 {i}" + ("（第 1 批）" if i <= 3 else "（第 2 批）"), f"Bottle {i}" + (" (wave 1)" if i <= 3 else " (wave 2)")),
        span={"q": T(f"<p>{riddle['zh']}</p>", f"<p>{riddle['en']}</p>"),
              "a": T(f"<b>{ans}</b>　也接受：{'、'.join(alts)}", f"<b>{ans}</b> · also accepted: {', '.join(alts)}")})


def editable(key, t_obj):
    return (f'<div class="ed zh" contenteditable="true" data-key="{key}:zh">{t_obj["zh"]}</div>'
            f'<div class="ed en" contenteditable="true" data-key="{key}:en">{t_obj["en"]}</div>')


def feedback(key):
    opts = [("", "状态 · Status"), ("ok", "✓ 通过 · Good"), ("edit", "✎ 要改 · Needs edit"), ("drop", "✕ 删掉 · Drop")]
    o = "".join(f'<option value="{v}">{label}</option>' for v, label in opts)
    return (f'<div class="fb"><select data-fb="{key}:status" aria-label="状态 Status">{o}</select>'
            f'<textarea data-fb="{key}:text" rows="2" placeholder="反馈 / Feedback"></textarea></div>')


def cell(key, c, t=None):
    label = (f'<div class="shiplabel" style="--c:{C.COLORS[t]}">{C.SHIPS[t]["zh"]}</div>' if t else
             '<div class="shiplabel all"><span class="zh">四队相同</span><span class="en">All four ships</span></div>')
    return (f'<div class="cell" data-cell="{key}">{label}{editable(key + ":q", c["q"])}'
            f'<details class="ans"><summary><span class="zh">答案</span><span class="en">Answer</span></summary>{editable(key + ":a", c["a"])}</details>'
            f'{feedback(key)}</div>')


def build():
    head = "".join(f'<div class="colh" style="--c:{C.COLORS[t]}"><b>{C.SHIPS[t]["zh"]}</b><span>'
                   f'<span class="zh">{C.PLAYERS[t]} 人 · 提示券 {C.HINT_TOKENS[t]} · 母港 {C.PORT_NAME[C.HOME[t]]["zh"]}</span>'
                   f'<span class="en">{C.PLAYERS[t]} players · {C.HINT_TOKENS[t]} hint tokens · home {C.PORT_NAME[C.HOME[t]]["en"]}</span></span></div>' for t in TEAMS)
    body_rows, last_act = [], None
    for r in ROWS:
        if r["act"] != last_act:
            body_rows.append(f'<div class="act"><span class="zh">{r["act"]["zh"]}</span><span class="en">{r["act"]["en"]}</span></div>')
            last_act = r["act"]
        title = (f'<div class="rowh"><span class="pid">{r["id"]}</span>{editable(r["id"] + ":title", r["title"])}'
                 f'<span class="tag">{"<span class=zh>四队相同</span><span class=en>Same for all</span>" if r["span"] else "<span class=zh>各队不同</span><span class=en>Differs by ship</span>"}</span></div>')
        if r["span"]:
            cells = f'<div class="span">{cell(r["id"] + ":all", r["span"])}</div>'
        else:
            cells = "".join(cell(f'{r["id"]}:{t}', r["cells"][t], t) for t in TEAMS)
        body_rows.append(f'<section class="prow" id="{r["id"]}">{title}<div class="cells">{cells}</div></section>')
    tpl = (Path(__file__).parent / "review_template.html").read_text(encoding="utf-8")
    html_out = tpl.replace("__HEAD__", head).replace("__ROWS__", "\n".join(body_rows)).replace("__COUNT__", str(len(ROWS))).replace("__BUILD__", BUILD)
    OUT.write_text(html_out, encoding="utf-8", newline="\n")
    print("wrote", OUT, len(ROWS), "rows", len(html_out) // 1024, "KB")


if __name__ == "__main__":
    build()
