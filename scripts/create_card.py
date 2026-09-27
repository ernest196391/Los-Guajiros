from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public'/'downloads'; OUT.mkdir(parents=True,exist_ok=True)
URL='https://los-guajiros.vercel.app/'
W,H=1134,661  # 90x50 mm + 3 mm bleed, 300 dpi
SAFE=70
green='#173d2a'; cream='#fff5df'; red='#c94a3d'; gold='#f1d39a'; ink='#203229'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(path,size): return ImageFont.truetype(path,size)
def cover(im,size):
    im=im.convert('RGB'); s=max(size[0]/im.width,size[1]/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
    x=(im.width-size[0])//2; y=(im.height-size[1])//2
    return im.crop((x,y,x+size[0],y+size[1]))
def hat(draw,x,y,s=1):
    draw.ellipse((x,y+62*s,x+190*s,y+112*s),fill=gold,outline=ink,width=max(3,int(7*s)))
    draw.polygon([(x+48*s,y+76*s),(x+67*s,y+8*s),(x+124*s,y+8*s),(x+144*s,y+76*s)],fill=gold,outline=ink)
    draw.line((x+48*s,y+61*s,x+145*s,y+61*s),fill=red,width=max(4,int(13*s)))

facade=cover(Image.open(ROOT/'public/brand/fachada-hero.webp'),(W,H)).filter(ImageFilter.GaussianBlur(.15))
front=facade.copy(); overlay=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(overlay)
od.rectangle((0,0,W,H),fill=(12,35,23,112))
od.polygon([(0,0),(690,0),(540,H),(0,H)],fill=(18,57,37,220))
front=Image.alpha_composite(front.convert('RGBA'),overlay)
d=ImageDraw.Draw(front); hat(d,SAFE,58,.55)
d.text((SAFE,185),'LOS GUAJIROS',font=font(bold,74),fill=cream)
d.text((SAFE,275),'Tu antojo vive aquí',font=font(bold,39),fill='#ffe2a4')
d.text((SAFE,345),'Productos caseros en Marianao',font=font(regular,27),fill='white')
d.rounded_rectangle((SAFE,438,430,526),radius=44,fill=red)
d.text((SAFE+42,459),'ESCANEA Y PIDE',font=font(bold,25),fill='white')
d.text((SAFE,H-66),'9:00 a. m. - 9:00 p. m.  ·  Recogida o mensajería',font=font(regular,20),fill='#f9ead1')
front.convert('RGB').save(OUT/'tarjeta-los-guajiros-frente.png',quality=95,dpi=(300,300))

qr=qrcode.QRCode(version=None,error_correction=ERROR_CORRECT_H,box_size=16,border=4)
qr.add_data(URL); qr.make(fit=True); qim=qr.make_image(fill_color=ink,back_color='white').convert('RGB')
qim.save(OUT/'qr-los-guajiros.png',dpi=(300,300))
matrix=qr.get_matrix(); n=len(matrix)
with open(OUT/'qr-los-guajiros.svg','w',encoding='utf-8') as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="white"/><path fill="{ink}" d="')
    for y,row in enumerate(matrix):
        for x,v in enumerate(row):
            if v:f.write(f'M{x},{y}h1v1h-1z')
    f.write('"/></svg>')

back=Image.new('RGB',(W,H),cream); d=ImageDraw.Draw(back)
d.rectangle((0,0,18,H),fill=red); d.rounded_rectangle((58,55,530,H-55),radius=30,fill='white')
qrfit=qim.resize((415,415),Image.Resampling.NEAREST); back.paste(qrfit,(86,123))
hat(d,635,70,.48)
d.text((630,190),'MIRA LO',font=font(bold,43),fill=green)
d.text((630,240),'DISPONIBLE HOY',font=font(bold,43),fill=green)
d.line((630,310,1055,310),fill=red,width=7)
d.text((630,348),'Recogida o mensajería',font=font(bold,25),fill=ink)
d.text((630,398),'9:00 a. m. - 9:00 p. m.',font=font(regular,23),fill=ink)
d.text((630,444),'Calle 88, Marianao',font=font(regular,23),fill=ink)
d.text((630,505),'Escanea y pide desde tu móvil',font=font(bold,22),fill=red)
d.text((630,548),'los-guajiros.vercel.app',font=font(regular,19),fill=green)
back.save(OUT/'tarjeta-los-guajiros-reverso.png',quality=95,dpi=(300,300))

# PNG horizontal para usos que no acepten SVG.
logo=Image.new('RGBA',(1640,480),(0,0,0,0)); ld=ImageDraw.Draw(logo)
hat(ld,48,82,1.15)
ld.text((470,105),'LOS GUAJIROS',font=font(bold,132),fill='#1f5638')
ld.line((474,264,1480,264),fill=red,width=12)
ld.text((474,300),'TU ANTOJO VIVE AQUÍ',font=font(bold,55),fill=ink)
logo.save(OUT/'logo-los-guajiros.png',dpi=(300,300))

pdf=OUT/'tarjeta-los-guajiros-imprenta.pdf'; c=canvas.Canvas(str(pdf),pagesize=(96*mm,56*mm))
print_images=[]
for i,image in enumerate([OUT/'tarjeta-los-guajiros-frente.png',OUT/'tarjeta-los-guajiros-reverso.png']):
    jpeg=OUT/f'.print-{i}.jpg'
    Image.open(image).convert('RGB').save(jpeg,quality=94,subsampling=0,dpi=(300,300))
    print_images.append(jpeg)
for image in print_images:
    c.drawImage(ImageReader(str(image)),0,0,width=96*mm,height=56*mm)
    c.showPage()
c.save()
for image in print_images: image.unlink(missing_ok=True)
print(URL)
