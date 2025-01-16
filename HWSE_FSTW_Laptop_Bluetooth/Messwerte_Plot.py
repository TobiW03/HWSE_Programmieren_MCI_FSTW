import pandas as pd
import matplotlib.pyplot as plt

# Lesen der Datei FloMesswerte
file_name = "Messwerte/FloSprungNeu30s.txt"
data = pd.read_csv(file_name)

# Daten prüfen
print(data.head())

# Daten plotten
plt.figure(figsize=(12, 8))

# Plot für X-Achse
plt.subplot(3, 1, 1)
plt.plot(data['Timestamp'], data['X-Axis'], label='X-Achse')
plt.xlabel('Zeit (s)')
plt.ylabel('Beschleunigung')
plt.title('Beschleunigung in X-Richtung')
plt.legend()
plt.grid()

# Plot für Y-Achse
plt.subplot(3, 1, 2)
plt.plot(data['Timestamp'], data['Y-Axis'], label='Y-Achse', color='orange')
plt.xlabel('Zeit (s)')
plt.ylabel('Beschleunigung')
plt.title('Beschleunigung in Y-Richtung')
plt.legend()
plt.grid()

# Plot für Z-Achse
plt.subplot(3, 1, 3)
plt.plot(data['Timestamp'], data['Z-Axis'], label='Z-Achse', color='green')
plt.xlabel('Zeit (s)')
plt.ylabel('Beschleunigung')
plt.title('Beschleunigung in Z-Richtung')
plt.legend()
plt.grid()

# Plots anzeigen
plt.tight_layout()
plt.show()
