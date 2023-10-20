# control built-in RGB LED brightness with analog input on pin G1

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

adc = None
adc_val = None
rgb = None

def setup():
  global adc, adc_val, rgb
  M5.begin()
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  rgb = RGB(io=38, n=20, type="SK6812")
  
  # configure ADC input on pin G1 with 11dB attenuation:
  adc = ADC(Pin(1), atten=ADC.ATTN_11DB)
  # configure AtomS3 Lite built-in RGB LED:
  rgb = RGB()

def loop():
  global adc, adc_val
  M5.update()
  # read 12-bit analog value (0 - 4095 range):
  adc_val = adc.read()
  # convert adc_val from 12-bit to 8-bit (0 - 255 range):
  adc_val_8bit = map_value(adc_val, in_min = 0, in_max = 4095,
                           out_min = 0, out_max = 255)
  print(adc_val_8bit)
  # change red color brightness according to analog input:
  # blue_brightness = adc_val_8bit
  # rgb.fill_color(get_color(0, 0, blue_brightness))
  # time.sleep_ms(100)
  # convert adc_val from 0-4095 range to 0-9
  n = map_value(adc_val, 0, 4095, 0, 19)
  rgb.fill_color(0)
  rgb.set_color(n, get_color(0, 255, 0))
  time.sleep_ms(100)
  
# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color

# map an input value (v_in) between min/max ranges:
def map_value(in_val, in_min, in_max, out_min, out_max):
  v = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if (v < out_min): 
    v = out_min 
  elif (v > out_max): 
    v = out_max
  return int(v)

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