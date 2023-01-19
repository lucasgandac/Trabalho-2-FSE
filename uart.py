import serial
import crcmod
import struct
import time

matricula = b'\x09\x06\x06\x08'

def inicializaEstado():
    m1 = b''.join([b'\x01', b'\x16', b'\xD3', matricula, b'\x01' ])
    return m1

def initUart():
    uart = serial.Serial('/dev/serial0',9600, 8)
    if (uart == -1):
        print("Erro - Não foi possível iniciar a UART.\n");
    else:
        print("UART inicializada!\n");
    return uart

def initEstado(uart):
    estado = b''.join([b'\x01', b'\x16', b'\xD3', matricula, b'\x00' ])
    funcionamento = b''.join([b'\x01', b'\x16', b'\xD4', matricula, b'\x00' ])
    controleTemp = b''.join([b'\x01', b'\x16', b'\xD5', matricula, b'\x00' ])
    msg1 = adicionaCRC(estado)
    msg2 = adicionaCRC(funcionamento)
    msg3 = adicionaCRC(controleTemp)
    uart.write(msg1)
    uart.write(msg2)
    uart.write(msg3)
    time.sleep(0.5)

def adicionaCRC(mensagem):
    crc16 = crcmod.predefined.mkCrcFun('crc-16')
    crc = crc16(mensagem)
    crc = crc.to_bytes(2, 'little')
    mensagem = mensagem + crc
    return mensagem

def solicitaTemperaturas(uart):
    tempInterna = b''.join([b'\x01', b'\x23', b'\xC1', matricula])
    tempReferencia = b''.join([b'\x01', b'\x23', b'\xC2', matricula])
    msgInterna = adicionaCRC(tempInterna)
    msgReferencia = adicionaCRC(tempReferencia)
    uart.write(msgInterna)
    print("escrevendo primeira", msgInterna)
    interna = uart.read(9)
    print(interna)
    uart.write(msgReferencia)
    referencia = uart.read(9)
    return interna, referencia



uart = initUart()
#initEstado(uart)
time.sleep(1)
interna, referencia = solicitaTemperaturas(uart)
print("Codigo da temp interna", interna)
print("Codigo da temp referencia", referencia)
pos = referencia[3:7]
f = struct.unpack('f', pos)
f = str(f)
f = f.replace('(', '').replace(')', '').replace(',','')
print(f)
print(type(f))
'''m1 = b''.join([b'\x01', b'\x16', b'\xC1', b'\x09\x06\x06\x08'])

crc16 = crcmod.predefined.mkCrcFun('crc-16')
crc = crc16(m1)
msg = m1 + crc.to_bytes(2, 'little')
#print(msg)
#print(adicionaCRC(m1))'''

'''m3 = b''.join([b'\x01', b'\x23', b'\xC1', b'\x09\x06\x06\x08'])
crc16 = crcmod.predefined.mkCrcFun('crc-16')
crc3 = crc16(m3)
msg = m3 + crc3.to_bytes(2, 'little')
uart.write(msg)
response = uart.read(9)
pos = response[3:7]
f = struct.unpack('f', pos)
print("Temp interna: ", f)


while True:
    uart.write(message)
    if uart.inWaiting() > 0:
        response = uart.read(4)
        print(response)
    time.sleep(0.5)'''
