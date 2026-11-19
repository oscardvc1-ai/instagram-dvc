import sys; sys.path.insert(0, "tools")
from reel import slideshow_reel
A = "/mnt/user-data/attachments/a633a4d6-9781-5c8e-81cf-30028eaaa118/"
B = sys.argv[1]  # foto con el cartel difuminado
slideshow_reel([
    (A + "af645582-image.jpg", "frente al mar"),
    (A + "482b2699-image.jpg", "palmeras y parterres"),
    (B, "césped recién segado"),
    (A + "72640a01-image.jpg", "hasta la playa"),
], "2026-11/reel-mar.mp4", "JARDINES QUE CUIDAMOS · JÁVEA", "Un jardín junto al mar", secs=3.2)
