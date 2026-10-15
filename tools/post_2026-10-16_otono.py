import sys; sys.path.insert(0,"tools")
from brand import *
slides=[
 {"type":"cover","kicker":"GUÍA DE OTOÑO","title":"Tu piscina,\nlista para","accent":"el invierno","sub":"5 consejos para que llegue limpia y sin sustos a la primavera."},
 {"type":"tip","title":"No la vacíes","body":"El agua protege el vaso. Vacía, el sol y el frío pueden agrietar el gresite e incluso levantarla.","tip":"Mejor llena y tratada todo el invierno."},
 {"type":"tip","title":"Menos horas de depuradora","body":"Con el agua más fría las algas crecen mucho menos, así que no hace falta filtrar tanto.","tip":"Regla práctica: temperatura del agua ÷ 2 = horas al día."},
 {"type":"tip","title":"Vigila el pH","body":"Mantenlo entre 7,2 y 7,6. Con el pH alto, el cloro apenas hace efecto.","tip":"Mídelo cada semana, aunque nadie se bañe."},
 {"type":"tip","title":"Cestos limpios","body":"Skimmer y prefiltro llenos de hojas significan menos caudal y más esfuerzo para la bomba.","tip":"Vacíalos cada semana durante el otoño."},
 {"type":"tip","title":"Invernador y cubierta","body":"Cuando el agua baje de 15 °C, producto de invernaje y la cubierta puesta.","tip":"En primavera, la puesta a punto es mucho más fácil."},
 {"type":"cta","title":"¿Prefieres","accent":"olvidarte?","body":"Cuidamos tu piscina y tu jardín todo el año en Jávea y Dénia.","button":"Presupuesto por WhatsApp","note":"English spoken · link en la bio"},
]
p=carousel(slides,"2026-10/otono-v2")
photo_post("/root/.claude/uploads/a633a4d6-9781-5c8e-81cf-30028eaaa118/c6f0d566-image.jpg","2026-10/ciclamenes-v3.jpg","JARDÍN EN JÁVEA","El color del otoño",cy=0.45)
contact_sheet(p+["2026-10/ciclamenes-v2.jpg"],sys.argv[1])
