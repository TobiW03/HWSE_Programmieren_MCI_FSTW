import time
from machine import I2C, Pin
from ADXL345 import ADXL345_I2C

# Initialisiere I2C-Schnittstelle
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Initialisiere den ADXL345-Sensor
adxl = ADXL345_I2C(i2c)

# Dauer der Messung in Sekunden
measurement_duration = 30
time_step = 0.1  # Zeitschritt in Sekunden

start_time = time.time()

print("Messung gestartet...")
print("Timestamp,X-Axis,Y-Axis,Z-Axis")  # CSV-Kopfzeile

# Initialisiere aktuellen Timestamp
current_time = 0.0

while current_time < measurement_duration:
    x = adxl.xValue
    y = adxl.yValue
    z = adxl.zValue

    # Sende die Daten über die serielle Verbindung
    print(f"{current_time:.1f},{x},{y},{z}")

    # Erhöhe den Timestamp um den Zeitschritt
    current_time += time_step
    time.sleep(time_step)

print("Messung abgeschlossen.")
