#Imports
import asyncio #asyncio ermöglicht, asynchrone Funktionen auszuführen
from bleak import BleakClient #Bleak ermöglicht, mit Bluetooth Low Energy (BLE) Geräten zu kommunizieren
import keyboard  #Bibliothek zur Simulation von Tasteneingaben

# Die MAC-Adresse des ESP32
ESP32_ADDRESS = "7C:9E:BD:61:9E:76"  # Unsere Mac-Adresse des ESP32

# UUIDs für den Service und die Charakteristik, die auf dem ESP32 registriert sind.
SERVICE_UUID = "00001818-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Funktion, die aufgerufen wird, wenn Benachrichtigungen von der angegebenen Charakteristik empfangen werden.
def notification_handler(sender, data):
    message = data.decode("utf-8").strip()
    print(f"Empfangen: {message}")  # Ausgabe der empfangenen Nachricht
    if message == "Sprung":
        print("Simuliere Tastendruck: Leertaste")
        keyboard.press_and_release('space')  # Leertaste simulieren

# Asynchrone Funktion, die den BLE-Client steuert und mit dem ESP32 verbindet.
async def run():
    async with BleakClient(ESP32_ADDRESS) as client:
        print(f"Verbunden mit {ESP32_ADDRESS}")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Warte asynchron auf Benachrichtigungen, ohne künstliche Pausen
        await asyncio.Event().wait()  # Blockiere den Task ohne Verzögerung

# Hauptaufruf, um die asynchrone Funktion zu starten
asyncio.run(run())