"""Identidad visual de @jardinesdvc para Instagram (1080x1350).

Uso:
    from brand import photo_post, before_after, carousel
    photo_post("foto.jpg", "out.jpg", kicker="JARDÍN EN JÁVEA", title="Color de otoño")
    before_after("antes.jpg", "despues.jpg", "out.jpg", title="De verde a cristalina")
    carousel(slides, "prefijo")   # ver docstring de carousel()
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math

W, H = 1080, 1350
CREAM = (243, 238, 227)
GREEN = (30, 58, 43)
TERRA = (185, 100, 63)
SAGE = (143, 163, 130)
SAGE_BG = (226, 229, 214)
INK = (45, 52, 46)

_LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
_LORA_I = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
_INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"


def serif(size, weight="SemiBold", italic=False):
    f = ImageFont.truetype(_LORA_I if italic else _LORA, size)
    w = {"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700}[weight]
    f.set_variation_by_axes([w])
    return f


def sans(size, weight="Medium"):
    return ImageFont.truetype(_INTER.format(weight), size)


def tracked(d, xy, text, font, fill, spacing=4, anchor="l"):
    """Texto con espaciado entre letras (etiquetas en mayúsculas)."""
    x, y = xy
    total = sum(d.textlength(c, font=font) + spacing for c in text) - spacing
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for c in text:
        d.text((x, y), c, font=font, fill=fill, anchor="ls")
        x += d.textlength(c, font=font) + spacing


def leaf(d, cx, cy, size, angle, fill):
    """Hoja sencilla (dos arcos) para adornos."""
    pts = []
    for t in range(0, 181, 6):
        r = math.radians(t)
        pts.append((math.sin(r) * size * 0.32, -math.cos(r) * size / 2))
    pts += [(-x, y) for x, y in reversed(pts)]
    a = math.radians(angle)
    pts = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    d.polygon(pts, fill=fill)


def sprig(d, x, y, scale=1.0, fill=SAGE):
    """Ramita con hojas alternas."""
    d.line((x, y, x, y - 150 * scale), fill=fill, width=max(2, int(4 * scale)))
    for i, k in enumerate(range(5)):
        yy = y - 25 * scale - k * 28 * scale
        side = -1 if i % 2 else 1
        leaf(d, x + side * 22 * scale, yy, 46 * scale, side * 55, fill)
    leaf(d, x, y - 160 * scale, 44 * scale, 0, fill)


def _fit(im, w, h, cy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int(min(max(im.height * cy - h / 2, 0), im.height - h))
    return im.crop((x, y, x + w, y + h))


def _rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), radius=r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), m)
    return out


def _open(p):
    return ImageOps.exif_transpose(Image.open(p)).convert("RGB")


def _footer(d, y=H - 58, page=None, dark=False):
    c = CREAM if dark else GREEN
    tracked(d, (60, y), "JARDINES DVC", sans(22, "SemiBold"), c, 5)
    if page:
        tracked(d, (W - 60, y), page, sans(22, "Medium"), SAGE, 3, anchor="r")
    else:
        tracked(d, (W - 60, y), "@JARDINESDVC", sans(22, "Medium"), SAGE, 3, anchor="r")


def photo_post(src, out, kicker, title, crop=None, cy=0.5, retouch=1.0):
    """Foto enmarcada en crema con titular serif debajo.
    crop=(x0,y0,x1,y1) en coordenadas de la foto para quitar zonas (números, carteles)."""
    im = _open(src)
    if crop:
        im = im.crop(crop)
    if retouch:
        im = enhance(im, strength=retouch)
    c = Image.new("RGB", (W, H), CREAM)
    pw, ph = W - 80, 1040
    tile = _rounded(_fit(im, pw, ph, cy), 26)
    c.paste(tile, (40, 40), tile)
    d = ImageDraw.Draw(c)
    tracked(d, (60, 1150), kicker, sans(24, "SemiBold"), TERRA, 5)
    d.text((60, 1225), title, font=serif(62, "SemiBold"), fill=GREEN, anchor="ls")
    sprig(d, W - 95, 1255, 0.55)
    _footer(d)
    c.save(out, quality=93)


def before_after(a, b, out, title, kicker="ANTES Y DESPUÉS", cy=0.5, retouch=1.0):
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    pw, ph = (W - 80 - 16) // 2, 1040
    for i, (src, lab) in enumerate(((a, "antes"), (b, "después"))):
        x = 40 + i * (pw + 16)
        img = _open(src)
        if retouch:  # mismo retoque en las dos: comparación honesta
            img = enhance(img, strength=retouch)
        tile = _rounded(_fit(img, pw, ph, cy), 24)
        c.paste(tile, (x, 40), tile)
        f = serif(40, "Medium", italic=True)
        tw = d.textlength(lab, font=f)
        cx = x + pw / 2
        d.rounded_rectangle((cx - tw / 2 - 28, ph - 52, cx + tw / 2 + 28, ph + 16), radius=34, fill=CREAM)
        d.text((cx, ph - 16), lab, font=f, fill=GREEN if i else TERRA, anchor="mm")
    tracked(d, (60, 1150), kicker, sans(24, "SemiBold"), TERRA, 5)
    d.text((60, 1225), title, font=serif(62, "SemiBold"), fill=GREEN, anchor="ls")
    sprig(d, W - 95, 1255, 0.55)
    _footer(d)
    c.save(out, quality=93)


def _wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                line = t
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


def carousel(slides, prefix):
    """slides: lista de dicts.
      {"type":"cover","kicker":..,"title":..,"accent":..,"sub":.., "photo": opcional}
      {"type":"tip","title":..,"body":..,"tip":..}
      {"type":"cta","title":..,"accent":..,"body":..,"button":..,"note":..}
    Guarda prefix-1.jpg ... prefix-n.jpg y devuelve la lista de rutas."""
    n = len(slides)
    paths = []
    k = 0
    for i, s in enumerate(slides, 1):
        page = f"{i:02d} / {n:02d}"
        if s["type"] == "cta":
            c = Image.new("RGB", (W, H), GREEN)
        else:
            c = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(c)
        if s["type"] == "cover":
            if s.get("photo"):
                ph = _rounded(_fit(_open(s["photo"]), W - 80, 600), 26)
                c.paste(ph, (40, 40), ph)
                top = 760
            else:
                for j, (x, y, sc, ang) in enumerate(((930, 260, 1.4, -20), (1010, 330, 1.0, 25), (860, 330, 0.9, -45))):
                    sprig(d, x, y, sc, SAGE if j % 2 == 0 else (171, 187, 160))
                top = 470
            tracked(d, (60, top), s["kicker"], sans(26, "SemiBold"), TERRA, 6)
            y = top + 130
            for line in s["title"].split("\n"):
                d.text((56, y), line, font=serif(118, "SemiBold"), fill=GREEN, anchor="ls")
                y += 128
            d.text((60, y + 10), s["accent"], font=serif(76, "Regular", italic=True), fill=TERRA, anchor="ls")
            y += 110
            for line in _wrap(d, s["sub"], sans(36, "Regular"), 760):
                d.text((60, y), line, font=sans(36, "Regular"), fill=INK, anchor="ls")
                y += 50
            tracked(d, (60, H - 130), "DESLIZA  →", sans(26, "SemiBold"), GREEN, 5)
            _footer(d, page=page)
        elif s["type"] == "tip":
            k += 1
            tl = _wrap(d, s["title"], serif(84, "SemiBold"), 940)
            bl = _wrap(d, s["body"], sans(42, "Regular"), 920)
            lines = _wrap(d, s["tip"], serif(44, "Medium", italic=True), 820)
            box_h = 96 + 58 * len(lines)
            total = 260 + 96 * len(tl) + 40 + 62 * len(bl) + 70 + box_h
            top = max(90, (H - 120 - total) // 2)
            d.text((56, top + 210), f"{k:02d}", font=serif(230, "Regular", italic=True), fill=TERRA, anchor="ls")
            d.line((60, top + 260, 180, top + 260), fill=SAGE, width=4)
            y = top + 380
            for line in tl:
                d.text((56, y), line, font=serif(84, "SemiBold"), fill=GREEN, anchor="ls")
                y += 96
            y += 40
            for line in bl:
                d.text((60, y), line, font=sans(42, "Regular"), fill=INK, anchor="ls")
                y += 62
            box_top = y + 40
            d.rounded_rectangle((40, box_top, W - 40, box_top + box_h), radius=28, fill=SAGE_BG)
            leaf(d, 100, box_top + 64, 46, 40, SAGE)
            yy = box_top + 80
            for line in lines:
                d.text((140, yy), line, font=serif(44, "Medium", italic=True), fill=GREEN, anchor="ls")
                yy += 58
            _footer(d, page=page)
        else:  # cta
            for j, (x, y, sc) in enumerate(((960, 300, 1.5), (880, 360, 1.0))):
                sprig(d, x, y, sc, (70, 102, 80))
            y = 520
            for line in s["title"].split("\n"):
                d.text((56, y), line, font=serif(104, "SemiBold"), fill=CREAM, anchor="ls")
                y += 116
            d.text((60, y), s["accent"], font=serif(72, "Regular", italic=True), fill=(222, 160, 125), anchor="ls")
            y += 100
            for line in _wrap(d, s["body"], sans(38, "Regular"), 900):
                d.text((60, y), line, font=sans(38, "Regular"), fill=CREAM, anchor="ls")
                y += 54
            y += 50
            f = sans(38, "SemiBold")
            bw = d.textlength(s["button"], font=f) + 110
            d.rounded_rectangle((60, y, 60 + bw, y + 100), radius=50, fill=TERRA)
            d.text((60 + bw / 2, y + 50), s["button"], font=f, fill=CREAM, anchor="mm")
            if s.get("note"):
                d.text((60, y + 170), s["note"], font=serif(34, "Regular", italic=True), fill=SAGE, anchor="ls")
            _footer(d, page=page, dark=True)
        p = f"{prefix}-{i}.jpg"
        c.save(p, quality=93)
        paths.append(p)
    return paths


def contact_sheet(paths, out, cols=4, tw=360):
    th = int(tw * H / W)
    rows = math.ceil(len(paths) / cols)
    s = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * th + (rows + 1) * 10), (200, 200, 200))
    for i, p in enumerate(paths):
        s.paste(Image.open(p).resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    s.save(out)


# ---------------------------------------------------------------------------
# Retoque fotográfico (estilo "revista de jardín": luz cálida, verdes vivos,
# detalle nítido). Natural: no cambia lo que hay en la foto, solo la luz/color.
# ---------------------------------------------------------------------------
def enhance(src, out=None, strength=1.0, warmth=1.0, vignette=0.2):
    """Retoque natural: abre sombras, protege cielos, verdes y flores vivos,
    luz cálida, nitidez. strength 0.5 = suave, 1 = normal, 1.3 = intenso."""
    import numpy as np
    import cv2
    im = _open(src) if isinstance(src, str) else src.convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    k = strength

    lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
    # 1) exposición automática suave hacia una mediana ~0.48
    med = float(np.median(lum))
    if med < 0.46:
        g = np.clip(np.log(0.48) / np.log(max(med, 0.05)), 0.75, 1.0)
        a = a ** (1 - (1 - g) * k)
        lum = a @ np.array([0.299, 0.587, 0.114], np.float32)

    # 2) abrir sombras y proteger luces (según luminancia)
    sh = (1 - lum) ** 3
    hi = np.clip((lum - 0.75) / 0.25, 0, 1) ** 2
    gain = 1 + 0.45 * k * sh - 0.10 * k * hi
    a = np.clip(a * gain[..., None], 0, 1)

    # 3) claridad: contraste local (CLAHE en L) mezclado suave
    lab = cv2.cvtColor((a * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
    L = lab[..., 0].astype(np.float32)
    cl = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8)).apply(lab[..., 0]).astype(np.float32)
    lab[..., 0] = np.clip(L * (1 - 0.45 * k) + cl * 0.45 * k, 0, 255).astype(np.uint8)
    a = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0

    # 4) contraste global suave en medios (curva S)
    a = np.clip(a + 0.10 * k * (a - 0.5) * (1 - np.abs(2 * a - 1)), 0, 1)

    # 5) vibrance + verdes y flores algo más vivos
    hsv = cv2.cvtColor((a * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    H, S = hsv[..., 0], hsv[..., 1] / 255.0
    boost = 1 + 0.35 * k * (1 - S)
    green = np.exp(-((H - 50) / 18) ** 2)          # amarillo-verde a verde
    boost += 0.12 * k * green
    hsv[..., 1] = np.clip(hsv[..., 1] * boost, 0, 255)
    # verdes amarillentos (césped seco) un poco hacia verde
    hsv[..., 0] = np.where((H > 22) & (H < 40), H + 3 * k * (1 - np.abs(H - 31) / 9), H)
    a = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32) / 255.0

    # 6) calidez "hora dorada"
    w = 0.04 * warmth * k
    a[..., 0] = np.clip(a[..., 0] * (1 + w), 0, 1)
    a[..., 1] = np.clip(a[..., 1] * (1 + w * 0.35), 0, 1)
    a[..., 2] = np.clip(a[..., 2] * (1 - w * 0.6), 0, 1)

    # 7) nitidez
    u8 = (a * 255).astype(np.uint8)
    blur = cv2.GaussianBlur(u8, (0, 0), 1.6)
    u8 = cv2.addWeighted(u8, 1 + 0.5 * k, blur, -0.5 * k, 0)

    # 8) viñeta suave
    if vignette:
        h, wd = u8.shape[:2]
        yy, xx = np.mgrid[0:h, 0:wd]
        r = np.sqrt(((xx - wd / 2) / (wd / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        m = 1 - vignette * np.clip(r - 0.65, 0, 1) ** 1.5
        u8 = np.clip(u8 * m[..., None], 0, 255).astype(np.uint8)

    res = Image.fromarray(u8)
    if out:
        res.save(out, quality=95)
    return res
