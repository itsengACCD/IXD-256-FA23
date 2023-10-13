import os, sys, io
import M5
from M5 import *
from hardware import *
import time
# import NeoPixel module:
from driver.neopixel import NeoPixel

# global variable for neopixel strip:
np = None

rainbow = [
  (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
  (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
  (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
  (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

def setup():
  # initialize M5 board:
  M5.begin()
  global np
  # initialize neopixel strip on pin G2 with 16 pixels:
  np = NeoPixel(pin=Pin(2), n=16)
  
def loop():
  global np, rainbow
  # update M5 board:
  M5.update()
  # cycle the list of rainbow colors:
  rainbow = rainbow[-1:] + rainbow[:-1]
  for i in range(16):
    # set pixel i to color i of rainbow:
    np[i] = rainbow[i]
  # update neopixel strip:
  np.write()
  time.sleep_ms(50)

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")