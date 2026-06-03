import serial
import serial.tools.list_ports


class SerialManager:
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.serial_port = None

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())

        for port in ports:
            desc = port.description.lower()

            if (
                "stlink" in desc
                or "stm" in desc
                or "nucleo" in desc
                or "usb serial" in desc
                or "com" in port.device.lower()
            ):
                return port.device

        return None

    def connect(self, port=None):
        if port is None:
            port = self.find_port()

        if port is None:
            raise Exception("Aucun port série trouvé")

        self.serial_port = serial.Serial(
            port="COM6",
            baudrate=115200,
            timeout=0.1
        )

    def is_connected(self):
        return self.serial_port is not None and self.serial_port.is_open

    def read_line(self):
        if not self.is_connected():
            return ""

        line = self.serial_port.readline().decode("utf-8", errors="ignore")
        return line.strip()

    def send(self, message):
        if not self.is_connected():
            raise Exception("Port série non connecté")

        self.serial_port.write(message.encode("utf-8"))

    def close(self):
        if self.is_connected():
            self.serial_port.close()