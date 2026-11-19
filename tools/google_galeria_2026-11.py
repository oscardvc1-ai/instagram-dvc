"""Fotos limpias (retocadas, sin texto) para la galería de Google Business Profile."""
import sys, math; sys.path.insert(0, "tools")
import brand
from PIL import Image
A = "/mnt/user-data/attachments/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
fotos = [
    ("ea2ebacc-image.jpg", "jardin-palmeras-javea", None, 0),
    ("d3e6c74e-image.jpg", "palmeral-cesped-javea", None, 0),
    ("af645582-image.jpg", "jardin-frente-al-mar-javea", None, 0),
    ("72640a01-image.jpg", "cesped-hasta-la-playa-javea", None, 0),
    ("caaeb6e3-image.jpg", "jardin-piscina-javea", None, 0),
    ("54ee553a-b02021ea-59dc-473c-8e08-2ba2054efebb-1_all_1163.jpg", "urbanizacion-cesped-javea", (0.38, 0.0, 1.0, 1.0), 0),
    ("f623d79e-55959.jpg", "ciclamenes-jardineras-javea", None, 0),
    ("e0181737-56360.jpg", "seto-cipres-recortado-javea", None, 0),
    ("d52c14ee-48491.jpg", "piscina-limpia-javea", None, 0),
    ("54086f89-image.jpg", "zonas-comunes-comunidad-javea", None, 3.5),
]
for src, name, crop, rot in fotos:
    im = brand._open(A + src)
    if rot:
        w, h = im.size; m = int(max(w, h) * math.sin(math.radians(rot))) + 4
        im = im.rotate(rot, resample=Image.BICUBIC).crop((m, m, w - m, h - m))
    if crop:
        w, h = im.size; im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    im = brand.enhance(im, strength=0.85, vignette=0)
    im.thumbnail((2000, 2000), Image.LANCZOS)
    im.save(f"google/{name}.jpg", quality=92)
    print(name, im.size)
