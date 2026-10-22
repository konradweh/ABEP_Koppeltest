# RFN-Spule in COMSOL – Briefing für die Präsentation

Stand: 30. September 2026
Autor der Simulation: Konrad Wehkamp, Masterarbeit PTRA (JLU Gießen / THM)

---

## Auftrag an den Slide-Assistenten

Aus diesem Dokument sollen **5 bis 8 Folien** für einen **Zwischenstandsbericht an den Betreuer**
entstehen. Der Betreuer kennt den RF-Neutralisator und das ABEP-Projekt, er braucht keine
Einführung in die Grundlagen. Was ihn interessiert: Ist das Modell belastbar, was kommt heraus,
und was bedeutet das für den Aufbau.

Sprache: Deutsch.

Stil: Die Texte sollen nach einem Menschen klingen, nicht nach einem Sprachmodell. Also keine
Gedankenstrich-Ketten, keine Doppelpunkt-Konstruktionen die eine Erklärung ankündigen statt den
Satz weiterzuführen, keine "nicht nur X, sondern Y"-Konstruktionen, keine floskelhaften
Übergangswörter, keine leeren Dreier-Aufzählungen, wechselnde Satzlängen. Auf Folien dürfen
Stichpunkte stehen, aber sie sollen etwas aussagen und nicht aus Schlagwörtern bestehen.

Was auf jeden Fall vorkommen muss: die vier Kernzahlen (Spulenwiderstand, Induktivität,
Spulentemperatur, Glastemperatur), die Validierung gegen die Handrechnungen, und die
Konsequenzen für die Hardware. Der Proximity-Effekt ist das physikalisch interessanteste
Ergebnis und verdient eine eigene Folie mit dem Verlustdichte-Bild.

Was weggelassen werden kann: die Löserprobleme während der Entwicklung, die Fehlersuche bei der
Strahlungskopplung, die Details der COMSOL-Bedienung. Das steht hier nur zur Vollständigkeit
und für Rückfragen.

Abbildungen liegen als PNG vor, siehe Abschnitt "Verfügbare Abbildungen" am Ende.

---

## Fragestellung

Der RF-Neutralisator des ABEP-Systems erzeugt sein Plasma induktiv. Eine Kupferspule sitzt
außen auf einem Quarzglasgefäß und koppelt bei einigen Megahertz Leistung ein. Im Vakuum gibt
es weder Konvektion noch eine Wärmesenke über die Luft, und die Spule hat außer Strahlung
keinen Weg, ihre Wärme loszuwerden.

Die Simulation soll zwei Fragen beantworten. Erstens, wie groß der Wechselstromwiderstand der
Spule wirklich ist, weil er bestimmt, wie viel Generatorleistung in der Spule verheizt statt ins
Plasma gekoppelt wird. Zweitens, wie heiß Spule und Gefäß im Betrieb werden, weil das über die
Materialwahl für Lötstellen, Isolierungen und Halterungen entscheidet.

---

## Modell

### Geometrie
Die Spule ist eine einlagige Helix aus 3 mm dickem Kupferdraht, 5,9 Windungen, Steigung 5 mm.
Die Drahtmitte liegt auf einem Radius von 28,6 mm, das lässt einen Millimeter Luft zur
Glasaußenwand. Die abgewickelte Drahtlänge beträgt 1012,7 mm, rückgerechnet aus dem vernetzten
Spulenvolumen von 7158 mm³.

Das Quarzglasgefäß ist parametrisch nachgebaut, nach dem Inventor-Modell des realen Bauteils:
Hauptkörper außen 26,1 mm und innen 20,2 mm Radius, ein Sockel mit 31 mm außen und 23 mm innen,
ein Hals mit 10 mm außen und 7,9 mm innen. Beides steckt in einer Vakuumkugel.

### Betriebspunkt
Frequenz 4 MHz, Spulenstrom 5 A als Scheitelwert, eingeprägt. Auf die Glasinnenwand werden
60 W Plasmaleistung als Wärmequelle gelegt. Umgebungstemperatur 293,15 K. Emissionsgrade:
0,3 für das Kupfer, was zwischen poliert und oxidiert liegt, und 0,9 für Quarzglas im Infraroten.

### Physik
Drei gekoppelte Interfaces. Magnetische Felder im Frequenzbereich mit der Spule als
Einzelleiter, Wärmetransport in Feststoffen, und Oberfläche-zu-Oberfläche-Strahlung. Dazu zwei
Multiphysik-Kopplungen, elektromagnetische Erwärmung und Wärmeübertragung mit
Oberfläche-zu-Oberfläche-Strahlung.

Die Strahlung ist im Vakuum die einzige Wärmesenke. Ohne sie hat die Wärmegleichung keine
eindeutige Lösung.

### Netz
440.977 Elemente. Entscheidend ist die Auflösung der Skintiefe: Bei 4 MHz beträgt sie 32,6 µm
bei einem Drahtradius von 1,5 mm, also ein Verhältnis von 1 zu 46. Auf der Drahtoberfläche
liegen deshalb fünf Randschichten, die erste 10 µm dick, gestreckt mit Faktor 1,4, zusammen etwa
3,3 Skintiefen. Tangential ist das Netz bewusst gröber, weil sich die Stromdichte entlang des
Drahtes nur langsam ändert.

---

## Rechnung

Studie 1 löst das Magnetfeld allein, 617.783 Freiheitsgrade, direkter Löser, gut fünf Minuten
und 15 GB Arbeitsspeicher.

Studie 2 löst Temperatur und Oberflächenradiosität, 104.473 Freiheitsgrade, 21 Sekunden.
Das Magnetfeld wird dabei nicht mitgerechnet, sondern aus Studie 1 übernommen. Das ist zulässig,
weil der spezifische Widerstand des Kupfers im Modell temperaturunabhängig ist und das Magnetfeld
damit gar nicht von der Temperatur abhängt. Vorher faktorisierte der Löser die große Matrix in
jeder Kopplungsiteration neu, was die Rechenzeit von 21 Sekunden auf über eine halbe Stunde trieb.

Der gesamte Ablauf ist in einem Python-Skript über die MPh-Schnittstelle automatisiert. Das
Skript arbeitet immer auf einer Zeitstempel-Kopie, prüft die Parameter gegen Sollwerte, rechnet
beide Studien, wertet aus und exportiert die Bilder.

---

## Ergebnisse, elektromagnetisch

| Größe | Simulation | Vergleichsrechnung | Abweichung |
|---|---|---|---|
| Ohmsche Verlustleistung | 1,568 W | – | – |
| Wechselstromwiderstand | **125,4 mΩ** | 55,3 mΩ (Einzeldraht-Formel) | Faktor 2,27 |
| Induktivität | **1,941 µH** | 2,03 µH (Wheeler) | 4,6 % |

Der Widerstand folgt aus dem Volumenintegral der Verlustdichte über das Kupfer,
R = 2P/I₀². Die Induktivität folgt aus dem Integral der magnetischen Feldenergie,
L = 4W/I₀². Beide Größen kommen also aus Feldintegralen und nicht aus einer Klemmengröße.

### Der Proximity-Effekt ist das eigentliche Ergebnis
Die Lehrbuchformel R = ρL/(2πaδ) beschreibt einen einzelnen, freistehenden Draht. In der Spule
liegen die Windungen nur 2 mm auseinander bei 3 mm Drahtdicke. Das Feld der Nachbarwindungen
drängt den Strom auf die dem Glas zugewandte Innenseite, und damit steht weniger als die Hälfte
des Umfangs für die Stromführung zur Verfügung. Der Widerstand steigt entsprechend auf das
2,3fache.

Das ist im Verlustdichte-Plot direkt sichtbar, als schmales helles Band auf der Innenseite jeder
Windung, während die Außenseite dunkel bleibt.

**Kein Literaturvergleich auf dieser Folie.** Naheliegend wäre der Wert von 1,07 Ω aus Dietz et al.
Der steht dort aber in der Tabelle "Parameters used in all simulations" und ist ein Eingabeparameter
für das globale Plasmamodell, also der Widerstand des gesamten Spulenzweigs im Ersatzschaltbild,
mit dem die Leistungsaufteilung zwischen Plasma und Spule berechnet wird. Wie er bestimmt wurde,
steht nicht im Paper, und Drahtdurchmesser und Wickelradius werden ebenfalls nicht genannt. Der Wert
ist deshalb nicht mit einem simulierten Wechselstromwiderstand einer blanken Helix vergleichbar.
Der Proximity-Effekt trägt sich auf dieser Folie allein durch das Bild und die Netzkonvergenz.

---

## Ergebnisse, thermisch

| Körper | Minimum | Maximum |
|---|---|---|
| Spule | 530,9 K / **257,7 °C** | 608,7 K / **335,6 °C** |
| Glas | 608,3 K / 335,2 °C | 733,1 K / **460,0 °C** |

Das Glas ist der heiße Körper, weil dort die 60 W eingespeist werden. Die Spule läuft kühler,
aber bei weitem nicht kühl: Sie sieht durch den Millimeter Spalt fast nur heißes Glas und nimmt
dessen Strahlung auf.

Die eigenen Verluste der Spule spielen dabei kaum eine Rolle. 1,57 W stehen gegen 60 W aus dem
Plasma. Ohne die Strahlungskopplung ans Glas käme die Spule auf etwa 55 °C. Die Temperatur der
Spule wird also nicht von ihrem eigenen Strom bestimmt, sondern davon, wie heiß das Gefäß neben
ihr ist.

---

## Warum man den Zahlen trauen kann

**Energiebilanz.** 60 W Plasma plus 1,57 W Spulenverluste ergeben 61,6 W. Setzt man das
Strahlungsgleichgewicht über die Außenfläche des Gefäßes an, mit εA ≈ 1,2·10⁻² m², kommt man
überschlägig auf 545 K. Der kälteste simulierte Punkt liegt bei 531 K.

**Induktivität.** 1,94 µH aus der Feldenergie gegen 2,03 µH nach Wheeler, also 4,6 % Abweichung
für eine Näherungsformel.

**Strahlungskopplung.** Das Maximum der Spule liegt bei 608,7 K, das Minimum des Glases bei
608,3 K. Vier Zehntel Kelvin. Über den Millimeter Spalt koppeln beide Körper so stark, dass sie
dort praktisch dieselbe Temperatur annehmen. Genau das erwartet man bei einem so kleinen Abstand
und Emissionsgraden von 0,3 und 0,9.

**Netzkonvergenz.** Die Randschichten wurden von drei auf fünf verdichtet, die erste Schicht von
30 auf 10 µm, also von einer ganzen auf ein Drittel Skintiefe. Zusätzlich wurde das
Oberflächennetz auf der Spule verfeinert.

| Netz | Randschichten | Oberfläche | Elemente | R aus Verlustintegral |
|---|---|---|---|---|
| A | 3 Schichten, erste 30 µm | max 2 mm | 316.948 | 131,1 mΩ |
| C | 5 Schichten, erste 10 µm | max 1,5 mm | 440.977 | 125,4 mΩ |

Der Widerstand ändert sich dabei um 4,3 %, die Temperaturen um 4 K, also 0,6 %. Ein noch
feineres Netz scheiterte am direkten Löser.

**Reproduzierbarkeit.** Drei Läufe auf demselben Netz liefern für das Verlustintegral auf zehntel
Milliwatt identische Werte.

---

## Konsequenzen für die Hardware

Die Spule liegt zwischen 258 und 336 °C, das Glas zwischen 335 und 460 °C. Daraus folgt direkt:

Weichlot schmilzt bei 183 bis 190 °C. Gelötete Verbindungen an der Spule fallen aus, es muss
hartgelötet oder geklemmt werden.

Elastomerdichtungen am Sockel sind ebenfalls erledigt, Viton geht bis etwa 200 °C.

PTFE ist mit einer Dauergrenze um 260 °C grenzwertig, Kapton mit rund 300 °C trägt gerade so.

Kupfer rekristallisiert oberhalb von etwa 200 °C und verliert seine Federhärte. Die Wicklung
hält ihre Form nicht mehr von selbst und braucht eine mechanische Halterung.

Das Quarzglas selbst ist bei 460 °C unkritisch, sein Erweichungspunkt liegt bei rund 1600 °C.

---

## Methodische Erkenntnis: das Coil-Feature liefert falsche Klemmengrößen

Dieser Abschnitt gehört nicht zwingend auf eine Folie, ist aber der Grund dafür, dass die
Auswertung über Volumenintegrale läuft.

COMSOLs Spulen-Feature gibt eine Klemmenspannung von rund 1,06·10⁵ V aus. Das entspräche einer
Induktivität von 856 µH statt der tatsächlichen 1,94 µH. Die Aufspaltung der Feldenergie
erklärt es: Von insgesamt 5,351 mJ stecken 5,339 mJ im **elektrischen** Anteil und nur
1,21·10⁻⁵ J im magnetischen. Im Interface für magnetische Felder gilt E = −jωA, und bei 4 MHz
multipliziert ω jede Unsauberkeit im Hilfspotential der Spulengeometrie-Analyse mit 2,5·10⁷.

Magnetfeld und ohmsche Verluste bleiben davon unberührt, weil beide nur am eingeprägten Strom
hängen. Der aus der Klemmenspannung gebildete Widerstand dagegen erbt den Defekt: Er driftet
beim Netzverfeinern nach oben, während das Verlustintegral nach unten konvergiert, und er
streut zwischen identischen Läufen um zwei Prozent, während das Integral auf zehntel Milliwatt
stabil bleibt.

---

## Einschränkungen

Die 60 W Plasmaleistung sind eine Annahme, keine Messung. Dietz arbeitet mit 30 bis 75 W am
Generator, Zorn nennt 100 W. Eine Parameterstudie über diesen Wert steht noch aus. Wegen der
vierten Potenz im Strahlungsgesetz ist die Temperatur allerdings robust: Von 60 auf 100 W sind
es nur etwa elf Prozent in Kelvin.

Der spezifische Widerstand des Kupfers ist konstant angesetzt. Bei 336 °C wäre er in
Wirklichkeit gut doppelt so groß, die Skintiefe entsprechend größer und der
Wechselstromwiderstand ebenfalls. Für die Temperatur ändert das wenig, für die Anpassung des
HF-Generators ist es relevant.

Die Eigenkapazität der Wicklung ist nicht im Modell. Bei 2 mm Windungsabstand liegt die
Eigenresonanz typischerweise im zweistelligen Megahertzbereich, also weit genug von 4 MHz
entfernt.

Halterung, Zuleitungen und Wärmeleitung über Befestigungspunkte fehlen. Beides würde die
realen Temperaturen eher senken.

---

## Nächste Schritte

Parameterstudie über die Plasmaleistung mit 30, 60 und 100 W. Das ist der stärkste Hebel und
zugleich die unsicherste Annahme, und es kostet dank der entkoppelten Studie 2 nur Minuten.

Stromstudie von 3 bis 7 A. Für die Temperatur nebensächlich, weil die Spulenverluste selbst bei
7 A nur 3,6 W betragen, für den Generator aber wichtig.

Temperaturabhängige Leitfähigkeit des Kupfers einbauen und damit die Rückkopplung heiße Spule
zu höherem Widerstand schließen.

---

## Verfügbare Abbildungen

`verlustdichte_20260930_151914.png`
Verlustdichte im Kupfer bei 4 MHz und 5 A, mit Farbskala in W/m³. Zu sehen ist das schmale
helle Band auf der dem Glas zugewandten Innenseite jeder Windung. Das ist die Abbildung für die
Proximity-Folie.

`temperatur_20260930_151959.png`
Temperaturfeld von Glas und Spule im stationären Zustand, mit Farbskala. Das Gefäß ist heiß,
die Spulenwindungen heben sich als kühlere Ringe ab, und der Hals oben ist durch Wärmeleitung
ebenfalls warm, obwohl dort kein Plasma sitzt.

Beide liegen im Ausgabeordner `C:\Users\Kristof\rfn_sim\output`.

---

## Vorschlag für die Foliengliederung

1. **Fragestellung und Modell.** Was simuliert wird und warum, mit einem Bild der Geometrie.
   Betriebspunkt 4 MHz, 5 A, 60 W auf die Glasinnenwand.
2. **Aufbau der Rechnung.** Drei gekoppelte Physiken, Strahlung als einzige Senke im Vakuum,
   Netzauflösung der Skintiefe. Kurz halten.
3. **Elektromagnetisches Ergebnis.** 125,4 mΩ und 1,94 µH, jeweils mit der Gegenrechnung daneben.
4. **Proximity-Effekt.** Verlustdichte-Bild und Faktor 2,3 gegenüber der Einzeldraht-Formel.
   Kein Literaturvergleich, Begründung siehe oben.
5. **Thermisches Ergebnis.** Temperaturbild plus die vier Zahlen für Spule und Glas.
   Der Satz, dass die Spulentemperatur vom Glas kommt und nicht von den eigenen Verlusten.
6. **Konsequenzen für die Hardware.** Weichlot, Dichtungen, Kupferfestigkeit.
7. **Validierung.** Energiebilanz, Wheeler, Netzkonvergenz. Kompakt als Tabelle.
8. **Offene Punkte und nächste Schritte.**

Bei sechs Folien lassen sich Punkt 2 und 7 zusammenlegen und Punkt 8 auf die letzte Folie
schieben.

---

## Quellen

Dietz et al. (2020), EPJ Applied Physics. Quarzgefäß Ø 4 cm × 3,5 cm, 7 Windungen,
Betriebsfrequenz etwa 2,4 MHz, Generatorleistung 30 bis 75 W. Wird hier als Beleg dafür
herangezogen, dass Betriebspunkt und Gefäßgröße unseres Aufbaus im üblichen Rahmen liegen.
Der dort angegebene Spulenwiderstand von 1,07 Ω ist ein Eingabeparameter des globalen Modells
und taugt nicht als Vergleichswert für eine feldbasierte Rechnung.

Zorn et al. (2025), Journal of Electric Propulsion. RF-Neutralisator bei 1,3 bis 2,0 MHz,
100 W, 100 mA Emissionsstrom.
