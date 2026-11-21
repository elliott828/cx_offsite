# -*- coding: utf-8 -*-
"""Printable props: the Cape knot card, the four night-chart quarter cards and a host reference sheet.

python build_print.py  ->  ../打印物料_星图卡与绳结卡.html   (print on A4, 100% scale)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import knot as K
import starchart as SC

OUT = Path(__file__).parent.parent / "打印物料_星图卡与绳结卡.html"
NAMES = {1: ("海豚号", "Dolphin"), 2: ("玫瑰号", "Rose"), 3: ("星辰号", "Star"), 4: ("雄鹰号", "Eagle")}
POS = {1: ("左上", "top-left"), 2: ("右上", "top-right"), 3: ("左下", "bottom-left"), 4: ("右下", "bottom-right")}

CSS = """
@page { size: A4; margin: 12mm; }
* { box-sizing: border-box; }
body { margin: 0; background: #d9d4c7; color: #1d2f4a; font: 13px/1.5 "PingFang SC", "Microsoft YaHei", "Noto Sans SC", Georgia, serif; }
.page { width: 210mm; min-height: 297mm; margin: 10mm auto; background: #fff; padding: 14mm; position: relative; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.page h1 { font-family: Georgia, "Songti SC", serif; font-weight: 400; font-size: 22px; margin: 0 0 2mm; }
.page .sub { color: #7a5a3a; font-size: 12px; margin: 0 0 6mm; }
.note { color: #6b5d4f; font-size: 11px; }
.toolbar { max-width: 210mm; margin: 8mm auto 0; display: flex; gap: 8px; align-items: center; font-size: 13px; color: #333; }
/* knot card */
.knotcard { border: 2px solid #5b3a1e; border-radius: 4mm; padding: 8mm; background: #f3e9d2; }
.knotcard h2 { font-family: Georgia, serif; font-weight: 400; font-size: 26px; margin: 0; }
.knotcard .en { color: #7a5a3a; font-size: 12px; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin: 6mm 0; }
.step { text-align: center; }
.step svg { width: 100%; height: 55mm; }
.step .n { display: inline-block; width: 7mm; height: 7mm; border-radius: 50%; background: #9c3d1f; color: #fff; font-weight: 700; line-height: 7mm; margin-bottom: 2mm; }
.step p { margin: 1mm 0; font-size: 12.5px; }
.rules { border-top: 1px dashed #7a5a3a; padding-top: 4mm; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; font-size: 12.5px; }
.rules b { color: #9c3d1f; }
/* star cards */
.cardwrap { display: flex; flex-direction: column; align-items: center; gap: 5mm; }
.crop { position: relative; width: 150mm; height: 150mm; }
.crop svg { width: 150mm; height: 150mm; display: block; }
.crop::before, .crop::after { content: ""; position: absolute; inset: -6mm; pointer-events: none;
  background:
    linear-gradient(#999,#999) 0 6mm/4mm .3mm no-repeat, linear-gradient(#999,#999) 6mm 0/.3mm 4mm no-repeat,
    linear-gradient(#999,#999) 100% 6mm/4mm .3mm no-repeat, linear-gradient(#999,#999) calc(100% - 6mm) 0/.3mm 4mm no-repeat,
    linear-gradient(#999,#999) 0 calc(100% - 6mm)/4mm .3mm no-repeat, linear-gradient(#999,#999) 6mm 100%/.3mm 4mm no-repeat,
    linear-gradient(#999,#999) 100% calc(100% - 6mm)/4mm .3mm no-repeat, linear-gradient(#999,#999) calc(100% - 6mm) 100%/.3mm 4mm no-repeat; }
.crop::after { display: none; }
.cardnote { text-align: center; }
.cardnote b { font-family: Georgia, serif; font-size: 16px; }
/* host sheet */
.assembled { width: 170mm; margin: 0 auto; display: block; }
.assembled svg { width: 100%; height: auto; display: block; }
.answerbox { margin: 6mm auto 0; width: 170mm; border: 1.5px solid #9c3d1f; border-radius: 3mm; padding: 4mm 6mm; }
@media print {
  body { background: #fff; }
  .toolbar { display: none; }
  .page { margin: 0; box-shadow: none; width: auto; min-height: auto; padding: 0; page-break-after: always; }
  .page:last-child { page-break-after: auto; }
}
"""


def knot_page():
    steps = "".join(
        f'<div class="step"><span class="n">{i}</span>{K.panel(i)}<p>{zh}</p><p class="en">{en}</p></div>'
        for i, (zh, en) in enumerate(K.STEPS, start=1))
    return f"""<section class="page">
  <h1>港口挑战 · 好望角 · 8 字结图卡</h1>
  <p class="sub">Port challenge · Cape of Good Hope · figure-eight knot card — 放在好望角港口桌上 / place on the Cape port table</p>
  <div class="knotcard">
    <h2>绕过风暴角 <span class="en">Round the Cape</span></h2>
    <p>照图打一个 8 字结。<span class="en">Tie a figure-eight knot by following the pictures.</span></p>
    <div class="steps">{steps}</div>
    <div class="rules">
      <div><b>规则</b><br>船上每个人各拿一根绳，各打一个，限时 <b>90 秒</b>。<br>半数以上打成：<b>2 金币</b>；全员打成：<b>3 金币</b>。</div>
      <div><b>Rules</b><br>Every sailor takes a rope and ties one knot, <b>90 seconds</b>.<br>Half or more tied: <b>2 doubloons</b>; everyone: <b>3</b>.</div>
    </div>
  </div>
  <p class="note">给港务长：桌上再挂一个打好的样品结，比看图更直观。每条船来之前把绳子解开。短绳 6 根，每根约 60 cm，粗一点更好打。<br>
  For the Port Master: hang one finished sample knot beside the card; it helps more than the drawing. Untie the ropes between ships. Six short ropes, about 60 cm each; thicker rope is easier.</p>
</section>"""


def star_page(t):
    zh, en = NAMES[t]
    pz, pe = POS[t]
    return f"""<section class="page">
  <h1>夜航星图 · {zh} <span style="font-size:15px;color:#7a5a3a">Night chart · {en}</span></h1>
  <p class="sub">沿四角的裁切线剪下，放进{zh}的船长箱。四张拼在一起时，这张在<b>{pz}</b>。<br>Cut along the corner marks and put it in the {en} chest. When the four are joined, this card goes <b>{pe}</b>.</p>
  <div class="cardwrap"><div class="crop">{SC.quarter_svg(t)}</div>
  <p class="cardnote note">建议用 200 g 以上的卡纸彩色打印，100% 比例。成品 15 × 15 cm，四张拼成 30 × 30 cm。<br>Print in colour on card stock (200 g+), at 100%. Each card is 15 × 15 cm; together they make 30 × 30 cm.</p></div>
</section>"""


def host_page():
    return f"""<section class="page">
  <h1>主持人参考 · 星图拼好后的样子（不要发给玩家）</h1>
  <p class="sub">Host reference · the joined chart (do not hand out)</p>
  <div class="assembled">{SC.full_svg()}</div>
  <div class="answerbox"><b>答案 Answer：A</b>（第五枚印章 · the fifth seal）。<br>
  四张卡的金色星星和虚线连成一个大写字母 A，罗盘玫瑰只有四张拼在中间时才完整。<br>
  The gold stars and dashed lines join into a capital A; the compass rose is only whole when all four cards meet at the centre.</div>
</section>"""


def build():
    pages = [knot_page()] + [star_page(t) for t in (1, 2, 3, 4)] + [host_page()]
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>打印物料 · 星图卡与绳结卡</title><style>{CSS}</style></head>
<body>
<div class="toolbar">用浏览器打印（Ctrl+P），纸张 A4，缩放 100%，勾选“背景图形”。共 6 页：绳结卡 1 页、星图卡 4 页、主持人参考 1 页。</div>
{''.join(pages)}
</body></html>"""
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", OUT, len(html) // 1024, "KB")


if __name__ == "__main__":
    build()
