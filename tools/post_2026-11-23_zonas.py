import sys, math, tempfile; sys.path.insert(0, "tools")
import brand
from PIL import Image
A = "/mnt/user-data/attachments/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
im = brand._open(A + "54086f89-image.jpg"); r = 3.5   # enderezar horizonte
w, h = im.size; m = int(max(w, h) * math.sin(math.radians(r))) + 4
tmp = tempfile.mktemp(suffix=".jpg")
im.rotate(r, resample=Image.BICUBIC).crop((m, m, w - m, h - m)).save(tmp, quality=96)
brand.photo_post(tmp, "2026-11/zonas-comunes.jpg", "COMUNIDADES · JÁVEA", "Zonas comunes cuidadas", cy=0.5)
