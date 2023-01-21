import RPi.GPIO as gpio
import time    



class GpioController:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        
    def ligaResistor(self, dc, pwm):
        #dc = 0
        if dc > 100:
          dc = 100
        pwm.ChangeDutyCycle(dc)
        ''' pwm = gpio.PWM(23,1000)
        pwm.start(dc)'''
        #while True:
        #pwm.ChangeDutyCycle(dc)
        '''while True:
            if dc > 100:
                 dc = 100
            pwm.ChangeDutyCycle(dc)
            dc += 1'''
            
    def desligaResistor(self):
        '''gpio.output(23,True)
        time.sleep(40)
        gpio.output(23,False)'''
        
controleTemp = GpioController()
pwm = gpio.PWM(24,1000)
pwm.start(0)
#pwm.ChangeDutyCycle(100)
dc = 100
while True:
      controleTemp.ligaResistor( dc, pwm)


#controleTemp.desligaResistor()

'''gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)'''
