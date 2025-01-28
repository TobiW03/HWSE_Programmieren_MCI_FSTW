from machine import Pin, I2C, PWM, Timer
from time import sleep, sleep_ms
import ubluetooth
from ADXL345 import ADXL345_I2C

class ESP32_BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.timer1 = Timer(0)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

        # Initialisiere I2C und Sensor
        self.i2c = I2C(scl=Pin(22), sda=Pin(21))
        self.sensor = ADXL345_I2C(self.i2c)
        self.jump_threshold = -100  # Standardwert für Schwellenwert

        # Initialisiere Piezo-Speaker
        self.buzzer = PWM(Pin(25))  # GPIO 25 für Piezo-Speaker

        # Initialisiere Onboard-LED (GPIO 2)
        self.led = Pin(2, Pin.OUT)
        self.led.off()

    def beep(self, frequency, duration):
        """Piepton mit Frequenz und Dauer"""
        self.buzzer.freq(frequency)  # Frequenz des Tons
        self.buzzer.duty(512)       # Lautstärke (50% Duty Cycle)
        sleep(duration)             # Dauer des Tons
        self.buzzer.duty(0)         # Ton ausschalten

    def connected(self):
        global is_ble_connected
        is_ble_connected = True
        self.timer1.deinit()

    def disconnected(self):
        global is_ble_connected
        is_ble_connected = False
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: None)

    def ble_irq(self, event, data):
        global ble_msg
        if event == 1:
            self.connected()
        elif event == 2:
            self.advertiser()
            self.disconnected()
        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            ble_msg = buffer.decode('UTF-8').strip()

    def register(self):
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data)

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray([0x02, 0x01, 0x06]) + bytearray([len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(100, adv_data)

    def success_melody(self):
        """Spielt eine Melodie für den Erfolg"""
        melody = [(784, 0.3), (880, 0.3), (988, 0.3), (1047, 0.5)]  # G5, A5, B5, C6
        for freq, duration in melody:
            self.beep(freq, duration)
            sleep(0.1)

    def funny_tone(self):
        """Spielt einen lustigen Ton"""
        tones = [(400, 0.1), (800, 0.1), (600, 0.2)]
        for freq, duration in tones:
            self.beep(freq, duration)
            sleep(0.05)

    def waiting_tone(self):
        """Spielt ein Wartegeräusch"""
        self.beep(200, 0.1)
        sleep(0.1)

    def blink_led(self):
        """Lässt die Onboard-LED blinken"""
        self.led.on()
        sleep_ms(200)
        self.led.off()
        sleep_ms(200)

    def calibrate_jump_threshold(self, num_jumps=5):
        print(f"Starte Kalibrierung für {num_jumps} Sprünge...")
        jump_values = []

        for i in range(num_jumps):
            print(f"Warte auf Sprung {i + 1}...")
            while True:
                self.blink_led()  # LED blinkt während der Kalibrierung
                self.waiting_tone()  # Warte-Ton
                x = self.sensor.xValue
                if x > self.jump_threshold:
                    jump_values.append(x)
                    print(f"Sprung {i + 1} erkannt: {x}")
                    self.funny_tone()  # Lustiger Ton bei Sprungerkennung
                    sleep_ms(500)  # Warte, um Mehrfacherkennungen zu vermeiden
                    break

        if jump_values:
            self.jump_threshold = min(jump_values) - 10
            print(f"Kalibrierung abgeschlossen. Neuer Schwellenwert: {self.jump_threshold}")
            self.success_melody()  # Erfolgsmelodie abspielen

        # Schalte die LED aus
        self.led.off()

    def detect_jump(self):
        while True:
            if is_ble_connected:
                x = self.sensor.xValue
                y = self.sensor.yValue
                z = self.sensor.zValue

                if x > self.jump_threshold:
                    print("Sprung erkannt!")
                    self.send('Sprung')
                    self.funny_tone()  # Lustiger Ton bei Sprungerkennung
                    sleep_ms(350)

# Initialisiere den ESP32-BLE
ble = ESP32_BLE("ESP32BLE")

# Kalibrierungsmodus
ble.calibrate_jump_threshold(num_jumps=5)

# Starte die Sprung-Erkennung
while True:
    ble.detect_jump()
