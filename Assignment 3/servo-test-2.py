# servo.py library file should be burned on AtomS3 board

from servo import Servo
import time

servo = Servo(pin=7)

while(True):
    servo.move(65) # move slowly clockwise
    #servo.move(100) # move slowly counterclockwise
    time.sleep_ms(500)
    servo.move(90) # stop between 90-95
    time.sleep(2)
