"""Make web-weight WebP copies of the house crests and award artwork.

Re-run after replacing assets/houses/logo-*.png or assets/award-*.png. Sources are never modified.
"""
from pathlib import Path
from PIL import Image

root = Path(__file__).parent / "assets"
jobs = [(p, p.with_suffix(".webp"), 320) for p in sorted((root / "houses").glob("logo-*.png"))]
jobs += [(p, root / p.name.replace(".png", ".webp"), 520) for p in sorted(root.glob("award-*.png")) if ".web." not in p.name]

total = 0
for src, dest, box in jobs:
    im = Image.open(src).convert("RGBA")
    # trim near-transparent margins (some sources carry faint alpha haze) so crests size consistently
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 32 else 0).getbbox())
    im.thumbnail((box, box), Image.LANCZOS)
    im.save(dest, "WEBP", quality=86, method=6)
    total += dest.stat().st_size
    print(f"{dest.relative_to(root)!s:34} {im.size}  {dest.stat().st_size // 1024} KB")

# page 5 background (Codex, see 5th-page-prompt.md) — optional until it exists
finale = root / "finale-harbour.png"
if finale.exists():
    im = Image.open(finale).convert("RGB")
    im.thumbnail((900, 1950), Image.LANCZOS)
    dest = root / "finale-harbour.web.jpg"
    im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    total += dest.stat().st_size
    print(f"{dest.name:34} {im.size}  {dest.stat().st_size // 1024} KB")
print(f"total {total // 1024} KB")
