import network

wlan = network.WLAN(network.STA_IF)
print('wlan is connected() =', wlan.isconnected())