import sys; sys.path.insert(0, "tools")
from brand import photo_post, gallery_slide, carousel, contact_sheet
A = "/mnt/user-data/attachments/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
o = "2026-11/galeria-"
photo_post(A + "ea2ebacc-image.jpg", o + "1.jpg", "JARDINES QUE CUIDAMOS · JÁVEA", "Entre palmeras", cy=0.45)
gallery_slide(A + "d3e6c74e-image.jpg", o + "2.jpg", "02 / 05", "Césped recién cortado", cy=0.45)
gallery_slide(A + "943c60cd-image.jpg", o + "3.jpg", "03 / 05", "Setos a punto, con vistas al mar", cy=0.45)
gallery_slide(A + "caaeb6e3-image.jpg", o + "4.jpg", "04 / 05", "Verde hasta el borde de la piscina", cy=0.5)
carousel([{"type": "cta", "title": "¿Un jardín", "accent": "así de cuidado?",
           "body": "Mantenimiento de jardines para villas, comunidades y hoteles en Jávea y Dénia.",
           "button": "Visita y presupuesto gratis", "note": "English spoken · WhatsApp en la bio"}],
         "2026-11/galeria-cta", start=5, total=5)
contact_sheet([o + f"{i}.jpg" for i in range(1, 5)] + ["2026-11/galeria-cta-5.jpg"], sys.argv[1], cols=5)
