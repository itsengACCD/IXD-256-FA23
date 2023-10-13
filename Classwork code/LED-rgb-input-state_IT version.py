import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
state = 'yellow'
input_pin = None

def setup():
  global rgb, input_pin
  M5.begin()
  #custom RGB setting using pin G35
  #rgb = RGB(io=35, n=1, type="SK6812")
  #custom RGB setting using pin G35
  rgb = RGB(io=2, n=10, type="WS2812")
  # initialize pin 39 as input:
  input_pin = Pin(39, mode=Pin.IN, pull=Pin.PULL_UP)

def get_color(r, g, b):
  rgb_color = (r << 16)|(g << 8)| b
  return rgb_color

def loop():
  global rgb, state
  M5.update()
  if(state == 'yellow'):
    # if button is pressed change to red state:
    if (input_pin.value() == 0):
      state = 'red'
      print('change to ', state)
      time.sleep(1)
    else:
      for i in range (10):
        rgb.set_color(i, get_color(0, 0, 255))
        time.sleep_ms(100)
      rgb.fill_color(0xff0000)
      time.sleep_ms(500)
  elif(state == 'red'):
    # if button is pressed change to yellow state:
    if (input_pin.value() == 0):
      state = 'yellow'
      print('change to ', state)
      time.sleep(1)
    else:
      # chase RGB green
      rgb.fill_color(0xffcc00)
      time.sleep_ms(500)
      rgb.fill_color(0x000000)
      time.sleep_ms(500)

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
