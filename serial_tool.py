import serial.tools.list_ports
from serial import SerialException


class SerialTool:

    @staticmethod
    def listar_portas():
        """
        Lista todas as portas Comm detectadas no sistema.

        :return: dispositivos: uma lista [str] com os nomes dos dispositivos.
        """
        portas = serial.tools.list_ports.comports()
        dispositivos = []

        for p in portas:
            dispositivos.append(p.device)

        print(f'Dispositivos detectados: {dispositivos}')
        return dispositivos

    @staticmethod
    def conectar(dispositivo, bauds):
        try:
            device = serial.Serial(dispositivo, bauds)
            print(f'{device.portstr}')
            return device
        except SerialException as err:
            print(err)
