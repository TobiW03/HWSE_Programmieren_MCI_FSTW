# Importiere notwendige Bibliotheken:
# - Pin: Um die GPIO Pins des ESP32 zu steuern
# - I2C: Für die Kommunikation über den I2C-Bus (z.B. mit dem ADXL345)
# - Timer: Für zeitgesteuerte Aufgaben (wie z.B. das Blinken der LED)
# - sleep_ms: Damit der Mikrocontroller für eine bestimmte Zeit „schläft“
# - ubluetooth: Für Bluetooth Low Energy (BLE) Kommunikation
# - ADXL345: Die Bibliothek für die Kommunikation mit dem ADXL345-Beschleunigungssensor
from machine import Pin, I2C, Timer
from time import sleep_ms
import ubluetooth
from ADXL345 import ADXL345_I2C

# Initialisierungen
ble_msg = ""  # Variable für empfangene Nachrichten
is_ble_connected = False  # Statusvariable für die BLE-Verbindung

# Definition der ESP32_BLE-Klasse
class ESP32_BLE():
    # Der Konstruktor initialisiert die grundlegenden Komponenten
    def __init__(self, name):
        self.name = name  # Der Name des Geräts, der für die Werbung genutzt wird
        self.ble = ubluetooth.BLE()  # Initialisiert das BLE-Modul
        self.ble.active(True)  # Aktiviert das BLE-Modul
        self.timer1 = Timer(0)  # Initialisiert einen Timer für die LED
        self.disconnected()  # Ruft die Methode auf, um den Zustand für "getrennt" zu setzen
        self.ble.irq(self.ble_irq)  # Setzt den Interrupt-Handler für BLE-Ereignisse
        self.register()  # Registriert den BLE-Service und die Charakteristik
        self.advertiser()  # Startet die BLE-Werbung

        # Initialisiere I2C und ADXL345
        self.i2c = I2C(scl=Pin(22), sda=Pin(21))  # Initialisiert den I2C-Bus mit den Pins 22 und 21
        self.sensor = ADXL345_I2C(self.i2c)  # Initialisiert den ADXL345-Beschleunigungssensor
        self.jump_threshold = -100  # Schwellenwert für die Sprung-Erkennung (hier: 250)

    # Methode für den Zustand, wenn der ESP32 mit einem Gerät verbunden ist
    def connected(self):
        global is_ble_connected
        is_ble_connected = True  # Setzt die BLE-Verbindung auf 'verbunden'
        self.timer1.deinit()  # Deaktiviert den Timer, wenn die Verbindung hergestellt wurde

    # Methode für den Zustand, wenn der ESP32 von einem Gerät getrennt ist
    def disconnected(self):
        global is_ble_connected
        is_ble_connected = False  # Setzt den BLE-Verbindungsstatus auf 'getrennt'
        # Startet den Timer, der eine LED blinkt (dies könnte für Indikatoren wie "Verbindung verloren" verwendet werden)
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: None)

    # BLE IRQ Handler: Wird für bestimmte BLE-Ereignisse aufgerufen
    def ble_irq(self, event, data):
        global ble_msg
        if event == 1:  # _IRQ_CENTRAL_CONNECT: Ein Gerät hat sich mit dem ESP32 verbunden
            self.connected()

        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT: Ein Gerät hat die Verbindung getrennt
            self.advertiser()  # Starte wieder die Werbung
            self.disconnected()  # Setze den Status auf 'getrennt'
        
        elif event == 3:  # _IRQ_GATTS_WRITE: Ein Gerät hat auf eine Charakteristik des ESP32 geschrieben
            buffer = self.ble.gatts_read(self.rx)  # Lese den Inhalt der Charakteristik
            ble_msg = buffer.decode('UTF-8').strip()  # Dekodiere und entferne Leerzeichen

    # Registrierung des Nordic UART Services und der Charakteristiken
    def register(self):
        # Die UUIDs für den Nordic UART Service und die zugehörigen RX- und TX-Charakteristiken
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        # Definiert die Charakteristiken mit den entsprechenden Flags
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)

        # Kombiniert die Services und Charakteristiken
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        # Registriert den Service und erhält die Handles für TX und RX
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    # Methode zum Senden von Daten über BLE (Benachrichtigungen)
    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + 'n')  # Sende eine Nachricht (Benachrichtigung)

    # Startet die Werbung, sodass der ESP32 von anderen Geräten gefunden werden kann
    def advertiser(self):
        name = bytes(self.name, 'UTF-8')  # Wandelt den Gerätenamen in Bytes um
        # Setzt die Werbepayload zusammen (hier wird der Name und einige Standardwerte hinzugefügt)
        adv_data = bytearray([0x02, 0x01, 0x06]) + bytearray([len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(100, adv_data)  # Startet die Werbung mit den definierten Daten

    # Die Methode zur Sprung-Erkennung
    def detect_jump(self):
        while True:
            if is_ble_connected:  # Überprüft, ob der ESP32 mit einem Gerät verbunden ist
                # Holt die Beschleunigungswerte aus dem ADXL345-Sensor
                x = self.sensor.xValue
                y = self.sensor.yValue
                z = self.sensor.zValue

                # Überprüft, ob die Z-Achse eine starke Beschleunigung erfährt, die einen Sprung anzeigt
                if x > self.jump_threshold:  # Wenn der Wert auf der Z-Achse den Schwellenwert überschreitet
                    print("Sprung")  # Gibt "Sprung" auf der Konsole aus
                    self.send('Sprung')  # Sende die Nachricht "Sprung" an den verbundenen Client
                    print("Sprung erkannt, Nachricht gesendet.")
                sleep_ms(350)  # Pause zwischen den Abfragen                

# Initialisiere den ESP32-BLE mit einem Namen
ble = ESP32_BLE("ESP32BLE")

# Start der Sprung-Erkennung
while True:
    ble.detect_jump()  # Sprung-Erkennung starten