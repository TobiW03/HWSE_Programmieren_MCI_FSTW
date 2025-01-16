
# Wir importieren die notwendigen Bibliotheken:
import asyncio
from bleak import BleakClient
import keyboard  # Neue Bibliothek zur Simulation von Tasteneingaben

# Die MAC-Adresse des ESP32. Diese muss mit der tatsächlichen MAC-Adresse des ESP32 übereinstimmen.
ESP32_ADDRESS = "7C:9E:BD:61:9E:76"  # Beispiel: Ersetze dies mit der korrekten MAC-Adresse

# UUIDs für den Service und die Charakteristik, die auf dem ESP32 registriert sind.
SERVICE_UUID = "00001818-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Funktion, die aufgerufen wird, wenn Benachrichtigungen von der angegebenen Charakteristik empfangen werden.
def notification_handler(sender, data):
    message = data.decode("utf-8").strip()
    print(f"Empfangen: {message}")  # Ausgabe der empfangenen Nachricht
    if message == "Sprungn":
        print("Simuliere Tastendruck: Leertaste")
        keyboard.press_and_release('space')  # Leertaste simulieren

# Asynchrone Funktion, die den BLE-Client steuert und mit dem ESP32 verbindet.
async def run():
    async with BleakClient(ESP32_ADDRESS) as client:
        print(f"Verbunden mit {ESP32_ADDRESS}")
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Endlosschleife, um die Benachrichtigungen zu empfangen.
        while True:
            await asyncio.sleep(1)

# Hauptaufruf, um die asynchrone Funktion zu starten
asyncio.run(run())
