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
        self.setWindowTitle("IHM - Asservissement de température")
        self.resize(1280, 760)

        self._setup_window_style()
        self.setup_ui()

    def _setup_window_style(self) -> None:
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f7fb;
                color: #1f2937;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: 700;
                color: #0f172a;
                padding: 4px 0 0 0;
            }
            QLabel#subtitleLabel {
                font-size: 14px;
                color: #64748b;
                padding-bottom: 10px;
            }
            QGroupBox {
                background: #ffffff;
                border: 1px solid #dbe3ef;
                border-radius: 16px;
                margin-top: 14px;
                padding: 18px 16px 16px 16px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
                color: #334155;
            }
            QSpinBox {
                background: #f8fafc;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px 10px;
                min-height: 20px;
                
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 16px;
                background: #dbeafe;
                color: #1d4ed8;
            }
            QPushButton:hover {
                background: #bfdbfe;
            }
            QPushButton#primaryButton {
                background: #2563eb;
                color: white;
            }
            QPushButton#primaryButton:hover {
                background: #1d4ed8;
            }
            QPushButton#dangerButton {
                background: #fee2e2;
                color: #b91c1c;
            }
            QPushButton#dangerButton:hover {
                background: #fecaca;
            }
            QLabel#infoValue {
                font-size: 16px;
                font-weight: 600;
                color: #0f172a;
        """)

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 24)
        main_layout.setSpacing(18)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)

        title_label = QLabel("Pilotage thermique")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel(
            "Interface de suivi pour la température, la résistance, le voltage et la puissance"
        )
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(16)

        temperature_input_group = QGroupBox("Consigne de température")
        temperature_input_layout = QVBoxLayout()
        temperature_input_layout.setSpacing(12)

        input_hint = QLabel("Définir une consigne entre 0 et 100 °C")
        input_hint.setObjectName("inputHint")

        self.temperature_input = QSpinBox()
        self.temperature_input.setRange(0, 100)
        self.temperature_input.setSuffix(" °C")
        self.temperature_input.setSingleStep(1)
        self.temperature_input.setValue(25)

        self.submit_temperature_button = QPushButton("Valider la consigne")
        self.submit_temperature_button.setObjectName("primaryButton")

        temperature_input_layout.addWidget(input_hint)
        temperature_input_layout.addWidget(self.temperature_input)
        temperature_input_layout.addWidget(self.submit_temperature_button)
        temperature_input_group.setLayout(temperature_input_layout)
        temperature_input_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        left_panel.addWidget(temperature_input_group)

        info_group = QGroupBox("Informations système")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        self.temperature_label = QLabel("Température actuelle : -- °C")
        self.consigne_label = QLabel("Consigne : -- °C")
        self.status_label = QLabel("État : Non connecté")

        self.temperature_label.setObjectName("infoValue")
        self.consigne_label.setObjectName("infoValue")
        self.status_label.setObjectName("infoValue")

        info_layout.addWidget(self.temperature_label)
        info_layout.addWidget(self.consigne_label)
        info_layout.addWidget(self.status_label)
        info_group.setLayout(info_layout)
        info_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        left_panel.addWidget(info_group)

        button_group = QGroupBox("Commandes")
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        self.connect_button = QPushButton("Connecter")
        self.start_button = QPushButton("Démarrer")
        self.stop_button = QPushButton("Arrêter")

        self.connect_button.setObjectName("primaryButton")
        self.stop_button.setObjectName("dangerButton")

        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_group.setLayout(button_layout)
        button_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        left_panel.addWidget(button_group)
        left_panel.addStretch()

        plots_group = QGroupBox("Mesures en temps réel")
        plots_layout = QGridLayout()
        plots_layout.setHorizontalSpacing(14)
        plots_layout.setVerticalSpacing(14)

        self.temperature_plot = self._create_plot_widget("Température", "Température", "°C", "#ef4444")
        self.resistance_plot = self._create_plot_widget("Résistance", "Résistance", "Ω", "#f59e0b")
        self.voltage_plot = self._create_plot_widget("Voltage", "Voltage", "V", "#2563eb")
        self.power_plot = self._create_plot_widget("Puissance", "Puissance", "W", "#10b981")

        self.temperature_curve = self.temperature_plot.plot([], [], pen=pg.mkPen("#ef4444", width=2))
        self.resistance_curve = self.resistance_plot.plot([], [], pen=pg.mkPen("#f59e0b", width=2))
        self.voltage_curve = self.voltage_plot.plot([], [], pen=pg.mkPen("#2563eb", width=2))
        self.power_curve = self.power_plot.plot([], [], pen=pg.mkPen("#10b981", width=2))

        plots_layout.addWidget(self.temperature_plot, 0, 0)
        plots_layout.addWidget(self.resistance_plot, 0, 1)
        plots_layout.addWidget(self.voltage_plot, 1, 0)
        plots_layout.addWidget(self.power_plot, 1, 1)
        plots_group.setLayout(plots_layout)

        content_layout.addLayout(left_panel, 1)
        content_layout.addWidget(plots_group, 3)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def _create_plot_widget(
        self,
        title: str,
        label: str,
        unit: str,
        color: str,
    ) -> pg.PlotWidget:
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground("#ffffff")
        plot_widget.setTitle(
            f"<span style='color:#0f172a; font-size:14pt; font-weight:600;'>{title}</span>"
        )
        plot_widget.setLabel("left", label, units=unit, color="#475569")
        plot_widget.setLabel("bottom", "Temps", units="s", color="#475569")
        plot_widget.showGrid(x=True, y=True, alpha=0.2)
        plot_widget.getAxis("left").setPen(pg.mkPen("#94a3b8"))
        plot_widget.getAxis("bottom").setPen(pg.mkPen("#94a3b8"))
        plot_widget.getAxis("left").setTextPen(pg.mkPen("#64748b"))
        plot_widget.getAxis("bottom").setTextPen(pg.mkPen("#64748b"))
        plot_widget.getPlotItem().getViewBox().setBorder(pg.mkPen("#e2e8f0"))
        plot_widget.setMinimumHeight(220)

        title_font = QFont("Segoe UI", 10)
        title_font.setBold(True)
        plot_widget.getPlotItem().titleLabel.item.setFont(title_font)
        plot_widget.getPlotItem().titleLabel.item.setDefaultTextColor(pg.mkColor(color))

        return plot_widget
