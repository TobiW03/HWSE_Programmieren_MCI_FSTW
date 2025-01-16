# Wir importieren die notwendigen Bibliotheken:
# `asyncio` für die Verwaltung von asynchronen Aufgaben
# `BleakClient` aus der Bleak-Bibliothek, um mit BLE-Geräten zu kommunizieren.
import asyncio
from bleak import BleakClient

# Die MAC-Adresse des ESP32. Diese muss mit der tatsächlichen MAC-Adresse des ESP32 übereinstimmen.
# Die MAC-Adresse dient dazu, den ESP32 eindeutig zu identifizieren, wenn der Laptop versucht, sich mit ihm zu verbinden.
ESP32_ADDRESS = "7C:9E:BD:61:9E:76"  # Beispiel: Ersetze dies mit der korrekten MAC-Adresse

# UUIDs für den Service und die Charakteristik, die auf dem ESP32 registriert sind.
# Diese UUIDs sind notwendig, um den richtigen Service und die richtige Charakteristik auf dem ESP32 zu identifizieren.
# SERVICE_UUID ist die UUID des Accelerometer-Service, aber in diesem Fall verwenden wir die UUID für den Nordic UART Service.
SERVICE_UUID = "00001818-0000-1000-8000-00805f9b34fb"  # Accelerometer Service UUID (0x1818)

# CHARACTERISTIC_UUID ist die UUID der Charakteristik, mit der der ESP32 Daten sendet (in diesem Fall das Benachrichtigungsfeld).
CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # TX Characteristic UUID (Notifying)

# Funktion, die aufgerufen wird, wenn Benachrichtigungen von der angegebenen Charakteristik empfangen werden.
# Diese Funktion wird immer dann ausgeführt, wenn der ESP32 Daten an den Laptop sendet.
def notification_handler(sender: int, data: bytearray):
    # Hier decodieren wir die empfangenen Daten von Bytes zu einem String und geben sie aus.
    print(f"Empfangen: {data.decode('utf-8')}")  # Ausgabe der empfangenen Nachricht

# Asynchrone Funktion, die den BLE-Client steuert und mit dem ESP32 verbindet.
# Die Funktion ist asynchron, damit sie nicht den gesamten Code blockiert, während auf Nachrichten gewartet wird.
async def run():
    # Versuche, mit dem ESP32 zu verbinden, indem du die MAC-Adresse verwendest.
    async with BleakClient(ESP32_ADDRESS) as client:
        # Wenn die Verbindung erfolgreich hergestellt wurde, wird dieser Code ausgeführt.
        print(f"Verbunden mit {ESP32_ADDRESS}")
        
        # Wir starten die Benachrichtigungen für die angegebene Charakteristik.
        # Sobald eine Benachrichtigung vom ESP32 empfangen wird, wird die `notification_handler`-Funktion aufgerufen.
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Endlosschleife, um die Benachrichtigungen zu empfangen.
        # In dieser Schleife bleibt der Laptop am Warten auf neue Benachrichtigungen vom ESP32.
        # `await asyncio.sleep(1)` gibt dem Event-Loop Zeit, um andere Aufgaben zu erledigen.
        while True:
            await asyncio.sleep(1)  # Wartet 1 Sekunde, bevor die Schleife erneut ausgeführt wird.

# Diese Zeile startet die asynchrone Funktion `run()` und blockiert den Rest des Codes, bis die Verbindung und die Benachrichtigungen abgeschlossen sind.
asyncio.run(run())
