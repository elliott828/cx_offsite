# -*- coding: utf-8 -*-
"""Build the Option A v2 playtest page.

python build_v2.py                                  -> ../方案A_v2_测试页.html (this device only)
python build_v2.py --vercel <supabase_url> <anon>   -> ../vercel_v2/index.html (synced)
"""
import hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import enc, norm  # same crypto and normalisation as v1
from content import HOST_PASSWORD
import content_v2 as C

HERE = Path(__file__).parent
OUT = HERE.parent / "方案A_v2_测试页.html"
BACKEND = None
if len(sys.argv) >= 4 and sys.argv[1] == "--vercel":
    BACKEND = {"url": sys.argv[2].rstrip("/"), "key": sys.argv[3], "prefix": "v2-"}
    OUT = HERE.parent / "vercel_v2" / "index.html"
    OUT.parent.mkdir(exist_ok=True)


def gate_blobs(pid, gate):
    answers, reveal = gate["answers"], gate["reveal"]
    aliases = gate.get("aliases", {})
    blobs = {}
    for tk, rv in reveal.items():
        ans = answers.get(tk, answers.get(0))
        canon = norm(ans, gate)
        assert canon == ans, (pid, ans, canon)
        variants = list(dict.fromkeys([canon] + [norm(a, gate) for a, v in aliases.items() if v == canon]))
        blobs[str(tk)] = [enc(f"{pid}#{tk}", v, rv) for v in variants]
    return blobs


def build():
    keys, puzzles = {}, []
    for p in C.PUZZLES:
        q = {k: v for k, v in p.items() if k != "gate"}
        q["body"] = {str(k): v for k, v in p["body"].items()}
        if "gate" in p:
            g = p["gate"]
            q["gate"] = {k: g[k] for k in ("label", "ph", "dir", "numwords") if k in g}
            q["gate"]["blobs"] = gate_blobs(p["id"], g)
            keys[p["id"]] = {str(k): v for k, v in g["answers"].items()}
        puzzles.append(q)

    bottles = []
    for i, (riddle, ans, alts) in enumerate(C.BOTTLES, start=1):
        pid = f"BOT{i}"
        g = {"answers": {0: ans}, "aliases": {a: ans for a in alts}, "numwords": True,
             "reveal": {0: C.T(f"漂流瓶 {i} 答对了：<b>{ans}</b>", f"Bottle {i} solved: <b>{ans}</b>")}}
        bottles.append({"id": pid, "riddle": riddle, "wave": 1 if i <= 3 else 2, "blobs": gate_blobs(pid, g)["0"]})
        keys[pid] = {"0": ans}

    sol = {"html": C.SOLUTION, "keys": keys,
           "quiz": [a for _, a in C.QUIZ], "malacca": C.MALACCA_Q}
    data = {
        "teams": C.TEAMS, "ships": C.SHIPS, "colors": C.COLORS, "players": C.PLAYERS, "hintTokens": C.HINT_TOKENS,
        "ports": C.PORTS, "portName": C.PORT_NAME, "portLetter": C.PORT_LETTER, "home": C.HOME,
        "keyholder": C.KEYHOLDER, "portChallenge": C.PORT_CHALLENGE,
        "quiz": [q for q, _ in C.QUIZ], "bottles": bottles, "stars": C.STAR_SHEETS,
        "puzzles": puzzles, "events": C.EVENTS, "protocol": C.PROTOCOL, "minutes": 60, "onTime": 52,
        "sol": enc("SOL#0", hashlib.sha256(("aod-sol|" + norm(HOST_PASSWORD)).encode()).hexdigest(), sol),
        "backend": BACKEND,
    }
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (HERE / "template_v2.html").read_text(encoding="utf-8").replace("__DATA__", raw)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    for secret in ["FLORA", "\"6387\"", "\"2327\"", "MALACCA\"", "NUTMEG", "FOOTSTEPS", "Pacific", "太平洋"]:
        assert secret not in html, f"leak: {secret}"
    print("wrote", OUT, len(html) // 1024, "KB")


if __name__ == "__main__":
    build()
