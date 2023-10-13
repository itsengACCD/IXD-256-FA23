# change RGB LED colors with digital input and time using state logic
# 4 states are implemented as shown:
# 'START'  -> turns on RGB green
# 'OPEN'   -> pulsate RGB red
# 'CLOSED' -> fade in RGB blue if digital input is closed
# 'FINISH' -> fade in RGB green 4 seconds after 'CLOSED' state
#             fade out RGB to black after 1 seconds

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
state = 'START'
state_timer = 0

def setup():
  global rgb, input_pin
  M5.begin()
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  rgb = RGB(io=2, n=20, type="SK6812")
  
  # initialize pin G39 (M5 PortABC Extension red connector) as input:
  input_pin = Pin(39, mode=Pin.IN, pull=Pin.PULL_UP)
  
  # turn on RGB green and wait 3 seconds:
  if (state == 'START'):
    print('start with RGB green..')
    rgb.fill_color(get_color(0, 255, 0))
    time.sleep(3)  
    check_input()

def loop():
  global state, state_timer
  M5.update()
      
  if (state == 'OPEN'):
    print('pulsate red..')
    # fade in RGB red:
    for i in range(100):
      rgb.fill_color(get_color(i, 0, 0))
      time.sleep_ms(5)
    # fade out RGB red:
    for i in range(100):
      rgb.fill_color(get_color(100-i, 0, 0))
      time.sleep_ms(5)
    check_input()
    
  elif (state == 'CLOSED'):
    # if less than 1 seconds passed since change to 'CLOSED':
    if(time.ticks_ms() < state_timer + 900):
      print('blink blue..')
      rgb.fill_color(get_color(0, 0, 255))
      time.sleep_ms(150)
      rgb.fill_color(get_color(0, 0, 0))
      time.sleep_ms(150)
      rgb.fill_color(get_color(0, 0, 255))
      time.sleep_ms(150)
      rgb.fill_color(get_color(0, 0, 0))
      time.sleep_ms(150)
      rgb.fill_color(get_color(0, 0, 255))
      time.sleep_ms(150)
      rgb.fill_color(get_color(0, 0, 0))
      time.sleep_ms(150)
    # if more than 1 seconds passed since change to 'CLOSED':
    elif(time.ticks_ms() > state_timer + 1000):
      state = 'FINISH'
      print('change to', state)
      # save current time in milliseconds:
      state_timer = time.ticks_ms()
      
  elif (state == 'FINISH'):
    print('fade from blue to green..')
    for i in range(100):
      rgb.fill_color(get_color(0, i, 100-i))
      time.sleep_ms(20)
      
    # if 2 seconds passed since change to 'FINISH':
    if(time.ticks_ms() > state_timer + 2000):
      print('fade from green to black..') 
      for i in range(100):
        rgb.fill_color(get_color(0, 100-i, 0))
        time.sleep_ms(20)
      time.sleep(1)
      check_input()

# check input pin and change state to 'OPEN' or 'CLOSED'
def check_input():
  global state, state_timer
  if (input_pin.value() == 0):
    if(state != 'CLOSED'):
      print('change to CLOSED')
    state = 'CLOSED'
    # save current time in milliseconds:
    state_timer = time.ticks_ms()
  else:
    if(state != 'OPEN'):
      print('change to OPEN')
    state = 'OPEN'
    
    
# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

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