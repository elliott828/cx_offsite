# -*- coding: utf-8 -*-
"""Build the playtest page: encrypt answer-gated content and inject it into template.html."""
import base64, hashlib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content import GAMES, HOST_PASSWORD, SPICE_NAME, SPICES, T  # noqa: E402

HERE = Path(__file__).parent
OUT = HERE.parent / "大航海解谜_可行性测试.html"
BACKEND = None
# python build.py --vercel <supabase_url> <anon_key>  -> writes ../vercel/index.html
if len(sys.argv) >= 4 and sys.argv[1] == "--vercel":
    BACKEND = {"url": sys.argv[2].rstrip("/"), "key": sys.argv[3]}
    OUT = HERE.parent / "vercel" / "index.html"
    OUT.parent.mkdir(exist_ok=True)

NUMW = {"ZERO": "0", "ONE": "1", "TWO": "2", "THREE": "3", "FOUR": "4", "FIVE": "5", "SIX": "6", "SEVEN": "7", "EIGHT": "8", "NINE": "9",
        "零": "0", "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
DIRS = {"→": "R", "←": "L", "↑": "U", "↓": "D", "右": "R", "左": "L", "上": "U", "下": "D", "东": "R", "西": "L", "北": "U", "南": "D"}


def norm(s, g=None):
    s = str(s).upper()
    if g and g.get("dir"):
        s = "".join(DIRS.get(c, c) for c in s)
    s = re.sub(r"[^A-Z0-9一-鿿]", "", s)
    if g and g.get("numwords") and s in NUMW:
        s = NUMW[s]
    return s


def enc(pidc, key, obj):
    K = hashlib.sha256(f"aod|{pidc}|{key}".encode()).digest()
    pt = ("OK|" + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))).encode()
    out = bytearray()
    for b in range(0, (len(pt) + 31) // 32):
        ks = hashlib.sha256(K + b.to_bytes(4, "big")).digest()
        chunk = pt[b * 32:(b + 1) * 32]
        out += bytes(x ^ y for x, y in zip(chunk, ks))
    return base64.b64encode(bytes(out)).decode()


def build():
    games_out, keys, sols = [], {}, {}
    for g in GAMES:
        gp = []
        for p in g["puzzles"]:
            q = {k: v for k, v in p.items() if k not in ("gate", "rewards")}
            if "rewards" in p:
                q["rewards"] = {str(k): v for k, v in p["rewards"].items()}
            q["body"] = {str(k): v for k, v in p["body"].items()}
            gate = p.get("gate")
            keys[p["id"]] = {}
            if p.get("jigsaw"):
                keys[p["id"]] = {"0": "MAP"}
            if gate:
                answers, reveal = gate["answers"], gate["reveal"]
                aliases = gate.get("aliases", {})
                blobs = {}
                for tk, rv in reveal.items():
                    ans = answers.get(tk, answers.get(0))
                    canon = norm(ans, gate)
                    assert canon == ans, (p["id"], ans, canon)
                    variants = [canon] + [norm(a, gate) for a, v in aliases.items() if v == canon]
                    variants = list(dict.fromkeys(variants))
                    blobs[str(tk)] = [enc(f"{p['id']}#{tk}", v, rv) for v in variants]
                for tk, ans in answers.items():
                    keys[p["id"]][str(tk)] = ans
                q["gate"] = {k: gate[k] for k in ("label", "ph", "dir", "numwords") if k in gate}
                q["gate"]["blobs"] = blobs
            if p.get("envelope"):
                from content import C_LETTER
                keys[p["id"]] = {str(k): v for k, v in C_LETTER.items()}
            gp.append(q)
        go = {k: v for k, v in g.items() if k not in ("puzzles", "solution")}
        go["roles"] = {str(k): v for k, v in g["roles"].items()}
        for k in ("recipes", "home", "foreign", "foot"):
            if k in go:
                go[k] = {str(a): b for a, b in go[k].items()}
        go["puzzles"] = gp
        games_out.append(go)
        sols[g["id"]] = g["solution"]

    # B1 smell station layout belongs with the answers
    sols["B"] = {lang: sols["B"][lang] + (
        "<h4>闻香台摆放（测试用）</h4><p>1 号 肉桂 · 2 号 肉豆蔻 · 3 号 黑胡椒 · 4 号 八角 · 5 号 丁香 → 答案 31524</p>" if lang == "zh" else
        "<h4>Smell station layout (test)</h4><p>Jar 1 cinnamon · 2 nutmeg · 3 pepper · 4 star anise · 5 clove → answer 31524</p>") for lang in ("zh", "en")}

    data = {
        "games": games_out,
        "spices": SPICES,
        "itemNames": SPICE_NAME,
        "sol": enc("SOL#0", hashlib.sha256(("aod-sol|" + norm(HOST_PASSWORD)).encode()).hexdigest(), {"games": sols, "keys": keys}),
        "backend": BACKEND,
        "events": {
            "monsoon": T("季风到来：交易所银行卖价降到 3 金币一箱。", "The monsoon arrives: the bank now sells at 3 coins a crate."),
            "embargo": T("荷兰封锁班达群岛：银行停售肉豆蔻。", "Dutch blockade of the Banda Islands: the bank stops selling nutmeg."),
            "pirates": T("海盗来袭！如果还没把海盗藏身处报给交易所，每家商行交 1 箱香料给海盗（交易面板里的“交给海盗”）。",
                         "Pirate raid! If the hideout hasn't been reported, every house hands 1 crate to the pirates (use “Hand 1 crate to the pirates”)."),
            "closed": T("交易所闭市。请看看你们配方卡的底部。", "The Exchange is closed. Look at the foot of your recipe card."),
        },
        "protocol": {
            "schedule": T(
                "<div class=\"tw\"><table><tr><th>时间</th><th>内容</th><th>主持人</th></tr>"
                "<tr><td>0:00–0:10</td><td>介绍目的；每人在自己手机或电脑上打开页面，选测试员编号 1–5</td><td>确认右上角显示“已同步”</td></tr>"
                "<tr><td>0:10–0:45</td><td><b>A 局</b>（35 分钟）</td><td>在“测试流程”里点开始；看实时进度</td></tr>"
                "<tr><td>0:45–0:50</td><td>A 局反馈</td><td>点结束；提醒每人填反馈</td></tr>"
                "<tr><td>0:50–1:30</td><td><b>B 局</b>（40 分钟）</td><td>兼任交易所书记员；25′ 季风、32′ 封锁、38′ 海盗、42′ 闭市</td></tr>"
                "<tr><td>1:30–1:40</td><td>B 局反馈 + 休息</td><td></td></tr>"
                "<tr><td>1:40–2:20</td><td><b>C 局</b>（40 分钟）</td><td>25′ 和 35′ 各巡一次卡点</td></tr>"
                "<tr><td>2:20–2:25</td><td>C 局反馈</td><td></td></tr>"
                "<tr><td>2:25–2:45</td><td>看“结果对比”，讨论并选定方案</td><td>公开答案，一起复盘</td></tr></table></div>",
                "<div class=\"tw\"><table><tr><th>Time</th><th>What</th><th>Host</th></tr>"
                "<tr><td>0:00–0:10</td><td>Explain the goal; everyone opens the page on their own phone or laptop and picks tester 1–5</td><td>Check the top bar says “Synced”</td></tr>"
                "<tr><td>0:10–0:45</td><td><b>Game A</b> (35 min)</td><td>Press Start under Session; watch live progress</td></tr>"
                "<tr><td>0:45–0:50</td><td>Feedback on A</td><td>Press End; remind everyone to fill in feedback</td></tr>"
                "<tr><td>0:50–1:30</td><td><b>Game B</b> (40 min)</td><td>Act as Exchange clerk; 25′ monsoon, 32′ blockade, 38′ pirates, 42′ close</td></tr>"
                "<tr><td>1:30–1:40</td><td>Feedback on B + break</td><td></td></tr>"
                "<tr><td>1:40–2:20</td><td><b>Game C</b> (40 min)</td><td>Check for stalls at 25′ and 35′</td></tr>"
                "<tr><td>2:20–2:25</td><td>Feedback on C</td><td></td></tr>"
                "<tr><td>2:25–2:45</td><td>Review Results together and pick the game</td><td>Reveal answers and walk through them</td></tr></table></div>"),
            "prep": T(
                "<ul><li>在分享菜单里把 4 位测试员加为 <b>Contributor</b>（或更高）。只能查看的人写不进进度和反馈。</li>"
                "<li>五个人分坐五张桌子，模拟真实的跨队距离。跨队信息必须走过去当面说，不许截图转发。</li>"
                "<li>B 局需要一个闻香台：5 个不透明小罐，编号 1–5（摆放方式见完整答案）。没有香料时，主持人可以在实时进度里手动标记 B1 已解。</li>"
                "<li>准备纸笔，方便推理题和画网格。</li><li>主持人保持答案锁定，直到最后复盘。</li></ul>",
                "<ul><li>In the share menu, add the four testers as <b>Contributor</b> or higher. View-only people can't save progress or feedback.</li>"
                "<li>Seat the five people at five separate tables to mimic real distances. Cross-team information must be carried in person; no screenshots.</li>"
                "<li>Game B needs one smell station: 5 opaque jars numbered 1–5 (layout in the full solutions). Without spices, the host can mark B1 solved from Live progress.</li>"
                "<li>Have paper and pens for the logic puzzles and grids.</li><li>Keep the answers locked until the final review.</li></ul>"),
        },
    }
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (HERE / "template.html").read_text(encoding="utf-8").replace("__DATA__", raw)
    OUT.write_text(html, encoding="utf-8")
    # make sure no final code leaks in plain text
    plain = html
    for secret in ["FEAST", "SPICE\"", "TABLE\"", "LCGMM", "RRUU\"", "\"889\"", "\"250\"", "MOLUCCAS", "ANTWERP", "GALLEY\"", "ECHOISLAND"]:
        assert secret not in plain, f"leak: {secret}"
    print("wrote", OUT, len(html) // 1024, "KB")
    print("host token sha256:", hashlib.sha256(("aod-host|" + norm(HOST_PASSWORD)).encode()).hexdigest())


if __name__ == "__main__":
    build()
