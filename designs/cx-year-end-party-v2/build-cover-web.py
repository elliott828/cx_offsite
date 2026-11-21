"""Convert Codex's cover layer pack (assets/cover) into web-weight WebP files (assets/cover-web).

Re-run whenever Codex updates assets/cover. Never writes into assets/cover.
"""
import json
from pathlib import Path
from PIL import Image, ImageFilter

root = Path(__file__).parent
src = root / "assets" / "cover"
out = root / "assets" / "cover-web"
out.mkdir(exist_ok=True)

# name -> (max width, quality)
jobs = {
    "base": (1055, 80),
    "statue": (510, 85),
    "halo": (520, 85),
    "plate-invited": (365, 88),
    "title": (1010, 88),
    "plate-together": (605, 88),
    "ship": (350, 85),
    "waves": (345, 85),
    "cupid-body": (375, 85),
    "cupid-wing": (165, 88),
    "globe-frame": (310, 88),
    "globe-map": (1024, 82),
}

total = 0
for name, (max_w, q) in jobs.items():
    im = Image.open(src / f"{name}.png")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    if name in ("base", "globe-map"):
        im = im.convert("RGB")
    if name == "base":
        # soften the hard seam where the reference plate meets the bottom extension (y = 401 + 1491)
        seam, half = 1892, 30
        band = im.crop((0, seam - half, im.width, seam + half))
        soft = band.filter(ImageFilter.GaussianBlur(6))
        mask = Image.new("L", band.size)
        mask.putdata([round(255 * max(0, 1 - abs(y - half) / half)) for y in range(band.height) for _ in range(band.width)])
        im.paste(Image.composite(soft, band, mask), (0, seam - half))
        # patch left over above the invited-plate crown (lighter strip + gold tip, x≈535–625, y≈399–417):
        # rebuild it by blending the clean velvet rows just above and below, feathered at the sides
        x0, x1, y0, y1, f = 520, 640, 397, 419, 14
        px = im.load()
        for x in range(x0, x1):
            edge = min(x - x0, x1 - 1 - x)
            a = min(1, edge / f)
            top, bot = px[x, y0], px[x, y1]
            for y in range(y0 + 1, y1):
                t = (y - y0) / (y1 - y0)
                fill = tuple(round(top[c] * (1 - t) + bot[c] * t) for c in range(3))
                old = px[x, y]
                px[x, y] = tuple(round(old[c] * (1 - a) + fill[c] * a) for c in range(3))
    dest = out / f"{name}.webp"
    im.save(dest, "WEBP", quality=q, method=6)
    total += dest.stat().st_size
    print(f"{dest.name:22} {im.size}  {dest.stat().st_size // 1024} KB")

(out / "layers.json").write_text((src / "layers.json").read_text(encoding="utf-8"), encoding="utf-8")
print(f"total {total // 1024} KB")
