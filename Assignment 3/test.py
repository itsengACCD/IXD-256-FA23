import os, sys, io
import M5
from M5 import *
from hardware import *
import time

# global pwm1 variable:
pwm1 = None

def setup():
  global 
  M5.begin()
  
def loop():
  global

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