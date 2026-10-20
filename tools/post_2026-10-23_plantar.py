import sys; sys.path.insert(0, "tools")
from brand import carousel, contact_sheet
slides = [
 {"type": "cover", "kicker": "GUÍA DE OTOÑO", "title": "Qué plantar\nen otoño", "accent": "en la Costa Blanca",
  "sub": "El otoño es la mejor época del año para plantar: tierra templada y primeras lluvias."},
 {"type": "tip", "title": "Ciclámenes y pensamientos", "body": "Las flores de temporada: aguantan el fresco y dan color de noviembre a la primavera.",
  "tip": "En macetas y jardineras, a media sombra."},
 {"type": "tip", "title": "Lavanda y romero", "body": "Aromáticas mediterráneas, de poco riego. Plantadas ahora enraízan con las lluvias y llegan fuertes al verano.",
  "tip": "Sol directo y suelo con buen drenaje."},
 {"type": "tip", "title": "Arbustos y setos nuevos", "body": "Es el momento ideal: la raíz crece todo el invierno sin el estrés del calor.",
  "tip": "Plantar en otoño ahorra mucho riego en verano."},
 {"type": "tip", "title": "Bulbos de primavera", "body": "Narcisos, ranúnculos o fresias. Se plantan ahora y florecen entre febrero y abril.",
  "tip": "Entiérralos a dos o tres veces su altura."},
 {"type": "tip", "title": "Resembrar el césped", "body": "Las calvas del verano se arreglan ahora: la semilla germina bien con temperaturas suaves.",
  "tip": "Escarifica, siembra y riega poco y a menudo."},
 {"type": "cta", "title": "¿Lo plantamos", "accent": "por ti?", "body": "Diseñamos, plantamos y cuidamos tu jardín en Jávea y Dénia.",
  "button": "Visita y presupuesto gratis", "note": "English spoken · WhatsApp en la bio"},
]
p = carousel(slides, "2026-10/plantar")
contact_sheet(p, sys.argv[1])
