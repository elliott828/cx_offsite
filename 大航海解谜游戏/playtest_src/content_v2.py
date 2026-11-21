# -*- coding: utf-8 -*-
"""Playtest content for Option A v2 (The Five Fragments, rebuilt).

Four ships = the four Houses. Tester N plays ship N. Plain fields are shown in
the page; `reveal`, answers and `solution` are encrypted by build_v2.py.
"""
from content import T, key_caesar, key_a1z26, key_morse, key_atbash, BARRELS

TEAMS = [1, 2, 3, 4]
SHIPS = {1: T("海豚号 Dolphin", "Dolphin"), 2: T("玫瑰号 Rose", "Rose"),
         3: T("星辰号 Star", "Star"), 4: T("雄鹰号 Eagle", "Eagle")}
COLORS = {1: "#14284b", 2: "#6b1831", 3: "#b8a36e", 4: "#8a6a3c"}
PLAYERS = {1: 4, 2: 5, 3: 5, 4: 5}
HINT_TOKENS = {1: 3, 2: 2, 3: 2, 4: 2}

FLAGS = {1: "SIX", 2: "ONE", 3: "NINE", 4: "TWO"}
DIG1 = {1: "6", 2: "1", 3: "9", 4: "2"}
TURNS = {
    1: T("右转 90° → 右转 45° → 左转 180°", "Right 90° → Right 45° → Left 180°"),
    2: T("左转 45° → 左转 90° → 右转 45°", "Left 45° → Left 90° → Right 45°"),
    3: T("右转 135° → 左转 45° → 右转 90°", "Right 135° → Left 45° → Right 90°"),
    4: T("右转 180° → 左转 45° → 左转 90°", "Right 180° → Left 45° → Left 90°"),
}
DIG3 = {1: "8", 2: "7", 3: "5", 4: "2"}
CODE = {t: DIG1[t] + "3" + DIG3[t] + "7" for t in TEAMS}  # 6387 1377 9357 2327

PORTS = ["L", "C", "G", "M"]
PORT_NAME = {"L": T("里斯本 Lisbon", "Lisbon"), "C": T("好望角 Cape", "Cape of Good Hope"),
             "G": T("果阿 Goa", "Goa"), "M": T("马六甲 Malacca", "Malacca")}
PORT_LETTER = {"L": "F", "C": "L", "G": "O", "M": "R"}
HOME = {1: "L", 2: "C", 3: "G", 4: "M"}
HOME_ANS = {1: "LISBON", 2: "CAPE", 3: "GOA", 4: "MALACCA"}
ENC = {1: "OLVERQ", 2: "3 · 1 · 16 · 5", 3: "--. / --- / .-", 4: "NZOZXXZ"}
HALF = {1: T("跟着香料的味道", "Follow the scent of spice"), 2: T("穿过风暴之角", "through the Cape of Storms"),
        3: T("越过季风之海", "across the monsoon sea"), 4: T("走过狭窄的海峡", "past the narrow strait")}
# chest of team t holds the key card for fragment KEYFOR[t]
KEYFOR = {1: 4, 2: 1, 3: 2, 4: 3}
KEYHOLDER = {v: k for k, v in KEYFOR.items()}  # fragment -> team holding its key
KEYFN = {1: key_caesar, 2: key_a1z26, 3: key_morse, 4: key_atbash}

PORT_CHALLENGE = {
    "L": T("<b>出海歌</b>：全船齐声喊出口号，再唱或念四句出海歌：<i>Heave away, my ____ crew, / Lisbon fades in morning blue, / Spice and gold beyond the sea, / Pull together — one, two, three!</i><br>完成 2 金币；全员参与且气势足 3 金币。",
           "<b>Shanty send-off</b>: shout your chant, then sing or chant: <i>Heave away, my ____ crew, / Lisbon fades in morning blue, / Spice and gold beyond the sea, / Pull together — one, two, three!</i><br>Done: 2 · everyone in, real gusto: 3."),
    "C": T("<b>绕过风暴角</b>：照图卡打 8 字结，每人一根绳，限时 90 秒。半数以上打成 2 金币；全员打成 3 金币。",
           "<b>Round the Cape</b>: everyone ties a figure-eight knot from the picture card in 90 seconds. Half or more: 2 · everyone: 3."),
    "G": T("<b>香料市场</b>：闻 3 个小罐（黑胡椒、肉桂、丁香），说出各是什么。只闻不尝。对 2 个 2 金币；全对 3 金币。",
           "<b>Spice market</b>: sniff three jars (black pepper, cinnamon, clove) and name each. Smell only. Two right: 2 · all three: 3."),
    "M": T("<b>海峡过路费</b>：港务长念 5 道判断题，答对 4 道放行，没过的话等 1 分钟再答。4 对 2 金币；5 对 3 金币。",
           "<b>The strait toll</b>: the Port Master reads five true/false questions; 4 right to pass, or wait a minute and retry. Four right: 2 · five: 3."),
}
MALACCA_Q = T(
    "<ol><li>麦哲伦本人完成了环球航行。<b>错</b></li><li>肉豆蔻曾经只产在班达群岛。<b>对</b></li><li>哥伦布以为自己到了亚洲。<b>对</b></li>"
    "<li>马六甲海峡连接印度洋和南中国海。<b>对</b></li><li>大航海时代的船靠卫星定位。<b>错</b></li></ol>",
    "<ol><li>Magellan himself completed the voyage around the world. <b>False</b></li><li>Nutmeg once grew only in the Banda Islands. <b>True</b></li>"
    "<li>Columbus believed he had reached Asia. <b>True</b></li><li>The Strait of Malacca links the Indian Ocean and the South China Sea. <b>True</b></li>"
    "<li>Age of Discovery ships navigated by satellite. <b>False</b></li></ol>")

QUIZ = [
    (T("麦哲伦因为风平浪静，给哪个大洋取了名字？", "Which ocean did Magellan name for its calm waters?"), T("太平洋", "Pacific")),
    (T("达伽马从葡萄牙航行到了哪个国家？", "Vasco da Gama sailed from Portugal to which country?"), T("印度", "India")),
    (T("哥伦布的三艘船：Niña、Pinta 和……？", "Columbus's three ships: Niña, Pinta and…?"), T("Santa María", "Santa María")),
    (T("好望角在哪个大洲的南端？", "The Cape of Good Hope is at the tip of which continent?"), T("非洲", "Africa")),
    (T("哪种香料被称为“黑色黄金”？", "Which spice was called “black gold”?"), T("黑胡椒", "Pepper")),
    (T("水手的坏血病是缺哪种维生素？", "Scurvy comes from a lack of which vitamin?"), T("维生素 C", "Vitamin C")),
    (T("郑和下西洋是哪个朝代？", "Zheng He sailed for which Chinese dynasty?"), T("明朝", "Ming")),
    (T("测量太阳高度角、用来定纬度的仪器叫什么？", "What instrument measures the sun's angle to find latitude?"), T("六分仪（星盘、象限仪也算对）", "Sextant (astrolabe or quadrant also accepted)")),
]

BOTTLES = [
    (T("我有脸有两只手却没有手臂；没有我，水手算不出经度。", "I have a face and two hands but no arms; without me, sailors can't find longitude."),
     "CLOCK", ["CHRONOMETER", "钟", "航海钟", "时钟", "ACLOCK"]),
    (T("你拿走得越多，留下得也越多。", "The more you take, the more you leave behind."), "FOOTSTEPS", ["FOOTSTEP", "脚印", "足迹", "STEPS"]),
    (T("我有一只眼睛却看不见，每个补帆的水手都要用我。", "I have an eye but cannot see; every sail-mender needs me."), "NEEDLE", ["针", "ANEEDLE"]),
    (T("浑身是洞，却能装水。", "Full of holes, yet I hold water."), "SPONGE", ["海绵", "ASPONGE"]),
    (T("麦哲伦的船队五艘出发，最后有几艘回到西班牙？", "Magellan's fleet left with five ships. How many made it back to Spain?"), "1", ["ONE", "一", "1艘", "一艘"]),
    (T("荷兰人据说为了一个小岛上的哪种香料，把曼哈顿让给了英国？", "For which spice's island did the Dutch reportedly give Manhattan to the English?"), "NUTMEG", ["肉豆蔻"]),
]

# star chart: 9x9 grid; the union of the four sheets draws a capital A
STAR_SHEETS = {
    1: {"stars": [[4, 0], [1, 6], [6, 4]], "decoy": [[8, 0]]},
    2: {"stars": [[3, 2], [0, 8], [7, 6]], "decoy": [[0, 1]]},
    3: {"stars": [[2, 4], [5, 2], [4, 4]], "decoy": [[8, 3]]},
    4: {"stars": [[8, 8], [3, 4], [5, 4]], "decoy": [[0, 4]]},
}


def chest_reveal(t, lang):
    fo = KEYFOR[t]
    ship_other = SHIPS[fo][lang]
    if lang == "zh":
        return (f'<div class="chestgrid"><div class="fragment"><p class="eyebrow">残图 · {SHIPS[t]["zh"]}</p>'
                f'<p class="encport">{ENC[t]}</p><p class="halfline">“{HALF[t]["zh"]} ……”</p>'
                f'<p class="note">这是你们母港的名字，被加密了。钥匙不在你们船上。</p></div>'
                f'<div class="keycard"><p class="eyebrow">钥匙卡 · 背面写着：{ship_other}</p>{KEYFN[fo]("zh")}</div></div>'
                f'<p>箱底还有：<b>2 枚金币</b>，以及一张看不懂的<b>“夜航星图”透明片</b>（先收好）。</p>'
                f'<p class="note">信使规则：钥匙卡只能给对方看，不能截图转发。</p>')
    return (f'<div class="chestgrid"><div class="fragment"><p class="eyebrow">Fragment · {SHIPS[t]["en"]}</p>'
            f'<p class="encport">{ENC[t]}</p><p class="halfline">“{HALF[t]["en"]} …”</p>'
            f'<p class="note">This is your home port, encrypted. Its key is not on your ship.</p></div>'
            f'<div class="keycard"><p class="eyebrow">Key card · back reads: {ship_other}</p>{KEYFN[fo]("en")}</div></div>'
            f'<p>Also in the chest: <b>2 doubloons</b> and a puzzling <b>“night chart” transparency</b> (keep it for later).</p>'
            f'<p class="note">Messenger rule: show key cards in person; no screenshots.</p>')


PUZZLES = [
    {"id": "A0", "stage": "intra", "target": 3, "kind": "chant",
     "title": T("集结口号", "Muster chant"),
     "body": {0: T("<p>给你们的船编一句 4–8 个字的口号，写在下面。到里斯本港和暴风雨抢答前都要当众喊出来。</p>",
                   "<p>Write a short rallying cry for your ship. You'll shout it at Lisbon and before the storm quiz.</p>")}},
    {"id": "A1", "stage": "intra", "target": 6, "title": T("信号旗", "Signal flags"),
     "body": {t: T(f'<p>桅杆上挂着一串旗。对照信号旗表，拼出锁的第 1 位数字。</p><div class="flagrow" data-flags="{FLAGS[t]}"></div>'
                   '<details class="chart"><summary>国际信号旗对照表</summary><div data-flagchart></div></details>',
                   f'<p>A string of flags flies from the mast. Use the chart to spell digit 1 of the lock.</p><div class="flagrow" data-flags="{FLAGS[t]}"></div>'
                   '<details class="chart"><summary>International signal flag chart</summary><div data-flagchart></div></details>') for t in TEAMS},
     "gate": {"label": T("锁的第 1 位", "Digit 1"), "ph": "0–9", "answers": DIG1, "numwords": True,
              "reveal": {t: T(f"正确，第 1 位是 <b>{DIG1[t]}</b>。", f"Correct. Digit 1 is <b>{DIG1[t]}</b>.") for t in TEAMS}},
     "hints": [T("每面旗代表一个字母。", "Each flag is one letter."), T("拼出来是一个英文单词。", "They spell an English word."), T("这个单词是一个数字。", "The word is a number.")]},
    {"id": "A2", "stage": "intra", "target": 8, "title": T("船员名册", "Crew roster"),
     "body": {0: T("<p>1–4 号铺住着 Pedro、Juan、Diego、Luis，职位是领航员、厨师、木匠、炮手（每人一个）。</p><ol class=\"clues\">"
                   "<li>领航员睡在 1 号铺。</li><li>厨师的铺号正好比 Juan 大 1。</li><li>Luis 睡在最后一个铺位。</li>"
                   "<li>Diego 既不是木匠，也不是厨师。</li><li>炮手和木匠的铺位不相邻。</li></ol><p><b>厨师睡几号铺？这是第 2 位。</b></p>",
                   "<p>Pedro, Juan, Diego and Luis sleep in bunks 1–4 as navigator, cook, carpenter and gunner (one each).</p><ol class=\"clues\">"
                   "<li>The navigator sleeps in bunk 1.</li><li>The cook's bunk is exactly one higher than Juan's.</li><li>Luis sleeps in the last bunk.</li>"
                   "<li>Diego is neither the carpenter nor the cook.</li><li>The gunner and the carpenter are not in adjacent bunks.</li></ol><p><b>Which bunk is the cook in? That's digit 2.</b></p>")},
     "gate": {"label": T("锁的第 2 位", "Digit 2"), "ph": "1–4", "answers": {0: "3"}, "numwords": True,
              "reveal": {0: T("正确，第 2 位是 <b>3</b>。", "Correct. Digit 2 is <b>3</b>.")}},
     "hints": [T("画一张 4×4 表格。", "Draw a 4×4 grid."), T("从第 3 条和第 1 条入手，再讨论 Diego。", "Start with clues 3 and 1, then test Diego."), T("Diego 是领航员。", "Diego is the navigator.")]},
    {"id": "A3", "stage": "intra", "target": 5, "title": T("罗盘转向", "Compass turns"),
     "body": {t: T(f'<p>罗盘：北=1 东北=2 东=3 东南=4 南=5 西南=6 西=7 西北=8。船头朝北出发，日志写着：</p><p class="logline">{TURNS[t]["zh"]}</p><p>最终朝向的数字是第 3 位。</p>',
                   f'<p>Compass: N=1 NE=2 E=3 SE=4 S=5 SW=6 W=7 NW=8. The bow starts north; the log reads:</p><p class="logline">{TURNS[t]["en"]}</p><p>The final heading’s digit is digit 3.</p>') for t in TEAMS},
     "gate": {"label": T("锁的第 3 位", "Digit 3"), "ph": "1–8", "answers": DIG3, "numwords": True,
              "reveal": {t: T(f"正确，第 3 位是 <b>{DIG3[t]}</b>。", f"Correct. Digit 3 is <b>{DIG3[t]}</b>.") for t in TEAMS}},
     "hints": [T("站起来真的转一转。", "Stand up and turn."), T("右转是顺时针，45° 是一格。", "Right is clockwise; 45° is one step."), T("把每一步的朝向写下来。", "Write down each heading.")]},
    {"id": "A4", "stage": "intra", "target": 5, "title": T("超重的木桶", "The overweight barrel"),
     "body": {0: T("<p>清点货舱时，有一个桶的重量不对劲。它的桶号是第 4 位。</p>" + BARRELS["zh"],
                   "<p>One barrel in the hold weighs wrong. Its number is digit 4.</p>" + BARRELS["en"])},
     "gate": {"label": T("锁的第 4 位（桶号）", "Digit 4 (barrel no.)"), "ph": "1–9", "answers": {0: "7"}, "numwords": True,
              "reveal": {0: T("正确，第 4 位是 <b>7</b>。", "Correct. Digit 4 is <b>7</b>.")}},
     "hints": [T("逐桶算出应有重量。", "Work out each barrel's expected weight."), T("大米按 kg 计。", "Rice is listed by the kilo."), T("比较 7、8、9 号桶。", "Compare barrels 7, 8 and 9.")]},
    {"id": "A-chest", "stage": "intra", "target": 1, "title": T("打开船长箱", "Open the captain's chest"),
     "body": {0: T("<p>4 位数字锁，顺序 A1 → A2 → A3 → A4。越早打开，名次奖越高。</p>", "<p>A 4-digit lock, order A1 → A2 → A3 → A4. The earlier you open it, the bigger the placement bonus.</p>")},
     "gate": {"label": T("4 位密码", "4-digit code"), "ph": "0000", "answers": CODE,
              "reveal": {t: T(chest_reveal(t, "zh"), chest_reveal(t, "en")) for t in TEAMS}},
     "hints": [T("按 A1–A4 的顺序连起来。", "Join A1–A4 in order."), T("四道题都要先解。", "Solve all four first."), T("检查 A3 的每一次转向。", "Re-check each turn in A3.")]},
    {"id": "B1", "stage": "cross", "target": 6, "requires": "A-chest", "title": T("解出母港", "Decode your home port"),
     "body": {0: T("<p>去找持有你们钥匙卡的那艘船，请他们给你看钥匙。解出母港后，到那个港口报出港名才能进港。解出后，帮你的那艘船也得 2 金币。</p>",
                   "<p>Find the ship holding your key card and ask to see it. Then go to that port and name it to enter. The ship that helped you also earns 2 doubloons.</p>")},
     "gate": {"label": T("母港名", "Home port"), "ph": T("港口名", "Port"), "answers": HOME_ANS,
              "aliases": {"里斯本": "LISBON", "好望角": "CAPE", "CAPEOFGOODHOPE": "CAPE", "果阿": "GOA", "马六甲": "MALACCA"},
              "reveal": {t: T(f"母港是 <b>{PORT_NAME[HOME[t]]['zh']}</b>。去那个港口开始巡航。", f"Your home port is <b>{PORT_NAME[HOME[t]]['en']}</b>. Start your circuit there.") for t in TEAMS}},
     "hints": [T("钥匙卡背面写着船名。", "The key card names a ship on its back."), T("凯撒往回数 3 位；埃特巴什是 A↔Z 对折。", "Caesar: shift back 3. Atbash: A↔Z."), T("四个港口都在里斯本到香料群岛的航线上。", "All four ports lie on the Lisbon–Spice Islands route.")]},
    {"id": "PORTS", "stage": "cross", "target": 12, "kind": "ports", "requires": "B1",
     "title": T("港口巡航", "The port circuit"),
     "body": {0: T("<p>从母港出发，按航线顺序走完四个港口。每过一个港口，港务长会在航行证上盖章（就是下面的字母）。</p>",
                   "<p>Start at your home port and visit all four in route order. Each Port Master stamps your pass (the letters below).</p>")}},
    {"id": "C1", "stage": "fleet", "target": 5, "kind": "quiz", "title": T("暴风雨抢答", "Storm quiz"),
     "body": {0: T("<p>全体回到中央。主持人念题，第一个举手答对的船得 1 金币；答错一次这题就不能再答。</p>",
                   "<p>Everyone back to the centre. First ship to raise a hand and answer right earns 1 doubloon; a wrong answer locks you out of that question.</p>")}},
    {"id": "C2", "stage": "fleet", "target": 5, "kind": "stars", "requires": "A-chest", "shared": True,
     "title": T("星图叠合", "Star-chart overlay"),
     "body": {0: T("<p>“乌云散了，但只有四张夜航星图合在一起，才看得见方向。”把你们的星图放上桌，四条船都放好才看得清。</p>",
                   "<p>“The clouds have parted, but only all four night charts together show the way.” Place your chart on the table; the picture appears once all four ships have placed theirs.</p>")},
     "gate": {"label": T("星空给的第五枚印章", "The fifth seal from the stars"), "ph": "?", "answers": {0: "A"},
              "reveal": {0: T("第五枚印章：<b>A</b>。", "The fifth seal: <b>A</b>.")}},
     "hints": [T("四条船都要放。", "All four ships must place their charts."), T("把星星连起来。", "Connect the stars."), T("一个大写字母。", "A capital letter.")]},
    {"id": "D1", "stage": "final", "target": 6, "shared": True, "title": T("最终宝箱", "The final chest"),
     "body": {0: T("<p>“按航线顺序盖上四个港口的印章，再加上星空给的第五枚。”航线：Lisbon → Cape → Goa → Malacca。任何一条船都可以提交，开箱的船得 2 金币；52 分钟内开箱，每条船再得 3 金币。</p>",
                   "<p>“Stamp the four ports' seals in the order of the voyage, then add the fifth the stars gave you.” Route: Lisbon → Cape → Goa → Malacca. Any ship may submit; the opener earns 2 doubloons, and if it opens within 52 minutes every ship earns 3.</p>")},
     "gate": {"label": T("5 位字母", "5 letters"), "ph": "XXXXX", "answers": {0: "FLORA"},
              "reveal": {0: T("<p class=\"letter\">“我把地图撕成四片，因为只有四艘船一起，才到得了这里。香料群岛不在海图上，它在四楼。今晚的盛宴在 Flora，属于整支船队。”</p><p>全体起航，去 4 楼 Flora。</p>",
                              "<p class=\"letter\">“I tore the chart into four because only four ships together could reach this place. The Spice Islands aren't on any chart. They're on the fourth floor. Tonight's feast is at Flora, and it belongs to the whole fleet.”</p><p>All hands: set sail for Flora on 4F.</p>")}},
     "hints": [T("四个港口的章上各有一个字母。", "Each port stamp carries a letter."), T("按 Lisbon → Cape → Goa → Malacca 排。", "Order them Lisbon → Cape → Goa → Malacca."), T("最后加上星图的字母。", "Add the star chart's letter last.")]},
]

SOLUTION = T(
    "<h4>船长箱与港口</h4><table><tr><th>船</th><th>A1</th><th>A2</th><th>A3</th><th>A4</th><th>密码</th><th>母港（密文 → 明文）</th><th>持有谁的钥匙</th><th>巡航顺序</th></tr>"
    + "".join(f"<tr><td>{SHIPS[t]['zh']}</td><td>{FLAGS[t]}={DIG1[t]}</td><td>3</td><td>{DIG3[t]}</td><td>7</td><td><b>{CODE[t]}</b></td><td>{ENC[t]} → {HOME_ANS[t]}</td><td>{SHIPS[KEYFOR[t]]['zh']}</td><td>{' → '.join(PORTS[(PORTS.index(HOME[t]) + k) % 4] for k in range(4))}</td></tr>" for t in TEAMS)
    + "</table><h4>港口章</h4><p>Lisbon F · Cape L · Goa O · Malacca R；星图 A；终局 <b>FLORA</b>。</p><h4>马六甲判断题</h4>" + MALACCA_Q["zh"]
    + "<h4>暴风雨抢答</h4><ol>" + "".join(f"<li>{q['zh']} <b>{a['zh']}</b></li>" for q, a in QUIZ) + "</ol>"
    + "<h4>漂流瓶</h4><ol>" + "".join(f"<li>{q['zh']} <b>{a}</b></li>" for q, a, _ in BOTTLES) + "</ol>",
    "<h4>Chests and ports</h4><table><tr><th>Ship</th><th>A1</th><th>A2</th><th>A3</th><th>A4</th><th>Code</th><th>Home port (cipher → plain)</th><th>Holds key for</th><th>Circuit</th></tr>"
    + "".join(f"<tr><td>{SHIPS[t]['en']}</td><td>{FLAGS[t]}={DIG1[t]}</td><td>3</td><td>{DIG3[t]}</td><td>7</td><td><b>{CODE[t]}</b></td><td>{ENC[t]} → {HOME_ANS[t]}</td><td>{SHIPS[KEYFOR[t]]['en']}</td><td>{' → '.join(PORTS[(PORTS.index(HOME[t]) + k) % 4] for k in range(4))}</td></tr>" for t in TEAMS)
    + "</table><h4>Port stamps</h4><p>Lisbon F · Cape L · Goa O · Malacca R; star chart A; final <b>FLORA</b>.</p><h4>Malacca true/false</h4>" + MALACCA_Q["en"]
    + "<h4>Storm quiz</h4><ol>" + "".join(f"<li>{q['en']} <b>{a['en']}</b></li>" for q, a in QUIZ) + "</ol>"
    + "<h4>Bottles</h4><ol>" + "".join(f"<li>{q['en']} <b>{a}</b></li>" for q, a, _ in BOTTLES) + "</ol>")

PROTOCOL = {
    "schedule": T(
        "<div class=\"tw\"><table><tr><th>时间</th><th>内容</th><th>主持人</th></tr>"
        "<tr><td>0:00–0:10</td><td>说明测试目的；4 位测试员各自打开页面，选 1–4 号船</td><td>确认右上角显示“已同步”；准备港口道具</td></tr>"
        "<tr><td>0:10–1:10</td><td><b>完整跑一遍 60 分钟</b></td><td>点“开始”；16′ 放第一批漂流瓶，26′ 广播抓壮丁，30′ 放第二批，34′ 广播暴风雨并开抢答</td></tr>"
        "<tr><td>1:10–1:20</td><td>每人填反馈</td><td>点“结束”</td></tr>"
        "<tr><td>1:20–1:40</td><td>看结果、公开答案、复盘</td><td>重点讨论港口巡航用时和金币是否平衡</td></tr></table></div>",
        "<div class=\"tw\"><table><tr><th>Time</th><th>What</th><th>Host</th></tr>"
        "<tr><td>0:00–0:10</td><td>Explain the goal; the 4 testers open the page and pick ships 1–4</td><td>Check the bar says “Synced”; set out port props</td></tr>"
        "<tr><td>0:10–1:10</td><td><b>One full 60-minute run</b></td><td>Press Start; 16′ release bottles wave 1, 26′ press gang, 30′ wave 2, 34′ storm + quiz</td></tr>"
        "<tr><td>1:10–1:20</td><td>Everyone fills in feedback</td><td>Press End</td></tr>"
        "<tr><td>1:20–1:40</td><td>Review results, reveal answers, debrief</td><td>Focus on the port circuit timing and doubloon balance</td></tr></table></div>"),
    "prep": T(
        "<ul><li>每位测试员代表一整条船。正式活动是 4–5 人一船，所以第一幕的用时会偏长。</li>"
        "<li>港口挑战要真人主持：主持人或其他组织者扮港务长，在“港务长”面板里给分盖章。需要绳子、3 个香料罐、出海歌卡。</li>"
        "<li>抢答由主持人念题、在面板里记谁答对；题目会同时显示在测试员屏幕上。</li>"
        "<li>星图叠合在页面里完成：四条船都点“放上桌”后，图案会自动出现。</li>"
        "<li>跨船信息必须走过去当面说，不许截图转发。</li></ul>",
        "<ul><li>Each tester stands in for a whole ship. Real ships have 4–5 people, so Act 1 will run long.</li>"
        "<li>Port challenges need a live Port Master: the host or another organizer runs them and scores in the Port Masters panel. Bring rope, 3 spice jars and the shanty card.</li>"
        "<li>The host reads the storm quiz and records winners in the panel; questions also appear on testers' screens.</li>"
        "<li>The star-chart overlay happens in the page: once all four ships place their charts, the picture appears.</li>"
        "<li>Cross-ship information is carried in person; no screenshots.</li></ul>"),
    "watch": T(["港口巡航是否排队、每港实际用时", "抓壮丁后被换走的人是否还有参与感", "漂流瓶是否让快的船有事做", "金币是否让 4 人船也有机会赢", "终局时四条船是否都在场"],
               ["Whether ports queue, and real time per port", "Whether pressed sailors stay engaged on their new ship", "Whether bottles keep fast ships busy", "Whether doubloons give the 4-person ship a real chance", "Whether all four ships are present at the finale"]),
}

EVENTS = {
    "press": T("抓壮丁！每条船立刻派一名水手去下一条船，直到游戏结束：海豚 → 玫瑰 → 星辰 → 雄鹰 → 海豚。",
               "Press gang! Each ship sends one sailor to the next ship for the rest of the game: Dolphin → Rose → Star → Eagle → Dolphin."),
    "storm": T("暴风雨来了！全体回到中央，每条船先喊一次口号，抢答马上开始。",
               "A storm! Everyone back to the centre. Each ship shouts its chant, then the quiz begins."),
    "wave1": T("第一批漂流瓶已经冲上岸（1–3 号）。", "Bottles 1–3 have washed ashore."),
    "wave2": T("第二批漂流瓶已经冲上岸（4–6 号）。", "Bottles 4–6 have washed ashore."),
    "stars": T("乌云散了。把你们的夜航星图放上桌。", "The clouds have parted. Place your night charts on the table."),
}
