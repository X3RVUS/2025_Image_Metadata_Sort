-----

# Metadaten-basierter Bild-Sortierer (Image Sorter by Metadata)

Dieses Python-Skript organisiert automatisch deine Fotosammlung, indem es die EXIF-Metadaten (Aufnahmedatum und GPS-Standort) ausliest und die Bilder in eine übersichtliche Ordnerstruktur verschiebt.

Verabschiede dich von unübersichtlichen Ordnern mit tausenden von Bildern und begrüße eine perfekt sortierte Bibliothek nach **Jahr**, **Monat** und **Aufnahmeort**.

-----

## 📂 Funktionsweise

Das Skript verwandelt eine flache Ordnerstruktur in eine logisch verschachtelte Hierarchie.

**VORHER:**

```
input_Image/
├── IMG_1001.JPG  (Juni 2024, Berlin)
├── IMG_1002.JPG  (Juni 2024, Berlin)
├── DJ_0050.JPG   (Dezember 2023, München)
├── P100025.JPG   (Juli 2024, Hamburg)
└── ...
```

**NACHHER:**

```
Bilder_Sortiert/
└── 2023/
|   └── 12_Dezember/
|       └── München/
|           └── 2023_DJ_0050.JPG
|
└── 2024/
    ├── 06_Juni/
    |   └── Berlin/
    |       ├── 2024_IMG_1001.JPG
    |       └── 2024_IMG_1002.JPG
    |
    └── 07_Juli/
        └── Hamburg/
            └── 2024_P100025.JPG
```

-----

## ✨ Features

  * **Vollautomatische Sortierung**: Verschiebt Bilder basierend auf ihren Metadaten.
  * **Logische Ordnerstruktur**: Erstellt eine Hierarchie nach `Jahr > Monat > Ort`.
  * **Intelligente Datumserkennung**: Nutzt das EXIF-Aufnahmedatum. Falls dieses fehlt, wird das Änderungsdatum der Datei als Alternative verwendet.
  * **Geolokalisierung**: Liest GPS-Koordinaten aus den EXIF-Daten.
  * **Reverse Geocoding**: Wandelt GPS-Koordinaten mithilfe einer Online-API in reale Ortsnamen (z.B. Städtenamen) um.
  * **Flexibel**: Bilder ohne GPS-Informationen werden in einem anpassbaren Standardordner (z.B. `Unbekannter_Ort`) abgelegt.
  * **Anpassbar**: Eingabe- und Ausgabeordner sowie weitere Optionen können einfach am Anfang des Skripts konfiguriert werden.

-----

## ⚙️ Installation

1.  **Klone das Repository:**

    ```bash
    git clone https://github.com/DEIN_BENUTZERNAME/DEIN_PROJEKTNAME.git
    cd DEIN_PROJEKTNAME
    ```

2.  **Erstelle eine `requirements.txt`-Datei** mit folgendem Inhalt:

    ```
    Pillow
    geopy
    ```

3.  **Installiere die Abhängigkeiten:**

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🚀 Anwendung

1.  **Bilder vorbereiten**: Lege alle Bilder, die du sortieren möchtest, in den Ordner `input_Image`. Falls dieser Ordner nicht existiert, wird er beim ersten Ausführen des Skripts automatisch erstellt.
2.  **Skript ausführen**: Starte das Skript über dein Terminal. Es sind keine weiteren Argumente notwendig.
    ```bash
    python dein_skript_name.py
    ```
3.  **Ergebnis prüfen**: Nach Abschluss des Vorgangs findest du deine sortierten Bilder im Ordner `Bilder_Sortiert`.

> **Wichtiger Hinweis:** Für die Umwandlung von GPS-Koordinaten in Ortsnamen benötigt das Skript eine **aktive Internetverbindung**.

-----
