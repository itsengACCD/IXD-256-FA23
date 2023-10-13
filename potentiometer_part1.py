import os, sys, io
import M5
from M5 import *
import time
from unit import *


angle_0 = None


angle_val = None


def setup():
  global angle_0, angle_val

  angle_0 = Angle((1,2))
  M5.begin()


def loop():
  global angle_0, angle_val
  M5.update()
  angle_val = angle_0.get_value()
  print(angle_val)
  time.sleep_ms(200)


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