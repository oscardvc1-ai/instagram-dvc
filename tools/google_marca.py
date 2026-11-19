"""Logo (720x720) y portada (1080x608) para la ficha de Google."""
import sys; sys.path.insert(0, "tools")
import brand as b
from PIL import Image, ImageDraw
A = "/mnt/user-data/attachments/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
# logo: círculo verde con ramita y nombre
S = 720
im = Image.new("RGB", (S, S), b.GREEN); d = ImageDraw.Draw(im)
b.sprig(d, S // 2, 330, 1.25, b.SAGE)
d.text((S / 2, 470), "Jardines DVC", font=b.serif(84, "SemiBold"), fill=b.CREAM, anchor="ms")
b.tracked(d, (S / 2, 540), "JÁVEA · DÉNIA", b.sans(30, "SemiBold"), (222, 160, 125), 7, anchor="m")
im.save("google/marca/logo-jardines-dvc.jpg", quality=95)
# portada: foto del jardín frente al mar, retocada, sin texto
p = b.enhance(A + "af645582-image.jpg", strength=0.85, vignette=0)
b._fit(p, 1080, 608, 0.55).save("google/marca/portada-jardines-dvc.jpg", quality=93)
