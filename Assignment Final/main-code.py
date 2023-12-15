import os, sys, io
import M5
from M5 import *
from hardware import *
from servo import Servo
import time
from umqtt import *

mqtt_client = None
user_name = 'USERNAME_HERE'

adc_sensor1 = None
adc_sensor1_val = None
adc_sensor2 = None
adc_sensor2_val = None
adc_sensor3 = None
adc_sensor3_val = None
adc_timer = 0

# configure servo on pin G38:
servo = Servo(pin=38)
sensor2_time = 0
sensor3_time = 0

program_state = 'READY'

def setup():
  global adc_sensor1, adc_sensor1_val, adc_sensor2, adc_sensor2_val
  global adc_sensor3, adc_sensor3_val
  global mqtt_client
  M5.begin()
  mqtt_client = MQTTClient(
      'my_atom_board', 
      'io.adafruit.com', 
      port=1883, 
      user=user_name, 
      password='PASSWORD_HERE', 
  )
  mqtt_client.connect(clean_session=True)
  # configure ADC input on pin G1 with 11dB attenuation:
  adc_sensor1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  # configure ADC input on pin G8 with 11dB attenuation:
  adc_sensor2 = ADC(Pin(8), atten=ADC.ATTN_11DB)
  # configure ADC input on pin G6 with 11dB attenuation:
  adc_sensor3 = ADC(Pin(6), atten=ADC.ATTN_11DB)
  
  #print('test publish speed..')
  #mqtt_client.publish(user_name+'/feeds/toy-car-feed', str(2.2), qos=0)

def loop():
  global adc_sensor1, adc_sensor1_val, adc_sensor2, adc_sensor2_val
  global adc_sensor3, adc_sensor3_val, adc_timer
  global sensor2_time, sensor3_time
  global program_state
  global mqtt_client
  
  M5.update()
  
  # read adc and update servo every 2 seconds:
  if(time.ticks_ms() > adc_timer + 2000):
    # read 12-bit analog value (0 - 4095 range):
    adc_sensor1_val = adc_sensor1.read()
    #print(adc_val)
    # convert adc_val from 12-bit to 8-bit (0 - 255 range):
    servo_val = map_value(adc_sensor1_val, in_min = 0, in_max = 4095,
                           out_min = 98
                          , out_max = 100)
    # print 8-bit ADC value ending with comma:
    print(servo_val)
    servo.move(servo_val)
    #time.sleep_ms(100)
    # update timer variable:
    adc_timer = time.ticks_ms()  
  
  if(program_state == 'READY'):
    # read sensor 2:
    adc_sensor2_val = adc_sensor2.read()
    if (adc_sensor2_val > 1500):
      # save sensor2 time in milliseconds:
      sensor2_time = time.ticks_ms()
      print('sensor2_time', sensor2_time)
      program_state = 'SENSOR2'
      print('change program_state to', program_state)

  elif(program_state == 'SENSOR2'):
    # read sensor 3:
    adc_sensor3_val = adc_sensor3.read()
    if (adc_sensor3_val > 1500):
      # save sensor3 time in milliseconds:
      sensor3_time = time.ticks_ms()
      # calculate time difference between sensor2 and sensor3 in milliseconds:
      duration = sensor3_time - sensor2_time
      print('duration =', duration)
      program_state = 'SENSOR3'
      print('change program_state to', program_state)
      speed = ("{:.2f}".format(279.4/duration))
      print('Captured speed =', speed, 'meters per second')
      program_state = 'READY'
      
      # publish analog value as a string:
      mqtt_client.publish(user_name+'/feeds/toy-car-feed', str(speed), qos=0)
      print('publish speed..', str(speed))


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