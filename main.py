
from pid import PID
from bme import BME280Sensor
from gpio import GpioController
from uart import UartController
import time
import threading
import csv 
import datetime

class MainController:
    def __init__(self):
        self.pid = PID()
        self.gpio = GpioController()
        self.i2c = BME280Sensor()
        self.uart = UartController()

        self.conexaoUart = self.uart.initUart()
        self.uart.initEstado(self.conexaoUart)
        self.modoTemp = 0
        self.estadoSistema = 0 
        self.estadoFuncionamento = 0
        self.tempReferencia = 0
        
    def registraLog(self, intn, ref, amb, resis):
        current_time = datetime.datetime.now()
        with open('logs/log.csv', 'a') as f:
            cm = str(current_time) + ", " + str(intn) + ", " + str(ref) +", " + str(amb) + ", " + str(resis)
            f.write(cm + '\n')
   
    def controleTemperatura(self):
        print(self.estadoFuncionamento)
        if(self.estadoFuncionamento ==1):
            print("dentro")
            tempAmbiente = self.i2c.read_data()
            tempInterna,tempRef = self.uart.solicitaTemperaturas(self.conexaoUart)
            print(tempInterna, tempRef)
            if(self.modoTemp==0):
                self.tempReferencia = tempRef
            self.pid.pid_atualiza_referencia(self.tempReferencia)
            sinalControle = self.pid.pid_controle(tempInterna)
            if (self.estadoFuncionamento == 1):
                self.uart.enviaControle(self.conexaoUart , sinalControle)
                time.sleep(0.05)
            self.gpio.controlaTemperatura(sinalControle)
            self.registraLog(tempInterna, self.tempReferencia, tempAmbiente, sinalControle)
            time.sleep(1)

    def interpretaComando(self, comando):
        valid_comandos = [161, 162, 163, 164, 165]
        if comando == 165:
            if self.modoTemp == 0 :
                self.modoTemp = 1
                self.uart.leituraModoTemp(self.conexaoUart, self.modoTemp)
            elif self.modoTemp == 1 :
                self.modoTemp = 0
                self.uart.leituraModoTemp(self.conexaoUart, self.modoTemp)
        elif comando in valid_comandos:
            if comando == 161 :
                self.estadoSistema = 1
            if comando == 162 :
                self.estadoSistema = 0
                self.estadoFuncionamento = 0
                self.modoTemp = 0
            if (comando == 163 and self.estadoSistema==1):
                self.estadoFuncionamento = 1
            if comando == 164 :
                self.estadoFuncionamento = 0
            self.uart.enviaComando(self.conexaoUart, comando, self.estadoSistema)

    def menu(self):
        while True:
            option = input("Gostaria de controlar temperatura de referência ou os parâmetros Kp, Ki e Kd ?\n1. Controle temperatura\n2. Controle parâmetros\n")
            while option != "1" and option != "2":
                option = input("Opção inválida.\n")
            if option == "1":
                optionTemp = input("Digite 0 para controlar via valor na  Dashboard e 1 para definir via terminal\n")
                while optionTemp != "0" and optionTemp != "1":
                    optionTemp = input("Opção inválida.\n")
                if optionTemp == "0" : 
                    self.modoTemp = 0
                elif optionTemp == "1" : 
                    self.modoTemp = 1
                    temperatura = input("Digite o valor da temperatura de referência: ")
                    temperatura = float(temperatura)
                    self.tempReferencia = temperatura
            elif option == "2":
                kp = input("Digite o valor de Kp: " )
                ki = input("Digite o valor de Ki: " )
                kd = input("Digite o valor de Kd: " )
                self.pid.pid_configura_constantes(kp, ki, kd)
                    
    def run(self):
        while True:
            comando = self.uart.leComandos(self.conexaoUart)
            #print(comando)
            #self.pid.printaPID()
            self.interpretaComando(comando)
            #self.controleTemperatura()
            time.sleep(0.4)
            #self.estado.control_temp(command)

try: 
    main_controller = MainController()
    thread = threading.Thread(target=main_controller.menu, args=[])
    thread.start() 
    thread2 = threading.Thread(target=main_controller.controleTemperatura, args=[])
    thread2.start()   
    main_controller.run()
    
except KeyboardInterrupt:
    main_controller.uart.initEstado(main_controller.conexaoUart)
    exit()