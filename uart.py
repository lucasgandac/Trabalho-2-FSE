import serial
import crcmod
import struct
import time

import serial
import crcmod
import struct
import time
from pid import PID

class UartController:
    def __init__(self):
        self.matricula = b'\x09\x06\x06\x08'
        self.codigo16 = b'\x01\x16'
        self.codigo23 = b'\x01\x23'
        self.codC1 = b'\xC1'
        self.codC2 = b'\xC2'
        self.codC3 = b'\xC3'
        self.codD1 = b'\xD1'
        self.codD2 = b'\xD2'
        self.codD3 = b'\xD3'
        self.codD4 = b'\xD4'
        self.codD5 = b'\xD5'
        self.codD6 = b'\xD6'
        self.codOn = b'\x01'
        self.codOff = b'\x00'

    def initUart(self):
        self.uart = serial.Serial('/dev/serial0',9600, 8)
        if (self.uart == -1):
            print("Erro - Não foi possível iniciar a UART.\n");
        else:
             print("UART inicializada!\n");
        return self.uart

    def initEstado(self, uart):
        estado = b''.join([self.codigo16, self.codD3, self.matricula, self.codOff ])
        funcionamento = b''.join([self.codigo16, self.codD4, self.matricula, self.codOff ])
        controleTemp = b''.join([self.codigo16, self.codD5, self.matricula, self.codOff ])
        msg1 = self.adicionaCRC(estado)
        msg2 = self.adicionaCRC(funcionamento)
        msg3 = self.adicionaCRC(controleTemp)
        uart.write(msg1)
        uart.write(msg2)
        uart.write(msg3)

    def adicionaCRC(self,mensagem):
        crc16 = crcmod.predefined.mkCrcFun('crc-16')
        crc = crc16(mensagem)
        crc = crc.to_bytes(2, 'little')
        mensagem = mensagem + crc
        return mensagem

    def leituraModoTemp(self,uart, sinal):
        if sinal == 0:
            controle = self.codOff
        elif sinal == 1:
            controle = self.codOn            
        cod = b''.join([self.codigo23, self.codD4, self.matricula, controle])
        msg = self.adicionaCRC(cod)
        uart.write(msg)
        

    def solicitaTemperaturas(self, uart):
        codInterna = b''.join([self.codigo23, self.codC1, self.matricula])
        codReferencia = b''.join([self.codigo23, self.codC2, self.matricula])
        msgInterna = self.adicionaCRC(codInterna)
        msgReferencia = self.adicionaCRC(codReferencia)
        uart.write(msgInterna)
        interna = uart.read(9)
        uart.write(msgReferencia)
        referencia = uart.read(9)
        tempReferencia = referencia[3:7]
        ref = struct.unpack('f', tempReferencia)
        ref = str(ref)
        ref = ref.replace('(', '').replace(')', '').replace(',','')
        tempInterna = interna[3:7]
        itrn = struct.unpack('f', tempInterna)
        itrn = str(itrn)
        itrn = itrn.replace('(', '').replace(')', '').replace(',','')
        itrn = float(itrn)
        ref = float(ref)
        return itrn, ref
    
    
    def leComandos(self, uart):
        codLeitura = b''.join([self.codigo23, self.codC3, self.matricula])
        msgLeitura = self.adicionaCRC(codLeitura)
        uart.write(msgLeitura)
        response = uart.read(9)
        comando = response[3]
        return comando
    
    '''def modoTemperatura(self, uart, comando):
        if comando ==  '''
    
    def enviaComando(self, uart, comando):
        comandosList = {161: b''.join([self.codigo23, self.codD3,self.matricula,self.codOn]), 162: b''.join([self.codigo23,self.codD3,self.matricula,self.codOff]), 163: b''.join([self.codigo23, self.codD5,self.matricula,self.codOn]), 
                   164: b''.join([self.codigo23, self.codD5,self.matricula,self.codOff])}
        if comando in comandosList:
            print(comando)
            cod = comandosList[comando]
            print(cod)
            msgEnvio = self.adicionaCRC(cod)
            uart.write(msgEnvio)
            
'''uartObj = UartController() 
uartConexao = uartObj.initUart()
while True:
    uartObj.leComandos(uartConexao)
    time.sleep(0.5)'''
        
'''temp_control = TemperatureControl()
uart = temp_control.initUart()
#temp_control.initEstado(uart)
interna, referencia = temp_control.solicitaTemperaturas(uart)
pid = PID()
pid.pid_atualiza_referencia(referencia)
print(pid.pid_controle(interna))
print(interna, referencia)
'''

'''matricula = b'\x09\x06\x06\x08'
codigo16 = b'\x01\x16'
codigo23 = b'\x01\x23'
codC1 = b'\xC1'
codC2 = b'\xC2'
codC3 = b'\xC3'
codD1 = b'\xD1'
codD2 = b'\xD2'
codD3 = b'\xD3'
codD4 = b'\xD4'
codD5 = b'\xD5'
codD6 = b'\xD6'
codOn = b'\x01'
codOff = b'\x02'

def initUart():
    uart = serial.Serial('/dev/serial0',9600, 8)
    if (uart == -1):
        print("Erro - Não foi possível iniciar a UART.\n");
    else:
        print("UART inicializada!\n");
    return uart

def initEstado(uart):
    estado = b''.join([codigo16, codD3, matricula, codOff ])
    funcionamento = b''.join([codigo16, codD4, matricula, codOff ])
    controleTemp = b''.join([codigo16, codD5, matricula, codOff ])
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
    codInterna = b''.join([codigo23, codC1, matricula])
    codReferencia = b''.join([codigo23, codC2, matricula])
    msgInterna = adicionaCRC(codInterna)
    msgReferencia = adicionaCRC(codReferencia)
    uart.write(msgInterna)
    interna = uart.read(9)
    uart.write(msgReferencia)
    referencia = uart.read(9)
    tempReferencia = referencia[3:7]
    ref = struct.unpack('f', tempReferencia)
    ref = str(ref)
    ref = ref.replace('(', '').replace(')', '').replace(',','')
    tempInterna = interna[3:7]
    itrn = struct.unpack('f', tempInterna)
    itrn = str(itrn)
    itrn = itrn.replace('(', '').replace(')', '').replace(',','')
    return itrn, ref

'''

'''uart = initUart()
#initEstado(uart
time.sleep(1)
#initEstado(uart)
interna, referencia = solicitaTemperaturas(uart)
print("Temperatura interna", interna)
print("Temperatura referencia", referencia)'''

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
