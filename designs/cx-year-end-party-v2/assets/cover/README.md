# Cover layer package

Canvas: **1055 × 2293**, with the original 1055 × 1491 reference at **y = 401**. Coordinates in `layers.json` are 1x canvas coordinates.

## Production notes

- `base.png`: original reference retained outside the removal masks. Removed regions are filled from the imagegen clean-background edit. The invited-plate patch extends below the former crown. The top extension uses a 120px clean-background smoothstep seam; the bottom uses the generated velvet/satin continuation directly so books are not mirrored or vertically smeared. The information-panel dot is replaced with feathered cream-paper texture.
- `cupid-body.png`: cropped from original reference pixels with hand-authored polygon, spatial and color masks to exclude the original wing, gold-frame fragment, velvet and cloud fragments.
- `cupid-wing.png`: reference-guided complete feathered wing extraction with a reconstructed wing root for animation.
- `ship.png`, `waves.png`: reference-guided transparent extractions, used because the original subjects overlap clouds, engraving paper and each other too heavily for a clean animated edge.
- `statue.png`: taken from the clean edit, then polygon and emerald-color masked so the right facial/neck contour is transparent outside the sculpture and cannot block the rotating halo.
- `plate-invited.png`, `plate-together.png`, `globe-frame.png`: reference-guided transparent extractions generated to eliminate visible background chunks during animation.
- `title.png`: reference-guided transparent extraction preserving the exact wording, two-line composition, inset star and hot-pink underline without the cloud/dress contamination produced by color-key extraction.
- `halo.png`: newly generated transparent 360-degree gilded sunburst, normalized to 800 × 800.
- `globe-map.png`: newly generated antique equirectangular texture, normalized to 2048 × 1024; the outer 64px were mirrored/averaged so left and right edges match.
- `@2x` files: Lanczos/high-quality bicubic output from the final 1x files.
- QA: `_composite.png` is rebuilt from `base.png` plus the manifest layers; `_diff.png` compares y=401..1891 against the source reference; `_layers-preview.png` shows isolated transparency; `_halo-check.png` rotates the halo 15 degrees under the statue.

## QA result

Mean absolute RGB difference: **37.761 / 255** per channel.

## Known limitations

- No callable Python interpreter was available, so the required deterministic pixel operations and QA were performed with Windows System.Drawing instead of Python/Pillow.
- Built-in image editing cannot accept the task's exact mask geometry. The clean background was generated once, then inserted only through deterministic masks; this preserves all untouched reference pixels but leaves some generated texture under moving layers.
- The Cupid body retains reference pixels, while the completed wing and globe frame are reference-guided reconstructions; their hidden geometry is approximate rather than a full 3D reconstruction.
- The top/bottom extensions are reference-guided material outpaints. Their far edges intentionally avoid focal objects; the 120px smoothstep feather may still soften tiny edge details.
