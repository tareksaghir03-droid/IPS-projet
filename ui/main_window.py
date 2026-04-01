from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QGridLayout,
    QSpinBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Interface de Régulation Thermique")
        self.resize(1450, 820)

        self._setup_window_style()
        self.setup_ui()

    def _setup_window_style(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #eef2f7;
                color: #1e293b;
                font-family: "Segoe UI";
                font-size: 15px;
            }

            QLabel#titleLabel {
                font-size: 28px;
                font-weight: 700;
                color: #0f172a;
                padding-top: 4px;
            }

            QLabel#subtitleLabel {
                font-size: 15px;
                color: #64748b;
                padding-bottom: 6px;
            }

            QGroupBox {
                background-color: #f8fafc;
                border: 1px solid #d7e0ea;
                border-radius: 14px;
                margin-top: 12px;
                padding: 16px;
                font-weight: 600;
                color: #334155;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #1e3a5f;
                font-size: 16px;
                font-weight: 700;
            }

            QGroupBox#leftPanelGroup::title {
                font-size: 18px;
            }

            QLabel#hintLabel {
                color: #64748b;
                font-size: 16px;
                padding-bottom: 4px;
            }

            QLabel#valueBox {
                background-color: #ffffff;
                border: 1px solid #cfd8e3;
                border-radius: 8px;
                padding: 8px 10px;
                color: #0f172a;
                font-size: 17px;
                font-weight: 600;
                min-height: 18px;
            }

            QLabel#statusBox {
                background-color: #fff7ed;
                border: 1px solid #fdba74;
                border-radius: 10px;
                padding: 14px;
                color: #c2410c;
                font-size: 18px;
                font-weight: 700;
            }

            QSpinBox {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 9px;
                padding: 8px;
                color: #0f172a;
                font-size: 17px;
                min-height: 28px;
            }

            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 17px;
                font-weight: 700;
            }

            QPushButton#primaryButton {
                background-color: #2563eb;
                color: white;
            }

            QPushButton#primaryButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#secondaryButton {
                background-color: #e2e8f0;
                color: #1e293b;
            }

            QPushButton#secondaryButton:hover {
                background-color: #cbd5e1;
            }

            QPushButton#dangerButton {
                background-color: #fee2e2;
                color: #b91c1c;
            }

            QPushButton#dangerButton:hover {
                background-color: #fecaca;
            }
        """)

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 14, 18, 18)
        main_layout.setSpacing(14)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)

        title_label = QLabel("Pilotage thermique intelligent")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel(
            "Suivi en temps réel de la température, de la résistance, de la tension et de la puissance"
        )
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(14)

        # Bloc consigne
        setpoint_group = QGroupBox("Réglage de la consigne")
        setpoint_group.setObjectName("leftPanelGroup")
        setpoint_layout = QVBoxLayout()
        setpoint_layout.setSpacing(10)

        hint_label = QLabel("Choisir une température cible entre 0 et 100 °C")
        hint_label.setObjectName("hintLabel")

        self.temperature_input = QSpinBox()
        self.temperature_input.setRange(0, 100)
        self.temperature_input.setValue(25)
        self.temperature_input.setSuffix(" °C")

        self.submit_temperature_button = QPushButton("Appliquer la consigne")
        self.submit_temperature_button.setObjectName("primaryButton")

        setpoint_layout.addWidget(hint_label)
        setpoint_layout.addWidget(self.temperature_input)
        setpoint_layout.addWidget(self.submit_temperature_button)
        setpoint_group.setLayout(setpoint_layout)
        setpoint_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Bloc mesures
        info_group = QGroupBox("Mesures instantanées")
        info_group.setObjectName("leftPanelGroup")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        self.temperature_label = QLabel("Température : -- °C")
        self.resistance_label = QLabel("Résistance : -- Ω")
        self.voltage_label = QLabel("Tension : -- V")
        self.power_label = QLabel("Puissance : -- W")

        self.temperature_label.setObjectName("valueBox")
        self.resistance_label.setObjectName("valueBox")
        self.voltage_label.setObjectName("valueBox")
        self.power_label.setObjectName("valueBox")

        info_layout.addWidget(self.temperature_label)
        info_layout.addWidget(self.resistance_label)
        info_layout.addWidget(self.voltage_label)
        info_layout.addWidget(self.power_label)
        info_group.setLayout(info_layout)
        info_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Bloc commandes
        button_group = QGroupBox("Actions système")
        button_group.setObjectName("leftPanelGroup")
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        self.connect_button = QPushButton("Connexion")
        self.start_button = QPushButton("Lancer")
        self.stop_button = QPushButton("Stop")

        self.connect_button.setObjectName("primaryButton")
        self.start_button.setObjectName("secondaryButton")
        self.stop_button.setObjectName("dangerButton")

        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_group.setLayout(button_layout)
        button_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Bloc état
        status_group = QGroupBox("État du système")
        status_group.setObjectName("leftPanelGroup")
        status_layout = QVBoxLayout()

        self.status_label = QLabel("Non connecté")
        self.status_label.setObjectName("statusBox")
        self.status_label.setAlignment(Qt.AlignCenter)

        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        status_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        left_panel.addWidget(setpoint_group)
        left_panel.addWidget(info_group)
        left_panel.addWidget(button_group)
        left_panel.addWidget(status_group)
        left_panel.addStretch()

        # Zone graphes
        plots_group = QGroupBox("Visualisation en temps réel")
        plots_layout = QGridLayout()
        plots_layout.setHorizontalSpacing(14)
        plots_layout.setVerticalSpacing(14)

        self.temperature_plot = self._create_plot_widget("Température", "Température", "°C")
        self.resistance_plot = self._create_plot_widget("Résistance", "Résistance", "kΩ")
        self.voltage_plot = self._create_plot_widget("Tension", "Tension", "V")
        self.power_plot = self._create_plot_widget("Puissance", "Puissance", "W")

        self.temperature_curve = self.temperature_plot.plot([], [], pen=pg.mkPen("#dc2626", width=2))
        self.resistance_curve = self.resistance_plot.plot([], [], pen=pg.mkPen("#d97706", width=2))
        self.voltage_curve = self.voltage_plot.plot([], [], pen=pg.mkPen("#2563eb", width=2))
        self.power_curve = self.power_plot.plot([], [], pen=pg.mkPen("#059669", width=2))

        plots_layout.addWidget(self.temperature_plot, 0, 0)
        plots_layout.addWidget(self.resistance_plot, 0, 1)
        plots_layout.addWidget(self.voltage_plot, 1, 0)
        plots_layout.addWidget(self.power_plot, 1, 1)

        plots_group.setLayout(plots_layout)

        content_layout.addLayout(left_panel, 1)
        content_layout.addWidget(plots_group, 3)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        self._apply_left_panel_fonts()

    def _apply_left_panel_fonts(self) -> None:
        scale = max(1.0, min(1.45, self.width() / 1450))

        group_title_font = QFont("Segoe UI", int(14 * scale), QFont.Bold)
        hint_font = QFont("Segoe UI", int(12 * scale))
        input_font = QFont("Segoe UI", int(13 * scale))
        value_font = QFont("Segoe UI", int(12 * scale), QFont.DemiBold)
        button_font = QFont("Segoe UI", int(12 * scale), QFont.Bold)
        status_font = QFont("Segoe UI", int(13 * scale), QFont.Bold)

        self.temperature_input.setFont(input_font)
        self.temperature_input.setMinimumHeight(int(42 * scale))

        self.submit_temperature_button.setFont(button_font)
        self.submit_temperature_button.setMinimumHeight(int(42 * scale))
        self.connect_button.setFont(button_font)
        self.connect_button.setMinimumHeight(int(42 * scale))
        self.start_button.setFont(button_font)
        self.start_button.setMinimumHeight(int(42 * scale))
        self.stop_button.setFont(button_font)
        self.stop_button.setMinimumHeight(int(42 * scale))

        self.temperature_label.setFont(value_font)
        self.resistance_label.setFont(value_font)
        self.voltage_label.setFont(value_font)
        self.power_label.setFont(value_font)
        self.status_label.setFont(status_font)
        self.status_label.setMinimumHeight(int(48 * scale))

        for label in self.findChildren(QLabel, "hintLabel"):
            label.setFont(hint_font)

        for group_box in self.findChildren(QGroupBox, "leftPanelGroup"):
            group_box.setFont(group_title_font)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "temperature_input"):
            self._apply_left_panel_fonts()

    def _create_plot_widget(self, title: str, label: str, unit: str) -> pg.PlotWidget:
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground("#ffffff")
        plot_widget.setMinimumHeight(285)

        plot_widget.setTitle(
            f"<span style='color:#0f172a; font-size:18pt; font-weight:700;'>{title}</span>"
        )

        plot_widget.setLabel("left", label, units=unit, color="#475569")
        plot_widget.setLabel("bottom", "Temps", units="s", color="#475569")

        plot_widget.showGrid(x=True, y=True, alpha=0.15)

        left_axis = plot_widget.getAxis("left")
        bottom_axis = plot_widget.getAxis("bottom")

        left_axis.setPen(pg.mkPen("#94a3b8"))
        bottom_axis.setPen(pg.mkPen("#94a3b8"))
        left_axis.setTextPen(pg.mkPen("#64748b"))
        bottom_axis.setTextPen(pg.mkPen("#64748b"))
        left_axis.setStyle(tickFont=pg.Qt.QtGui.QFont("Segoe UI", 11))
        bottom_axis.setStyle(tickFont=pg.Qt.QtGui.QFont("Segoe UI", 11))

        plot_widget.getPlotItem().getViewBox().setBorder(pg.mkPen("#dbe3ef"))

        return plot_widget
