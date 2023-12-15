# Final Project

Hot Wheels Speed Trap

# Introduction   

Utilizing one light sensor to activate the turntable and two more light sensors to calculate the traveling speed of the cars, the Hot Wheels Speed Trap is an interactive track piece to enhance the play experience of your Hot Wheels toy cars. The initial idea was built upon project 3's light sensor activated servo unit turntable and expanded into an interactive track for Hot Wheels. The final project concept follows true to the initial sketches from part 1, with a single lane track placed on a slope built upon a lego technic chassis and laser cut acrylic cladding on the outside of the device.  

## Design Sketches

![sketch1](./sketch1.jpg)
![sketch2](./sketch2.jpg)
![sketch3](./sketch3.jpg)

# Implementation   


## Enclosure / Mechanical Design   

The prototype began initially with reconstruction of my project 3 Rube Goldberg machine and new sketches. Based on the initial sketches, I took apart the Rube Goldberg machine made of lego technic parts and re-engineered the structure to mechanically support Hot Wheels orange track pieces.

![car1](./Photos/car1.jpg)

The exterior enclosure is made from laser cut transparent 1/4" thick acrylic. On the largest piece, the Hot Wheels logo and "Speed Trap" are raster etched into the side for branding. 

![lasercut2](./Photos/lasercut2.png)
![enclosure1](./Photos/enclosure1.jpg)
![enclosure2](./Photos/enclosure2.jpg)
![enclosure3](./Photos/enclosure3.jpg)

The turntable is also made from laser cut white 1/8" thick acrylic. The pieces are stacked to create just the right amount of height to house the toy car without it falling out of the turntable, but not too thick so that the material gets too heavy and difficult to turn.

![lasercut1](./Photos/lasercut1.png)
![turntable1](./Photos/turntable1.jpg)
![turntable2](./Photos/turntable2.jpg)

To create the connection between the turntable and servo unit, I had to create a custom gear set using lego technic gears. The main challenge was to translate the rotational motion along a horizontal axis from the servo into an angled vertical axis for the turntable to line up to the track. I connected one large gear to the servo unit, and connected that to a row of four smaller gears to translate the horizontal-axis rotation to vertical-axis rotation. Lastly I connected the last in the row of four gears to a CV joint piece, and connected that to the turntable gear. The laser cut turntable was then affixed to the turntable gear using lego technic connector pieces.

![gears1](./Photos/gears1.jpg)
![gears2](./Photos/gears2.jpg)


## Hardware

### Components:
* One M5Stack AtomS3 Lite Controller
* One M5Stack ATOMIC PortABC Extension Base
* One Brick-compatible 360° Servo Unit
* Three Light Sensor Units with Photo-resistance

The underlying Rube Goldberg machine initially only had one light sensor and one servo unit, so I had to add on two additional light sensor units in order to create the speed sensor component for this project. I then changed the lego technic chassis to accomodate the two extra light sensors and cut out the backs of the orange tracks so that the light sensors could lie flush underneath the tracks seemlessly and perform properly to sense the toy cars passing over.

Section one of this device contains one light sensor unit and one servo unit. Covering the light sensor triggers the servo unit to begin turning slowly, so the presence of a waiting toy car covers the light sensor and the turntable turns until it lines up with the track and releases the toy car.

Section two of this device is the speed trap, composed of two sequential light sensors embedded into the track. The speed is calculated by dividing the fixed distance between the two light sensors, by the time spent for the car to travel between the two light sensors. I therefore programmed in the firmware to record the time difference between the triggering of the first light sensor and the triggering of the second light sensor.

### Below are photos of how the light sensors are embedded into the track:

![sensor1](./Photos/sensor1.jpg)
![sensor2](./Photos/sensor2.jpg)
![sensor3](./Photos/sensor3.jpg)

### Here is the schematic diagram showing the wiring connections between the M5Stack AtomS3 board and the other components:

With the three light sensors and one servo unit, all of the ports on the AtomS3 Lite with extension base were utilized fully. The three ADC ports that work with cloud function are pin 1, pin 6, and pin 8, therefore these three pins are connected to the light sensors. However, I found that pin 38/39 do not work over cloud for ADC sensors, so pin 38 is dedicated to the 360° servo unit.

![gears2](./Photos/gears2.jpg)

### Below are photos of the hardware wiring in the device:

![wire1](./Photos/wire1.jpg)
![wire2](./Photos/wire2.jpg)
![wire3](./Photos/wire3.jpg)
![wire4](./Photos/wire4.jpg)


## Firmware   

After creating the overall mechanical components of the prototype, I moved onto writing the firmware for the prototype's functionality.

[MicroPython Code](./main-code.py/)

Due to the use of three adc sensors (the light sensors), I defined each one as a variable by the order which the toy car passes over them. So the first light sensor that activates the turntable is adc_sensor1. For the speed trap component, the two light sensors are named adc_sensor2 and adc_sensor3 respectively.

``` Python  
  # configure ADC input on pin G1 with 11dB attenuation:
  adc_sensor1 = ADC(Pin(1), atten=ADC.ATTN_11DB)
  # configure ADC input on pin G8 with 11dB attenuation:
  adc_sensor2 = ADC(Pin(8), atten=ADC.ATTN_11DB)
  # configure ADC input on pin G6 with 11dB attenuation:
  adc_sensor3 = ADC(Pin(6), atten=ADC.ATTN_11DB)
```

To connect to Adafruit IO, I included the code below to link specifically to my account.

``` Python  
  mqtt_client = MQTTClient(
      'my_atom_board', 
      'io.adafruit.com', 
      port=1883, 
      user=user_name, 
      password='PASSWORD_HERE', 
  )
  mqtt_client.connect(clean_session=True)
```

In order to control the servo unit and allow it to rotate at a slow speed under the classroom overhead light, I converted the light sensor output min and max values to a narrow range between 98 and 100. I then defined the output to sensor_val as the variable for the servo.move function.

``` Python  
  if(time.ticks_ms() > adc_timer + 2000):
    # read 12-bit analog value (0 - 4095 range):
    adc_sensor1_val = adc_sensor1.read()
    # convert adc_val from 12-bit to 8-bit (0 - 255 range):
    servo_val = map_value(adc_sensor1_val, in_min = 0, in_max = 4095,
                           out_min = 98, out_max = 100)
    servo.move(servo_val)
    # update timer variable:
    adc_timer = time.ticks_ms() 
```

Lastly in order to record the time between the two sequential light sensors for the speed trap, I defined a minimum sensor value of 1500 to trigger the light sensors to begin recording the current time. Whenever a toy car travels over the light sensor, the sensor value spikes over 1500 and begins the time using time.ticks_ms. Once the first sensor is triggered, the program state changes from 'Ready' to 'Sensor2' which signifies the system is now waiting to record the value from the last light sensor. Once both sensors have been triggered, the program state changes to 'Sensor3' and the duration for the toy car to travel between the two light sensors is calculated. The time is then used to divide 279.4 to give a speed reading in meters per second. Finally at the end the program state returns to 'Ready' to reset the loop back to the beginning for the next car.

``` Python  
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
```

In the end the recorded speed is published to Adafruit IO using the code below:

``` Python  
  mqtt_client.publish(user_name+'/feeds/toy-car-feed', str(speed), qos=0)
  print('publish speed..', str(speed)) 
```


## Software   

software (HTML/CSS/JavaScript or other code)
If applicable, explain the important software components of your project with relevant code snippets and links.  

## Integrations   

The main cloud integration utilized is Adafruit IO. Below is the link to the Toy Car Feed to record outputs from the device:
[Adafruit Toy Car Feed](https://io.adafruit.com/itAP12/feeds/toy-car-feed)

![AdafruitFeed](./Photos/AdafruitFeed.png)

The feed data is then displayed on the dashboard using a gauge display:
[Adafruit Toy Car Speed Dashboard](https://io.adafruit.com/itAP12/dashboards/toy-car-speed)

![AdafruitDashboard](./Photos/AdafruitDashboard.png)


integrations (Adafruit IO, IFTTT, etc.)
Include a link to and/or screenshots of other functional components of your project, like Adafruit IO feeds, dashboards, IFTTT applets, etc.  In general, think of your audience as someone new trying to learn how to make your project and make sure to cover anything helpful to explain the functional parts of it.

## Project outcome  

Summarize the results of your final project implementation and include at least 2 photos of the prototype and a video walkthrough of the functioning demo.

## Conclusion  

As you wrap up the project, reflect on your experience of creating it.  Use this as an opportunity to mention any discoveries or challenges you came across along the way.  If there is anything you would have done differently, or have a chance to continue the project development given more time or resources, it’s a good way to conclude this section.

## Project references  

Please include links to any online resources like videos or tutorials that you may have found helpful in your process of implementing the prototype. If you used any substantial code from an online resource, make sure to credit the author(s) or sources.
