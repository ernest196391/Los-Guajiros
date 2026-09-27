from pathlib import Path
import re
import vtracer

root = Path(__file__).resolve().parents[1]
source = root.parent / "generated_images" / "exec-b5035d4b-4bf3-4882-8699-b848d6454017.png"
target = root / "public" / "brand" / "logo-los-guajiros-v2-trazado.svg"

vtracer.convert_image_to_svg_py(
    str(source),
    str(target),
    colormode="color",
    hierarchical="stacked",
    mode="spline",
    filter_speckle=64,
    color_precision=7,
    layer_difference=24,
    corner_threshold=60,
    length_threshold=4.0,
    max_iterations=12,
    splice_threshold=45,
    path_precision=3,
)

svg = target.read_text(encoding="utf-8")
svg = svg.replace('width="1774" height="887"', 'viewBox="40 65 1715 785" preserveAspectRatio="xMidYMid meet"')
target.write_text(svg, encoding="utf-8")

colors = re.compile(r'fill="#[0-9A-Fa-f]{6}"')
mono = colors.sub('fill="#073b2b"', svg)
white = colors.sub('fill="#fff7e5"', svg)
(target.parent / "logo-los-guajiros-v2-monocromo-trazado.svg").write_text(mono, encoding="utf-8")
(target.parent / "logo-los-guajiros-v2-blanco-trazado.svg").write_text(white, encoding="utf-8")

print(target)
