import js as p5
from js import document

data_string = None
data_list = None
angle_val = None
button_val = None

# load image data and assign it to variable:
valley_img = p5.loadImage('valley.png')
cloud_img = p5.loadImage('cloud.png')

def setup():
  p5.createCanvas(800, 400)

def draw():
  global data_string, data_list
  global angle_val, button_val

  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  angle_val = int(data_list[0])
  button_val = int(data_list[1])

  p5.fill(0)
  p5.noStroke()
  p5.text('sensor_val = ' + str(angle_val), 10, 20)
  p5.text('button_val = ' + str(button_val), 10, 35)

  # change fill color with button value:
  if(button_val == 0):
    p5.fill(255, 200, 0)  # yellow fill
    p5.background(angle_val-100, angle_val-55, angle_val+100)

  else:
    p5.fill(255, 255, 200)  # pale yellow fill
    p5.background(0-angle_val, 0-angle_val, 100-angle_val)

  # change sun height with sensor value:
  p5.ellipse(400, 355-angle_val, 100, 100)
  p5.image(valley_img, 0, 0, 800, 400)
  p5.image(cloud_img, 0, 0, 800, 400)
