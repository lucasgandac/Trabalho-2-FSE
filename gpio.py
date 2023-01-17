import RPi.GPIO as gpio
import time    


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)

gpio.output(24, 1)
time.sleep(45)
gpio.output(24,0)
