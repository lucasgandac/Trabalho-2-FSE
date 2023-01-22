import RPi.GPIO as gpio
import time    



class GpioController:
    def __init__(self):
        gpio.cleanup()
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
            self.ligaResistor(sinalControle)
        if sinalControle < 0:
            self.ligaVentoinha(sinalControle)
               
    def ligaResistor(self, sinalControle):
        if sinalControle > 100:
          sinalControle = 100
        self.pwmResistor.ChangeDutyCycle(sinalControle)
        
    def ligaVentoinha(self, sinalControle):
        sinalControle = sinalControle * (-1)
        if sinalControle > 100:
          sinalControle = 100
        if sinalControle < 40:
          sinalControle = 40
        print(sinalControle)
        self.pwmVentoinha.ChangeDutyCycle(sinalControle)
        
#pwm = gpio.PWM(23,1000)
#pwm.start(0)
#pwm.ChangeDutyCycle(100)
'''control_temp = GpioController()
dc = 100
while True:
    control_temp.ligaResistor(dc)'''


#controleTemp.desligaResistor()

'''gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)'''
