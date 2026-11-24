import sys; sys.path.insert(0, "tools")
from PIL import Image, ImageFilter
from brand import photo_post, gallery_slide, carousel, contact_sheet
U = "/mnt/user-data/uploads/"


def blur(src, boxes, out, crop=None):
    """Difumina los números de casa (cx, cy, r) y recorta si hace falta."""
    im = Image.open(src).convert("RGB")
    soft = im.filter(ImageFilter.GaussianBlur(7))
    mask = Image.new("L", im.size, 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(mask)
    for cx, cy, r in boxes:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    im.paste(soft, (0, 0), mask.filter(ImageFilter.GaussianBlur(6)))
    if crop:
        im = im.crop(crop)
    im.save(out, quality=96)
    return out


camino = blur(U + "295cc1d0-image.jpg",
              [(257, 882, 34), (438, 866, 24), (600, 871, 22), (759, 876, 22), (961, 884, 22), (1068, 888, 20)],
              "/tmp/camino.jpg")
piscina = blur(U + "437cd61d-image.jpg",
               [(145, 938, 24), (382, 942, 22), (576, 943, 22), (797, 948, 22)],
               "/tmp/piscina.jpg", crop=(430, 480, 1659, 2030))   # fuera la farola del primer plano

o = "2026-11/comunidad-"
photo_post(camino, o + "1.jpg", "JARDINES QUE CUIDAMOS · JÁVEA", "Verde en noviembre", cy=0.55)
gallery_slide(piscina, o + "2.jpg", "02 / 03", "Césped segado hasta la piscina", cy=0.5)
carousel([{"type": "cta", "title": "¿Tu comunidad", "accent": "así de cuidada?",
           "body": "Mantenimiento de jardines para comunidades y villas en Jávea, todo el año.",
           "button": "Visita y presupuesto gratis", "note": "English spoken · WhatsApp en la bio"}],
         "2026-11/comunidad-cta", start=3, total=3)
contact_sheet([o + "1.jpg", o + "2.jpg", "2026-11/comunidad-cta-3.jpg"], sys.argv[1], cols=3)
