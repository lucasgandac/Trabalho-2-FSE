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

    def enviaControle(self, uart, controle):
        controle = int(controle)
        controletoByte = controle.to_bytes(4, 'little', signed=True)
        mensagem = b''.join([self.codigo16, self.codD1, self.matricula, controletoByte])
        msg = self.adicionaCRC(mensagem)
        uart.write(msg)

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
        response = self.checaCrc(response)
        comando = response[3]
        return comando

    def checaCrc(self, comando):
        mensagem = comando[:7]
        crc = comando [-2:]
        crc16 = crcmod.predefined.mkCrcFun('crc-16')
        crCalc = crc16(mensagem)
        crCalc = crCalc.to_bytes(2, 'little')
        if(crCalc == crc):
            return comando
        else:
            return b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    
    '''def modoTemperatura(self, uart, comando):
        if comando ==  '''
    
    def enviaComando(self, uart, comando, estado):
        comandosList = {161: b''.join([self.codigo23, self.codD3,self.matricula,self.codOn]), 162: b''.join([self.codigo23,self.codD3,self.matricula,self.codOff]), 163: b''.join([self.codigo23, self.codD5,self.matricula,self.codOn]), 
                   164: b''.join([self.codigo23, self.codD5,self.matricula,self.codOff])}
        if (comando == 163 and estado == 0 ):  
            pass
        elif comando == 162:
            codsist = comandosList[comando]
            codfunc = b''.join([self.codigo23, self.codD5,self.matricula,self.codOff])
            msgSist = self.adicionaCRC(codsist)
            uart.write(msgSist)
            msgFunc = self.adicionaCRC(codfunc)
            uart.write(msgFunc)
            self.leituraModoTemp(uart, 0)
        elif comando in comandosList:
            cod = comandosList[comando]
            msgEnvio = self.adicionaCRC(cod)
            uart.write(msgEnvio)
            
