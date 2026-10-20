import sys; sys.path.insert(0, "tools")
from brand import before_after, photo_post, contact_sheet
U = "/root/.claude/uploads/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
A, B = U + "becd997b-image.jpg", U + "aeb2bebf-image.jpg"
before_after(A, B, "2026-10/seto-1.jpg", "Un seto como nuevo", kicker="RECORTE DE SETO · JÁVEA", cy=0.55, retouch=0.75)
photo_post(A, "2026-10/seto-2.jpg", "ANTES", "Ramas sueltas y sin forma", cy=0.5, retouch=0.75)
photo_post(B, "2026-10/seto-3.jpg", "DESPUÉS", "Recto, denso y limpio", cy=0.5, retouch=0.75)
contact_sheet(["2026-10/seto-1.jpg", "2026-10/seto-2.jpg", "2026-10/seto-3.jpg"], sys.argv[1], cols=3)
