# RFN Geometrie Version 11: neue Blendenaufnahme für COMSOL

Stand 23. Oktober 2026. Übergabe aus dem Konstruktionschat an den COMSOL-Chat.
Quelle ist `RFN_Aufnahme_Parameter.xlsx` Stand v5d. Parameterdatei zum Laden:
`claude/rfn_parameter_v11.txt`. Ausgangsmodell ist `Spule_test_10.mph` mit seinen
elf Gebieten aus `rfn-netz-und-gebiet.md`.

Kurz vorweg, damit die Arbeit richtig eingeschätzt wird: Das ist kein Satz neuer
Zahlenwerte. Die untere Aufnahme ist neu konstruiert. Ring_unten aus Aluminium,
Isolierring, axialer Dichtring und Wellenfeder gibt es nicht mehr. Glas, Spule,
Vakuumkugel und Abdeckblech bleiben.

## 1. Koordinaten

Glasboden und Spule bleiben, wo sie sind. Der Glasboden liegt weiter bei
z_COMSOL = −26,85, und auf ihm liegt jetzt direkt die Blende. In der
Konstruktion zählt z ab der Blendenunterseite, deshalb gilt

    z_COMSOL = z_Konstruktion − 27,35

Alle Maße unten sind schon umgerechnet. Radien ab der Achse, in mm.

## 2. Die drei Antworten

**Zahlenwerte.** Für Glas, Spule und Vakuumkugel bleiben alle Werte gleich.
Bei Blende und GFK-Ring oben reicht es, Zahlen zu ändern. Für alle anderen
Teile gibt es neue Profile, Tabelle in Abschnitt 4.

**Gebiete.** Die Zahl steigt von 11 auf 12. Isolierring wird zum Träger und
Ring_unten zum Edelstahlring, beide als neue Profile in derselben Rolle.
Vakuum_nut fällt weg, weil die Restspalte der neuen Nut an bestehenden Vakuumgebieten hängen. Klemmring und flacher O-Ring kommen dazu. Lässt man den
flachen O-Ring weg, bleibt es bei 11. Die Nummern verschieben sich so oder so,
weil COMSOL nach der Lage nummeriert und nicht nach dem Feature.

**Kontaktflächen.** Sie ändern sich grundlegend. Die Blende war vorher an
knapp 80 mm² mit dem Glas verbunden und an gut 150 mm² mit GFK. Jetzt liegt
sie mit 2410 mm² auf dem Klemmring aus Stahl und mit gut 1000 mm² am GFK-Träger.
Der obere GFK-Ring hat keinen Metallkontakt mehr, er schwebt 0,3 mm über dem
Stahl. Die neue Wärmesenke ist die Auflage des Edelstahlrings auf der
Frontplatte. Die Ergebnisse von gestern sind deshalb nicht mit Version 11
vergleichbar.

## 3. Bauteile

Nicht rotationssymmetrische Details lässt das Modell weg. Dazu gehören
Bohrungen, Gewinde, Lasche, Schlitz, Kerben, Entlüftungsbohrungen, Federn,
Hülsen, Schrauben und Keramikhülse. Für Wärmeleitung und Feld spielen sie
keine nennenswerte Rolle. Wo sie doch etwas beitragen, steht es dabei.

### Blende (bleibt, Maße ändern sich)

Molybdän wie bisher, `sigma_mo`, `eps_mo` 0,2. Volumen im Feld mit
Randschichten wie bisher.

    Rechteck   r 3 bis 36   z −27,35 bis −26,85   (vorher r 3 bis 25, 0,3 dick)
    Volumen    2022 mm³ mit Ø6-Öffnung             (vorher 581)

Die Blende ist jetzt ein Wechselteil Ø72. Ihr Rand sitzt in der Tasche des
Trägers, unten liegt der Klemmring, oben stehen Glas und Träger. Mit 0,5 mm
Dicke gehen vier Randschichten zu 15 µm mit Faktor 1,3 bequem hinein, je Seite
93 µm.

### Klemmring (neu)

1.4301, `sigma_st` 1,39e6 S/m, Skintiefe 213 µm bei 4 MHz. Dicke 1,5 mm,
das sind 7 Skintiefen, also passt er in `mf_passiv` mit Impedanzrandbedingung.

    Rechteck   r 23 bis 36   z −28,85 bis −27,35
    Volumen    3614 mm³

Er drückt die Blende von unten an den Träger und gehört elektrisch zur Blende.
Zu Stahlring und Frontplatte ist er durch den Träger isoliert. Mit dem Rand
liegt er in der Tasche, im Modell mit 0,5 mm Luft (siehe Träger).

### Träger (ersetzt den Isolierring)

GFK wie bisher, also ρ 1900, cp 1000, `k_gfk`, `eps_gfk` 0,9. Bleibt im
Feldgebiet wie der Isolierring.

    Profil, geschlossen
    A  r 31,3   z −26,85     Taschenboden innen
    B  r 36,5   z −26,85
    C  r 36,5   z −28,85     Taschenwand
    D  r 40,0   z −28,85     Unterseite
    E  r 40,0   z −22,85     Außenwand = Bohrung Frontplatte
    F  r 31,3   z −22,85     Oberseite
    Volumen    9477 mm³

Zwei bewusste Modellvereinfachungen gibt es hier. Die Bohrung hat real r 31,1
und damit 0,1 mm Spiel zum Glasfuß. Im Modell sitzt sie auf r 31,3 wie die
Stahlbohrung. Die Taschenwand liegt real bei r 36,05, also 0,05 mm neben Blende
und Klemmring. Im Modell steht sie auf r 36,5. Im Vakuum leitet ein Spalt von
0,05 oder 0,5 mm gleich wenig, die Strahlung hängt nicht von der Spaltweite ab.
Einen Splitter von 0,05 mm wollen wir nach der Erfahrung mit `Lösche Details`
aber nicht im Netz haben.

### Edelstahlring (ersetzt Ring_unten)

1.4301 statt Aluminium, `sigma_st`, `eps_st` 0,3 als Annahme. Bleibt in
`mf_passiv` mit Impedanzrandbedingung.

    Profil, geschlossen, gegen den Uhrzeigersinn
    r 31,30  z −22,85      Unterseite innen
    r 32,40  z −22,85      Flachnut
    r 32,40  z −22,10
    r 33,80  z −22,10
    r 33,80  z −22,85
    r 44,00  z −22,85      Unterseite außen
    r 44,00  z −17,35      Außenwand
    r 31,30  z −17,35      Oberseite
    r 31,30  z −18,05      Bohrung über der Radialnut
    r 33,05  z −18,05      Radialnut, Grund Ø66,1
    r 33,05  z −21,65
    r 31,30  z −21,65      Bohrung unter der Radialnut
    Volumen    15 032 mm³   (Ring_unten vorher 23 968)

Real gibt es auf der Unterseite noch eine Entlüftungsnut, r 36,5 bis 38,5 und
0,3 tief. Sie würde eine geschlossene Vakuumtasche zwischen Stahl und Träger
bilden, also ein weiteres Gebiet. Ich würde sie weglassen. Der Preis dafür:
Die Kontaktfläche Stahl–Träger ist im Modell 1658 statt 1186 mm².

Zur Impedanzrandbedingung: Die dünnsten Stege sind 0,45 mm zwischen Flachnut
und Radialnut und 0,7 mm über der Radialnut. Das sind nur 2 bis 3
Skintiefen. Weil die unterste Windung 1,1 mm über der Oberseite liegt, ist das
die Stelle, an der der Feldteil am ehesten nachgeprüft werden sollte.

### O-Ring radial (ersetzt den Dichtring)

FFKM wie der alte Dichtring. Größe 61,5 × 2,65. Im Modell als
**flächengleiches Rechteck**, das radial von Glas bis Nutgrund reicht und
mittig in der Nut sitzt:

    Rechteck   r 31,0 bis 33,05   z −21,195 bis −18,505   (Höhe 2,69)
    Querschnitt 5,52 mm² = π/4 · 2,65²
    Volumen    1110 mm³

Die beiden Restspalte in der Nut erzeugen kein neues Gebiet. Der untere,
0,45 hoch, hängt am Ringspalt und gehört zu Vakuum_ringspalt. Der obere hängt
am 0,3-Spalt über der Nut und gehört zu Vakuum_haupt. Das ist der Unterschied
zum alten Modell: Dort war der Rest der axialen Nut rundum von Alu, Glas und
Ring eingeschlossen, deshalb gab es Vakuum_nut.

Nutfüllend wäre einfacher, ist aber schlechter. Der Ring ist ein Wärmepfad vom
Glasfuß in den Stahl, und kein ganz kleiner: Mit k = 0,2 W/(m·K), 2,05 mm
Weg und 2,69 mm Kontakthöhe leitet er rund 0,05 W/K. Bei 100 K Unterschied
sind das gut 5 W. Ein nutfüllendes Rechteck mit 3,6 mm Kontakthöhe läge ein
Drittel darüber. Auch das flächengleiche Rechteck überschätzt noch, weil ein
verpresster O-Ring real nur auf etwa 1,5 mm Breite anliegt. Für eine
Abschätzung nach unten kann man die Höhe im Modell auf 1,5 setzen.

### O-Ring flach (neu, optional)

FFKM, 64 × 1, in der Flachnut auf der Stahlunterseite, ebenfalls nutfüllend:

    Rechteck   r 32,4 bis 33,8   z −22,85 bis −22,10
    Volumen    218 mm³

Hier ist nutfüllend in Ordnung. Flächengleich wären es r 32,4 bis 33,45, und
der Rest der Nut außen wäre ein geschlossener Vakuumring, also ein eigenes
Gebiet. Der Ring liegt parallel zur direkten Auflage Stahl auf GFK, die mit
rund 1650 mm² viel größer ist, sein Fehler geht darin unter. Lässt man den
Ring ganz weg, ist die Flachnut ebenfalls ein geschlossener Vakuumring und ein
eigenes Gebiet. Willst du kein zwölftes Gebiet, dann lass Nut und Ring beide weg. Die
Stahlunterseite liegt dann von r 31,3 bis 44 flach auf, und der Kontakt
Stahl–Träger wird 1949 mm².

### GFK-Ring oben (bleibt, Maße ändern sich)

GFK wie bisher. Stand v7 vom 24. Oktober: Die Spule läuft jetzt innen im Ring,
das Modell und der reale Ring sind damit gleich.

    r 30,4 bis 43,5     z −17,05 bis −11,15
    Glassenkung unten   bis r 31,1, 0,4 tief, also Fläche bei z −16,65
    Volumen    17 890 mm³ (ohne Bohrungen)

    Real zusätzlich: Fase 0,1 innen, Anschlussnut für das untere Spulenende bei 140°

Die unterste Windung liegt bei r 27,1 bis 30,1 und z −16,25, also 0,4 mm über
der Fußoberseite. Zwischen Spule und Ringbohrung bleiben 0,3 mm. Der Ring
drückt auf den Glasfuß nur auf r 30,4 bis 31, das sind 116 mm². Die Senkung
r 31,1 zentriert ihn mit 0,1 mm Spiel auf dem Fuß. Auf dem Stahl liegt der Ring
nicht auf. Zwischen seiner Unterseite und der Stahloberseite bleiben 0,3 mm,
und dieser Spalt ist nach außen zum Abdeckblech offen, gehört also zu
Vakuum_haupt.

### Glas, Spule, Vakuumkugel

Unverändert. Glasfuß r 31, Boden eben r 24,5 bis 29,5, Fase 1,5 × 45° außen,
R1-Hohlkehle am Übergang zum Hals.

### Abdeckblech

Aluminium, unverändert bis auf die Unterkante. Die Bleche enden an der
Vorderseite der Frontplatte, und die liegt jetzt bei z −22,85 statt −23,45.
Der Innenradius muss mindestens 44 betragen. Zwischen Blech und GFK-Ring
bleibt dann ein Spalt von 0,5 mm.

### Frontplatte

Sie ist bisher nicht im Modell und muss es auch jetzt nicht sein. Sie ist aber
die Wärmesenke, siehe Abschnitte 6 und 7.

## 4. Parameter alt und neu

Die alten Namen stammen aus `RFN_Dichtung_Parameter.xlsx` v8. Sie stecken
größtenteils auch in `rfn_parameter_v9.txt`. Namen, die nur im COMSOL-Modell
existieren, etwa `t_iso`, kenne ich nicht genau. Sie sind nach Bauteil
einzuordnen: Alles, was zum Isolierring, zur Wellenfeder, zum Alusteg, zur
axialen Nut oder zur Passscheibe gehört, fällt weg.

| alt | Wert alt | neu | Bemerkung |
|---|---|---|---|
| `d_blende` | 0,3 | `t_bl` 0,5 | |
| — | r 25 | `r_bl_a` 36 | Blende Ø72 |
| `r_glas_eben` | 29,5 | 29,5 | bleibt |
| `h_glas_fuss` | 10,2 | 10,2 | bleibt |
| `t_gfk_ring` | 5,9 | `t_ro` 5,9 | bleibt |
| `h_gfk_senk` | 0,9 | `h_ro_senk` 0,4 | |
| — | r 42,5 | `r_ro_a` 43,5 | |
| — | z −17,45 | `z_ro_u` −17,05 | folgt aus der Senkung |
| `r_alu_bohr` | 32 | `r_st_i` 31,3 | Stahlbohrung |
| `d1_oring` | 54 | entfällt | axialer Ring entfällt, neu radial 61,5 × 2,65 |
| `d2_oring` | 1,5 | entfällt | |
| `t_nut`, `b_nut`, `r_nut_a`, `r_nut_i`, `r_kante`, `sp_radial` | | entfällt | axiale Nut in Ring_unten. Neu `r_nr_a`, `z_nr_u`, `z_nr_o` |
| `r_oring_m`, `r_oring_a`, `a_ell`, `b_ell`, `r_ell_m` | | entfällt | |
| `t_steg`, `sp_steg` | 1,0 / 0,15 | entfällt | kein Alusteg, das Glas steht auf der Blende |
| `h_iso_bett`, `h_iso_kragen`, `r_iso_i`, `r_iso_bett`, `r_iso_a`, `h_iso_unten`, `sp_blende` | | entfällt | Isolierring. Neu Träger `r_tr_*`, `z_tr_*` |
| `fw_iso`, `h_tasche_iso`, `h_feder_min`, `h_tasche_fert` | | entfällt | Wellenfeder und Isoliertasche |
| `h_alu_steg_rand`, `t_tasche`, `s_scheibe`, `k_scheibe`, `luft_rand` | | entfällt | GFK-Tasche im Alu und Passscheibe |
| `s_verpress`, `s_max`, `f_kalt` | | entfällt | Kennwerte, keine Geometrie |
| Ring_unten-Profil | r 24…44, z −29,45…−11,45 | Edelstahlring-Profil | neu, Abschnitt 3 |
| Abdeckblech Unterkante | −23,45 | `z_blech_u` −22,85 | |

Neu sind alle Parameter in `claude/rfn_parameter_v11.txt`, 37 Zeilen, Format
für „Aus Datei laden“. Dazu kommen `eps_st` und `sigma_st` für den Stahl.

## 5. Gebiete

COMSOL nummeriert nach der Lage. Die Nummern unten sind die Rolle aus Version
10, nicht die Nummer, die nach dem Neuaufbau herauskommt.

| Rolle v10 | Gebiet v10 | v11 | Material | Feld | Änderung |
|---|---|---|---|---|---|
| Vakuum_haupt | 1 | bleibt | Vakuum | aktiv | enthält jetzt den 0,3-Spalt unter dem GFK-Ring und den 0,5-Spalt an der Tasche |
| Abdeckblech | 2 | bleibt | Alu | passiv | Unterkante −22,85 |
| Ring_unten | 3 | **Edelstahlring** | 1.4301 statt Alu | passiv | neues Profil, neues Material |
| Vakuum_ringspalt | 4 | bleibt, viel kleiner | Vakuum | aktiv | Glasfase, 0,3-Spalt und unterer Nutrest bis zum O-Ring, 621 statt 3289 mm³, weiterhin abgeschlossen |
| Ring_oben | 5 | bleibt | GFK | aktiv | Zahlenwerte |
| Glas | 6 | bleibt | Quarz | aktiv | |
| Dichtring | 7 | **O-Ring radial** | FFKM | aktiv | andere Lage, flächengleich |
| Vakuum_nut | 8 | **entfällt** | | | die Nutreste hängen an Ringspalt und Vakuum_haupt |
| Isolierring | 9 | **Träger** | GFK | aktiv | neues, größeres Profil |
| Blende | 10 | bleibt | Mo | aktiv, Volumen | Zahlenwerte |
| Spule | 11 | bleibt | Cu | aktiv | |
| — | — | **Klemmring, neu** | 1.4301 | passiv | |
| — | — | **O-Ring flach, neu** | FFKM | aktiv | optional, siehe Abschnitt 3 |

Damit das Nachziehen nur einmal nötig ist und nie wieder: Stell alle benannten
Auswahlen vor dem Neuaufbau auf Geometrie-Auswahlen um. In jedem Rotations-
und Primitiv-Knoten der Geometrie gibt es unter *Auswahlen der resultierenden
Objekte* den Punkt *Ergebnisobjekte als Auswahl erstellen*, dazu *Beitragen
zu* eine benannte Auswahl. Diese Auswahlen überleben den Verbund und jede neue
Nummerierung. Für Ränder geht das über *Angrenzende Auswahl* oder *Box-Auswahl*
auf diesen Gebietsauswahlen.

Was nachgezogen werden muss:

- **`mf_passiv`**: Edelstahlring, Abdeckblech, Klemmring.
- **`Impedanz_BC`**: alle Ränder der drei passiven Leiter, mit eigenem σ je Werkstoff. Neu ist die Grenzfläche Klemmring–Blende. Dort grenzt ein passiver an einen aktiven Leiter. Ich würde dort die Impedanzbedingung mit Stahl ansetzen.
- **`Strahlungsflaechen`**: alle Ränder fester Körper gegen Vakuum. Neu sind Klemmring unten, innen und außen, Träger unten, Taschenwand und Bohrung, die Stahlbohrung, die Unterseite des GFK-Rings gegen den 0,3-Spalt und die Blende unten r 3 bis 23. Die Flächen im abgeschlossenen Ringspalt strahlen nur untereinander.
- **Diffuse Oberflächen**: Der Knoten für Ring_unten mit dem Emissionsgrad von Aluminium gilt jetzt für Stahl mit `eps_st`. Der Klemmring kommt dazu.
- **Netzknoten**: Isolierring auf Träger umhängen, mit h wie GFK. Klemmring wie Ring_unten, weil passiv. Für den flachen O-Ring `h_di`. Die Randschichten der Blende müssen auf ihren beiden Flachseiten neu gewählt werden.
- **Kontrolle**: Bei der Blende muss das Volumenintegral 2022 mm³ ergeben, beim Klemmring 3614, beim Träger 9477, beim Edelstahlring 15 032, beim GFK-Ring 17 890, beim radialen O-Ring 1110, beim Ringspalt 621.

## 6. Kontaktflächen

Wärme fließt im Vakuum nur über Berührung und Strahlung. An dieser Tabelle
hängt das Ergebnis.

| Kontakt | v7 bis v10 laut Notizen | v11 | Fläche v11 |
|---|---|---|---|
| Glasboden – Blende | r 24,5 bis 25 | r 24,5 bis 29,5 | 848 mm² (vorher 78) |
| Glasboden – GFK unten | r 25 bis 26, Isolierring | entfällt | — |
| Blende – GFK | r 24 bis 25, Isolierring | Blende oben an den Taschenboden des Trägers, r 31,3 bis 36 | 994 mm² (real 1033, vorher 154) |
| Blende – Stahl | — | Blende unten auf den Klemmring, r 23 bis 36 | **2410 mm², neu** |
| Klemmring – Träger | — | nur am Rand, im Modell 0,5 Luft | kein Kontakt |
| Träger – Edelstahlring | — | Trägeroberseite an die Stahlunterseite | 1658 mm² mit Flachnut, 1186 real mit Entlüftungsnut |
| Glas – Ring_unten / Stahl | kein Kontakt, 0,15 Luft | kein Kontakt, 0,3 Luft | — |
| Glas – Träger | — | kein Kontakt, real 0,1 Luft | — |
| Glas – O-Ring – Stahl | über den Dichtring | über den radialen O-Ring, Kontakthöhe 2,69 | rund 0,05 W/K, also einige W, siehe Abschnitt 3 |
| Glasfuß oben – GFK-Ring oben | ja, Option C r 30,6 bis 31 | r 30,4 bis 31, auch real so | 116 mm² |
| GFK-Ring oben – Metall | in der Alutasche, bitte im Modell nachsehen | **kein Kontakt**, 0,3 Luft zum Stahl | — |
| Abdeckblech – Ring | am Aluring | am Edelstahlring r 44 | wie bisher |
| Edelstahlring – Frontplatte | — | Unterseite r 40 bis 44 | 1056 mm², **die Wärmesenke** |
| Träger – Frontplatte | — | Außenwand r 40, Passung | 1508 mm² |

Was das physikalisch bedeutet:

- Die Blende hängt jetzt flächig am Klemmring aus Stahl. Der Klemmring hat aber keinen eigenen Weg nach außen. Er berührt nur die Blende und gibt Wärme über Strahlung nach hinten ab. Zwischen ihm und dem Stahlring liegt immer GFK.
- Der Weg Blende → Träger → Edelstahlring → Frontplatte führt durch 4 mm GFK. Das ist der engste Engpass im neuen Aufbau, und genau dort sitzt die Frage, ob der Träger unter seiner Glasübergangstemperatur bleibt.
- Der GFK-Ring oben gibt nichts mehr an Metall ab. Er hängt nur am Glasfuß und strahlt über den 0,3-Spalt zum Stahl.
- Aluminium leitet mit 237 W/(m·K), Edelstahl mit 16. Der Ring selbst verteilt die Wärme also schlechter, sein Emissionsgrad ist aber höher.

## 7. Was sich außer der Thermik verschiebt

**Feldteil.** Der Edelstahlring sitzt dort, wo der Aluring war, also direkt
unter der untersten Windung. Bei gleichem Feld steigt der
Oberflächenwiderstand mit der Wurzel aus σ_Al/σ_St, also etwa um den Faktor 5.
Die 434 mW in Aluring und Blech werden deshalb deutlich steigen, und der Stahl
verdrängt weniger Fluss, L fällt also weniger stark. Beides ist Ergebnis,
kein Fehler. Edelstahl 1.4301 hat μr ≈ 1. Durch das Zerspanen kann er leicht
magnetisch werden, das gehört aber nicht ins Modell.

**Wärmesenke.** Die geplante thermische Anbindung als Sweep über `h_anb`
gehört jetzt an zwei Flächen. Die erste ist die Unterseite des Edelstahlrings
bei r 40 bis 44 und z −22,85. Die zweite ist die Außenwand des Trägers bei
r 40. Eine Frontplatte ins Modell zu nehmen, ist nicht nötig.

## 8. Offene Punkte

1. **Spulenlage.** Seit v7 passt der Ring zur Modellspule, die unterste
   Windung läuft innen im Ring. Die reale Lage der untersten Windung am ersten
   RFN muss trotzdem gemessen werden, ebenso die Rundung an der Außenkante des
   Glasfußes. Sie muss kleiner bleiben als die 0,5 mm breite Auflage.
2. **Entlüftungsnut und flacher O-Ring.** Beide sind vereinfacht, Abschnitt 3.
   Beide ändern nur die Kontaktfläche Stahl–Träger.
3. **Emissionsgrad Stahl.** `eps_st` 0,3 ist geschätzt, gedreht und leicht
   oxidiert. Ein Sweep von 0,2 bis 0,5 lohnt sich zusammen mit `eps_blech`.
4. **O-Ring-Temperatur.** Der radiale FFKM-Ring sitzt bei z −21,65 bis −18,05
   am Glasfuß. Das ist die zweite Zahl, die aus Version 11 herauskommen muss,
   neben der Trägertemperatur. FFKM hält dauerhaft etwa 300 °C.
