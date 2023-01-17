import serial
import crcmod
import struct

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
           
print("escrevendo...")
uart.write(msg)
response = uart.read(4) # read the response
print(response)
#last_byte = response[-1]
#float_data = struct.unpack('f', response)[-1]
#print(last_byte)
print(msg)
