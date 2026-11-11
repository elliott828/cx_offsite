# -*- coding: utf-8 -*-
"""Playtest content for the Age of Discovery puzzle game.

Every puzzle is written for the 5-person feasibility test: tester N plays team N
in all three games. Plain fields are visible in the page; anything under
`reveal` or `solution` is encrypted by build.py and only opens with the right
answer (or the host password).
"""

def T(zh, en):
    return {"zh": zh, "en": en}

TEAMS = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------- helpers
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MORSE = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
         "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
         "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
         "Y": "-.--", "Z": "--.."}


def row_table(top_label, top, bot_label, bot):
    head = "".join(f"<td>{c}</td>" for c in top)
    body = "".join(f"<td>{c}</td>" for c in bot)
    return (f'<div class="tw"><table class="keytab"><tr><th>{top_label}</th>{head}</tr>'
            f'<tr><th>{bot_label}</th>{body}</tr></table></div>')


def key_caesar(lang):
    shifted = ALPHA[3:] + ALPHA[:3]
    lab = ("密文", "明文") if lang == "zh" else ("Cipher", "Plain")
    note = "凯撒密码轮 · 指针固定在 +3" if lang == "zh" else "Caesar wheel · fixed at +3"
    return f"<p class=\"keyname\">{note}</p>" + row_table(lab[0], shifted, lab[1], ALPHA)


def key_a1z26(lang):
    note = "字母数字对照表" if lang == "zh" else "Letter–number table"
    return f"<p class=\"keyname\">{note}</p>" + row_table("A–Z", ALPHA, "#", [str(i) for i in range(1, 27)])


def key_mirror(lang):
    if lang == "zh":
        return '<p class="keyname">镜面卡</p><div class="mirrorcard">真相藏在倒影里。</div>'
    return '<p class="keyname">Mirror card</p><div class="mirrorcard">The truth is in the reflection.</div>'


def key_morse(lang):
    note = "摩尔斯电码表" if lang == "zh" else "Morse code chart"
    cells = "".join(f'<span><b>{k}</b> <code>{v}</code></span>' for k, v in MORSE.items())
    return f'<p class="keyname">{note}</p><div class="morsegrid">{cells}</div>'


def key_atbash(lang):
    note = "埃特巴什码表（字母表首尾对折）" if lang == "zh" else "Atbash table (alphabet folded end to end)"
    return f"<p class=\"keyname\">{note}</p>" + row_table("A–Z", ALPHA, "↔", ALPHA[::-1])


# ================================================================ GAME A
A_SHIPS = {1: T("海鹰号", "Sea Hawk"), 2: T("北极星号", "Polaris"), 3: T("信风号", "Trade Wind"),
           4: T("珊瑚号", "Coral"), 5: T("晨星号", "Morning Star")}
A_FLAGS = {1: "SIX", 2: "ONE", 3: "NINE", 4: "TWO", 5: "FIVE"}
A_DIG1 = {1: "6", 2: "1", 3: "9", 4: "2", 5: "5"}
A_TURNS = {
    1: T("右转 90° → 右转 45° → 左转 180°", "Right 90° → Right 45° → Left 180°"),
    2: T("左转 45° → 左转 90° → 右转 45°", "Left 45° → Left 90° → Right 45°"),
    3: T("右转 135° → 左转 45° → 右转 90°", "Right 135° → Left 45° → Right 90°"),
    4: T("右转 180° → 左转 45° → 左转 90°", "Right 180° → Left 45° → Left 90°"),
    5: T("右转 90° → 右转 90° → 左转 45°", "Right 90° → Right 90° → Left 45°"),
}
A_DIG3 = {1: "8", 2: "7", 3: "5", 4: "2", 5: "4"}
A_CODE = {t: A_DIG1[t] + "3" + A_DIG3[t] for t in TEAMS}
A_PORT = {1: "LISBON", 2: "CAPE", 3: "GOA", 4: "MALACCA", 5: "MOLUCCAS"}
A_PORT_ZH = {1: "里斯本", 2: "好望角", 3: "果阿", 4: "马六甲", 5: "摩鹿加"}
A_ENC = {1: "OLVERQ", 2: "3 · 1 · 16 · 5", 3: '<span class="mirror">GOA</span>',
         4: "-- .- .-.. .- -.-. -.-. .-", 5: "NLOFXXZH"}
A_HALF = {1: T("跟着香料的味道", "Follow the scent of spice"),
          2: T("穿过风暴之角", "through the Cape of Storms"),
          3: T("越过季风之海", "across the monsoon sea"),
          4: T("走过狭窄的海峡", "past the narrow strait"),
          5: T("宴席就在终点 ✕", "the feast waits at the end ✕")}
# key card inside team t's chest decodes fragment (t-1); team 1 holds key for fragment 5
A_KEYFOR = {1: 5, 2: 1, 3: 2, 4: 3, 5: 4}
A_KEYFN = {1: key_caesar, 2: key_a1z26, 3: key_mirror, 4: key_morse, 5: key_atbash}
A_SEAL = {1: "F", 2: "E", 3: "A", 4: "S", 5: "T"}  # seal for fragment n's port


def a_chest_reveal(t, lang):
    frag_owner = A_KEYFOR[t]
    ship = A_SHIPS[frag_owner][lang]
    own = A_SHIPS[t][lang]
    if lang == "zh":
        return (f'<div class="chestgrid"><div class="fragment"><p class="eyebrow">残图 {t} · {own}</p>'
                f'<p class="encport">{A_ENC[t]}</p><p class="halfline">“{A_HALF[t]["zh"]} ……”</p>'
                f'<p class="note">港口名被加密了。钥匙不在你的船上。</p></div>'
                f'<div class="keycard"><p class="eyebrow">钥匙卡 · 背面写着：{ship}</p>{A_KEYFN[frag_owner]("zh")}'
                f'<p class="seal">印章 <b>{A_SEAL[frag_owner]}</b> · 背面写着“{A_PORT_ZH[frag_owner]}”'
                f'<span class="note">（要等 {ship} 解出港口后，你才知道这是哪个港口）</span></p></div></div>'
                f'<p class="note">信使规则：钥匙卡只能给对方看，不能转发截图。</p>')
    return (f'<div class="chestgrid"><div class="fragment"><p class="eyebrow">Fragment {t} · {own}</p>'
            f'<p class="encport">{A_ENC[t]}</p><p class="halfline">“{A_HALF[t]["en"]} …”</p>'
            f'<p class="note">The port name is encrypted. Its key is not on your ship.</p></div>'
            f'<div class="keycard"><p class="eyebrow">Key card · back reads: {ship}</p>{A_KEYFN[frag_owner]("en")}'
            f'<p class="seal">Seal <b>{A_SEAL[frag_owner]}</b> · back reads “{A_PORT[frag_owner].title()}”'
            f'<span class="note"> (you only learn which port that is once {ship} decodes it)</span></p></div></div>'
            f'<p class="note">Messenger rule: show key cards in person; no screenshots.</p>')


GAME_A = {
    "id": "A",
    "name": T("五片航海图", "The Five Fragments"),
    "mode": T("纯合作", "Pure cooperation"),
    "testMinutes": 35, "realMinutes": 50,
    "roles": A_SHIPS,
    "roleWord": T("船", "Ship"),
    "story": T(
        "1519 年，五艘船准备从里斯本出发寻找香料群岛。老船长临终前把唯一的航海图撕成五片，分别锁进五艘船的船长箱。"
        "今晚舰队在港口重新集结，必须在天亮前拼出完整航线。<b>每一片地图都不完整，每一把钥匙都不在它自己的船上。</b>",
        "1519: five ships prepare to leave Lisbon for the Spice Islands. The dying Admiral tore the only chart into five "
        "pieces and locked one in each captain's chest. Tonight the fleet regroups and must rebuild the route before dawn. "
        "<b>No fragment is complete, and no key is on its own ship.</b>"),
    "testNote": T(
        "测试时一个人代表一整条船。第一幕的三道谜在真实活动里由 5 人并行，所以你的用时会偏长，这正是我们要观察的数据。",
        "In this test one person plays a whole ship. In the real event five people split Act 1, so your times will run "
        "long. That is exactly the data we want."),
    "puzzles": [
        {
            "id": "A1", "stage": "intra", "target": 6,
            "title": T("信号旗", "Signal flags"),
            "body": {t: T(
                f'<p>桅杆上挂着一串旗。对照下方的国际信号旗表，拼出你的第一个数字。</p><div class="flagrow" data-flags="{A_FLAGS[t]}"></div>'
                '<details class="chart"><summary>国际信号旗对照表</summary><div data-flagchart></div></details>',
                f'<p>A string of flags flies from the mast. Use the signal flag chart below to spell your first number.</p>'
                f'<div class="flagrow" data-flags="{A_FLAGS[t]}"></div>'
                '<details class="chart"><summary>International signal flag chart</summary><div data-flagchart></div></details>')
                for t in TEAMS},
            "gate": {"label": T("锁的第 1 位数字", "Digit 1 of the lock"), "ph": T("例如 4", "e.g. 4"),
                     "answers": A_DIG1, "numwords": True,
                     "reveal": {t: T(f"正确。第 1 位是 <b>{A_DIG1[t]}</b>。", f"Correct. Digit 1 is <b>{A_DIG1[t]}</b>.") for t in TEAMS}},
            "hints": [T("每面旗代表一个字母。", "Each flag stands for one letter."),
                      T("逐面查表，拼出一个英文单词。", "Look each flag up; they spell an English word."),
                      T("这个单词是一个数字的英文。", "The word is a number.")],
        },
        {
            "id": "A2", "stage": "intra", "target": 8,
            "title": T("船员名册", "Crew roster"),
            "body": {0: T(
                "<p>1–4 号铺住着 Pedro、Juan、Diego、Luis，职位分别是领航员、厨师、木匠、炮手（每人一个）。</p><ol class=\"clues\">"
                "<li>领航员睡在 1 号铺。</li><li>厨师的铺号正好比 Juan 大 1。</li><li>Luis 睡在最后一个铺位。</li>"
                "<li>Diego 既不是木匠，也不是厨师。</li><li>炮手和木匠的铺位不相邻。</li></ol><p><b>厨师睡在几号铺？这是锁的第 2 位。</b></p>",
                "<p>Pedro, Juan, Diego and Luis sleep in bunks 1–4. Their jobs are navigator, cook, carpenter and gunner (one each).</p><ol class=\"clues\">"
                "<li>The navigator sleeps in bunk 1.</li><li>The cook's bunk is exactly one higher than Juan's.</li>"
                "<li>Luis sleeps in the last bunk.</li><li>Diego is neither the carpenter nor the cook.</li>"
                "<li>The gunner and the carpenter are not in adjacent bunks.</li></ol><p><b>Which bunk is the cook in? That is digit 2.</b></p>")},
            "gate": {"label": T("锁的第 2 位数字", "Digit 2 of the lock"), "ph": T("1–4", "1–4"),
                     "answers": {0: "3"}, "numwords": True,
                     "reveal": {0: T("正确。第 2 位是 <b>3</b>。", "Correct. Digit 2 is <b>3</b>.")}},
            "hints": [T("画一张 4×4 表格，先填确定的信息。", "Draw a 4×4 grid and fill in what is certain."),
                      T("从第 3 条和第 1 条入手，再分情况讨论 Diego 的职位。", "Start from clues 3 and 1, then test each job for Diego."),
                      T("Diego 是领航员，Juan 在 2 号铺。", "Diego is the navigator; Juan is in bunk 2.")],
        },
        {
            "id": "A3", "stage": "intra", "target": 5,
            "title": T("罗盘转向", "Compass turns"),
            "body": {t: T(
                f'<p>罗盘卡：北=1，东北=2，东=3，东南=4，南=5，西南=6，西=7，西北=8。</p>'
                f'<p>船头朝北出发。航海日志写着：</p><p class="logline">{A_TURNS[t]["zh"]}</p><p>最终船头所指方向的数字，就是锁的第 3 位。</p>',
                f'<p>Compass card: N=1, NE=2, E=3, SE=4, S=5, SW=6, W=7, NW=8.</p>'
                f'<p>The bow starts facing north. The log reads:</p><p class="logline">{A_TURNS[t]["en"]}</p><p>The digit of your final heading is digit 3.</p>')
                for t in TEAMS},
            "gate": {"label": T("锁的第 3 位数字", "Digit 3 of the lock"), "ph": T("1–8", "1–8"),
                     "answers": A_DIG3, "numwords": True,
                     "reveal": {t: T(f"正确。第 3 位是 <b>{A_DIG3[t]}</b>。", f"Correct. Digit 3 is <b>{A_DIG3[t]}</b>.") for t in TEAMS}},
            "hints": [T("站起来真的转一转。", "Stand up and actually turn."),
                      T("右转是顺时针，45° 是罗盘上相邻的一格。", "Right is clockwise; 45° is one step on the compass."),
                      T("第一次转向后你朝向哪里？写下每一步。", "Write down your heading after every turn.")],
        },
        {
            "id": "A-chest", "stage": "intra", "target": 1,
            "title": T("打开船长箱", "Open the captain's chest"),
            "body": {0: T("<p>船长箱挂着一把 3 位数字锁，顺序是 A1 → A2 → A3。</p>",
                          "<p>The chest has a 3-digit lock, in the order A1 → A2 → A3.</p>")},
            "gate": {"label": T("3 位密码", "3-digit code"), "ph": "000", "answers": A_CODE,
                     "reveal": {t: T(a_chest_reveal(t, "zh"), a_chest_reveal(t, "en")) for t in TEAMS}},
            "hints": [T("把 A1、A2、A3 的数字按顺序连起来。", "Join the digits from A1, A2 and A3 in order."),
                      T("三道题都要先解出来。", "All three must be solved first."),
                      T("检查 A3 的每一次转向。", "Re-check each turn in A3.")],
        },
        {
            "id": "A4", "stage": "cross", "target": 12, "requires": "A-chest",
            "title": T("解开你的港口名", "Decode your port"),
            "body": {0: T("<p>你的残图上的港口名是加密的。找到持有你钥匙卡的那艘船，请他们给你看钥匙。解出港口后在这里提交。</p>",
                          "<p>The port on your fragment is encrypted. Find the ship holding your key card and ask to see it. Submit the port here.</p>")},
            "gate": {"label": T("港口名（英文或中文）", "Port name"), "ph": "PORT",
                     "answers": A_PORT,
                     "aliases": {"里斯本": "LISBON", "好望角": "CAPE", "CAPEOFGOODHOPE": "CAPE", "果阿": "GOA",
                                 "马六甲": "MALACCA", "摩鹿加": "MOLUCCAS", "摩鹿加群岛": "MOLUCCAS", "MOLUCCA": "MOLUCCAS",
                                 "SPICEISLANDS": "MOLUCCAS", "香料群岛": "MOLUCCAS"},
                     "reveal": {t: T(f"港口徽章到手：<b>{A_PORT_ZH[t]} {A_PORT[t]}</b>。告诉持有你港口印章的那艘船。",
                                     f"Port badge earned: <b>{A_PORT[t].title()}</b>. Tell the ship holding your port's seal.") for t in TEAMS}},
            "hints": [T("钥匙卡背面写着船名，去找那艘船。", "The key card names a ship on its back. Go find it."),
                      T("凯撒：每个字母往回数 3 位；埃特巴什：A↔Z 对折。", "Caesar: shift back 3. Atbash: fold A↔Z."),
                      T("五个港口都在从里斯本到香料群岛的路上。", "All five ports lie on the route from Lisbon to the Spice Islands.")],
        },
        {
            "id": "A5", "stage": "cross", "target": 5, "shared": True,
            "title": T("航线顺序", "Route order"),
            "body": {0: T("<p>全舰队一起决定五个港口的航行顺序，把半截句子按顺序连起来。任何一条船都可以提交。</p>",
                          "<p>The whole fleet agrees the order of the five ports and joins the half-sentences. Any ship may submit.</p>")},
            "gate": {"label": T("按顺序输入 5 个港口的英文首字母", "First letters of the 5 ports, in order"), "ph": "XXXXX",
                     "answers": {0: "LCGMM"},
                     "reveal": {0: T("<p>五段连起来：<b>跟着香料的味道 / 穿过风暴之角 / 越过季风之海 / 走过狭窄的海峡 / 宴席就在终点</b>。</p><p>最后一片残图上的 ✕ 指向：<b>厨房门口</b>。那里有一只挂着 5 位字母锁的宝箱。</p>",
                                     "<p>Joined: <b>Follow the scent of spice / through the Cape of Storms / across the monsoon sea / past the narrow strait / the feast waits at the end</b>.</p><p>The ✕ on the last fragment points to <b>the kitchen door</b>, where a chest waits with a 5-letter lock.</p>")}},
            "hints": [T("从里斯本出发，往南绕过非洲。", "Leave Lisbon and head south around Africa."),
                      T("印度之后是一条狭窄的海峡。", "After India comes a narrow strait."),
                      T("里斯本 → 好望角 → 果阿 → ……", "Lisbon → Cape → Goa → …")],
        },
        {
            "id": "A6", "stage": "final", "target": 6, "shared": True, "requires": "A5",
            "title": T("老船长的最后宝箱", "The Admiral's last chest"),
            "body": {0: T("<p>宝箱上刻着：“按航线顺序，盖上每一个港口的印章。”</p>",
                          "<p>The lid reads: “Stamp each port's seal, in the order of the voyage.”</p>")},
            "gate": {"label": T("5 位字母密码", "5-letter code"), "ph": "XXXXX", "answers": {0: "FEAST"},
                     "reveal": {0: T("<p class=\"letter\">“我把地图撕成五片，不是因为不信任你们，而是我知道，只有五艘船一起，才到得了这里。欢迎来到香料群岛。今晚的盛宴，属于整支船队。”</p><p>主持人摇铃，厨房上菜。</p>",
                                     "<p class=\"letter\">“I tore the chart into five not because I distrusted you, but because only five ships together could reach this place. Welcome to the Spice Islands. Tonight's feast belongs to the whole fleet.”</p><p>The host rings the bell and dinner is served.</p>")}},
            "hints": [T("每条船手里都有一枚印章。", "Every ship holds one seal."),
                      T("印章背面写着港口名。", "Each seal names a port on its back."),
                      T("按 A5 的港口顺序排印章。", "Order the seals by the route from A5.")],
        },
    ],
    "solution": T(
        "<h4>锁码与答案</h4><table><tr><th>船</th><th>A1 旗</th><th>A2</th><th>A3</th><th>船长箱</th><th>港口</th><th>持有的钥匙 / 印章</th></tr>"
        + "".join(f"<tr><td>{t} {A_SHIPS[t]['zh']}</td><td>{A_FLAGS[t]} = {A_DIG1[t]}</td><td>3</td><td>{A_DIG3[t]}</td><td><b>{A_CODE[t]}</b></td><td>{A_PORT_ZH[t]} {A_PORT[t]}</td><td>残图 {A_KEYFOR[t]} 的钥匙 · 印章 {A_SEAL[A_KEYFOR[t]]}</td></tr>" for t in TEAMS)
        + "</table><p>A2 推理：Luis=4；Diego 只能是领航员（1 号）；若 Juan=3 则木匠和炮手相邻，矛盾；所以 Juan=2，厨师 Pedro=3。</p>"
          "<p>A5：LCGMM（里斯本 → 好望角 → 果阿 → 马六甲 → 摩鹿加）。A6：印章按港口顺序 F-E-A-S-T = <b>FEAST</b>。</p>",
        "<h4>Codes and answers</h4><table><tr><th>Ship</th><th>A1 flags</th><th>A2</th><th>A3</th><th>Chest</th><th>Port</th><th>Holds key / seal</th></tr>"
        + "".join(f"<tr><td>{t} {A_SHIPS[t]['en']}</td><td>{A_FLAGS[t]} = {A_DIG1[t]}</td><td>3</td><td>{A_DIG3[t]}</td><td><b>{A_CODE[t]}</b></td><td>{A_PORT[t]}</td><td>Key for fragment {A_KEYFOR[t]} · seal {A_SEAL[A_KEYFOR[t]]}</td></tr>" for t in TEAMS)
        + "</table><p>A2: Luis=4; Diego can only be the navigator (bunk 1); Juan=3 would put carpenter and gunner side by side, so Juan=2 and the cook Pedro is in bunk 3.</p>"
          "<p>A5: LCGMM (Lisbon → Cape → Goa → Malacca → Moluccas). A6: seals in route order F-E-A-S-T = <b>FEAST</b>.</p>"),
    "watch": T(["第一幕谁最先完成、闲了多久", "钥匙环有没有造成某条船长时间等待", "埃特巴什和镜像字是否太难或太简单", "A5 是全员讨论还是一个人拍板"],
               ["Who finishes Act 1 first and how long they sit idle", "Whether the key ring leaves one ship waiting", "Whether Atbash and mirror writing are too hard or too easy", "Whether A5 is a group discussion or one person deciding"]),
}

# ================================================================ GAME B
SPICES = ["pepper", "cinnamon", "clove", "nutmeg", "anise"]
SPICE_NAME = {"pepper": T("黑胡椒", "Pepper"), "cinnamon": T("肉桂", "Cinnamon"), "clove": T("丁香", "Clove"),
              "nutmeg": T("肉豆蔻", "Nutmeg"), "anise": T("八角", "Star anise"), "saffron": T("藏红花（万能）", "Saffron (wild)"),
              "coins": T("金币", "Coins")}
B_HOUSES = {1: T("狮子商行", "House of the Lion"), 2: T("雄鹰商行", "House of the Eagle"),
            3: T("海豚商行", "House of the Dolphin"), 4: T("玫瑰商行", "House of the Rose"), 5: T("星辰商行", "House of the Star")}
B_HOME = {t: SPICES[t - 1] for t in TEAMS}
B_FOREIGN = {t: SPICES[(t - 1 + 4) % 5] for t in TEAMS}
B_RECIPE = {t: [SPICES[(t - 1 + k) % 5] for k in range(4)] for t in TEAMS}
B_FOOT = {4: ("I", T("国王的宴席", "The King's feast"), "S"), 1: ("II", T("不属于", "belongs to"), "P"),
          5: ("III", T("任何一家商行", "no single house"), "I"), 3: ("IV", T("而属于", "but to"), "C"),
          2: ("V", T("所有远航归来的人", "all who sailed home"), "E")}
B_LEDGER_BAD = {1: 5, 2: 2, 3: 3, 4: 4, 5: 1}
LEDGER_LINES = [  # name, qty, price, correct, inflated
    (T("胡椒", "Pepper"), "XII", "III", "XXXVI", "XLVI"),
    (T("肉桂", "Cinnamon"), "VIII", "V", "XL", "L"),
    (T("丁香", "Clove"), "XV", "IV", "LX", "LXX"),
    (T("肉豆蔻", "Nutmeg"), "VI", "IX", "LIV", "LXIV"),
    (T("八角", "Star anise"), "X", "VII", "LXX", "LXXX"),
]
ROMAN = ["I", "II", "III", "IV", "V"]


def ledger_html(t, lang):
    rows = ""
    for i, (nm, q, p, ok, bad) in enumerate(LEDGER_LINES, start=1):
        val = bad if i == B_LEDGER_BAD[t] else ok
        unit = (" 袋 × ", " 金币 = ") if lang == "zh" else (" sacks × ", " coins = ")
        rows += f"<tr><td>{ROMAN[i-1]}</td><td>{nm[lang]}</td><td class=\"mono\">{q}{unit[0]}{p}{unit[1]}{val}</td></tr>"
    tot = "总计" if lang == "zh" else "Total"
    return f'<div class="tw"><table class="ledger">{rows}<tr><td></td><td>{tot}</td><td class="mono">CCLXX</td></tr></table></div>'


B_PRICES = {
    1: ("3 cr", "8 fl", "1 d + 10 r", "35 r", "ANTWERP"),
    2: ("3 cr", "10 fl", "1 d + 14 r", "37 r", "LISBON"),
    3: ("4 cr", "11 fl", "1 d + 18 r", "45 r", "SEVILLE"),
    4: ("4 cr", "11 fl", "1 d + 22 r", "43 r", "VENICE"),
    5: ("2 cr", "5 fl", "1 d", "22 r", "ANTWERP"),
}


def prices_html(t, lang):
    l, a, s, v, _ = B_PRICES[t]
    if lang == "zh":
        conv = lambda x: x.replace("cr", "克鲁扎多").replace("fl", "弗罗林").replace(" d", " 杜卡特").replace("1 d", "1 杜卡特").replace(" r", " 雷亚尔")
        return (f"<p>汇率：1 杜卡特 = 2 克鲁扎多；1 克鲁扎多 = 3 弗罗林；1 弗罗林 = 4 雷亚尔。</p>"
                f"<div class=\"tw\"><table><tr><th>里斯本</th><th>安特卫普</th><th>塞维利亚</th><th>威尼斯</th></tr>"
                f"<tr><td>{conv(l)}</td><td>{conv(a)}</td><td>{conv(s)}</td><td>{conv(v)}</td></tr></table></div><p><b>同一袋货在哪里最便宜？</b></p>")
    conv = lambda x: x.replace("cr", "cruzados").replace("fl", "florins").replace(" d", " ducat").replace(" r", " reales")
    return (f"<p>Rates: 1 ducat = 2 cruzados; 1 cruzado = 3 florins; 1 florin = 4 reales.</p>"
            f"<div class=\"tw\"><table><tr><th>Lisbon</th><th>Antwerp</th><th>Seville</th><th>Venice</th></tr>"
            f"<tr><td>{conv(l)}</td><td>{conv(a)}</td><td>{conv(s)}</td><td>{conv(v)}</td></tr></table></div><p><b>Where is the same sack cheapest?</b></p>")


TIMELINE = T(
    "<ul class=\"timeline\"><li><b>1405</b> 巨大的宝船，明朝的旗帜</li><li><b>1488</b> 非洲最南端的“风暴之角”</li>"
    "<li><b>1492</b> 三艘船，西班牙国旗，“西印度”</li><li><b>1498</b> 卡利卡特港，印度的胡椒</li>"
    "<li><b>1500</b> 意外漂到的南美海岸</li><li><b>1519</b> 五艘船出发，目标是绕地球一圈</li></ul>",
    "<ul class=\"timeline\"><li><b>1405</b> A colossal treasure ship under a Ming banner</li><li><b>1488</b> The “Cape of Storms” at Africa's tip</li>"
    "<li><b>1492</b> Three ships, a Spanish flag, “the Indies”</li><li><b>1498</b> The port of Calicut, Indian pepper</li>"
    "<li><b>1500</b> A South American coast reached by accident</li><li><b>1519</b> Five ships set out to circle the globe</li></ul>")


def events_card(evs, lang):
    head = "按下面事件的顺序，取每个事件发生年份的最后一位：" if lang == "zh" else "In the order below, take the last digit of each event's year:"
    return f"<p>{head}</p><ol>" + "".join(f"<li>{e[lang]}</li>" for e in evs) + "</ol>"


EV_ALPHA = [T("达伽马抵达印度", "Da Gama reaches India"), T("迪亚士绕过好望角", "Dias rounds the Cape"), T("麦哲伦船队出发", "Magellan's fleet departs")]
EV_BETA = [T("哥伦布抵达美洲", "Columbus reaches the Americas"), T("郑和首次下西洋", "Zheng He's first voyage"), T("卡布拉尔抵达巴西", "Cabral reaches Brazil")]

GAME_B = {
    "id": "B",
    "name": T("塞维利亚香料交易所", "The Seville Spice Exchange"),
    "mode": T("先竞争，后合作", "Compete, then cooperate"),
    "testMinutes": 40, "realMinutes": 50,
    "roles": B_HOUSES,
    "roleWord": T("商行", "House"),
    "market": True,
    "story": T(
        "1520 年代的塞维利亚，香料比黄金还贵。国王宣布：第一个献上“皇家宴会配方”全部香料的商行，将获得下一次远航的特许状。"
        "五家商行各控制一种香料的产地，谁也凑不齐自己的配方。<b>交易、结盟、海盗，以及最后的诏书。</b>",
        "Seville, 1520s, when spice is worth more than gold. The King promises the next royal charter to the first house that "
        "presents every spice in the Royal Banquet Recipe. Each house controls one spice and none can finish its recipe alone. "
        "<b>Trades, alliances, pirates, and a final decree.</b>"),
    "testNote": T(
        "测试时由主持人兼任交易所书记员，银行和事件在主持人视图里操作。香料“货箱”和金币都记在页面上，交易时双方各自点转账。B1 需要一个真实的闻香台（5 个罐子）。",
        "In this test the host doubles as the Exchange clerk; bank and events live in the host view. Crates and coins are tracked "
        "on the page: in a trade, each side sends its half. B1 needs one real smell station (5 jars)."),
    "puzzles": [
        {
            "id": "B1", "stage": "intra", "target": 6,
            "title": T("闻香辨货", "Smell the cargo"),
            "body": {0: T(
                "<p>去闻香台（5 个编号小罐）。根据描述判断每个罐子装的是什么。</p><ul class=\"cargo\">"
                "<li><b>黑胡椒</b>：马拉巴尔海岸的“黑色黄金”，闻一下就想打喷嚏。</li><li><b>肉桂</b>：锡兰树木的内皮，甜而温暖。</li>"
                "<li><b>丁香</b>：摩鹿加群岛的花蕾，像小钉子，闻久了舌头发麻。</li><li><b>肉豆蔻</b>：班达群岛的果核，味道最“闷”。</li>"
                "<li><b>八角</b>：来自中国南方的八角星，带甘草味。</li></ul>",
                "<p>Go to the smell station (5 numbered jars). Work out what each jar holds.</p><ul class=\"cargo\">"
                "<li><b>Black pepper</b>: the “black gold” of the Malabar Coast; one sniff and you sneeze.</li><li><b>Cinnamon</b>: Ceylon bark, sweet and warm.</li>"
                "<li><b>Clove</b>: a Moluccan flower bud shaped like a nail; it numbs the tongue.</li><li><b>Nutmeg</b>: a Banda Islands seed, the most “muted” smell.</li>"
                "<li><b>Star anise</b>: an eight-pointed star from southern China that smells of liquorice.</li></ul>")},
            "gate": {"label": T("按 胡椒·肉桂·丁香·肉豆蔻·八角 的顺序写罐号", "Jar numbers in the order pepper·cinnamon·clove·nutmeg·anise"),
                     "ph": "00000", "answers": {0: "31524"},
                     "reveal": {0: T("书记员核对通过。<b>本土香料 ×2</b> 已入库。", "Clerk confirms. <b>2 crates of your home spice</b> added.")}},
            "rewards": {t: [[B_HOME[t], 2]] for t in TEAMS},
            "hints": [T("先找最好认的：八角（甘草味）和肉桂（甜）。", "Start with the easy ones: anise (liquorice) and cinnamon (sweet)."),
                      T("丁香会让鼻子发麻；肉豆蔻最闷。", "Clove numbs; nutmeg is the most muted."),
                      T("1 号罐是肉桂，4 号罐是八角。", "Jar 1 is cinnamon and jar 4 is star anise.")],
        },
        {
            "id": "B2", "stage": "intra", "target": 5,
            "title": T("罗马数字账簿", "Roman-numeral ledger"),
            "body": {t: T("<p>司库偷了钱，还改了账本里的一行。找出被改的是第几行。</p>" + ledger_html(t, "zh"),
                          "<p>The treasurer stole money and altered one line of the ledger. Which line?</p>" + ledger_html(t, "en")) for t in TEAMS},
            "gate": {"label": T("被改的行号（1–5）", "Altered line (1–5)"), "ph": "1–5",
                     "answers": {t: str(B_LEDGER_BAD[t]) for t in TEAMS}, "numwords": True,
                     "aliases": {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5"},
                     "reveal": {t: T(f"抓到了：第 {B_LEDGER_BAD[t]} 行多记了 10 金币。<b>追回 5 金币</b>。", f"Caught: line {B_LEDGER_BAD[t]} was padded by 10. <b>5 coins recovered.</b>") for t in TEAMS}},
            "rewards": {t: [["coins", 5]] for t in TEAMS},
            "hints": [T("先把罗马数字换成阿拉伯数字。", "Convert the numerals first."),
                      T("I=1 V=5 X=10 L=50 C=100，小数在左边表示相减。", "I=1 V=5 X=10 L=50 C=100; smaller on the left subtracts."),
                      T("逐行算乘法，看哪行对不上。", "Multiply each line and find the mismatch.")],
        },
        {
            "id": "B3", "stage": "intra", "target": 5,
            "title": T("四国货币", "Four currencies"),
            "body": {t: T(prices_html(t, "zh"), prices_html(t, "en")) for t in TEAMS},
            "gate": {"label": T("最便宜的港口", "Cheapest port"), "ph": T("港口名", "Port"),
                     "answers": {t: B_PRICES[t][4] for t in TEAMS},
                     "aliases": {"安特卫普": "ANTWERP", "里斯本": "LISBON", "塞维利亚": "SEVILLE", "SEVILLA": "SEVILLE", "威尼斯": "VENICE"},
                     "reveal": {t: T(f"答对了。获得 <b>港口通行证</b> 和 1 箱外来香料（{SPICE_NAME[B_FOREIGN[t]]['zh']}）。",
                                     f"Correct. You get a <b>Port Pass</b> and 1 foreign crate ({SPICE_NAME[B_FOREIGN[t]]['en']}).") for t in TEAMS}},
            "rewards": {t: [[B_FOREIGN[t], 1], ["pass", 1]] for t in TEAMS},
            "hints": [T("把所有价格换成同一种货币。", "Convert every price to one currency."),
                      T("换成最小的雷亚尔最方便。", "The real, the smallest unit, is easiest."),
                      T("1 杜卡特 = 24 雷亚尔，1 克鲁扎多 = 12，1 弗罗林 = 4。", "1 ducat = 24 reales, 1 cruzado = 12, 1 florin = 4.")],
        },
        {
            "id": "B4a", "stage": "cross", "target": 8, "shared": True, "teams": [1, 2],
            "title": T("双锁宝箱 α", "Double-lock chest α"),
            "body": {1: T("<p>你手里是宝箱 α 的<b>事件卡</b>。年代图在雄鹰商行。</p>" + events_card(EV_ALPHA, "zh"),
                          "<p>You hold chest α's <b>event card</b>. The timeline is with the Eagle.</p>" + events_card(EV_ALPHA, "en")),
                     2: T("<p>你手里是宝箱 α 的<b>年代图</b>。事件卡在狮子商行。</p>" + TIMELINE["zh"],
                          "<p>You hold chest α's <b>timeline</b>. The event card is with the Lion.</p>" + TIMELINE["en"])},
            "gate": {"label": T("宝箱 α 的 3 位密码", "Chest α code"), "ph": "000", "answers": {0: "889"},
                     "reveal": {0: T("宝箱 α 打开：狮子和雄鹰各得 <b>1 箱藏红花</b>（万能香料）。", "Chest α opens: Lion and Eagle each get <b>1 saffron</b> (wildcard).")}},
            "rewards": {1: [["saffron", 1]], 2: [["saffron", 1]]},
            "hints": [T("你只有一半信息，去找另一家商行。", "You only have half. Find the other house."),
                      T("把事件和年代图上的图画一一对应。", "Match each event to a picture on the timeline."),
                      T("达伽马 = 1498。", "Da Gama = 1498.")],
        },
        {
            "id": "B4b", "stage": "cross", "target": 8, "shared": True, "teams": [3, 4],
            "title": T("双锁宝箱 β", "Double-lock chest β"),
            "body": {3: T("<p>你手里是宝箱 β 的<b>事件卡</b>。年代图在玫瑰商行。</p>" + events_card(EV_BETA, "zh"),
                          "<p>You hold chest β's <b>event card</b>. The timeline is with the Rose.</p>" + events_card(EV_BETA, "en")),
                     4: T("<p>你手里是宝箱 β 的<b>年代图</b>。事件卡在海豚商行。</p>" + TIMELINE["zh"],
                          "<p>You hold chest β's <b>timeline</b>. The event card is with the Dolphin.</p>" + TIMELINE["en"])},
            "gate": {"label": T("宝箱 β 的 3 位密码", "Chest β code"), "ph": "000", "answers": {0: "250"},
                     "reveal": {0: T("宝箱 β 打开：海豚和玫瑰各得 <b>1 箱藏红花</b>。", "Chest β opens: Dolphin and Rose each get <b>1 saffron</b>.")}},
            "rewards": {3: [["saffron", 1]], 4: [["saffron", 1]]},
            "hints": [T("你只有一半信息，去找另一家商行。", "You only have half. Find the other house."),
                      T("把事件和年代图上的图画一一对应。", "Match each event to a picture on the timeline."),
                      T("哥伦布 = 1492。", "Columbus = 1492.")],
        },
        {
            "id": "B5", "stage": "cross", "target": 8, "shared": True, "teams": [5, 2, 3],
            "title": T("海盗的藏身处", "The pirate hideout"),
            "body": {5: T("<p>你有海图：4×4 网格（列 A–D，行 1–4），岛屿在 <b>A2、B4、C1、C3、D2</b>。“海盗一定藏在岛上。”另外两条情报在雄鹰和海豚手里。</p>",
                          "<p>You hold the chart: a 4×4 grid (columns A–D, rows 1–4) with islands at <b>A2, B4, C1, C3, D2</b>. “Pirates always hide on an island.” Two more clues are with the Eagle and the Dolphin.</p>"),
                     2: T("<p>情报：“海盗不在 C 列，也不在 D 列。”海图在星辰商行。</p>", "<p>Intel: “The pirates are not in column C or D.” The chart is with the Star.</p>"),
                     3: T("<p>情报：“海盗藏身的行号大于 2。”海图在星辰商行。</p>", "<p>Intel: “The pirates' row number is greater than 2.” The chart is with the Star.</p>")},
            "gate": {"label": T("海盗所在格子（38 分钟前）", "Pirate square (before 38')"), "ph": "A1", "answers": {0: "B4"},
                     "reveal": {0: T("情报已报给交易所。海盗被皇家舰队击退，三家各得 <b>2 金币</b>。", "Reported to the Exchange. The Royal Navy drives the pirates off; each of the three houses gets <b>2 coins</b>.")}},
            "rewards": {5: [["coins", 2]], 2: [["coins", 2]], 3: [["coins", 2]]},
            "hints": [T("三条情报要合在一起。", "All three clues are needed together."),
                      T("先列出岛屿，再逐条排除。", "List the islands, then rule them out clue by clue."),
                      T("A、B 两列只有两个岛。", "Columns A and B hold only two islands.")],
        },
        {
            "id": "B7", "stage": "final", "target": 8, "shared": True,
            "title": T("国王的宴席", "The King's banquet"),
            "body": {0: T("<p>主持人宣布闭市并宣读诏书：“国王只接受一份配方。它被分成五段，写在五张商行配方卡的底部。”</p><p>看看你的配方卡底部（交易面板里）。</p>",
                          "<p>The host closes the market and reads the decree: “The King will accept one recipe only. It is split into five parts, written at the foot of the five house recipe cards.”</p><p>Look at the foot of your recipe card (in the trading panel).</p>")},
            "gate": {"label": T("皇家宝箱 5 位字母", "Royal chest, 5 letters"), "ph": "XXXXX", "answers": {0: "SPICE"},
                     "reveal": {0: T("<p class=\"letter\">“国王的宴席不属于任何一家商行，而属于所有远航归来的人。”</p><p>皇家特许状颁给五家商行。五位船长把香料一起送进御厨，主菜上桌。</p>",
                                     "<p class=\"letter\">“The King's feast belongs to no single house, but to all who sailed home.”</p><p>The royal charter goes to all five houses. The captains carry their spices to the kitchen together and the main course arrives.</p>")}},
            "hints": [T("五张卡底部的句段带着罗马数字。", "The five fragments carry Roman numerals."),
                      T("按 I–V 排好，句子就通了。", "Order them I–V and the sentence reads."),
                      T("印章字母也按 I–V 排。", "Order the seal letters I–V too.")],
        },
    ],
    "solution": T(
        "<h4>答案</h4><table><tr><th>商行</th><th>B1</th><th>B2 被改行</th><th>B3 港口</th><th>本土 / 外来</th><th>配方需要</th><th>底部句段 · 印章</th></tr>"
        + "".join(f"<tr><td>{t} {B_HOUSES[t]['zh']}</td><td>31524</td><td>{B_LEDGER_BAD[t]}</td><td>{B_PRICES[t][4]}</td><td>{SPICE_NAME[B_HOME[t]]['zh']} / {SPICE_NAME[B_FOREIGN[t]]['zh']}</td><td>{'、'.join(SPICE_NAME[s]['zh'] for s in B_RECIPE[t])}</td><td>{B_FOOT[t][0]} {B_FOOT[t][1]['zh']} · {B_FOOT[t][2]}</td></tr>" for t in TEAMS)
        + "</table><p>B4 α = <b>889</b>（1498、1488、1519）；β = <b>250</b>（1492、1405、1500）。B5 = <b>B4</b>。B7 = <b>SPICE</b>。</p>"
          "<p>供需：每种香料流通 3 箱、需求 4 家，缺口靠 4 箱藏红花和银行限售 3 箱补齐。</p>",
        "<h4>Answers</h4><table><tr><th>House</th><th>B1</th><th>B2 line</th><th>B3 port</th><th>Home / foreign</th><th>Recipe needs</th><th>Foot · seal</th></tr>"
        + "".join(f"<tr><td>{t} {B_HOUSES[t]['en']}</td><td>31524</td><td>{B_LEDGER_BAD[t]}</td><td>{B_PRICES[t][4]}</td><td>{SPICE_NAME[B_HOME[t]]['en']} / {SPICE_NAME[B_FOREIGN[t]]['en']}</td><td>{', '.join(SPICE_NAME[s]['en'] for s in B_RECIPE[t])}</td><td>{B_FOOT[t][0]} {B_FOOT[t][1]['en']} · {B_FOOT[t][2]}</td></tr>" for t in TEAMS)
        + "</table><p>B4 α = <b>889</b> (1498, 1488, 1519); β = <b>250</b> (1492, 1405, 1500). B5 = <b>B4</b>. B7 = <b>SPICE</b>.</p>"
          "<p>Supply: 3 crates of each spice circulate against 4 houses' demand; 4 saffron and the bank's 3 crates fill the gap.</p>"),
    "watch": T(["交易是否真的发生，还是有人囤货", "银行和事件是否给主持人带来太大负担", "反转（SPICE）时大家的反应", "有没有商行因为缺货完全卡死"],
               ["Whether trades actually happen or someone hoards", "Whether the bank and events overload the host", "How people react to the SPICE twist", "Whether any house is stuck for lack of goods"]),
    "recipes": {t: B_RECIPE[t] for t in TEAMS},
    "home": B_HOME, "foreign": B_FOREIGN,
    "foot": {t: {"num": B_FOOT[t][0], "text": B_FOOT[t][1], "seal": B_FOOT[t][2]} for t in TEAMS},
}

# ================================================================ GAME C
C_DEPTS = {1: T("领航组", "Navigators"), 2: T("制图组", "Cartographers"), 3: T("军需组", "Quartermasters"),
           4: T("船医组", "Surgeons"), 5: T("厨房组", "Galley")}
C_LETTER = {1: "T", 2: "A", 3: "B", 4: "L", 5: "E"}

BARRELS = T(
    "<div class=\"tw\"><table><tr><th>桶</th><th>清单</th><th>实测</th></tr>"
    "<tr><td>1</td><td>淡水 40 升</td><td>40 kg</td></tr><tr><td>2</td><td>饼干 20 包</td><td>10 kg</td></tr>"
    "<tr><td>3</td><td>腌肉 8 块</td><td>20 kg</td></tr><tr><td>4</td><td>葡萄酒 30 升</td><td>30 kg</td></tr>"
    "<tr><td>5</td><td>火药 12 包</td><td>18 kg</td></tr><tr><td>6</td><td>绳索 6 卷</td><td>18 kg</td></tr>"
    "<tr><td>7</td><td>大米 25 kg</td><td>37 kg</td></tr><tr><td>8</td><td>豆子 16 kg</td><td>16 kg</td></tr>"
    "<tr><td>9</td><td>盐 10 kg</td><td>10 kg</td></tr></table></div>"
    "<p class=\"note\">单位重量：淡水 1 kg/升 · 饼干 0.5 kg/包 · 腌肉 2.5 kg/块 · 葡萄酒 1 kg/升 · 火药 1.5 kg/包 · 绳索 3 kg/卷</p>",
    "<div class=\"tw\"><table><tr><th>Barrel</th><th>Manifest</th><th>Weighed</th></tr>"
    "<tr><td>1</td><td>Fresh water 40 L</td><td>40 kg</td></tr><tr><td>2</td><td>Biscuits 20 packs</td><td>10 kg</td></tr>"
    "<tr><td>3</td><td>Salt pork 8 pieces</td><td>20 kg</td></tr><tr><td>4</td><td>Wine 30 L</td><td>30 kg</td></tr>"
    "<tr><td>5</td><td>Gunpowder 12 bags</td><td>18 kg</td></tr><tr><td>6</td><td>Rope 6 coils</td><td>18 kg</td></tr>"
    "<tr><td>7</td><td>Rice 25 kg</td><td>37 kg</td></tr><tr><td>8</td><td>Beans 16 kg</td><td>16 kg</td></tr>"
    "<tr><td>9</td><td>Salt 10 kg</td><td>10 kg</td></tr></table></div>"
    "<p class=\"note\">Unit weights: water 1 kg/L · biscuits 0.5 kg/pack · salt pork 2.5 kg/piece · wine 1 kg/L · gunpowder 1.5 kg/bag · rope 3 kg/coil</p>")

DIARIES = T(
    "<div class=\"diary\"><p><b>水手长</b>：6 月 21 日。22:00 船长还在掌舵。22:30 我回舱睡觉。</p>"
    "<p><b>炮手</b>：23:00 船长来火药舱检查，十分钟就走了，说要去“找点吃的”。</p>"
    "<p><b>见习水手</b>：23:20 我在楼梯上和船长擦肩而过。他往下走，怀里抱着一个红色的盒子。</p>"
    "<p><b>领航员助手</b>：23:30 我在船尾值班，一个人都没看见。</p>"
    "<p><b>厨师</b>：（第 5 页全是餐具符号，看不懂）</p></div>",
    "<div class=\"diary\"><p><b>Boatswain:</b> 21 June. At 22:00 the Captain was still at the helm. At 22:30 I went below to sleep.</p>"
    "<p><b>Gunner:</b> At 23:00 the Captain checked the powder room, left after ten minutes, said he was going to “find something to eat”.</p>"
    "<p><b>Cabin boy:</b> At 23:20 I passed the Captain on the stairs. He was heading down, carrying a red box.</p>"
    "<p><b>Navigator's mate:</b> At 23:30 I was on watch at the stern. Saw no one.</p>"
    "<p><b>Cook:</b> (page 5 is all cutlery symbols, unreadable)</p></div>")

GALLEY_TABLE = T(
    "<div class=\"galleyitems\"><div><p class=\"eyebrow\">厨房日历 · 航海年鉴</p><p>3/21 赤纬 0° · 5/21 +20° · 6/21 +23° · 8/21 +12° · 9/21 0°</p></div>"
    "<div><p class=\"eyebrow\">餐具密码表</p><p class=\"cutlery\">🥄=E 🍴=C 🔪=H ☕=O 🍷=A 🧂=S 🍞=R 🫖=T 🍽️=N 🥢=I</p></div>"
    "<div><p class=\"eyebrow\">船长的秘制炖菜</p><p>面粉 21 克 · 黄油 33 克 · 盐 5 撮 · 鸡蛋 12 个 · 糖 50 勺</p></div></div>",
    "<div class=\"galleyitems\"><div><p class=\"eyebrow\">Kitchen calendar · almanac</p><p>21 Mar declination 0° · 21 May +20° · 21 Jun +23° · 21 Aug +12° · 21 Sep 0°</p></div>"
    "<div><p class=\"eyebrow\">Cutlery key</p><p class=\"cutlery\">🥄=E 🍴=C 🔪=H ☕=O 🍷=A 🧂=S 🍞=R 🫖=T 🍽️=N 🥢=I</p></div>"
    "<div><p class=\"eyebrow\">The Captain's secret stew</p><p>flour 21 g · butter 33 g · salt 5 pinches · eggs 12 · sugar 50 spoons</p></div></div>")

CAPTAIN_LETTER = T(
    "<p class=\"letter\">“致希望号的全体船员：没有哪场暴风雨能让我离开这艘船。我只是想看看，当船长不在的时候，你们能不能找到彼此。"
    "领航员读懂了天空，制图师读懂了大地，军需官守住了船舱，船医读懂了人心，厨师留住了家的味道。单靠任何一个部门，谁也到不了回声岛。"
    "最后一把锁，请按船上的岗位顺序打开：<b>掌舵、看图、清点、疗伤、开饭</b>。”</p><p>请当众念出这封信。每个部门都收到了一个小信封。</p>",
    "<p class=\"letter\">“To the whole crew of the Esperança: no storm could take me from this ship. I only wanted to see whether, with the Captain gone, "
    "you would find each other. The navigators read the sky, the cartographers the land, the quartermasters kept the hold, the surgeons read the heart, "
    "the cooks kept the taste of home. No single department could reach Echo Island alone. Open the last lock in the order of the watch: "
    "<b>steer, chart, count, heal, feed</b>.”</p><p>Read this letter aloud. Every department has received a small envelope.</p>")

GAME_C = {
    "id": "C",
    "name": T("最后一次航行", "The Last Voyage"),
    "mode": T("完全互相依赖", "Total interdependence"),
    "testMinutes": 40, "realMinutes": 50,
    "roles": C_DEPTS,
    "roleWord": T("部门", "Department"),
    "story": T(
        "远洋帆船“希望号”在一夜风暴后醒来：船长失踪，船偏离航线，淡水只够撑一小时。五个部门各自只掌握一部分线索。"
        "<b>船长留下一句话：“当你们找到彼此的时候，就会找到我。”</b>",
        "The Esperança wakes after a night of storms: the Captain is missing, the ship is off course, and there is an hour of water left. "
        "Each department holds only part of the picture. <b>The Captain left one line: “When you find each other, you will find me.”</b>"),
    "testNote": T(
        "这一局最考验依赖链：每个部门都要给出线索，也要等别人的线索。请留意你“干等”的时间，填反馈时会问到。",
        "This game is all about the dependency chain: every department gives and waits. Notice how long you spend just waiting; the feedback form asks."),
    "puzzles": [
        {
            "id": "C1a", "stage": "intra", "target": 6, "teams": [1],
            "title": T("时钟里的经度", "Longitude from a clock"),
            "body": {1: T("<p>母港位于 0° 经线，船上时钟保持母港时间。今天太阳升到最高点时，时钟显示 <b>16:00</b>。地球每小时自转 15°。</p><p>我们在母港以东还是以西？多少度？</p>",
                          "<p>Home port is on the 0° meridian; the ship's clock keeps home time. At local noon today the clock read <b>16:00</b>. The Earth turns 15° an hour.</p><p>Are we east or west of home, and by how much?</p>")},
            "gate": {"label": T("经度（格式：度数+E/W）", "Longitude (degrees + E/W)"), "ph": "45E", "answers": {1: "60W"},
                     "aliases": {"W60": "60W", "西经60": "60W", "60西": "60W"},
                     "reveal": {1: T("正确：<b>60°W</b>。纬度还缺数据，见下一题。", "Correct: <b>60°W</b>. Latitude still needs data; see the next card.")}},
            "hints": [T("太阳到头顶时，母港已经是下午了。", "When it is noon here, home is already in the afternoon."),
                      T("差几个小时就乘以 15°。", "Multiply the hour difference by 15°."),
                      T("16 − 12 = 4 小时，在母港以西。", "16 − 12 = 4 hours, west of home.")],
        },
        {
            "id": "C1b", "stage": "cross", "target": 8, "teams": [1], "requires": "C1a",
            "title": T("纬度", "Latitude"),
            "body": {1: T("<p>六分仪记录：“____ 日正午，太阳高度角 83°。”（日期被海水洇湿）</p><p>公式：纬度 = 90° − 太阳高度角 + 当日太阳赤纬。</p><p class=\"note\">日期和赤纬都不在你手上。</p>",
                          "<p>Sextant record: “Noon on ____: sun altitude 83°.” (the date is washed out)</p><p>Formula: latitude = 90° − sun altitude + the sun's declination that day.</p><p class=\"note\">Neither the date nor the declination is on your table.</p>")},
            "gate": {"label": T("纬度（格式：度数+N/S）", "Latitude (degrees + N/S)"), "ph": "10N", "answers": {1: "30N"},
                     "aliases": {"N30": "30N", "北纬30": "30N"},
                     "reveal": {1: T("坐标完整：<b>30°N 60°W</b>。交给制图组。", "Full position: <b>30°N 60°W</b>. Take it to the Cartographers.")}},
            "hints": [T("谁的日记里写着日期？", "Whose diaries carry dates?"),
                      T("哪种日历上会写太阳赤纬？", "What kind of calendar lists declination?"),
                      T("6 月 21 日，赤纬 +23°。", "21 June, declination +23°.")],
        },
        {
            "id": "C2a", "stage": "intra", "target": 8, "teams": [2], "jigsaw": True,
            "title": T("拼合海图", "Rebuild the chart"),
            "body": {2: T("<p>海图被撕成 6 块。依次点两块即可交换位置，经纬度刻度只印在边缘。</p><div data-jigsaw></div>",
                          "<p>The chart is torn into 6 pieces. Tap two pieces to swap them. Latitude and longitude labels are printed only on the edges.</p><div data-jigsaw></div>")},
            "hints": [T("先找带刻度的边缘块。", "Find the pieces with edge labels first."),
                      T("纬度从上到下递减，经度从左到右递减。", "Latitude falls top to bottom, longitude falls left to right."),
                      T("左上角是 50°N 90°W。", "The top-left corner is 50°N 90°W.")],
        },
        {
            "id": "C2b", "stage": "cross", "target": 6, "teams": [2], "requires": "C2a",
            "title": T("最短航线", "Shortest route"),
            "body": {2: T("<p>海图角落的说明：“船每次只能横向或纵向移动一格，不能进入礁石，必须走最短的航线。”</p><p>目的地坐标在领航组手里。</p>",
                          "<p>Note in the corner: “The ship moves one square at a time, horizontally or vertically, never into a reef, and must take the shortest route.”</p><p>The destination is with the Navigators.</p>")},
            "gate": {"label": T("航线（R/L/U/D 或 →←↑↓）", "Route (R/L/U/D or arrows)"), "ph": "RLUD", "answers": {2: "RRUU"}, "dir": True,
                     "reveal": {2: T("航线：<b>→ → ↑ ↑</b>。厨房组的红盒子需要它。", "Route: <b>→ → ↑ ↑</b>. The Galley's red box needs it.")}},
            "hints": [T("先确定回声岛的位置。", "Locate Echo Island first."),
                      T("先往北会撞礁。", "Going north first hits a reef."),
                      T("一共 2 格向东、2 格向北。", "Two squares east, two north.")],
        },
        {
            "id": "C3a", "stage": "intra", "target": 6, "teams": [3],
            "title": T("超重的木桶", "The overweight barrel"),
            "body": {3: T("<p>清点货舱时，有一个桶的重量不对劲。</p>" + BARRELS["zh"], "<p>One barrel in the hold weighs wrong.</p>" + BARRELS["en"])},
            "gate": {"label": T("桶号", "Barrel number"), "ph": "1–9", "answers": {3: "7"}, "numwords": True,
                     "reveal": {3: T("7 号信封里是一本挂着 <b>4 位字母锁</b>的密码本。其他信封里只有“就是普通的豆子”。", "Envelope 7 holds a codebook with a <b>4-letter lock</b>. The other envelopes say “Just beans. Really.”")}},
            "hints": [T("逐桶算出应有重量。", "Work out each barrel's expected weight."),
                      T("单位重量卡上没有大米，大米按 kg 计。", "Rice is listed by the kilo."),
                      T("比较 7、8、9 号桶。", "Compare barrels 7, 8 and 9.")],
        },
        {
            "id": "C3b", "stage": "cross", "target": 6, "teams": [3], "requires": "C3a",
            "title": T("密码本", "The codebook"),
            "body": {3: T("<p>密码本挂着 4 位字母锁。锁码不在你手上。</p>", "<p>The codebook has a 4-letter lock. The code is not on your table.</p>")},
            "gate": {"label": T("4 位字母", "4 letters"), "ph": "XXXX", "answers": {3: "ECHO"},
                     "reveal": {3: T("<p class=\"mono\">03 风暴 · 05 等于 · 09 船长 · 12 回声岛 · 17 厨房 · 21 红盒子 · 26 淡水 · 33 锁 · 41 星星 · 50 航线</p><p>哪个部门手里有一串奇怪的数字？</p>",
                                     "<p class=\"mono\">03 storm · 05 equals · 09 captain · 12 Echo Island · 17 galley · 21 red box · 26 fresh water · 33 lock · 41 star · 50 route</p><p>Which department is sitting on a list of odd numbers?</p>")}},
            "hints": [T("船医在调查船长最后说了什么。", "The Surgeons are investigating the Captain's last words."),
                      T("那个词写在厨师的日记里。", "The word is in the cook's diary."),
                      T("一个与“回声”有关的英文词。", "An English word meaning a repeated sound.")],
        },
        {
            "id": "C3c", "stage": "cross", "target": 5, "teams": [3, 5], "shared": True, "requires": "C3b",
            "title": T("解读炖菜食谱", "Decode the stew recipe"),
            "body": {3: T("<p>用密码本去解厨房组的食谱。</p>", "<p>Use the codebook on the Galley's recipe.</p>"),
                     5: T("<p>军需组拿到密码本后，和他们一起解你们的食谱。</p>", "<p>Once the Quartermasters open the codebook, decode your recipe together.</p>")},
            "gate": {"label": T("红盒子的锁 = 去哪个岛的航线？", "The red box lock = route to which island?"), "ph": T("岛名", "Island"),
                     "answers": {0: "ECHOISLAND"}, "aliases": {"回声岛": "ECHOISLAND", "ECHO": "ECHOISLAND"},
                     "reveal": {0: T("“红盒子的锁 = 去回声岛的航线”。找制图组要航线。", "“The red box's lock = the route to Echo Island.” Ask the Cartographers for the route.")}},
            "hints": [T("食谱的分量是数字代码。", "The recipe quantities are codes."),
                      T("21 33 05 12 50。", "21 33 05 12 50."),
                      T("红盒子 · 锁 · 等于 · 回声岛 · 航线。", "red box · lock · equals · Echo Island · route.")],
        },
        {
            "id": "C4a", "stage": "intra", "target": 7, "teams": [4],
            "title": T("船员日记", "The crew diaries"),
            "body": {4: DIARIES},
            "gate": {"label": T("船长最后去了哪里？", "Where did the Captain go last?"), "ph": T("地点", "Place"),
                     "answers": {4: "GALLEY"}, "aliases": {"厨房": "GALLEY", "KITCHEN": "GALLEY", "THEGALLEY": "GALLEY", "THEKITCHEN": "GALLEY"},
                     "reveal": {4: T("船长去了厨房。厨师的第 5 页全是餐具符号：<p class=\"cutlery big\">🥄🍴🔪☕</p>谁天天和餐具打交道？",
                                     "The Captain went to the galley. The cook's page 5 is all cutlery:<p class=\"cutlery big\">🥄🍴🔪☕</p>Who handles cutlery all day?")}},
            "hints": [T("按时间排序。", "Put the entries in time order."),
                      T("“找点吃的”+“往下走”。", "“Find something to eat” + “heading down”."),
                      T("吃的东西在哪里做？", "Where is food made?")],
        },
        {
            "id": "C4b", "stage": "cross", "target": 6, "teams": [4], "requires": "C4a",
            "title": T("第 5 页", "Page 5"),
            "body": {4: T("<p class=\"cutlery big\">🥄🍴🔪☕</p><p>你需要餐具密码表。</p>", "<p class=\"cutlery big\">🥄🍴🔪☕</p><p>You need the cutlery key.</p>")},
            "gate": {"label": T("船长低声说的词", "The word the Captain whispered"), "ph": "XXXX", "answers": {4: "ECHO"},
                     "reveal": {4: T("<b>ECHO</b>。把它交给军需组。日记里的日期（6 月 21 日）交给领航组。", "<b>ECHO</b>. Give it to the Quartermasters, and the diary date (21 June) to the Navigators.")}},
            "hints": [T("厨房组有一张对照表。", "The Galley has a key."),
                      T("一个符号对应一个字母。", "One symbol per letter."),
                      T("勺子是 E。", "The spoon is E.")],
        },
        {
            "id": "C5a", "stage": "intra", "target": 4, "teams": [5], "choice": ["salt", "sugar", "pepper", "anise", "cinnamon", "chili", "cumin", "sichuan"],
            "title": T("调料架后面", "Behind the spice rack"),
            "body": {5: T("<p>船长的字条：“我把最重要的东西，藏在了一个既不咸也不甜、来自东方、长着八个角的东西后面。”</p><div data-rack></div>"
                          "<p class=\"note\">你的桌上还摊着这些东西，别人可能会来要：</p>" + GALLEY_TABLE["zh"],
                          "<p>The Captain's note: “I hid what matters most behind something neither salty nor sweet, from the East, with eight points.”</p><div data-rack></div>"
                          "<p class=\"note\">Also lying on your table, in case anyone asks:</p>" + GALLEY_TABLE["en"])},
            "gate": {"answers": {5: "ANISE"},
                     "reveal": {5: T("八角罐后面是一个<b>红盒子</b>，挂着方向锁（上/下/左/右）。", "Behind the star anise jar: a <b>red box</b> with a direction lock (up/down/left/right).")}},
            "hints": [T("八个角。", "Eight points."),
                      T("来自中国南方的香料。", "A spice from southern China."),
                      T("八角。", "Star anise.")],
        },
        {
            "id": "C5b", "stage": "cross", "target": 8, "teams": [5], "requires": "C5a",
            "title": T("红盒子", "The red box"),
            "body": {5: T("<p>方向锁需要一串方向。</p>", "<p>The direction lock needs a sequence of directions.</p>")},
            "gate": {"label": T("方向（R/L/U/D 或 →←↑↓）", "Directions (R/L/U/D or arrows)"), "ph": "RLUD", "answers": {5: "RRUU"}, "dir": True,
                     "reveal": {5: CAPTAIN_LETTER}},
            "hints": [T("谁手里有海图？", "Who has the chart?"),
                      T("从希望号到回声岛的最短航线。", "The shortest route from the ship to Echo Island."),
                      T("先向东。", "East first.")],
        },
        {
            "id": "C6", "stage": "final", "target": 2, "from": "C5b", "envelope": True,
            "title": T("你的小信封", "Your envelope"),
            "body": {0: T("<p>红盒子打开后，信封会出现在这里。</p>", "<p>Your envelope appears here once the red box is open.</p>")},
            "gate": {"answers": {0: "RRUU"},
                     "reveal": {t: T(f"<p class=\"envelope\">信封上写着 <b>{C_DEPTS[t]['zh']}</b>，里面是一个字母：<span class=\"bigletter\">{C_LETTER[t]}</span></p>",
                                     f"<p class=\"envelope\">Addressed to the <b>{C_DEPTS[t]['en']}</b>. Inside, one letter: <span class=\"bigletter\">{C_LETTER[t]}</span></p>") for t in TEAMS}},
            "hints": [T("等厨房组打开红盒子。", "Wait for the Galley to open the red box."), T("", ""), T("", "")],
        },
        {
            "id": "C7", "stage": "final", "target": 6, "shared": True,
            "title": T("船长舱的宝箱", "The Captain's cabin chest"),
            "body": {0: T("<p>5 位字母锁。按信里的岗位顺序：掌舵、看图、清点、疗伤、开饭。</p>", "<p>A 5-letter lock. Follow the letter's order: steer, chart, count, heal, feed.</p>")},
            "gate": {"label": T("5 位字母", "5 letters"), "ph": "XXXXX", "answers": {0: "TABLE"},
                     "reveal": {0: T("<p class=\"letter\">“新大陆不在海图上，它就在这张餐桌上。开饭！”</p><p>“船长”从厨房门口走出来，宣布开饭。</p>",
                                     "<p class=\"letter\">“The New World is not on any chart. It is right here at this table. Dinner is served!”</p><p>The “Captain” walks out of the kitchen and opens dinner.</p>")}},
            "hints": [T("每个部门一个字母。", "One letter per department."),
                      T("掌舵 = 领航组。", "Steer = Navigators."),
                      T("领航、制图、军需、船医、厨房。", "Navigators, Cartographers, Quartermasters, Surgeons, Galley.")],
        },
    ],
    "solution": T(
        "<h4>答案与依赖链</h4><table><tr><th>部门</th><th>队内</th><th>要给出</th><th>要等待</th><th>信封</th></tr>"
        "<tr><td>1 领航组</td><td>C1a = 60W</td><td>30N 60W → 制图</td><td>日期 ← 船医；赤纬 +23° ← 厨房 → C1b = 30N</td><td>T</td></tr>"
        "<tr><td>2 制图组</td><td>C2a 拼图</td><td>RRUU → 厨房</td><td>坐标 ← 领航 → C2b = RRUU</td><td>A</td></tr>"
        "<tr><td>3 军需组</td><td>C3a = 7</td><td>解码 → 厨房</td><td>ECHO ← 船医 → C3b；C3c = 回声岛</td><td>B</td></tr>"
        "<tr><td>4 船医组</td><td>C4a = 厨房</td><td>ECHO → 军需；6/21 → 领航</td><td>餐具表 ← 厨房 → C4b = ECHO</td><td>L</td></tr>"
        "<tr><td>5 厨房组</td><td>C5a = 八角</td><td>赤纬 → 领航；餐具表 → 船医</td><td>航线 ← 制图 → C5b = RRUU</td><td>E</td></tr></table>"
        "<p>纬度 = 90 − 83 + 23 = 30。航线：从 (10°N, 80°W) 到 (30°N, 60°W)，先北撞 20°N 80°W 礁，先东一格再北撞 20°N 70°W 礁，唯一最短路线 →→↑↑。终局 <b>TABLE</b>。</p>",
        "<h4>Answers and chain</h4><table><tr><th>Dept.</th><th>Intra</th><th>Gives</th><th>Waits for</th><th>Envelope</th></tr>"
        "<tr><td>1 Navigators</td><td>C1a = 60W</td><td>30N 60W → Cartographers</td><td>date ← Surgeons; +23° ← Galley → C1b = 30N</td><td>T</td></tr>"
        "<tr><td>2 Cartographers</td><td>C2a jigsaw</td><td>RRUU → Galley</td><td>position ← Navigators → C2b = RRUU</td><td>A</td></tr>"
        "<tr><td>3 Quartermasters</td><td>C3a = 7</td><td>decoding → Galley</td><td>ECHO ← Surgeons → C3b; C3c = Echo Island</td><td>B</td></tr>"
        "<tr><td>4 Surgeons</td><td>C4a = galley</td><td>ECHO → QM; 21 June → Navigators</td><td>cutlery key ← Galley → C4b = ECHO</td><td>L</td></tr>"
        "<tr><td>5 Galley</td><td>C5a = star anise</td><td>declination → Navigators; key → Surgeons</td><td>route ← Cartographers → C5b = RRUU</td><td>E</td></tr></table>"
        "<p>Latitude = 90 − 83 + 23 = 30. Route from (10°N, 80°W) to (30°N, 60°W): north first hits the reef at 20°N 80°W; one east then north hits 20°N 70°W; the only shortest route is →→↑↑. Final: <b>TABLE</b>.</p>"),
    "watch": T(["依赖链有没有哪一环卡超过 5 分钟", "厨房组和船医组是否主动把东西给出去", "制图组拼图是否太简单", "终局念信时的气氛"],
               ["Whether any link in the chain stalls for more than 5 minutes", "Whether the Galley and Surgeons hand things over unprompted", "Whether the jigsaw is too easy", "The mood when the letter is read"]),
}

GAMES = [GAME_A, GAME_B, GAME_C]
HOST_PASSWORD = "CX26"
