# 四个 House Logo · Midjourney Prompts

## 用法
- **统一风格**：把封面参考图 `assets/visual-reference.png` 上传到 Midjourney，复制它的图片链接，替换每条 prompt 里的 `<REF_URL>`，作为 `--sref` 风格参考。`--sw 120` 控制参考强度：想更像封面就调高（最高 1000），觉得被参考图带偏了就调低。
- **背景**：Midjourney 不能直接出透明底，所以统一要求纯米白底 `#FAF3E8`。出图后用 remove.bg 或 rembg 去底，保存成透明 PNG：正方形、至少 1024px、标志主体占画面约 85%。
- **文件名**：放进 `assets/houses/`，命名为 `logo-dolphin.png`、`logo-rose.png`、`logo-star.png`、`logo-eagle.png`。我会把它们接到第 3 页的 logo 占位上。
- **外形**：每个 house 给了一条主 prompt 和一条变体。外形不要求规整，可以是不对称的卷草、飘带、半截框，只要在手机上缩到约 64px 还能一眼认出主体。
- 每条 prompt 末尾都已带好下面这段统一参数，直接复制整条使用即可：

```
--ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

---

## House of the Dolphin · Navy / Powder Blue / Silver

**主 prompt**
```
baroque heraldic emblem of a leaping dolphin curling around a swirling silver acanthus scroll, asymmetric rococo cartouche shape, sea foam and pearl drops splashing off the tail, deep navy blue enamel and powder blue enamel with polished silver gilding, hand-painted 17th century ornament mixed with modern sticker-like collage edge, crisp clean silhouette that reads at small size, centered isolated on a plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

**变体：更像徽章**
```
ornate baroque crest featuring a stylized dolphin diving through a silver wave crest, small compass star above, ribbon banner below with no lettering, navy, powder blue and silver palette, engraved metal and glossy enamel, playful bright baroque collage style, bold readable silhouette, isolated on plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

---

## House of the Rose · Burgundy / Blush / Antique Gold

**主 prompt**
```
baroque heraldic emblem of a single full-bloom rose with layered blush pink petals and deep burgundy heart, wrapped by an asymmetric antique gold rococo scroll and a fluttering burgundy satin ribbon, a few pearls, hand-painted 17th century ornament with modern fashion-editorial polish, crisp clean silhouette that reads at small size, centered isolated on a plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

**变体：玫瑰 + 王冠**
```
baroque monogram-style emblem without letters: a burgundy rose crowned by a small antique gold crown, thorned stem curling into a gold acanthus flourish, blush pink enamel accents, glossy gilt and velvet texture, bright playful baroque collage style, bold readable silhouette, isolated on plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

---

## House of the Star · Ivory / Champagne / Pearl Grey

**主 prompt**
```
baroque heraldic emblem of an eight-pointed navigator's compass star with long and short rays, set inside an asymmetric open rococo frame of champagne gold scrolls, ivory enamel and pearl grey silver details, a strand of pearls looping through, tiny sparkles, hand-painted 17th century ornament with modern minimal elegance, crisp clean silhouette that reads at small size, centered isolated on a plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

**变体：星辰 + 星盘**
```
baroque celestial emblem: a radiant star rising out of a small brass armillary sphere, champagne gold rays, ivory and pearl grey enamel, delicate filigree, soft shimmering highlights, bright playful baroque collage style, bold readable silhouette, isolated on plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

> Star 这一组配色很浅，去底后放在米色卡片上容易看不清。如果出现这个问题，在 prompt 里加 `with a thin deep emerald outline`。

---

## House of the Eagle · Emerald / Teal / Gold

**主 prompt**
```
baroque heraldic emblem of an eagle with spread wings rising from an asymmetric gold rococo scroll, wing feathers in emerald green and teal enamel edged with polished gold, a small gold crown and laurel sprig, dynamic upward pose, hand-painted 17th century ornament with modern bold graphic clarity, crisp clean silhouette that reads at small size, centered isolated on a plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

**变体：鹰首侧面**
```
baroque crest featuring a proud eagle head in profile emerging from a swirl of gold acanthus leaves and a teal satin ribbon, emerald and teal enamel, gilded beak and feathers, a compass star in the corner, bright playful baroque collage style, bold readable silhouette, isolated on plain flat cream background #FAF3E8 --ar 1:1 --v 7 --style raw --stylize 250 --sref <REF_URL> --sw 120 --no text, letters, words, watermark, signature, photo background, scenery
```

---

## 让四个 logo 看起来是一套
- 四个都定下来后，挑出最满意的一张，把它的链接加进其余三条的 `--sref`，并放在封面参考图链接后面，例如 `--sref <REF_URL> <ROSE_URL>`。这样线条粗细和镀金质感会更统一。
- 主体大小尽量一致；去底后我会在页面里统一缩放，并加上同样的投影。
