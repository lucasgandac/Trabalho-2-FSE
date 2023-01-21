import smbus2
import bme280
import time    

class BME280Sensor:
    def __init__(self, port=1, address=0x76):
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read_data(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        temp ="Temp : "  + str("{:.2f}".format(data.temperature))
        umid ="Umid :  " +  str("{:.2f}".format(data.humidity))
        return {'temp':temp, 'umid':umid}
    

temperature_read = BME280Sensor()
temperatura = temperature_read.read_data()
print(temperatura)
'''port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)
temp ="Temp : "  + str("{:.2f}".format(data.temperature))
umid ="Umid :  " +  str("{:.2f}".format(data.humidity))
'''