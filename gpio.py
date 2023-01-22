import RPi.GPIO as gpio
import time    



class GpioController:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)
        self.pwmVentoinha = gpio.PWM(24,1000)
        self.pwmVentoinha.start(0)
        self.pwmResistor = gpio.PWM(23,1000)
        self.pwmResistor.start(0)
        
    def controlaTemperatura(self, sinalControle):
        if sinalControle > 0:
            ligaResistor(sinalControle)
        if sinalControle < 0:
            ligaVentoinha(sinalControle)
               
    def ligaResistor(self, sinalControle):
        if dc > 100:
          dc = 100
        self.pwmResistor.ChangeDutyCycle(dc)
        
    def ligaResistor(self, sinalControle):
        sinalControle = sinalControle * (-1)
        if sinalControle > 100:
          sinalControle = 100
        if sinalControle < 40:
          sinalControle = 40
        self.pwmVentoinha.ChangeDutyCycle(dc)
        
controleTemp = GpioController()
#pwm = gpio.PWM(23,1000)
#pwm.start(0)
#pwm.ChangeDutyCycle(100)
'''dc = 100
while True:
      controleTemp.ligaResistor( dc)'''


#controleTemp.desligaResistor()

'''gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)'''
