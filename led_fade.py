import os, sys, io
import M5
from M5 import *
from hardware import *
import time


pwm1 = None


i = None


def setup():
  global pwm1, i

  M5.begin()
  pwm1 = PWM(Pin(1), freq=20000, duty=512)


def loop():
  global pwm1, i
  M5.update()
  for i in range(200):
    pwm1.duty(i)
    time.sleep_ms(5)
  for i in range(200):
    pwm1.duty(200-i)
    time.sleep_ms(5)


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
