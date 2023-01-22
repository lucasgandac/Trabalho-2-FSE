
from pid import PID
from bme import BME280Sensor
from gpio import GpioController
from uart import UartController

class MainController:
    def __init__(self):
        self.gpio = GpioController()
        self.i2c = BME280Sensor()
        self.uart = UartController()

        self.gpio.__init__()
        self.i2c.__init__()
        self.uart.__init__()
        self.conexaoUart = self.uart.initUart()
        self.uart.init_estado()

    def interpretaComando(self, comando):
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

    def run(self):
        print("teste")
        while True:
            print("dedntro dod run")
            comando = self.uart.read_command(self.conexaoUart)
            print(comando)
            self.interpretaComando(comando)
            #self.estado.control_temp(command)

# create an instance of MainController
main_controller = MainController()

# start running the loop
main_controller.run()
