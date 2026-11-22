#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Koordinatenraster ueber ein Praesentationsbild legen.

Die Beschriftungen in rfn_neu_bilder.tex benutzen Bildanteile:
(0,0) ist die untere linke, (1,1) die obere rechte Ecke des Bildes.
Dieses Skript legt genau dieses Raster sichtbar ueber das Bild, damit
sich die Koordinaten fuer \\anmerkung direkt ablesen lassen.

Aufruf (aus dem Ordner Praesentation):

    python tools/bildraster.py img/RFN_neu/01_gesamtschnitt.png

    -> schreibt raster_01_gesamtschnitt.png in denselben Ordner

Ausschnitt vergroessert anzeigen, wenn es eng wird:

    python tools/bildraster.py img/RFN_neu/06_blende_detail.png 0.1 0.0 0.5 0.4

    (Reihenfolge: x-links y-unten x-rechts y-oben, jeweils 0..1)

Benoetigt Pillow:  pip install pillow
"""
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow fehlt. Installieren mit:  pip install pillow")

Image.MAX_IMAGE_PIXELS = None

ROT = (220, 30, 30)
BLAU = (30, 60, 200)


def schrittweite(spanne):
    """Gitterabstand, der bei jeder Zoomstufe lesbar bleibt."""
    for s in (0.2, 0.1, 0.05, 0.02, 0.01, 0.005):
        if spanne / s <= 12:
            return s
    return 0.002


def main():
    if len(sys.argv) not in (2, 6):
        sys.exit(__doc__)

    quelle = Path(sys.argv[1])
    if not quelle.is_file():
        sys.exit(f"Datei nicht gefunden: {quelle}")

    if len(sys.argv) == 6:
        x0, y0, x1, y1 = (float(v) for v in sys.argv[2:6])
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            sys.exit("Ausschnitt muss 0 <= x0 < x1 <= 1 und 0 <= y0 < y1 <= 1 erfuellen.")
    else:
        x0, y0, x1, y1 = 0.0, 0.0, 1.0, 1.0

    im = Image.open(quelle).convert("RGB")
    bw, bh = im.size
    # y zaehlt im Bild von oben, in TikZ von unten
    im = im.crop((int(x0 * bw), int((1 - y1) * bh), int(x1 * bw), int((1 - y0) * bh)))

    # kleine Ausschnitte vergroessern, grosse Bilder verkleinern
    while max(im.size) < 700:
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im.thumbnail((1400, 1400), Image.LANCZOS)

    d = ImageDraw.Draw(im)
    w, h = im.size

    sx = schrittweite(x1 - x0)
    g = x0
    while g <= x1 + 1e-9:
        px = min(int((g - x0) / (x1 - x0) * w), w - 1)
        d.line([(px, 0), (px, h)], fill=ROT)
        d.text((px + 2, 2), f"{g:.3f}".rstrip("0").rstrip("."), fill=ROT)
        g = round(g + sx, 4)

    sy = schrittweite(y1 - y0)
    g = y0
    while g <= y1 + 1e-9:
        py = min(int(h - (g - y0) / (y1 - y0) * h), h - 1)
        d.line([(0, py), (w, py)], fill=BLAU)
        d.text((2, py + 2), f"{g:.3f}".rstrip("0").rstrip("."), fill=BLAU)
        g = round(g + sy, 4)

    ziel = quelle.with_name("raster_" + quelle.name)
    im.save(ziel)
    print(f"{ziel}   ({w}x{h})")
    print(f"rot = x (0 links .. 1 rechts),  blau = y (0 unten .. 1 oben)")


if __name__ == "__main__":
    main()
