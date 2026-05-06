import serial
import serial.tools.list_ports

class SerialManager:
    def __init__(self, port="COM3", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        """Open UART communication"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            print("UART Error:", e)
            return False

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()

    def available_ports(self):
        """List COM ports"""
        return [p.device for p in serial.tools.list_ports.comports()]

    def send(self, data: str):
        if self.serial and self.serial.is_open:
            self.serial.write((data + "\n").encode())

    def read_line(self):
        if self.serial and self.serial.is_open:
            try:
                return self.serial.readline().decode().strip()
            except:
                return ""
        return ""
