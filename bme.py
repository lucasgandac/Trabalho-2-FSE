import smbus2
import bme280
import time    


port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

for x in range(5):
    data = bme280.sample(bus, address, calibration_params)
    temp ="Temp : "  + str("{:.2f}".format(data.temperature))
    umid ="Umid :  " +  str("{:.2f}".format(data.humidity))
    print(temp)
    print(umid)
    time.sleep(2)

#print(temp)
#print(umid)
