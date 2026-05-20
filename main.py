import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from core.serial_manager import SerialManager
from core.controller import Controller


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    serial_manager = SerialManager(baudrate=115200)
    controller = Controller(window, serial_manager)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()