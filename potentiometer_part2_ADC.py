import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from unit import *


adc1 = None
angle_0 = None


angle_val = None


def setup():
  global adc1, angle_0, angle_val

  adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  M5.begin()


def loop():
  global adc1, angle_0, angle_val
  M5.update()
  angle_val = adc1.read()
  print(angle_val)
  time.sleep_ms(400)


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
