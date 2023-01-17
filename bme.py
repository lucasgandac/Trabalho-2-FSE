import socket
import fcntl
import struct
import time
import smbus2
import bme280


port = 0
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)


data = bme280.sample(bus, address, calibration_params)
temp ="Temp : "  + str("{:.2f}".format(data.temperature))

umid ="Umid :  " +  str("{:.2f}".format(data.humidity))

print(temp)
print(umid)
time.sleep(2)

#Apaga o display
#lcdi2c.lcd_clear()