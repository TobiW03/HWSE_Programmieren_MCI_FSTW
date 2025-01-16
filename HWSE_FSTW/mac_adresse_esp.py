import network

# Abrufen der MAC-Adresse des ESP32
mac = network.WLAN(network.STA_IF).config('mac')
print("MAC-Adresse des ESP32:", ':'.join(['{:02x}'.format(b) for b in mac]))
