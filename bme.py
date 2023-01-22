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
        #temp ="Temp : "  + str("{:.2f}".format(data.temperature))
        temp =str("{:.2f}".format(data.temperature))
        temp = float(temp)
        umid ="Umid :  " +  str("{:.2f}".format(data.humidity))
        return temp