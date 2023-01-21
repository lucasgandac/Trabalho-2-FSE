import RPi.GPIO as gpio
import time    



class GpioController:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        
    def ligaResistor(self):
        dc = 0
        pwm = gpio.PWM(24,1000)
        pwm.start(0)
        while True:
            pwm.ChangeDutyCycle(100)
        '''while True:
            if dc > 60:
                dc = 60
            pwm.ChangeDutyCycle(dc)
            dc += 1'''
            
    def desligaResistor(self):
        '''gpio.output(23,True)
        time.sleep(40)
        gpio.output(23,False)'''
        
controleTemp = GpioController()
controleTemp.ligaResistor()
#controleTemp.desligaResistor()

'''gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)'''
