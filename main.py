
from pid import PID
from bme import BME280Sensor
from gpio import GpioController
from uart import UartController
import time
import threading

class MainController:
    def __init__(self):
        self.pid = PID()
        self.gpio = GpioController()
        self.i2c = BME280Sensor()
        self.uart = UartController()

        self.conexaoUart = self.uart.initUart()
        self.uart.initEstado(self.conexaoUart)
        self.modoTemp = 0

    def interpretaComando(self, comando):
        #print(comando)
        if comando == 161:
            print("Liga o forno")
        if comando == 162:
            print("Desliga o forno")
        if comando == 163:
            print("Inicia aquecimento")
        if comando == 164:
            print("Cancela processo")
        if comando == 165:
            print("Alterna o modo temperatura")

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
            elif option == "2":
                kp = input("Digite o valor de Kp: " )
                ki = input("Digite o valor de Ki: " )
                kd = input("Digite o valor de Kd: " )
                self.pid.pid_configura_constantes(kp, ki, kd)
                    
    def run(self):
        while True:
            comando = self.uart.leComandos(self.conexaoUart)
            #print(comando)
            self.pid.printaPID()
            self.interpretaComando(comando)
            time.sleep(0.5)
            #self.estado.control_temp(command)

try: 
    main_controller = MainController()
    thread = threading.Thread(target=main_controller.menu, args=[])
    thread.start()  
    main_controller.run()
    
except KeyboardInterrupt:
    exit()