# Project Jump

##  Projektbeschreibung
Dieses Projekt verbindet einen ESP32 mit einem Laptop via Bluetooth, um ein Spiel durch physische Sprungbewegungen zu steuern. Der ESP32 erkennt Sprünge und sendet ein Signal an den Laptop, der die Eingabe verarbeitet und an das Spiel weiterleitet.

##  Ordnerstruktur
Das Repository enthält folgende Ordner:

- **HWSE_FSTW/** – Enthält den Code und die Konfiguration für den ESP32.
- **HWSE_FSTW_Laptop_Bluetooth/** – Code für die Bluetoothverbindung zwischen Laptop und ESP32.
- **Sonstiges/** – Enthält Präsentationen, Plots und weitere relevante Dateien.
- **Spiel/** – Der Code für das eigentliche Spiel.

##  Installation & Einrichtung
### Voraussetzungen
- Python 3.x
- Ein ESP32 mit MicroPython
- Bluetooth-fähiger Laptop
- Benötigte Python-Abhängigkeiten (siehe `requirements.txt`)

### Setup
1. **ESP32 vorbereiten**
   - Stelle sicher, dass MicroPython auf dem ESP32 installiert ist.
   - Lade den Code aus dem `HWSE_FSTW/` Ordner auf den ESP32 hoch.
   - Starte den ESP32.

2. **Laptop verbinden**
   - Stelle sicher, dass Bluetooth aktiviert ist.
   - Führe den Code im `HWSE_FSTW_Laptop_Bluetooth/` Ordner aus, um die Verbindung herzustellen.

3. **Spiel starten**
   - Öffne den `Spiel/` Ordner und starte das Spiel-Skript.
   - Das Spiel wird nun durch Sprünge gesteuert!

##  Features
- Echtzeit-Sprungdetektion mit ESP32 und IMU
- Bluetooth-Kommunikation zwischen ESP32 und Laptop
- Interaktive Spielsteuerung durch Bewegung
- Visualisierung von Sprungdaten (Plots in `Sonstiges/`)

##  Weiterentwicklung
Geplante Features:
- Automatische Kalibrierung der Sprunghöhe
- Erweiterte Spielmechaniken
- Optimierung der Bluetooth-Kommunikation
