# 任务：CX Year End Party 封面分层素材包

## 0. 背景与边界

- 这是一张网页邀请函的封面。封面要**严格按照参考图布局**，只把其中几个元素拆成独立图层，由网页做动画。
- 参考图：`assets/visual-reference.png`（1055×1491，以下简称 REF）。所有坐标都是 REF 像素坐标（左上角为原点）。
- 你只负责产出图片素材 + 清单文件。**不要修改 `index.html`、`dist/` 或任何其他已有文件**；所有输出放到新目录 `assets/cover/`。
- 风格基调：明快巴洛克拼贴——祖母绿丝绒、粉色云和牡丹、金色巴洛克框、大理石雕像、复古航海图。新生成的任何像素都必须和 REF 的笔触、光线、颗粒、饱和度一致，看不出拼接。
- 关键原则：**图层与底版逐像素对齐**。图层先从 REF 原像素切出来，只有被遮挡、需要补全的部分才用生图修补。静止或只做小幅动画的图层，抠图边缘只需在“动起来会露出背后”的那一侧精确；另一侧可以放宽，因为它下面就是一模一样的底版像素。

## 1. 画布：上下扩展到 0.46 比例

手机全屏约为 9:19.5。把 REF 上下各扩展 401px，得到 **1055×2293** 的 1x 画布，REF 原图贴在 y=401 处（下文称 CANVAS 坐标 = REF 坐标 + (0, 401)）。

- 顶部扩展区：从 REF 顶边自然延伸——左侧粉色牡丹和雕像发顶上方的粉云、中间祖母绿丝绒褶皱、右侧古地图纸张（带撕边）。不要出现新的主体物件，只是“画面往外多拍了一截”。
- 底部扩展区：从 REF 底边延伸——左下海神版画纸张的撕边下沿、中间粉色丝绒和祖母绿丝绒、右下牡丹和古书堆底部、散落珍珠。同样不要新增主体。
- 网页在宽屏上会裁掉扩展区的一部分，所以扩展区里离原图越远越“只是材质”，不要放重要细节。
- 生图工具一次出不了这么大时，分别生成顶部和底部两条（各带与 REF 重叠约 120px 的上下文），再用 Python 做 40–60px 羽化拼接。

扩展区参考 prompt（按工具需要调整）：

```
Outpaint this baroque collage poster upward/downward. Continue exactly the existing materials at the edge:
deep emerald green crushed velvet with soft folds, pastel pink clouds, pink peonies, aged sepia antique map paper
with torn white paper edges, scattered pearls. Same lighting, saturation, paper grain and painterly collage style.
No text, no new focal objects, no people, no frames. Seamless continuation of the edge.
```

## 2. 干净底版 `base.png`（1055×2293，不透明）

在扩展后的画布上，把下列区域**擦除并补画背景**（补出来的应该是该处本来会被挡住的丝绒 / 粉云 / 花 / 纸张 / 雕像衣褶等）：

| 擦除对象                             | REF 大致范围 (x1,y1,x2,y2)   | 补画内容                                                       |
| -------------------------------- | ------------------------ | ---------------------------------------------------------- |
| YOU'RE INVITED 金框牌子（含王冠）         | 415,25,728,278           | 祖母绿丝绒，左侧接雕像光芒外的丝绒                                          |
| 雕像背后的金色光芒                        | 190,0,430,300（只擦光芒，不擦雕像） | 丝绒 / 粉云                                                    |
| AGE OF DISCOVERY 字、中间八角星、粉色笔刷下划线 | 0,330,1010,795           | 字后面本来的东西：雕像粉色衣褶、左侧粉花和红色云、中右祖母绿丝绒、右侧粉云                      |
| Discover Together 金框牌子           | 250,675,815,1015         | 粉色云 + 少量丝绒                                                 |
| 帆船                               | 0,785,315,1100           | 粉云天空，下方接海                                                  |
| 海浪                               | 0,1075,295,1205          | 深海青绿色平静海面（波浪图层会盖在上面）                                       |
| 丘比特（含翅膀、号角、蓝飘带）                  | 700,600,1055,905         | 粉色云                                                        |
| 信息栏里的文字                          | 410,1050,730,1230        | **只擦 “DATE: [INSERT DATE]” 等三行文字**，保留左侧三个图标、金色分隔线、底部花饰和米色底 |

保留不动：雕像本体、粉色牡丹、右上古地图 + 罗盘星 + 蓝色胶带、左下海神版画、蓝色邮票、地球仪（第 3 节单独处理球面）、古书、珍珠、所有手绘涂鸦和小星星。

修补 prompt（每个区域用遮罩单独做）：

```
Inpaint only the masked area. Fill it with the background that would naturally be behind the removed object:
[emerald velvet folds | pastel pink clouds | pink satin drapery | calm teal sea]. Match surrounding lighting,
texture, grain and baroque collage style exactly. No text, no frames, no new objects.
```

## 3. 图层（透明 PNG）

除特别说明外，都从 REF 原像素抠出，用 AI 去背景（如 rembg / SAM）后人工修边，保留柔和的 1–2px 抗锯齿边缘和原有投影。

| 文件                   | 内容                                                                                | 网页动画               | 抠图要求                                               |
| -------------------- | --------------------------------------------------------------------------------- | ------------------ | -------------------------------------------------- |
| `plate-invited.png`  | YOU'RE INVITED 金框 + 王冠 + 文字                                                       | 第一个弹出              | 金框外轮廓精确，包含框下投影                                     |
| `title.png`          | AGE OF DISCOVERY 全部字母 + 中间八角星 + 粉色笔刷下划线                                           | 第二个弹出              | 米白字母边缘精确（可用色键提取米白 #f2e6d2 附近 + 人工修），去掉背后所有背景       |
| `plate-together.png` | Discover Together 金框 + 手写字 + 框内米色底                                                | 第三个弹出              | 金框外轮廓精确                                            |
| `halo.png`           | **新生成**：一圈完整的金色放射光芒（参考雕像背后那种细长尖刺光，金色带高光），正方形 800×800，圆心在图正中，四周透明                  | 缓慢旋转 + 呼吸光         | 完整 360°，不能缺口；光芒内圈留空约 30% 半径                        |
| `statue.png`         | 雕像头部、头发、珍珠、脖子、粉色衣褶上半                                                              | 静止（盖在光环上）          | **只有头顶到右侧脸、下巴、脖子这一侧轮廓需要精确**（光芒从这里露出）；左侧和下方可以带背景一起切 |
| `ship.png`           | 帆船（含帆、船身），不含海浪                                                                    | 上下起伏 + ±2° 摇摆      | 全轮廓精确；被海浪挡住的船底部分补画出来，往下多补 30px                     |
| `waves.png`          | 船下方那片海浪 + 白色浪花                                                                    | 左右涌动 + 轻微缩放        | 两侧边缘做柔和渐隐                                          |
| `cupid-body.png`     | 丘比特身体、头、号角、蓝飘带，**不含翅膀**                                                           | 整体轻轻漂浮             | 全轮廓精确；被翅膀挡住的背部补画出来                                 |
| `cupid-wing.png`     | 丘比特翅膀，**补画成一只完整的翅膀**（包括被身体挡住的翅根）                                                  | 以翅根为轴扇动            | 全轮廓精确；在清单里给出翅根枢轴点坐标                                |
| `globe-frame.png`    | 地球仪的铜环、子午圈、支架、底座——**去掉球面本身**，但保留从球面前方穿过的那段铜环                                      | 静止                 | 球面所在的圆形区域透明                                        |
| `globe-map.png`      | **新生成**：复古古地图贴图，等距圆柱投影，**左右无缝可平铺**，2048×1024；配色贴近 REF 球面（羊皮纸米黄陆地、淡青绿海洋、褐色海岸线和经纬线） | 网页里在圆形遮罩里横向滚动，模拟自转 | 左右边缘必须无缝                                           |

`globe-map.png` prompt：

```
Seamless equirectangular antique world map texture, 2:1, tileable left-right with no seam.
Aged parchment cream continents, soft pale teal-green oceans, sepia coastlines, faint latitude/longitude grid,
light foxing and paper grain, 17th-century cartography style. No text labels, no compass rose, no border, flat lighting
(no sphere shading).
```

`halo.png` prompt：

```
A full 360-degree baroque golden sunburst halo, many long thin sharp gilded rays of alternating length radiating from
an empty center, metallic gold with warm highlights, painterly collage style matching a baroque poster. Transparent
background, centered, perfectly circular, no figure, no text.
```

## 4. 清单 `assets/cover/layers.json`

记录每个图层在 **1x CANVAS 坐标**（已含 +401 偏移）里的位置，网页靠它摆放：

```json
{
  "canvas": { "w": 1055, "h": 2293, "refOffsetY": 401 },
  "layers": [
    { "id": "title", "file": "title.png", "x": 0, "y": 731, "w": 1010, "h": 465 },
    { "id": "cupid-wing", "file": "cupid-wing.png", "x": 0, "y": 0, "w": 0, "h": 0, "pivot": [0, 0] },
    { "id": "globe-frame", "file": "globe-frame.png", "x": 0, "y": 0, "w": 0, "h": 0,
      "sphere": { "cx": 0, "cy": 0, "r": 0 } },
    { "id": "halo", "file": "halo.png", "center": [0, 0], "displaySize": 0 }
  ]
}
```

- 图层 PNG 裁到内容的最小外接框，x/y 是外接框左上角。
- `pivot` 是翅根枢轴点（CANVAS 坐标）；`sphere` 是地球仪球面圆心和半径；`halo` 给出光芒在画布上的圆心和显示直径（对准 REF 中雕像背后光芒的中心，约在 REF (300,110) 附近，请实测）。

## 5. 分辨率

全部做完后，把 `base.png` 和每个图层再输出一份 **2x** 版本（文件名加 `@2x`），优先用 AI 超分（Real-ESRGAN 等），没有的话用 Lanczos。`layers.json` 始终用 1x 坐标。

## 6. 自检（必须做）

1. 用 Python 按 `layers.json` 把所有图层叠回 `base.png`，输出 `assets/cover/_composite.png`。halo 用旋转角 0，globe-map 贴进球面圆形遮罩。
2. 把 `_composite.png` 中 y=401..1892 的部分和 REF 做逐像素差，输出 `_diff.png` 和平均差值。目标：除了光环和球面贴图，其他地方肉眼看不出差别。
3. 输出 `_layers-preview.png`：每个图层单独放在棋盘格背景上排成一张图，方便检查透明边缘。
4. 在 `assets/cover/README.md` 里写明：每个文件怎么做的（原像素抠图 / 修补 / 新生成）、哪些地方你觉得还不完美。
