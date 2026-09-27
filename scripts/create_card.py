from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "downloads"
OUT.mkdir(parents=True, exist_ok=True)
URL = "https://los-guajiros.vercel.app/"
W, H = 1134, 661
GREEN, CREAM, RED, INK = "#173d2a", "#fff6e4", "#c94a3d", "#203229"
DISPLAY = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BODY = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BODY_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(image, size, focus_y=.5):
    image = image.convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    x = max(0, (image.width - size[0]) // 2)
    overflow_y = max(0, image.height - size[1])
    y = round(overflow_y * focus_y)
    return image.crop((x, y, x + size[0], y + size[1]))


def contain(image, box):
    image = image.convert("RGBA")
    scale = min(box[0] / image.width, box[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


def paste_center(base, image, center_x, top):
    base.alpha_composite(image, (round(center_x - image.width / 2), top))


# Frente: marca y promesa, sin dirección ni URL impresa.
facade = cover(Image.open(ROOT / "public/brand/fachada-hero-dia.webp"), (W, H), .46)
front = facade.filter(ImageFilter.GaussianBlur(.15)).convert("RGBA")
front = Image.alpha_composite(front, Image.new("RGBA", (W, H), (13, 45, 29, 150)))
gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(gradient)
for y in range(H):
    gd.line((0, y, W, y), fill=(8, 28, 18, int(42 + 105 * (y / H))))
front = Image.alpha_composite(front, gradient)
logo = contain(Image.open(ROOT / "public/brand/logo-los-guajiros-v2.png"), (610, 305))
paste_center(front, logo, W / 2, 62)
d = ImageDraw.Draw(front)
slogan = "Tu antojo vive aquí"
sb = d.textbbox((0, 0), slogan, font=font(DISPLAY, 52))
d.text(((W - (sb[2] - sb[0])) / 2, 392), slogan, font=font(DISPLAY, 52), fill=CREAM)
d.rounded_rectangle((332, 492, 802, 574), radius=41, fill=RED)
cta = "ESCANEA · ELIGE · PIDE"
cb = d.textbbox((0, 0), cta, font=font(BODY_BOLD, 24))
d.text(((W - (cb[2] - cb[0])) / 2, 517), cta, font=font(BODY_BOLD, 24), fill="white")
front.convert("RGB").save(OUT / "tarjeta-los-guajiros-frente.png", quality=96, dpi=(300, 300))

# Se reutiliza el QR vectorial ya auditado para no rasterizar ni alterar módulos.
qr_image = Image.open(OUT / "qr-los-guajiros.png").convert("RGB")

# Reverso: una sola acción. Sin dirección ni URL que ensucien la jerarquía.
back = Image.new("RGBA", (W, H), CREAM)
d = ImageDraw.Draw(back)
d.rectangle((0, 0, 26, H), fill=RED)
d.rounded_rectangle((70, 73, 562, H - 73), radius=34, fill="white", outline="#eadfcf", width=3)
qr_fit = qr_image.resize((430, 430), Image.Resampling.NEAREST)
back.alpha_composite(qr_fit.convert("RGBA"), (101, 115))
compact_logo = contain(Image.open(ROOT / "public/brand/logo-los-guajiros-v2.png"), (390, 195))
paste_center(back, compact_logo, 837, 62)
for index, line in enumerate(("LO RICO DE CASA,", "A UN ESCANEO.")):
    d.text((635, 282 + index * 61), line, font=font(DISPLAY, 39), fill=GREEN)
d.line((635, 420, 1055, 420), fill=RED, width=7)
d.text((635, 458), "Mira lo disponible y pide", font=font(BODY_BOLD, 24), fill=INK)
d.text((635, 494), "directamente por WhatsApp.", font=font(BODY, 23), fill=INK)
d.rounded_rectangle((635, 552, 1055, 606), radius=27, fill=GREEN)
hours = "TODOS LOS DÍAS · 9 A. M. — 9 P. M."
hb = d.textbbox((0, 0), hours, font=font(BODY_BOLD, 15))
d.text((845 - (hb[2] - hb[0]) / 2, 570), hours, font=font(BODY_BOLD, 15), fill=CREAM)
back.convert("RGB").save(OUT / "tarjeta-los-guajiros-reverso.png", quality=96, dpi=(300, 300))

# Vista previa de ambas caras para compartir por WhatsApp.
mock = Image.new("RGB", (1500, 1120), GREEN).convert("RGBA")
front_preview = front.convert("RGB").resize((910, 531), Image.Resampling.LANCZOS).convert("RGBA")
back_preview = back.convert("RGB").resize((910, 531), Image.Resampling.LANCZOS).convert("RGBA")
shadow = Image.new("RGBA", mock.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle((108, 83, 1038, 634), radius=24, fill=(0, 0, 0, 95))
sd.rounded_rectangle((462, 514, 1392, 1065), radius=24, fill=(0, 0, 0, 95))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
mock = Image.alpha_composite(mock, shadow)
mock.alpha_composite(front_preview, (88, 62))
mock.alpha_composite(back_preview, (442, 493))
mock.convert("RGB").save(OUT / "tarjeta-los-guajiros-mockup.png", quality=94)

# PDF listo para imprenta: frente y reverso, 96 x 56 mm con sangre.
pdf = OUT / "tarjeta-los-guajiros-imprenta.pdf"
c = canvas.Canvas(str(pdf), pagesize=(96 * mm, 56 * mm))
temporary = []
for index, image_path in enumerate((OUT / "tarjeta-los-guajiros-frente.png", OUT / "tarjeta-los-guajiros-reverso.png")):
    jpeg = OUT / f".print-{index}.jpg"
    Image.open(image_path).convert("RGB").save(jpeg, quality=96, subsampling=0, dpi=(300, 300))
    temporary.append(jpeg)
    c.drawImage(ImageReader(str(jpeg)), 0, 0, width=96 * mm, height=56 * mm)
    c.showPage()
c.save()
for image in temporary:
    image.unlink(missing_ok=True)

print(URL)
