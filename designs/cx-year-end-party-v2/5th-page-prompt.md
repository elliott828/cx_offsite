# Codex prompt — page 5 background: four ships setting sail

Paste everything inside the fence into Codex. Let Codex write only the files listed under **Output**. Claude converts the image into the web version and wires it into the page.

```
TASK
Create the background artwork for the last page of the "Age of Discovery" CX Year End Party web invitation:
FOUR baroque galleons setting sail from a grand harbour at golden hour. The page says "See you on deck".

STYLE — must match the cover (reference: designs/cx-year-end-party-v2/assets/visual-reference.png and assets/cover-web/base.webp)
- Bright baroque collage: hand-painted 17th-century oil-painting textures combined with torn-paper cut-out edges, like the cover's layered paper scraps.
- Shared palette and motifs with the cover:
  - candy-pink and peach cumulus clouds with a pink-violet twilight sky and small four-point gold sparkles
  - emerald-green crushed velvet drapery
  - polished gold baroque scrollwork
  - pearl strands
  - pink peonies
  - antique sepia map fragments
  - a blue-and-white engraving scrap (like the cover's Neptune engraving)
- The ships and sea should look painted in the same way as the cover's galleon and teal crashing waves (assets/cover-web/ship.webp, waves.webp).

COMPOSITION (portrait 1080 × 2340, the page is shown cropped to the phone's aspect, so keep key content inside the central 1080 × 1900)
- Top 0–8%: sky only, with a little velvet drape in one corner. A white title sits here.
- 8–52%: THE HERO ZONE. Four galleons sailing out of the harbour towards the viewer-right, staggered in depth:
  one large in front, one medium, and two smaller further back. All sails are full and pennants fly.
  Each ship is identified by its House colours on its sails, pennants and hull trim:
    1. House of the Dolphin — navy hull, powder-blue sails, silver trim; small leaping-dolphin emblem on the main sail.
    2. House of the Rose — burgundy hull, blush-pink sails, antique-gold trim; small rose emblem on the main sail.
    3. House of the Star — ivory hull, champagne sails, pearl-grey trim; small eight-point compass-star emblem.
    4. House of the Eagle — emerald hull, teal sails, gold trim; small spread-wing eagle emblem.
  Emblems are simple painted shapes only: no letters.
- Harbour on the left edge: a baroque stone quay with a lighthouse or a domed tower, gold lanterns, and confetti or rose petals drifting over the water. It should read as a send-off celebration.
- 52–100%: calmer water that darkens towards the bottom into deep teal and emerald, blending into emerald velvet and torn map paper at the very bottom. A cream information card will cover roughly 55–95% of the height, so keep that area low-detail. Nothing important should go there.
- Light: warm golden-hour glow behind the ships, with a soft lens bloom and sparkles on the water.

DO NOT
- Do not put any text, letters, numbers, logos or watermarks in the image.
- Do not add people's faces.
- Do not leave hard horizontal seams; this is a single continuous painting.
- Do not use dark or moody horror lighting; keep it bright and celebratory like the cover.

OUTPUT (write only these files)
- designs/cx-year-end-party-v2/assets/finale-harbour.png  (1080 × 2340, RGB)
- designs/cx-year-end-party-v2/assets/_finale-preview.jpg  (any size: a quick look at the full image)
```

## After Codex finishes
Claude runs `python -I build-web-extras.py`, which creates `assets/finale-harbour.web.jpg`. The page already points to that file, and until it exists the page shows a pink-to-teal gradient.
