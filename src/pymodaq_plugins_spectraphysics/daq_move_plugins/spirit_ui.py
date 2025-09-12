from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Signal, QObject
from qtpy.QtGui import QColor, QPalette

class SpiritUI(QObject):
    """
    User interface for the Spirit laser plugin.
    """
    
    # Signals to connect to plugin methods
    laser_on_signal = Signal()
    laser_off_signal = Signal()
    open_shutter_signal = Signal()
    close_shutter_signal = Signal()

    def __init__(self, parent_widget: QtWidgets.QWidget):
        super().__init__()
        self.parent_widget = parent_widget
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        control_group = QtWidgets.QGroupBox("Spirit Laser Control")
        grid_layout = QtWidgets.QGridLayout()

        status_group = QtWidgets.QGroupBox("Status")
        status_layout = QtWidgets.QFormLayout()
        
        self.power_label = self._create_status_label()
        self.rep_rate_label = self._create_status_label()
        self.shutter_label = self._create_status_label("Unknown", "gray")
        self.laser_status_label = self._create_status_label("Unknown", "gray")
        self.warmup_label = self._create_status_label()
        self.key_switch_label = self._create_status_label("Unknown", "gray")
        self.interlock_label = self._create_status_label("Unknown", "gray")

        status_layout.addRow("Output Power (W):", self.power_label)
        status_layout.addRow("Repetition Rate (kHz):", self.rep_rate_label)
        status_layout.addRow("Shutter:", self.shutter_label)
        status_layout.addRow("Laser Emission:", self.laser_status_label)
        status_layout.addRow("Warmup (min):", self.warmup_label)
        status_layout.addRow("Key Switch:", self.key_switch_label)
        status_layout.addRow("Interlock:", self.interlock_label)
        status_group.setLayout(status_layout)

        controls_group = QtWidgets.QGroupBox("Controls")
        controls_layout = QtWidgets.QHBoxLayout()
        self.on_button = QtWidgets.QPushButton("Emission ON")
        self.off_button = QtWidgets.QPushButton("Emission OFF")
        self.open_shutter_button = QtWidgets.QPushButton("Open Shutter")
        self.close_shutter_button = QtWidgets.QPushButton("Close Shutter")
        
        controls_layout.addWidget(self.on_button)
        controls_layout.addWidget(self.off_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.open_shutter_button)
        controls_layout.addWidget(self.close_shutter_button)
        controls_group.setLayout(controls_layout)

        grid_layout.addWidget(status_group, 0, 0)
        grid_layout.addWidget(controls_group, 1, 0)
        
        control_group.setLayout(grid_layout)
        main_layout.addWidget(control_group)
        main_layout.addStretch()
        self.parent_widget.setLayout(main_layout)
        
        self.on_button.clicked.connect(self.laser_on_signal.emit)
        self.off_button.clicked.connect(self.laser_off_signal.emit)
        self.open_shutter_button.clicked.connect(self.open_shutter_signal.emit)
        self.close_shutter_button.clicked.connect(self.close_shutter_signal.emit)

    def _create_status_label(self, text="-", color=None):
        label = QtWidgets.QLabel(text)
        label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        label.setFrameShadow(QtWidgets.QFrame.Sunken)
        label.setMinimumWidth(80)
        label.setAlignment(QtCore.Qt.AlignCenter)
        if color:
            self._set_label_color(label, color)
        return label

    def _set_label_color(self, label: QtWidgets.QLabel, color: str):
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(color))
        palette.setColor(QPalette.WindowText, QColor("white") if color not in ["lightgray", "orange"] else QColor("black"))
        label.setPalette(palette)
        label.setAutoFillBackground(True)

    def update_power(self, power: float):
        self.power_label.setText(f"{power:.3f}")

    def update_rep_rate(self, rep_rate: float):
        self.rep_rate_label.setText(f"{rep_rate:.1f}")

    def update_shutter_status(self, status: str):
        self.shutter_label.setText(status)
        self._set_label_color(self.shutter_label, "green" if status == "Open" else "red")

    def update_status(self, status_code: int):
        # Bit flags from Spirit Manual page 56
        system_ok = not bool(status_code & 0b1)
        laser_on = bool(status_code & 0b10)
        warmup = bool(status_code & 0b100)
        key_switch_on = bool(status_code & 0b10000000)
        shutter_open = bool(status_code & 0b100000000) # This might be redundant with SHUTTER?
        interlock_ok = not bool(status_code & 0b100000000000)
        
        # Laser Status
        if not system_ok:
            status_text, color = "Error", "red"
        elif warmup:
            status_text, color = "Warming Up", "orange"
        elif laser_on:
            status_text, color = "ON", "green"
        else:
            status_text, color = "OFF", "red"
        self.laser_status_label.setText(status_text)
        self._set_label_color(self.laser_status_label, color)

        # Key Switch
        self.key_switch_label.setText("ON" if key_switch_on else "OFF")
        self._set_label_color(self.key_switch_label, "green" if key_switch_on else "red")

        # Interlock
        self.interlock_label.setText("OK" if interlock_ok else "FAULT")
        self._set_label_color(self.interlock_label, "green" if interlock_ok else "red")


    def update_warmup_time(self, minutes: int):
        self.warmup_label.setText(str(minutes))
