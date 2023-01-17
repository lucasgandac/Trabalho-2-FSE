import serial
import crcmod
import struct
import time

matricula = b'\x09\x06\x06\x08'

def inicializaEstado():
    m1 = b''.join([b'\x01', b'\x16', b'\xD3', matricula, b'\x01' ])
    return m1

uart = serial.Serial('/dev/serial0',9600, 8)
if (uart == -1):
    print("Erro - Não foi possível iniciar a UART.\n");
else:
    print("UART inicializada!\n");

m1 = b''.join([b'\x01', b'\x16', b'\xC1', b'\x09\x06\x06\x08'])
#m1 = b''.join([b'\x01', b'\x16', b'\xD3', b'\x09\x06\x06\x08', b'\x00' ])

crc16 = crcmod.predefined.mkCrcFun('crc-16')
crc = crc16(m1)
msg = m1 + crc.to_bytes(2, 'little')

message = inicializaEstado()  
crc1 = crc16(message)
message = message + crc1.to_bytes(2, 'little')
print("escrevendo...")
#uart.write(msg)
#uart.write(message)
#response = uart.read(4) # read the response
#print(response)
#last_byte = response[-1]
#float_data = struct.unpack('f', response)[-1]
#print(last_byte)
print(msg)


""" m3 = b''.join([b'\x01', b'\x23', b'\xC3', b'\x09\x06\x06\x08'])
crc16 = crcmod.predefined.mkCrcFun('crc-16')
crc3 = crc16(m3)
msg = m3 + crc3.to_bytes(2, 'little')
while True:
    uart.write(message)
    if uart.inWaiting() > 0:
        response = uart.read(4)
        print(response)
    time.sleep(0.5) """