from machine import Pin
import time

# initialize pin1 as an output pin:
relay_pin = Pin(7, mode=Pin.OUT)

while(True):
    relay_pin.on()
    time.sleep(1)
    relay_pin.off()
    time.sleep(1)