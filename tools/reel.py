"""Reels verticales 1080x1920 con la identidad de @jardinesdvc.

before_after_reel(foto_antes, video_despues, out, kicker, title)
  - 2,5 s de la foto "antes" (zoom lento) + el vídeo "después" retocado.
  - Marco crema, titular serif arriba, etiqueta antes/después y pie de marca.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import brand as b

RW, RH = 1080, 1920
WIN = (40, 300, 1040, 1633)  # ventana 1000x1333 (3:4)


def _frame(kicker, title, label, label_color):
    """PNG con fondo crema, textos y ventana transparente redondeada."""
    im = Image.new("RGBA", (RW, RH), b.CREAM + (255,))
    mask = Image.new("L", (RW, RH), 0)
    ImageDraw.Draw(mask).rounded_rectangle(WIN, radius=30, fill=255)
    im.putalpha(Image.eval(mask, lambda v: 255 - v))
    d = ImageDraw.Draw(im)
    b.tracked(d, (60, 150), kicker, b.sans(28, "SemiBold"), b.TERRA, 6)
    d.text((56, 245), title, font=b.serif(76, "SemiBold"), fill=b.GREEN, anchor="ls")
    b.sprig(d, RW - 100, 260, 0.65)
    f = b.serif(48, "Medium", italic=True)
    tw = d.textlength(label, font=f)
    cx, cy = RW / 2, WIN[3] - 70
    d.rounded_rectangle((cx - tw / 2 - 34, cy - 40, cx + tw / 2 + 34, cy + 40), radius=40, fill=b.CREAM)
    d.text((cx, cy), label, font=f, fill=label_color, anchor="mm")
    d.text((60, 1760), "Visita y presupuesto gratis", font=b.serif(46, "Regular", italic=True), fill=b.GREEN, anchor="ls")
    b.tracked(d, (60, 1840), "JARDINES DVC", b.sans(26, "SemiBold"), b.GREEN, 6)
    b.tracked(d, (RW - 60, 1840), "@JARDINESDVC", b.sans(26, "Medium"), b.SAGE, 4, anchor="r")
    return im


def before_after_reel(before_img, after_video, out, kicker, title, before_secs=2.5, max_after=11.0):
    tmp = tempfile.mkdtemp()
    ww, wh = WIN[2] - WIN[0], WIN[3] - WIN[1]
    # foto antes retocada y ampliada un 8 % para el zoom
    im = b.enhance(before_img, strength=0.8)
    im = b._fit(im, int(ww * 1.08), int(wh * 1.08))
    im.save(f"{tmp}/before.jpg", quality=95)
    _frame(kicker, title, "antes", b.TERRA).save(f"{tmp}/f_before.png")
    _frame(kicker, title, "después", b.GREEN).save(f"{tmp}/f_after.png")
    n = int(before_secs * 30)
    look = "eq=contrast=1.07:saturation=1.22:brightness=0.02:gamma=1.05,colorbalance=rm=0.04:bm=-0.04:rh=0.02:bh=-0.03,unsharp=5:5:0.6"
    fc = (
        # antes: zoom lento hacia dentro
        f"[0:v]scale={int(ww*1.08)}:{int(wh*1.08)},zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={n}:s={ww}x{wh}:fps=30,setsar=1[a0];"
        f"color=c=0xF3EEE3:s={RW}x{RH}:r=30:d={before_secs}[bg0];"
        f"[bg0][a0]overlay={WIN[0]}:{WIN[1]}[c0];[c0][2:v]overlay=0:0,format=yuv420p[v0];"
        # después: vídeo recortado a 3:4, retocado
        f"[1:v]crop='min(iw,ih*3/4)':ih,scale={ww}:{wh},{look},fps=30,setsar=1[a1];"
        f"color=c=0xF3EEE3:s={RW}x{RH}:r=30[bg1];"
        f"[bg1][a1]overlay={WIN[0]}:{WIN[1]}:shortest=1[c1];[c1][3:v]overlay=0:0,format=yuv420p[v1];"
        f"[v0][v1]xfade=transition=fade:duration=0.4:offset={before_secs-0.4}[v]"
    )
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-t", str(before_secs), "-i", f"{tmp}/before.jpg",
        "-t", str(max_after), "-i", after_video,
        "-i", f"{tmp}/f_before.png", "-i", f"{tmp}/f_after.png",
        "-filter_complex", fc, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", out,
    ]
    subprocess.run(cmd, check=True)
    # portada (primer fotograma del "después") para Instagram
    cover = os.path.splitext(out)[0] + "-portada.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(before_secs + 1.5), "-i", out,
                    "-frames:v", "1", "-q:v", "2", cover], check=True)
    return out, cover
