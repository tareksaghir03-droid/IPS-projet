from PyQt5.QtCore import QObject, QTimer
import time


CURRENT_MIN_MA = 4.0
CURRENT_MAX_MA = 20.0
TEMPERATURE_MIN_C = 0.0
TEMPERATURE_MAX_C = 100.0


class Controller(QObject):

    def __init__(self, window, serial_manager):
        super().__init__()

        self.window = window
        self.serial_manager = serial_manager

        self.running = False
        self.start_time = time.time()

        self.time_data = []
        self.temperature_data = []
        self.power_data = []
        self.current_data = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_data)

        self.window.connect_button.clicked.connect(self.connect_serial)
        self.window.start_button.clicked.connect(self.start_acquisition)
        self.window.stop_button.clicked.connect(self.stop_acquisition)
        self.window.submit_temperature_button.clicked.connect(
            self.send_setpoint
        )

    # =========================================================
    # Connexion série
    # =========================================================

    def connect_serial(self):
        try:
            self.serial_manager.connect()
            self.window.status_label.setText("Connecté")

        except Exception as e:
            self.window.status_label.setText(
                f"Erreur connexion : {e}"
            )

    # =========================================================
    # Démarrer acquisition
    # =========================================================

    def start_acquisition(self):

        if not self.serial_manager.is_connected():
            self.window.status_label.setText(
                "Erreur : port série non connecté"
            )
            return

        self.running = True
        self.start_time = time.time()

        self.timer.start(100)

        self.window.status_label.setText(
            "Acquisition en cours"
        )

    # =========================================================
    # Stop acquisition
    # =========================================================

    def stop_acquisition(self):

        self.running = False

        self.timer.stop()

        self.window.status_label.setText(
            "Acquisition arrêtée"
        )

    # =========================================================
    # Envoi consigne STM32
    # =========================================================

    def send_setpoint(self):

        value = self.window.temperature_input.value()

        if not self.serial_manager.is_connected():

            self.window.status_label.setText(
                "Erreur : port série non connecté"
            )

            return

        try:
            # STM32 attend : S50
            self.serial_manager.send(f"S{value}\n")

            self.window.status_label.setText(
                f"Consigne envoyée : {value} °C"
            )

        except Exception as e:

            self.window.status_label.setText(
                f"Erreur envoi : {e}"
            )

    # =========================================================
    # Lecture données STM32
    # =========================================================

    def read_data(self):

        if not self.running:
            return

        try:

            line = self.serial_manager.read_line()
            print(line)

            if not line:
                return

            values = self.parse_data(line)

            if values is None:
                return

            temperature, current, power = values

            current_time = time.time() - self.start_time

            # stockage données
            self.time_data.append(current_time)
            self.temperature_data.append(temperature)
            self.power_data.append(power)
            self.current_data.append(current)

            self.keep_last_values(200)

            # affichage texte
            self.window.temperature_label.setText(
                f"Température calculée : {temperature:.2f} °C"
            )

            self.window.power_label.setText(
                f"Puissance : {power:.2f} W"
            )

            self.window.current_label.setText(
                f"Courant : {current * 1000:.1f} mA"
            )

            # update graphes
            self.update_graphs()

        except Exception as e:

            self.window.status_label.setText(
                f"Erreur lecture : {e}"
            )

    # =========================================================
    # Parse ligne STM32
    # =========================================================

    def parse_data(self, line):

        try:

            data = {}

            parts = line.split("|")

            for part in parts:

                if "=" in part:

                    key, value = part.split("=", 1)

                    key = key.strip()
                    value = value.strip()

                    value = value.replace(" C", "")
                    value = value.replace(" V", "")
                    value = value.replace(" A", "")
                    value = value.replace(" W", "")

                    data[key] = float(value)

            # vérifier champs nécessaires
            if (
                "Temp" not in data
                or "I" not in data
                or "P" not in data
            ):
                return None

            temperature = data["Temp"]
            current = data["I"]
            power = data["P"]

            return temperature, current, power

        except:
            return None

    # =========================================================
    # Ancienne conversion 4-20mA
    # =========================================================

    def calculate_temperature_from_current(
        self,
        current_ma
    ):

        current_span = (
            CURRENT_MAX_MA - CURRENT_MIN_MA
        )

        temperature_span = (
            TEMPERATURE_MAX_C - TEMPERATURE_MIN_C
        )

        if current_span == 0:
            return TEMPERATURE_MIN_C

        ratio = (
            (current_ma - CURRENT_MIN_MA)
            / current_span
        )

        return (
            TEMPERATURE_MIN_C
            + ratio * temperature_span
        )

    # =========================================================
    # Graphiques
    # =========================================================

    def update_graphs(self):

        self.window.temperature_curve.setData(
            self.time_data,
            self.temperature_data
        )

        self.window.power_curve.setData(
            self.time_data,
            self.power_data
        )

        self.window.current_curve.setData(
            self.time_data,
            self.current_data
        )

    # =========================================================
    # Limiter taille buffers
    # =========================================================

    def keep_last_values(self, max_points):

        self.time_data = self.time_data[-max_points:]

        self.temperature_data = (
            self.temperature_data[-max_points:]
        )

        self.power_data = (
            self.power_data[-max_points:]
        )

        self.current_data = (
            self.current_data[-max_points:]
        )