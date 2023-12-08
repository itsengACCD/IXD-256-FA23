import js as p5
from js import document

speed_val = None

def setup():
  p5.createCanvas(400, 400)
  

def draw():

  global speed_val

  # assign content of "data" div on index.html page to variable:
  speed_val = document.getElementById("data").innerText

  p5.fill(0)
  p5.noStroke()
  p5.text('speed_val = ' + "{:.1f}".format(279.4/duration), 'meters per second')

  # change circle size with sensor value:
  circle_size = p5.map(speed_val, 0, 255, 25, 100)
  p5.ellipse(75, 75, circle_size, circle_size)
