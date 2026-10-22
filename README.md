# ABEP_Koppeltest

## Struktur

```
CAD/                            Alle CAD-Baugruppen (Inventor .ipt/.iam, Zeichnungen .dwg)
├── Assembly_ABEP_Koppeltest.iam Gesamtbaugruppe
├── RF-Neutralisator/            RF-Neutralisator (aktueller Stand nach Redesign)
│   ├── Innenteil/
│   ├── Archiv_Sicherung_ohne_Federn/  Aeltere Variante ohne Federn, archiviert
│   ├── Zeichnungen/
│   └── OldVersions/              Inventor-Backups, nicht in Git (siehe .gitignore)
├── Aufhängung/                  Aufhängung/Drehscheibe
├── Halterung/                   Halterung (frueher "Koppeltest_Halterung")
├── 19K_001_010_00_A_RIM_10_2019_EFRE_3D_2024_0228/   Aelteres Projekt (historisch, Name gewachsen)
└── 22K_006_020_10_A_ZSB_VAKUUMTANK_F_ALT_TREIB_3D_20230427/  Aelteres Projekt (historisch, Name gewachsen)

Fertigung/                      Zeichnungen (.dwg) und STEP-Dateien (.stp) fuer die Werkstatt,
├── RF-Neutralisator/             gegliedert nach Baugruppe. Manuell gepflegte Kopien aus den
├── Aufhängung/                   jeweiligen CAD/<Baugruppe>/Zeichnungen/-Ordnern - nach jeder
└── Halterung/                    Revision hier manuell nachziehen, sonst veraltet der Stand.

COMSOL/                         Simulationsergebnisse (Briefing, Temperatur-/Verlustdichte-Plots)
Praesentation/                  LaTeX-Vortragsfolien
```

## Hinweise

- `OldVersions/`-Ordner werden von Autodesk Inventor automatisch beim Speichern
  angelegt (Tools -> Application Options -> Save-Tab -> "Old versions to keep",
  auf 0 stellen, um es abzuschalten).
  Sie sind seit der Repo-Reorganisation (2026-10) nicht mehr Teil von Git —
  die Git-Historie uebernimmt die Versionierung. Lokal bleiben sie auf der
  Platte, soweit Inventor sie weiterhin anlegt.
- Grosse CAD-Binaerformate (`*.ipt`, `*.iam`, `*.dwg`, `*.stp`) laufen seit
  2026-10 ueber Git LFS. Fuer bereits aeltere committete Dateien gilt das erst,
  sobald sie das naechste Mal gespeichert und committet werden.
