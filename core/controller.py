from PyQt5.QtCore import QObject, QTimer
import time


class Controller(QObject):
    def __init__(self, window, serial_manager):
        super().__init__()

        self.window = window
        self.serial_manager = serial_manager

        self.running = False
        self.start_time = time.time()

        self.time_data = []
        self.temperature_data = []
        self.resistance_data = []
        self.voltage_data = []
        self.power_data = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_data)

        self.window.connect_button.clicked.connect(self.connect_serial)
        self.window.start_button.clicked.connect(self.start_acquisition)
        self.window.stop_button.clicked.connect(self.stop_acquisition)
        self.window.submit_temperature_button.clicked.connect(self.send_setpoint)

    def connect_serial(self):
        try:
            self.serial_manager.connect()
            self.window.status_label.setText("Connecté")
        except Exception as e:
            self.window.status_label.setText(f"Erreur connexion : {e}")

    def start_acquisition(self):
        if not self.serial_manager.is_connected():
            self.window.status_label.setText("Erreur : port série non connecté")
            return

        self.running = True
        self.start_time = time.time()
        self.timer.start(100)
        self.window.status_label.setText("Acquisition en cours")

    def stop_acquisition(self):
        self.running = False
        self.timer.stop()
        self.window.status_label.setText("Acquisition arrêtée")

    def send_setpoint(self):
        value = self.window.temperature_input.value()

        if not self.serial_manager.is_connected():
            self.window.status_label.setText("Erreur : port série non connecté")
            return

        try:
            self.serial_manager.send(f"SET:{value}\n")
            self.window.status_label.setText(f"Consigne envoyée : {value} °C")
        except Exception as e:
            self.window.status_label.setText(f"Erreur envoi : {e}")

    def read_data(self):
        if not self.running:
            return

        try:
            line = self.serial_manager.read_line()

            if not line:
                return

            values = self.parse_data(line)

            if values is None:
                return

            temperature, resistance, voltage, power = values
            current_time = time.time() - self.start_time

            self.time_data.append(current_time)
            self.temperature_data.append(temperature)
            self.resistance_data.append(resistance)
            self.voltage_data.append(voltage)
            self.power_data.append(power)

            self.keep_last_values(200)

            self.window.temperature_label.setText(f"Température : {temperature:.2f} °C")
            self.window.resistance_label.setText(f"Résistance : {resistance:.2f} Ω")
            self.window.voltage_label.setText(f"Tension : {voltage:.2f} V")
            self.window.power_label.setText(f"Puissance : {power:.2f} W")

            self.update_graphs()

        except Exception as e:
            self.window.status_label.setText(f"Erreur lecture : {e}")

    def parse_data(self, line):
        """
        Format attendu depuis STM32 :
        temperature;resistance;voltage;power

        Exemple :
        25.4;120.5;3.12;0.08
        """

        try:
            line = line.strip()
            parts = line.split(";")

            if len(parts) != 4:
                return None

            temperature = float(parts[0])
            resistance = float(parts[1])
            voltage = float(parts[2])
            power = float(parts[3])

            return temperature, resistance, voltage, power

        except ValueError:
            return None

    def update_graphs(self):
        self.window.temperature_curve.setData(self.time_data, self.temperature_data)
        self.window.resistance_curve.setData(self.time_data, self.resistance_data)
        self.window.voltage_curve.setData(self.time_data, self.voltage_data)
        self.window.power_curve.setData(self.time_data, self.power_data)

    def keep_last_values(self, max_points):
        self.time_data = self.time_data[-max_points:]
        self.temperature_data = self.temperature_data[-max_points:]
        self.resistance_data = self.resistance_data[-max_points:]
        self.voltage_data = self.voltage_data[-max_points:]
        self.power_data = self.power_data[-max_points:]