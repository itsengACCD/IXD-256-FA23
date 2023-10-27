# controlling a servo using servo library
# servo.py library file should be burned on AtomS3 board

from servo import Servo
import time

# configure servo on pin G7:
servo = Servo(pin=7)

while(True):
    servo.move(85) # move slowly clockwise
    time.sleep_ms(500)
    servo.move(90) # stop between 90-95
    time.sleep(1)
    servo.move(103) # move slowly counterclockwise
    time.sleep_ms(500)
    servo.move(90) # stop between 90-95
    time.sleep(1)
