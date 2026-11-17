import sys; sys.path.insert(0, "tools")
from brand import carousel, contact_sheet
slides = [
 {"type": "cover", "kicker": "GUÍA DE INVIERNO", "title": "Tu césped\nen invierno", "accent": "verde hasta marzo",
  "sub": "5 cuidados para que llegue fuerte a la primavera, sin calvas ni hongos."},
 {"type": "tip", "title": "Corta más alto", "body": "Sube un punto la altura del cortacésped. La hoja más larga protege la raíz del frío.",
  "tip": "Nunca quites más de un tercio de la hoja de una vez."},
 {"type": "tip", "title": "Riega menos y de mañana", "body": "Con menos sol el agua tarda en secarse. El riego de noche favorece los hongos.",
  "tip": "Ajusta el programador: menos días y a primera hora."},
 {"type": "tip", "title": "Abono de otoño", "body": "Un abono rico en potasio endurece la planta y fortalece la raíz para el invierno.",
  "tip": "Mejor ahora que en pleno frío."},
 {"type": "tip", "title": "Fuera hojas", "body": "Las hojas caídas tapan la luz y pudren el césped que queda debajo.",
  "tip": "Rastrilla o sopla una vez por semana."},
 {"type": "tip", "title": "Airea si está duro", "body": "Si el agua se encharca o el suelo está compactado, pinchar el césped deja respirar la raíz.",
  "tip": "Con aireador o simplemente con una horca."},
 {"type": "cta", "title": "¿Lo cuidamos", "accent": "por ti?", "body": "Mantenimiento de jardines todo el año en Jávea y Dénia.",
  "button": "Visita y presupuesto gratis", "note": "English spoken · WhatsApp en la bio"},
]
p = carousel(slides, "2026-11/cesped")
contact_sheet(p, sys.argv[1])
